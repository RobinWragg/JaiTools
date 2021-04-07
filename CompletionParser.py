import sublime
import re

# rwtodo: remove contents of herestrings, similarly to comments.
# rwtodo: handle definitions that contain braces, such as struct literals: Vector3.{...}.
# rwtodo: filter out duplicates, such as when completing "immediate_quad" from Simp/immediate.jai
# rwtodo: if you write code to call a function, then write the function definition, it would be good if the name of the function is autocompleted when writing the definition. This can be done by grabbing the identifiers of any function calls that don't already exist in the completion list.

class CompletionParser:
  definition_pattern = re.compile(r'\b\w+\s*:[\w\W]*?(?:;|{|#string)')
  proc_pattern = re.compile(r'\b(\w+)\s*:\s*[:=]\s*\(([\w\W]*?)\)\s*(?:->\s*(.*?)\s*)?[{;]')
  proc_params_pattern = re.compile(r'(?:^|)\s*([^,]+?)\s*(?:$|,)')
  line_comment_pattern = re.compile(r'//.*?(?=\n)')
  
  # We can get completions for text or from a file; note that it is currently easier to get
  # completions from text, but it will be easier for the metaprogram to get completions from a file.
  
  def get_completions_from_file(self, path, name_for_user):
    jai_text = self._get_file_contents(path)
    return self.get_completions_from_text(jai_text, name_for_user)
  
  def get_completions_from_text(self, jai_text, file_name_for_user):
    definitions = self._extract_definitions_from_text(jai_text)
    
    completions = []
    
    for definition in definitions:
      # Replace all whitespace with single spaces. This resolves some formatting issues.
      definition = re.sub(r'\s+', ' ', definition)
      
      if self.proc_pattern.search(definition) == None:
        completion = self._make_completion_from_variable_definition(definition, file_name_for_user)
        completions.append(completion)
      else:
        completions += self._make_completions_from_proc_definition(definition, file_name_for_user)
    
    return completions
  
  def _strip_block_comments(self, jai_text):
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
  
  def _strip_line_comments(self, jai_text):
    return self.line_comment_pattern.sub('', jai_text)
  
  def _make_completions_from_proc_components(self, proc_name, params, return_type, file_name):
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
      completion = self._make_completion_from_variable_definition(param, file_name)
      completions.append(completion)
    
    return completions
  
  def _extract_definitions_from_text(self, jai_text):
    jai_text = self._strip_block_comments(jai_text)
    jai_text = self._strip_line_comments(jai_text)
    
    defs = self.definition_pattern.findall(jai_text)
    return list(set(defs))
  
  def _make_completions_from_proc_definition(self, definition, file_name):
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
    
    return self._make_completions_from_proc_components(proc_name, params_list, return_type, file_name)
  
  def _make_completion_from_variable_definition(self, definition, file_name):
    colon_index = definition.find(':')
    identifier = definition[:colon_index].strip()
    return [identifier + '\t ' + file_name, identifier]
  
  def _get_file_contents(self, file_path, char_count=None):
    file_view = sublime.active_window().find_open_file(file_path)
    
    # Load from the view buffer if it exists
    if file_view == None:
      with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    else:
      return self._get_view_contents(file_view)
  
  def _get_view_contents(self, view):
    buffer_region = view.find('[\w\W]*', 0)
    
    if buffer_region == None:
      return ''
    else:
      return view.substr(buffer_region)
  