import sublime
import subprocess
import os
import time

# This is an experimental parser that executes a Jai metaprogram and collects declarations.
# The current theoretical hurdle to get it working well is that no declarations are collected if build errors occur.
# This is likely, because the metaprogram only knows about one file at any given time.

class MetaprogramParser:
  def execute(self, args, cwd=None):
    startupinfo = None

    # if windows (rwtodo):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    proc = subprocess.Popen(
      args=args,
      startupinfo=startupinfo,
      stdin=subprocess.PIPE,   # python 3.3 bug on Win7
      stderr=subprocess.PIPE,
      stdout=subprocess.PIPE,
      universal_newlines=True,
      cwd=cwd
    )
    
    result, errors_and_warnings = proc.communicate()
    result = result.strip()
    
    if type(errors_and_warnings) is str:
      result += '\n' + errors_and_warnings.strip()
    
    return result
    
  def check_for_compiler_name(self, compiler_name):
    print(compiler_name)
    try:
      result = self.execute([compiler_name, '-version'])
      if 'Version:' in result:
        return True
    except:
      pass
    
    return False
    
  # This should return:
  #  an array when there were no parsing errors
  #  None when there were parsing errors
  #  an empty array when there were no errors and no completions
  #  None if the file to parse isn't readable. rwtodo: I don't think it does this yet.
  def get_completions_from_file(self, path, name_for_user):
    metaprogram_name = 'CompletionsMetaprogram.jai'
    
    # debug sleep rwtodo
    time.sleep(0.5)
    
    if path.endswith(metaprogram_name):
      return None
    # rwtodo: make this exception-safe. Return None on exception.
    
    # NOTE: when there are build warnings, no declarations are received from the compiler unless we set the current working directory to where the file lives. This might be a compiler bug.
    args = ['jai', metaprogram_name, '--', name_for_user, os.path.basename(path)]
    result = self.execute(args, os.path.dirname(path))
    
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
    # rwtodo
  
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
  