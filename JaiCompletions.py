import sublime
import sublime_plugin
import re
import os

# TODO: autocomplete non-function names
# TODO: gather from more than just the current view
# TODO: make a better .sublime-syntax file
# TODO: Rename functions to procedures.
# TODO: How to display parameters when using "goto symbol" for procedures?
# TODO: Maybe show line numbers alongside filename?

class JaiCompletions(sublime_plugin.EventListener):
  # func_contents_pattern = re.compile('[^(),]+')
  raw_completions = []
  
  def is_jai_view(self, view):
    file_name = view.file_name()
    if file_name != None and file_name[-4:].lower() == '.jai':
      return True
    elif view.settings().get('syntax').lower().find('Jai') >= 0:
      return True
    else:
      return False
      
  def gather_raw_completions(self, view):
    func_def_pattern = '(?:\s|^)(\w+)\s*::\s*\(([^()"]*)\)\s*(?:->\s*([^{]+))?{'
    formatter = '$1§$2'
    
    new_raw_completions = []
    view.find_all(func_def_pattern, 0, '$1§$2§$3', new_raw_completions)
    
    file_name = view.file_name()
    if file_name != None:
      for completion in new_raw_completions:
        self.raw_completions.append({'def': completion, 'file_name': file_name})
    else:
      for completion in new_raw_completions:
        self.raw_completions.append({'def': completion})
  
  def build_output_params(self, raw_params):
    if raw_params == '':
      return ''
    
    output_params = ''
    
    splitted_params = raw_params.split(',')
    
    for i in range(len(splitted_params)):
      output_params += '${' + str(i+1) + ':'
      output_params += splitted_params[i].strip()
      output_params += '}'
      if i < len(splitted_params) - 1:
        output_params += ', '
    
    return output_params
  
  def build_completion_from_raw(self, raw):
    splitted_completion = raw['def'].split('§')
    name = splitted_completion[0]
    params = splitted_completion[1]
    return_type = splitted_completion[2]
    
    trigger = name + '(' + params + ')'
    
    if return_type != '':
      trigger += ' -> ' + return_type.strip()
      
    if 'file_name' in raw:
      trigger += ' \t' + os.path.basename(raw['file_name'])
    
    replacement = name + '(' + self.build_output_params(params) + ')'
    
    return [trigger, replacement]
    
  def on_query_completions(self, view, prefix, locations):
    if not self.is_jai_view(view):
      return None
    
    self.raw_completions = []
    self.gather_raw_completions(view)
    
    completions_to_return = []
    
    for raw in self.raw_completions:
      if raw['def'].lower().startswith(prefix.lower()):
        completions_to_return.append(self.build_completion_from_raw(raw))
        
    return completions_to_return





