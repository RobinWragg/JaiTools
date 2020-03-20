from .JaiToolsCommon import *
import sublime_plugin
import subprocess
import threading
import re

# REWRITE
# TODO: If no build file is set, show error message with sublime.error_message('JaiTools: No build file has been chosen for this project. Run "JaiTools: Set Build File" from the Command Palette and try building again.')
# TODO: If the chosen build file doesn't exist, show error message with sublime.error_message('JaiTools: The following build file doesn't exist:\n<path>\nRun "JaiTools: Set Build File" from the Command Palette and try building again.')

class RunJaiBuildFileCommand(sublime_plugin.WindowCommand):
  result_file_regex = r'^File "([^"]+)" line (\d+) col (\d+)'
  result_line_regex = r'^\s+line (\d+) col (\d+)'
  
  encoding = 'utf-8'
  killed = False
  process = None
  panel = None
  panel_lock = threading.Lock()

  def is_enabled(self, kill=False):
    # The Cancel build option should only be available
    # when the process is still running
    if kill:
      return self.process is not None and self.process.poll() is None
    return True
  
  def try_to_get_build_file_path(self):
    project_data = sublime.active_window().project_data()
    if PROJECT_KEY_build_file_path in project_data:
      return project_data[PROJECT_KEY_build_file_path]
    else:
      return None
  
  def run(self, kill=False):
    
    if kill:
      if self.process:
        self.killed = True
        self.process.terminate()
      return
    
    build_file_path = self.try_to_get_build_file_path()
    
    if build_file_path == None:
      sublime.error_message('JaiTools: No build file has been chosen for this project. Run "JaiTools: Set Build File" from the Command Palette and try again.')
      return
    
    if not os.path.isfile(build_file_path):
      invalid_build_file_path_message = 'JaiTools: The following build file doesn\'t exist:\n\n' + build_file_path + '\n\nRun "JaiTools: Set Build File" from the Command Palette to select a new one.'
      sublime.error_message(invalid_build_file_path_message)
      return
    
    # A lock is used to ensure only one thread is touching the output panel at a time
    with self.panel_lock:
      # Creating the panel implicitly clears any previous contents
      self.panel = self.window.create_output_panel('jai_results')
      self.panel.set_syntax_file('Packages/JaiTools/Jai.sublime-syntax')
      self.window.run_command('show_panel', {'panel': 'output.jai_results'})
      
      args = ['jai', build_file_path]
      # args = ['echo', build_file_path]
      self.queue_write(' '.join(args) + '\n')
      # self.panel.run_command('append', {'characters': ' '.join(args) + '\n'})
      
      build_variables = self.window.extract_variables()
      working_dir = build_variables['file_path']

      # Enable result navigation. The result_file_regex does
      # the primary matching, but result_line_regex is used
      # when build output includes some entries that only
      # contain line/column info beneath a previous line
      # listing the file info. The result_base_dir sets the
      # path to resolve relative file names against.
      settings = self.panel.settings()
      settings.set(
        'result_file_regex',
        self.result_file_regex
      )
      settings.set(
        'result_line_regex',
        self.result_line_regex
      )
      settings.set('result_base_dir', working_dir) # TODO: this should be the project folder, or if multiple folders exist, the parent folder common to all project folders.

    if self.process is not None:
      self.process.terminate()
      self.process = None
    
    try:
      self.process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
      )
    except FileNotFoundError as e:
      self.queue_write(e.args[1])
      self.killed = True
      return
      
    self.killed = False

    threading.Thread(
      target=self.read_handle,
      args=(self.process.stdout,)
    ).start()

  def read_handle(self, handle):
    chunk_size = 2 ** 13
    out = b''
    while True:
      try:
        data = os.read(handle.fileno(), chunk_size)
        # If exactly the requested number of bytes was
        # read, there may be more data, and the current
        # data may contain part of a multibyte char
        out += data
        if len(data) == chunk_size:
          continue
        if data == b'' and out == b'':
          raise IOError('EOF')
        # We pass out to a function to ensure the
        # timeout gets the value of out right now,
        # rather than a future (mutated) version
        self.queue_write(out.decode(self.encoding))
        if data == b'':
          raise IOError('EOF')
        out = b''
      except (UnicodeDecodeError) as e:
        msg = 'Error decoding output using %s - %s'
        self.queue_write(msg  % (self.encoding, str(e)))
        break
      except (IOError):
        if self.killed:
          msg = 'Cancelled'
        else:
          msg = 'Finished'
        self.queue_write('\n[%s]' % msg)
        break

  def queue_write(self, text):
    sublime.set_timeout(lambda: self.do_write(text), 1)

  def do_write(self, text):
    with self.panel_lock:
      self.panel.run_command('append', {'characters': text})




