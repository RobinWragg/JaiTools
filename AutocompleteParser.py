import sublime
import re

# rwtodo: active file: all identifiers. all procs.
# rwtodo: inactive files: all declarations in module/export scope.
# rwtodo: Handle the 'using' keyword for params. just remove them?
# rwtodo: Braces in completions break Sublime's completion engine. Hopefully I can just backslash them.

class AutocompleteParser:
  def get_completions_from_file(self, path, ui_file_name):
    text = self._get_file_contents(path)
    return self.get_completions_from_text(text, ui_file_name)
  
  whitespace_pattern = re.compile(r'\s+')
  proc_decl_pattern = re.compile(r'\b\w+\s*:\s*[:=]\s*\(\s*(?:\$*?\w+\s*:|\)).*?[{;]')
  proc_decl_grouping_pattern = re.compile(r'(\w+)[\w\W]+?\(\s*(.*?)\s*\)\s*(->.+?)?\s*[#{;]')
  def get_completions_from_text(self, text, ui_file_name):
    # NOTE: The order of these text manipulation functions is important.
    
    text = self._remove_herestring_contents(text)
    text = self._remove_comments(text)
    
    # rwtodo: this is just for non-active files
    text = self._remove_file_scopes(text)
    
    # Remove excessive whitespace
    text = self.whitespace_pattern.sub(' ', text)
    
    masked_text = self._mask_string_literals(text)
    masked_text = self._mask_struct_literals(masked_text)
    
    proc_decl_matches = self.proc_decl_pattern.finditer(masked_text)
    
    completions = []
    proc_identifiers = set()
    
    for match in proc_decl_matches:      
      decl = text[match.start():match.end()]
      masked_decl = match.group(0)
      
      grouped_match = self.proc_decl_grouping_pattern.search(masked_decl)
      
      if grouped_match:
        identifier = grouped_match.group(1)
        proc_identifiers.add(identifier)
        
        params_string = decl[grouped_match.start(2):grouped_match.end(2)]
        masked_params_string = self._mask_parentheses(grouped_match.group(2))
        
        params = self._split_params(params_string, masked_params_string)
        
        suffix = decl[grouped_match.start(3):grouped_match.end(3)].strip()
        
        if len(suffix) == 0:
          suffix = None
        
        completions.append(self._make_proc_completion(identifier, params, suffix, ui_file_name))
      else:
        print('JaiTools: Failed to deconstruct procedure: ' + match.group(0))
    
    # rwtodo: don't filter out nested decls for the active file. Create _get_all_words()?
    # rwtodo: don't collect param identifiers for non-active files.
    identifiers = self._get_declaration_identifiers(masked_text)
    identifiers -= proc_identifiers
    
    for identifier in identifiers:
      completions.append(self._make_generic_completion(identifier, ui_file_name))
    
    # Enforce a maximum width. rwtodo: don't know if this is a significant performance hit yet. Might be better to do this when each completion is created, to avoid the cost of iteration and indexing into the list.
    # rwtodo: truncate the declaration from the right, leaving behind the filename, instead of truncating from the middle
    max_length = 90
    for c in range(len(completions)):
      if len(completions[c][0]) > 50:
        list_entry = completions[c][0]
        prefix_length = max_length // 2
        suffix_length = max_length // 2 - 3
        completions[c][0] = list_entry[:prefix_length] + '...' + list_entry[-suffix_length:]
    
    return completions
  
  comma_pattern = re.compile(r',')
  def _split_params(self, params_string, masked_params_string):
    if len(params_string.strip()) == 0:
      return []
    
    # Split masked_params_string by comma, and use the indices to split the non-masked params_string
    params = []
    param_start_index = 0
    
    for comma_match in self.comma_pattern.finditer(masked_params_string):
      comma_index = comma_match.start()
      params.append(params_string[param_start_index:comma_index])
      param_start_index = comma_match.end()
    params.append(params_string[param_start_index:])
    
    def remove_param_whitespace(param):
      return param.strip()
      
    return list(map(remove_param_whitespace, params))
  
  brace_or_decl_pattern = re.compile(r'{.*?(?=[{}])|}|([`$]*\w+)\s?:(?:\s?[:=]\s?(\w+))?')
  # rwtodo: this can probably be optimised by using a different regex when block depth is > 0.
  def _get_declaration_identifiers(self, text):
    declarations = set()
    start_index = 0
    block_depth = 0
    
    while True:
      match = self.brace_or_decl_pattern.search(text, pos=start_index)
      
      if match == None:
        break
        
      match_str = match.group(0)
      
      if match_str[0] == '{':
        block_depth += 1
      elif match_str == '}':
        block_depth -= 1
      elif block_depth == 0:
        identifier = match.group(1)
        declarations.add(identifier)
        # rwtodo: if the identifier is an enum, enum_flags or struct decl with a block, grab the members. Don't forget that struct members can be 'using', but it should 'just work' if you're looking for a colon prefix, unless you can do anonymous 'using's. Don't know.
        after_identifier = match.group(2)
        if after_identifier:
          if after_identifier == 'struct':
            pass
          if after_identifier == 'enum':
            pass
          if after_identifier == 'enum_flags':
            pass
        
      start_index = match.end()
    
    return declarations
  
  def _mask_string_literals(self, text):
    inside_string_literal = False
    
    pieces = []
    piece_start_index = 0
    
    for i in range(len(text)):
      if text[i] == '"' and (i == 0 or text[i-1] != '\\'):
        if inside_string_literal:
          pieces.append('"' * (i+1 - piece_start_index))
          piece_start_index = i + 1
        else:
          pieces.append(text[piece_start_index:i])
          piece_start_index = i
        
        inside_string_literal = not inside_string_literal
    
    if not inside_string_literal: # If the file ends inside a string literal, we don't care.
      # Append the remaining piece
      pieces.append(text[piece_start_index:])
    
    return ''.join(pieces)
  
  struct_literal_pattern = re.compile(r'\.{[^(?:\.{)]*?}')
  def _mask_struct_literals(self, text):
    # Keep overwriting all occurrences of literals that don't contain nested literals until none are left.
    text_changed = True
    
    while text_changed:
      text_changed = False
      
      matches = self.struct_literal_pattern.finditer(text)
      pieces = []
      piece_start_index = 0
      
      for match in matches:
        piece_end_index = match.start()
        pieces.append(text[piece_start_index:piece_end_index])
        
        piece_start_index = match.start()
        piece_end_index = match.end()
        pieces.append('"' * (piece_end_index - piece_start_index))
        piece_start_index = piece_end_index
      
      # Append the last piece
      pieces.append(text[piece_start_index:])
      
      modified_text = ''.join(pieces)
      
      if modified_text != text:
        text_changed = True
        text = modified_text
    
    return text
  
  parentheses_pattern = re.compile(r'\([^(]*?\)')
  def _mask_parentheses(self, text):
    # Keep overwriting all occurrences of literals that don't contain nested literals until none are left.
    text_changed = True
    
    while text_changed:
      text_changed = False
      
      matches = self.parentheses_pattern.finditer(text)
      pieces = []
      piece_start_index = 0
      
      for match in matches:
        piece_end_index = match.start()
        pieces.append(text[piece_start_index:piece_end_index])
        
        piece_start_index = match.start()
        piece_end_index = match.end()
        pieces.append('"' * (piece_end_index - piece_start_index))
        piece_start_index = piece_end_index
      
      # Append the last piece
      pieces.append(text[piece_start_index:])
      
      modified_text = ''.join(pieces)
      
      if modified_text != text:
        text_changed = True
        text = modified_text
    
    return text
  
  comment_pattern = re.compile(r'//.*?(?=\n)|\/\*[\w\W]*?\*\/')
  def _remove_comments(self, text):
    return self.comment_pattern.sub('', text)
  
  file_scope_pattern = re.compile(r'(?<=\n)\s*?#scope_file[\w\W]*?(?=#scope_)')
  def _remove_file_scopes(self, text):
    return self.file_scope_pattern.sub('', text)
  
  herestring_contents_pattern = re.compile(r'#string\s+(\w+)\s[\w\W]*?\1')
  def _remove_herestring_contents(self, text):
    return self.herestring_contents_pattern.sub('#string;', text)
  
  brace_replacer_pattern = re.compile(r'([^\\])([{}])')
  def _make_proc_completion(self, proc_name, params, suffix, file_name):
    trigger = proc_name + '('
    result = proc_name + '('
    
    for p in range(len(params)):
      if p > 0:
        trigger += ', '
        result += ', '
      
      param = params[p]
      trigger += param
      
      while True:
        match = self.brace_replacer_pattern.search(param)
        
        if not match:
          break
        
        escaped_brace = match.group(1) + '\\' + match.group(2)
        param = param[:match.start()] + escaped_brace + param[match.end():]
        
      result += '${' + str(p+1) + ':' + param + '}'
    
    trigger += ')'
    result += ')'
    
    if suffix:
      trigger += suffix
    
    trigger += '\t ' + file_name
    
    return [trigger, result]
  
  def _make_generic_completion(self, identifier, ui_file_name):
    return [identifier + '\t ' + ui_file_name, identifier]
  
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