import sublime
import sublime_plugin
import re
import os
import fnmatch
import time

class JaiCompletions(sublime_plugin.EventListener):
  # func_contents_pattern = re.compile('[^(),]+')
  raw_completions = []
  
  def get_all_jai_content(self, window):
    jai_files = []
    
    # Load all open jai files from views in case they are dirty
    for view in window.views():
      file = {
        'path': view.file_name()
      }
      
      if file['path'] != None and file['path'][-4:] == '.jai':
        region = view.find('[\w\W]*', 0)
        
        if region == None:
          continue
        
        file['contents'] = view.substr(region)
        jai_files.append(file)
    
    # Get all jai files in the open folders that aren't already in jai_files
    # TODO: Rewrite this with recursive glob if ST3 upgrades Python to 3.5+
    for folder in window.folders():
      for root, dirs, files in os.walk(folder):
        for file in fnmatch.filter(files, '*.jai'):
          file = {
            'path': os.path.join(root, file)
          }
            
          if not any(f['path'] == file['path'] for f in jai_files):
            
            with open(file['path'], 'r') as f:
              file['contents'] = f.read()
            
            jai_files.append(file)
    
    return jai_files
  
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
    
    start_time = time.time()
    
    
    
    
    self.get_all_jai_content(view.window())
    
    self.raw_completions = []
    self.gather_raw_completions(view)
    
    completions_to_return = []
    
    for raw in self.raw_completions:
      if raw['def'].lower().startswith(prefix.lower()):
        completions_to_return.append(self.build_completion_from_raw(raw))
    
    
    
    
    
    delta_time_ms = int((time.time() - start_time) * 1000)
    view.window().status_message('Jai completion took ' + str(delta_time_ms) + 'ms')
    return completions_to_return





