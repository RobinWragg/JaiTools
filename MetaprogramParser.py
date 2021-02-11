import sublime
import subprocess
import os
import time

class MetaprogramParser:
  def get_completions_from_file(self, path, name_for_user):
    metaprogram_name = 'CompletionsMetaprogram.jai'
    
    # debug sleep todo
    time.sleep(0.5)
    
    if path.endswith(metaprogram_name):
      return None
    # rwtodo: make this exception-safe. Return None on exception.
    
    dirname = os.path.dirname(os.path.abspath(__file__))
    
    startupinfo = None

    # if windows (rwtodo):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    proc = subprocess.Popen(
      args=['jai', metaprogram_name, '--', 'this is a UI-friendly name', 'test.jai'],
      startupinfo=startupinfo,
      stdin=subprocess.PIPE,   # python 3.3 bug on Win7
      stderr=subprocess.PIPE,
      stdout=subprocess.PIPE,
      universal_newlines=True,
      cwd=dirname
    )
    result, errors_and_warnings = proc.communicate()
    
    if type(errors_and_warnings) is str:
      result += errors_and_warnings
    
    result_lines = result.split('\n')
    
    completions = []
    
    for line in result_lines:
      if line.startswith('>'):
        #this line is a completion.
        completion = line[1:].strip().split('$$$')
        completions.append(completion)
      elif 'error' in line.lower():
        return None
    
    return completions
  
  def get_completions_from_text(self, jai_text, file_name_for_user):
    print("NOT IMPLEMENTED YET")
    crash
  
  def _get_file_contents(self, file_path):
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
  