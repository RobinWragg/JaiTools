import sublime

class MetaprogramParser:
  def get_completions_from_file(self, path, name_for_user):
    print("NOT IMPLEMENTED YET")
    crash
  
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
  