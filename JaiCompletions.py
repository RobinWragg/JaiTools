import sublime
import sublime_plugin
import re
import os
import fnmatch
import time

class JaiCompletions(sublime_plugin.EventListener):
  line_comment_pattern = re.compile(r'//.*?(?=\n)')
  proc_pattern = re.compile(r'\b(\w+)\s*:\s*[:=]\s*\(([\w\W]*?)\)\s*(?:->\s*(.*?)\s*)?{')
  
  def view_is_jai_syntax(self, view):
    return view.settings().get('syntax').find('Jai.sublime-syntax') >= 0
  
  def get_all_jai_file_paths(self):
    paths = set()
    window = sublime.active_window()
    
    # Get jai file paths from all open folders
    # TODO: Rewrite this with recursive glob if ST3 upgrades Python to 3.5+
    for folder in window.folders():
      for root, dirs, files in os.walk(folder):
        for file in fnmatch.filter(files, '*.jai'):
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
  
  def strip_nonglobal_scopes(self, jai_text):
    return jai_text # TODO
  
  def extract_procs_from_text(self, text):
    raw_procs = self.proc_pattern.findall(text)
    formatted_procs = []
    
    for raw_proc in raw_procs:
      identifier = raw_proc[0]
      
      params = None
      if len(raw_proc[1]) > 0:
        params = raw_proc[1].split(',')
      
      return_type = None
      if len(raw_proc[2]) > 0:
        return_type = raw_proc[2]
      
      formatted_procs.append((
        identifier,
        params,
        return_type,
        ))
      
    return formatted_procs
  
  def get_procs_from_file_path(self, path):
    contents = self.get_file_contents(path)
    contents = self.strip_block_comments(contents)
    contents = self.strip_line_comments(contents)
    contents = self.strip_nonglobal_scopes(contents)
    return self.extract_procs_from_text(contents)
    
  def on_query_completions(self, view, prefix, locations):
    start_time = time.time()
    
    if not self.view_is_jai_syntax(view):
      return None
    
    
    
    
    
    path = view.file_name()
    procs = self.get_procs_from_file_path(path)
    print(procs)
    print()
    # entire_buffer = view.find('[\w\W]*', 0)
    # text = file_view.substr(entire_buffer)
    
    
    
    
    completions_to_return = []
    
    # completions_to_return = [['triggertriggertriggertriggertrigger\t hint', 'funcname(${1:param1}, ${2:param2})']]
    
    
    # Report time spent building completions before returning
    delta_time_ms = int((time.time() - start_time) * 1000)
    message = 'Jai autocompletion took ' + str(delta_time_ms) + 'ms'
    view.window().status_message(message)
    
    return completions_to_return
    # e.g. [['trigger\t hint', 'result']]





