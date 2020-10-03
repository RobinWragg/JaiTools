import os
import sublime
import sublime_plugin
from .Common import *

# TODO: do this when jai gives build results:
# result_regions = list( map(lambda x: x['region'], build_results) )
# view.add_regions('jai_build_results', result_regions, 'invalid')

class BuildResultViewer(sublime_plugin.EventListener):
	
	def region_contains_point(self, region, point):
		return point >= region.a and point < region.b
		
	def on_selection_modified(self, view):
		if not view_is_jai(view) or len(build_results) == 0:
			return
		
		selection = view.sel()
		
		if len(selection) == 1:
			self.try_show_result_message(view, selection[0].b)
	
	def get_result_for_point_in_view(self, point, view):
		file_path = view.file_name()
		
		if file_path == None:
			return
		
		file_path = os.path.abspath(file_path)
		file_results = filter(lambda e: e['file_path'] == file_path, build_results)
		
		this_line = view.line(point)
		results_on_this_line = filter(lambda e: self.region_contains_point(this_line, e['region'].a), file_results)
		results_on_this_line = list(results_on_this_line)
		
		if len(results_on_this_line) == 0:
			return None
		
		results_on_this_line.sort(key=lambda e: e['region'].a)
		
		# Pick the build result that contains the point, if any
		for result in results_on_this_line:
			if self.region_contains_point(result['region'], point):
				return result
		
		# Default to the first result on the line
		return results_on_this_line[0]
		
	def try_show_result_message(self, view, point):
		result = self.get_result_for_point_in_view(point, view)
		
		if result == None:
			return
		
		# TODO: Make multiline messages presentable by inserting '<br>' at appropriate locations. The API assumes the HTML is one line high if you don't, and shows a one-line popup.
		html = """
			<html style="background-color: #800; color: #fff;">
				<body id=jai-build-result>%s</body>
			</html>
		""" % result['message']
		
		view.show_popup(html, location=result['region'].a+1, max_width=1200, max_height=500)
		






