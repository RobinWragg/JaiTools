import sublime
import os
import fnmatch

def view_is_jai(view):
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

def get_all_jai_project_file_paths():
  paths = set()
  
  for folder in sublime.active_window().folders():
    for root, dirs, files in os.walk(folder):
      for file in fnmatch.filter(files, '*.[jJ][aA][iI]'):
        file_path = os.path.join(root, file)
        paths.add(file_path)
        
  return paths

def get_view_contents(view, char_count=None):
  pattern = ''
  
  if char_count == None:
    pattern = '[\w\W]*'
  else:
    pattern = '^[\w\W]{0,' + str(char_count) + '}'
  
  buffer_region = view.find(pattern, 0)
  
  if buffer_region == None:
    return ''
  else:
    return view.substr(buffer_region)

def get_file_contents(file_path, char_count=None):
  file_view = sublime.active_window().find_open_file(file_path)
  
  # Load from the view buffer if it exists
  if file_view == None:
    with open(file_path, 'r') as f:
      if char_count == None:
        return f.read()
      else:
        return f.read(char_count) 
  elif char_count == None:
    return get_view_contents(file_view)
  else:
    return get_view_contents(file_view, char_count)
    







