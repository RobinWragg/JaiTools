import sublime
import sublime_plugin
import json
import subprocess

# rwtodo: don't forget to update the readme when this is done!
# rwtodo: weirdness is happening with the order of stdout and stderr

class GenerateJaiBuildSystemCommand(sublime_plugin.ApplicationCommand):
  def run(self):
    window = sublime.active_window()
    
    if window.project_file_name() == None:
      sublime.error_message('Project file not found. Choose "Project > Save Project As..." and try again.')
      return
    
    project = window.project_data()
    
    build_system = sublime.load_resource('Packages/JaiTools/Jai.sublime-build')
    build_system = json.loads(build_system)
    
    build_system['name'] = 'Jai Project'
    del build_system['selector']
    
    # rwtodo: ask for the build file and modify the 'shell_cmd' and 'working_dir' entries. make working_dir the project path, and use the full file path for *.jai with quotes.
    
    if 'build_systems' in project:
      project['build_systems'].append(build_system)
    else:
      project['build_systems'] = [build_system]
    
    window.set_project_data(project)








