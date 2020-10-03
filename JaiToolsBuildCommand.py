from .Common import *
import sublime_plugin
import subprocess
import threading
import re

class JaiToolsBuildCommand(sublime_plugin.WindowCommand):
	result_pattern_for_keyboard_navigation = r'^(.+?):(\d+)(?:,(\d+))?:\s*.+?$'
	result_pattern_for_custom_messages = r'\n(.+?):(\d+)(?:,(\d+))?:\s*(.+?)\n'
	result_regex = re.compile(result_pattern_for_custom_messages)
	
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
			sublime.error_message('JaiTools: No build file has been chosen for this project. Run "JaiTools: Set Build File" from the Command Palette and try building again.')
			return
		
		if not os.path.isfile(build_file_path):
			invalid_build_file_path_message = 'JaiTools: The following build file doesn\'t exist:\n\n' + build_file_path + '\n\nRun "JaiTools: Set Build File" from the Command Palette to select a new one, and try building again.'
			sublime.error_message(invalid_build_file_path_message)
			return
		
		# A lock is used to ensure only one thread is touching the output panel at a time
		with self.panel_lock:
			# Creating the panel implicitly clears any previous contents
			self.panel = self.window.create_output_panel(PANEL_KEY_build_results.replace('output.', ''))
			# self.panel.set_syntax_file('Packages/JaiTools/Jai.sublime-syntax')
			self.window.run_command('show_panel', {'panel': PANEL_KEY_build_results})
			
			args = ['cat', build_file_path]
			
			self.queue_write(' '.join(args) + '\n')
			
			build_variables = self.window.extract_variables()
			working_dir = build_variables['file_path']
			
			settings = self.panel.settings()
			settings.set(
				'result_file_regex',
				self.result_pattern_for_keyboard_navigation
			)

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
		compiler_output_str = ''
		
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
				output_section = out.decode(self.encoding)
				compiler_output_str += output_section
				self.queue_write(output_section)
				if data == b'':
					raise IOError('EOF')
				out = b''
			except (UnicodeDecodeError) as e:
				msg = 'Error decoding output using %s - %s'
				self.queue_write(msg  % (self.encoding, str(e)))
				break
			except (IOError):
				if self.killed:
					self.queue_write('[Cancelled]')
				else:
					self.queue_write('[Finished]')
					self.add_build_results_to_views(compiler_output_str)
				break

	def queue_write(self, text):
		sublime.set_timeout(lambda: self.do_write(text), 1)

	def do_write(self, text):
		with self.panel_lock:
			self.panel.run_command('append', {'characters': text})
	
	def add_build_results_to_views(self, compiler_output):
		build_results = []
		
		r = re.compile('robin')
		matches = re.finditer(self.result_regex, compiler_output)
		
		for i in matches:
			file = i.group(1).strip()
			line = int(i.group(2))
			col = i.group(3)
			msg = i.group(4).strip()
			
			if col == None:
				col = 0
			else:
				col = int(col)
			
			result = {
				'file_path': os.path.abspath(file),
				'line': line,
				'col': col,
				'message': msg
			}
			
			build_results.append(result)
			# TODO: get these results to BuildResultViewer somehow.
		
		




