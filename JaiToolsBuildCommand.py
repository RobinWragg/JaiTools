import sublime
import sublime_plugin
import os

class JaiToolsBuildCommand(sublime_plugin.WindowCommand):
	common_parent_dir = None
	abs_file_paths = []
	rel_file_paths = []
	active_rel_file_path = None
	
	def run(self):
		paths_set = get_all_jai_project_file_paths()
		
		# Add open files to the paths set, in case they're not part of the project
		for view in sublime.active_window().views():
			if view_is_jai(view) and view.file_name() != None:
				paths_set.add(view.file_name())
		
		if len(paths_set) == 0:
			sublime.error_message('There are no Jai files open or in your project. Save a Jai file and try again.')
			return None
		
		self.common_parent_dir = get_common_parent_dir(list(paths_set))
		
		if len(paths_set) == 1:
			self.active_rel_file_path = os.path.relpath(list(paths_set)[0], self.common_parent_dir)
			self.perform_exec_command()
		else:
			self.abs_file_paths = sorted(list(paths_set))
			self.rel_file_paths = list(map(lambda p: os.path.relpath(p, self.common_parent_dir), self.abs_file_paths))
			list_input = map(lambda p: "Run 'jai " + p + "'", self.rel_file_paths)
			
			self.window.show_quick_panel(list(list_input), self.on_quick_panel_done)
	
	def perform_exec_command(self):
		exec_args = {
			'cmd': ['jai', self.active_rel_file_path],
			'working_dir': self.common_parent_dir,
			'file_regex': build_result_file_regex
		}
		self.window.run_command('exec', exec_args)
	
	def on_quick_panel_done(self, file_path_index):
		if file_path_index < 0:
			return
		
		self.active_rel_file_path = self.rel_file_paths[file_path_index]
		self.perform_exec_command()
	







