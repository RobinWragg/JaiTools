import sublime
import sublime_plugin
import os

class OpenJaiToolsReadmeCommand(sublime_plugin.WindowCommand):
	def run(self):
		readme_view_name = 'JaiTools: Read Me'
		
		for view in self.window.views():
			if view.name() == readme_view_name:
				self.window.focus_view(view)
				return
		
		readme_view = self.window.new_file()
		readme_view.set_scratch(True)
		readme_view.set_name(readme_view_name)
		readme_view.set_syntax_file('Packages/Markdown/Markdown.sublime-syntax')
		
		readme_text = sublime.load_resource('Packages/JaiTools/README.md')
		readme_view.run_command('append', {'characters': readme_text})



