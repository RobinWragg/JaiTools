import sublime
import sublime_plugin
import re
import os
import fnmatch
import time

class JaiCompletions(sublime_plugin.EventListener):
  line_comment_pattern = re.compile(r'//.*?(?=\n)')
  proc_pattern = re.compile(r'\b(\w+)\s*:\s*[:=]\s*\(([\w\W]*?)\)\s*(?:->\s*(.*?)\s*)?{')
  
  def view_is_jai(self, view):
    if view.settings().get('syntax').find('Jai.sublime-syntax') >= 0:
      return True
    
    path = view.file_name()
    
    if path != None and path[-4:].lower() == '.jai':
      return True
      
    return False
  
  def get_all_jai_file_paths(self):
    paths = set()
    window = sublime.active_window()
    
    # Get jai file paths from all open folders
    # TODO: Rewrite this with recursive glob if ST3 upgrades Python to 3.5+
    for folder in window.folders():
      for root, dirs, files in os.walk(folder):
        for file in fnmatch.filter(files, '*.jai'): # TODO: what about uppercase extensions?
          file_path = os.path.join(root, file)
          paths.add(file_path)
    
    # Load all open jai files from views in case they're external files
    for view in window.views():
      file_path = view.file_name()
      
      if file_path != None and file_path[-4:] == '.jai':
        paths.add(file_path)
    
    return paths
  
  def get_file_contents(self, file_path):
    
    file_view = sublime.active_window().find_open_file(file_path)
    
    if file_view == None:
      with open(file_path, 'r') as f:
        return f.read()
    else:
      entire_buffer = file_view.find('[\w\W]*', 0)
      
      if entire_buffer == None:
        return ''
      else:
        return file_view.substr(entire_buffer)
  
  def strip_block_comments(self, jai_text):
    non_comments = []
    
    comment_end_index = 0
    block_comment_depth = 0
    
    for i in range(len(jai_text)):
      if jai_text[i:i+2] == '/*':
        if block_comment_depth == 0:
          non_comment = jai_text[comment_end_index:i]
          non_comments.append(non_comment)
        block_comment_depth += 1
      elif jai_text[i-2:i] == '*/':
        block_comment_depth -= 1
        if block_comment_depth == 0:
          comment_end_index = i
        if block_comment_depth < 0:
          block_comment_depth = 0
    
    non_comments.append(jai_text[comment_end_index:])
    return ''.join(non_comments)
  
  def strip_line_comments(self, jai_text):
    return self.line_comment_pattern.sub('', jai_text)
  
  def extract_procs_from_text(self, text):
    raw_procs = self.proc_pattern.findall(text)
    formatted_procs = []
    
    for raw_proc in raw_procs:
      identifier = raw_proc[0]
      
      params = []
      if len(raw_proc[1]) > 0:
        params = raw_proc[1].split(',')
      
      for p in range(len(params)):
        params[p] = params[p].strip()
      
      return_type = None
      if len(raw_proc[2]) > 0:
        return_type = raw_proc[2]
      
      formatted_procs.append({
        'identifier': identifier,
        'params': params,
        'return': return_type
        })
      
    return formatted_procs
  
  def make_completion_from_proc(self, proc, file_name):
    trigger = proc['identifier'] + '('
    result = proc['identifier'] + '('
    
    if len(proc['params']) > 0:
      for p in range(len(proc['params'])):
        if p > 0:
          trigger += ', '
          result += ', '
          
        trigger += proc['params'][p]
        result += '${' + str(p+1) + ':' + proc['params'][p] + '}'
    
    trigger += ')'
    result += ')'
    
    if proc['return'] != None:
      trigger += ' -> ' + proc['return']
    
    trigger += '\t ' + file_name
    
    return [trigger, result]
  
  def get_completions_from_file_path(self, path):
    contents = self.get_file_contents(path)
    
    # Currently unused in order to maximize speed
    # contents = self.strip_block_comments(contents)
    # contents = self.strip_line_comments(contents)
    
    procs = self.extract_procs_from_text(contents)
    
    file_name = os.path.split(path)[1]
    completions = []
    for proc in procs:
      completions.append(self.make_completion_from_proc(proc, file_name))
      
    return completions
    
  def on_query_completions(self, view, prefix, locations):
    start_time = time.time()
    
    if not self.view_is_jai(view):
      return None
    
    paths = self.get_all_jai_file_paths()
    completions = []
    for path in paths:
      completions += self.get_completions_from_file_path(path)
    
    # Report time spent building completions before returning
    delta_time_ms = int((time.time() - start_time) * 1000)
    message = 'Jai autocompletion took ' + str(delta_time_ms) + 'ms'
    view.window().status_message(message)
    
    return completions





