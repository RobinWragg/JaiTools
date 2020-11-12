from .Common import *
import sublime
import sublime_plugin
import os

# rwtodo: Check for jai exe and 'JaiTools couldn't build your code because the Jai compiler was not found. To fix this, add the compiler to your PATH environment variable.'

class GenerateJaiBuildSystemCommand(sublime_plugin.WindowCommand):
	def run(self):
		pass
		# rwtodo: ask for build command 'jai myfile.jai -args'



