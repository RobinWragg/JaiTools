import sublime
import sublime_plugin
import json
import subprocess

# rwtodo: don't forget to update the readme when this is done!

# rwtodo: weirdness is happening with the order of stdout and stderr.
#   https://stackoverflow.com/a/60232612
#   https://twitter.com/marcan42/status/1382970174773424133
#   https://bugs.eclipse.org/bugs/show_bug.cgi?id=9720
#   https://forum.sublimetext.com/t/different-priorisation-of-logging-and-print-message-outputs/25537

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








