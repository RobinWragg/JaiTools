from .Common import *
from .PythonParser import *
from .MetaprogramParser import *
import sublime_plugin
import time

# TODO: use filename, not file path, for the UI filenames, unless it's part of a module, in which case print only the module name.

class AutocompleteIndexer(sublime_plugin.EventListener):
  gather_from_unopen_files = False
  completion_index = {}
  parser = None
  
  full_reindex_interval_secs = 60 * 10 # Ten minutes
  last_full_reindex_secs = -full_reindex_interval_secs # Ensure re-indexing happens on launch
  
  def get_parser(self):
    # TODO: here we can check which parser to use.
    settings = sublime.load_settings('JaiTools.sublime-settings')
    
    if self.parser == None:
      if settings.get('use_compiler_for_completions') == True:
        self.parser = MetaprogramParser()
      else:
        self.parser = PythonParser()
        
    return self.parser
  
  def get_all_index_keys(self):
    index_keys = set()
    
    # Get jai file paths from all open folders
    if self.gather_from_unopen_files:
      index_keys = get_all_jai_project_file_paths()
    
    # Load all open jai views in case they're unsaved or external files
    for view in sublime.active_window().views():
      if view_is_jai(view):
        index_keys.add(self.get_view_index_key(view))
    
    return index_keys
  
  def get_view_index_key(self, view):
    file_path = view.file_name()
    
    if file_path == None:
      return view.buffer_id()
    else:
      return file_path
  
  def index_view(self, view, is_async):
    # If a full re-index hasn't been performed recently (see the value of
    # full_reindex_interval_secs), and this function will not block the user (an async event),
    # re-index everything in order to:
    #  - Gather completions from files that are in the project but aren't open
    #  - Remove deleted files (the API doesn't provide an event for file deletions)
    #  - Index any file changes that were made outside of Sublime Text
    if is_async and time.time() - self.last_full_reindex_secs > self.full_reindex_interval_secs:
      self.reindex_everything()
      return
    
    if not view_is_jai(view):
      return
    
    index_key = self.get_view_index_key(view)
    file_name_for_user = ''
    
    if isinstance(index_key, str):
      # index_key is the file path
      file_name_for_user = os.path.basename(index_key)
      
      # Ensure there is no reference to the buffer, as it would contain duplicate completions.
      buffer_id = view.buffer_id()
      if buffer_id in self.completion_index:
        del self.completion_index[buffer_id]
      
      self.completion_index[index_key] = self.get_parser().get_completions_from_file(index_key, file_name_for_user)
    else:
      # index_key is the buffer ID, meaning there is no corresponding file on disk.
      file_name_for_user = 'unsaved'
      jai_text = get_view_contents(view)
      self.completion_index[index_key] = self.get_parser().get_completions_from_text(jai_text, file_name_for_user)
  
  def reindex_everything(self):
    print('JaiTools: Starting re-indexing of completions')
    
    start_time = time.time()
    
    new_completion_index = {}
    all_index_keys = self.get_all_index_keys()
    
    # Split keys into file paths and buffer IDs to gather completions differently
    file_paths = filter(lambda x: isinstance(x, str), all_index_keys)
    buffer_ids = filter(lambda x: isinstance(x, int), all_index_keys)
    
    for path in file_paths:
      name_for_user = os.path.basename(path)
      new_completion_index[path] = self.get_parser().get_completions_from_file(path, name_for_user)
    
    for buffer_id in buffer_ids:
      # The API can't get text from the buffer directly, so find a view associated with it (if any).
      for view in sublime.active_window().views():
        if view.buffer_id() == buffer_id:
          jai_text = get_view_contents(view)
          new_completion_index[buffer_id] = self.get_parser().get_completions_from_text(jai_text, 'unsaved')
          break
    
    self.completion_index = new_completion_index
    self.last_full_reindex_secs = time.time()
    
    duration_ms = int((time.time() - start_time) * 1000)
    print('JaiTools: Full re-indexing of completions took ' + str(duration_ms) + 'ms')
    
  def on_pre_close(self, view):
    self.index_view(view, True)
  
  def on_deactivated_async(self, view):
    self.index_view(view, True)
  
  def on_activated_async(self, view):
    self.index_view(view, True)
  
  def on_query_completions(self, view, prefix, locations):
    if not view_is_jai(view):
      return None
    
    self.index_view(view, False)
    
    completions = []
    for key in self.completion_index.keys():
      completions += self.completion_index[key]
    
    return completions





