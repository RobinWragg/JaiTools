from .Common import *
import sublime_plugin
import re
import time

class Autocomplete(sublime_plugin.EventListener):
  gather_from_unopen_files = False
  completion_index = {}
  
  full_reindex_interval_secs = 60 * 10 # Ten minutes
  last_full_reindex_secs = -full_reindex_interval_secs # Ensure re-indexing happens on launch
  definition_pattern = re.compile(r'\b\w+\s*:[\w\W]*?[{;]')
  proc_pattern = re.compile(r'\b(\w+)\s*:\s*[:=]\s*\(([\w\W]*?)\)\s*(?:->\s*(.*?)\s*)?{')
  proc_params_pattern = re.compile(r'(?:^|)\s*([^,]+?)\s*(?:$|,)')
  line_comment_pattern = re.compile(r'//.*?(?=\n)')
  
  def get_all_index_keys(self):
    index_keys = set()
    
    # Get jai file paths from all open folders
    if self.gather_from_unopen_files:
      index_keys = get_all_jai_project_file_paths()
    
    # Load all open jai views in case they're unsaved or external files
    for view in sublime.active_window().views():
      if view_is_jai(view):
        index_keys.add(self.get_view_index_key(view))
    
    return index_keys
  
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
    jai_text = self.strip_block_comments(jai_text)
    jai_text = self.strip_line_comments(jai_text)
    
    defs = self.definition_pattern.findall(jai_text)
    return list(set(defs))
  
  def make_completions_from_proc_definition(self, definition, file_name):
    match = self.proc_pattern.match(definition)
    
    if match == None:
      return []
    
    groups = match.groups()
    
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
  
  def get_completions_from_text(self, jai_text, file_name_for_user):
    definitions = self.extract_definitions_from_text(jai_text)
    
    completions = []
    
    for definition in definitions:
      if self.proc_pattern.search(definition) == None:
        completion = self.make_completion_from_variable_definition(definition, file_name_for_user)
        completions.append(completion)
      else:
        completions += self.make_completions_from_proc_definition(definition, file_name_for_user)
        
    return completions
  
  def get_view_index_key(self, view):
    file_path = view.file_name()
    
    if file_path == None:
      return view.buffer_id()
    else:
      return file_path
  
  def index_view(self, view, is_async):
    # If a full re-index hasn't been performed recently (see the value of
    # full_reindex_interval_secs), and this function will not block the user (an async event),
    # re-index everything in order to:
    #  - Gather completions from files that are in the project but aren't open
    #  - Remove deleted files (the API doesn't provide an event for file deletions)
    #  - Index any file changes that were made outside of Sublime Text
    if is_async and time.time() - self.last_full_reindex_secs > self.full_reindex_interval_secs:
      self.reindex_everything()
      return
    
    if not view_is_jai(view):
      return
    
    index_key = self.get_view_index_key(view)
    file_name_for_user = ''
    
    if isinstance(index_key, str):
      # index_key is the file path
      file_name_for_user = os.path.basename(index_key)
      
      # Ensure there is no reference to the buffer, as it would contain duplicate completions.
      buffer_id = view.buffer_id()
      if buffer_id in self.completion_index:
        del self.completion_index[buffer_id]
    else:
      # index_key is the buffer ID, meaning there is no corresponding file on disk.
      file_name_for_user = 'unsaved'
    
    jai_text = get_view_contents(view)
    self.completion_index[index_key] = self.get_completions_from_text(jai_text, file_name_for_user)
  
  def reindex_everything(self):
    print('JaiTools: Starting re-indexing of completions')
    
    start_time = time.time()
    
    new_completion_index = {}
    all_index_keys = self.get_all_index_keys()
    
    # Split keys into file paths and buffer IDs to gather completions differently
    file_paths = filter(lambda x: isinstance(x, str), all_index_keys)
    buffer_ids = filter(lambda x: isinstance(x, int), all_index_keys)
    
    for path in file_paths:
      jai_text = get_file_contents(path)
      name_for_user = os.path.basename(path)
      new_completion_index[path] = self.get_completions_from_text(jai_text, name_for_user)
    
    for buffer_id in buffer_ids:
      # The API can't get text from the buffer directly, so find a view associated with it (if any).
      for view in sublime.active_window().views():
        if view.buffer_id() == buffer_id:
          jai_text = get_view_contents(view)
          new_completion_index[buffer_id] = self.get_completions_from_text(jai_text, 'unsaved')
          break
    
    self.completion_index = new_completion_index
    self.last_full_reindex_secs = time.time()
    
    duration_ms = int((time.time() - start_time) * 1000)
    print('JaiTools: Full re-indexing of completions took ' + str(duration_ms) + 'ms')
    
  def on_pre_close(self, view):
    self.index_view(view, True)
  
  def on_deactivated_async(self, view):
    self.index_view(view, True)
  
  def on_activated_async(self, view):
    self.index_view(view, True)
  
  def on_query_completions(self, view, prefix, locations):
    if not view_is_jai(view):
      return None
    
    self.index_view(view, False)
    
    completions = []
    for key in self.completion_index.keys():
      completions += self.completion_index[key]
    
    return completions





