from .JaiToolsCommon import *
import sublime
import sublime_plugin
import os
    
class SetBuildFileHandler(sublime_plugin.ListInputHandler):
  relative_file_paths = set()
  
  def __init__(self, paths):
    self.relative_file_paths = paths
  
  def name(self):
    return 'build_file_path'
  
  def list_items(self):
    return self.relative_file_paths

class SetJaiBuildFileCommand(sublime_plugin.WindowCommand):
  common_parent_dir = ''
  
  def input(self, args):
    paths_set = get_all_jai_project_file_paths()
    
    # Add open files to the paths set, in case they're not part of the project
    for view in sublime.active_window().views():
      if view_is_jai(view) and view.file_name() != None:
        paths_set.add(view.file_name())
    
    if len(paths_set) == 0:
      sublime.error_message('There are no Jai files open or in your project. Save a Jai file and try again.')
      return None
    
    self.common_parent_dir = get_common_parent_dir(list(paths_set))
    
    relative_paths = []
    
    for path in paths_set:
      relative_paths.append(os.path.relpath(path, self.common_parent_dir))
      
    return SetBuildFileHandler(relative_paths)
  
  def run(self, build_file_path=None):
    if build_file_path != None:
      project_data = sublime.active_window().project_data()
      
      build_file_path = os.path.join(self.common_parent_dir, build_file_path)
      project_data[PROJECT_KEY_build_file_path] = build_file_path
      
      sublime.active_window().set_project_data(project_data)




