import sublime
import sublime_plugin
import re
import os
import fnmatch
import time

class JaiCompletions(sublime_plugin.EventListener):
  definition_pattern = re.compile(r'\b\w+\s*:[\w\W]*?[{;]')
  proc_pattern = re.compile(r'\b(\w+)\s*:\s*[:=]\s*\(([\w\W]*?)\)\s*(?:->\s*(.*?)\s*)?{')
  proc_params_pattern = re.compile(r'(?:^|)\s*([^,]+?)\s*(?:$|,)')
  line_comment_pattern = re.compile(r'//.*?(?=\n)')
  
  def view_is_jai(self, view):
    settings = view.settings()
    
    if settings != None:
      syntax = settings.get('syntax')
      if syntax != None:
        if syntax.find('Jai.sublime-syntax') >= 0:
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
        for file in fnmatch.filter(files, '*.[jJ][aA][iI]'):
          file_path = os.path.join(root, file)
          paths.add(file_path)
    
    # Load all open jai files from views in case they're external files
    for view in window.views():
      file_path = view.file_name()
      
      if file_path != None and file_path[-4:].lower() == '.jai':
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
  
  def make_completions_from_proc_components(self, proc_name, params, return_type, file_name):
    trigger = proc_name + '('
    result = proc_name + '('
    
    if len(params) > 0:
      for p in range(len(params)):
        if p > 0:
          trigger += ', '
          result += ', '
          
        trigger += params[p]
        result += '${' + str(p+1) + ':' + params[p] + '}'
    
    trigger += ')'
    result += ')'
    
    if return_type != None:
      trigger += ' -> ' + return_type
    
    trigger += '\t ' + file_name
    
    # proc completion
    completions = [[trigger, result]]
    
    # param completions
    for param in params:
      completion = self.make_completion_from_variable_definition(param, file_name)
      completions.append(completion)
    
    return completions
  
  def extract_definitions_from_text(self, jai_text):
    defs = self.definition_pattern.findall(jai_text)
    return list(set(defs))
  
  def make_completions_from_proc_definition(self, definition, file_name):
    groups = self.proc_pattern.match(definition).groups()
    
    proc_name = groups[0]
    params_str = groups[1]
    return_type = groups[2]
    
    params_list = self.proc_params_pattern.findall(params_str)
    
    # Handle the case of empty space inside parentheses
    if len(params_list) == 1 and params_list[0].strip() == '':
      params_list = []
    
    return self.make_completions_from_proc_components(proc_name, params_list, return_type, file_name)
  
  def make_completion_from_variable_definition(self, definition, file_name):
    colon_index = definition.find(':')
    identifier = definition[:colon_index].strip()
    return [identifier + '\t ' + file_name, identifier]
  
  def get_completions_from_file_path(self, path):
    contents = self.get_file_contents(path)
    
    contents = self.strip_block_comments(contents)
    contents = self.strip_line_comments(contents)
    
    definitions = self.extract_definitions_from_text(contents)
    
    completions = []
    file_name = os.path.split(path)[1]
    
    for definition in definitions:
      if self.proc_pattern.search(definition) == None:
        completion = self.make_completion_from_variable_definition(definition, file_name)
        completions.append(completion)
      else:
        completions += self.make_completions_from_proc_definition(definition, file_name)
        
      
    return completions
  
  def report_indexing_duration(self, start_time_seconds):
    # Report time spent building completions before returning
    delta_time_ms = int((time.time() - start_time_seconds) * 1000)
    message = 'Jai completion indexing took ' + str(delta_time_ms) + 'ms'
    sublime.active_window().status_message(message)
  
  def on_query_completions(self, view, prefix, locations):
    start_time = time.time()
    
    if not self.view_is_jai(view):
      return None
    
    paths = self.get_all_jai_file_paths()
    completions = []
    for path in paths:
      completions += self.get_completions_from_file_path(path)
    
    self.report_indexing_duration(start_time)
    
    return completions





