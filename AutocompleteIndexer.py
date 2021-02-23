from .Common import *
from .PythonParser import *
from .MetaprogramParser import *
import sublime_plugin
import time

# TODO: parser can return a list of completions or None. If None, don't modify the completion index. This will mean ST will use completions from the last time the file was able to be parsed. If the index doesn't already contain completions for the file, assign an empty array.
# TODO: use filename, not file path, for the UI filenames, unless it's part of a module, in which case print only the module name.
# rwtodo: ensure a buffer and a file path of the same code can't exist in the cache. That would result in duplicated completions. Maybe just watch for the file save event and delete the buffer then.
# rwtodo: it appears that files that are open but not located in one of the project folders are not parsed.

class AutocompleteIndexer(sublime_plugin.EventListener):
  gather_from_unopen_files = True # rwtodo: add this as a preference
  completion_index = {} # rwtodo: rename to completion_cache, and rename index_key to cache_key etc
  parser = None
  reindex_in_progress = False
  
  full_reindex_interval_secs = 60 * 10 # Ten minutes
  last_full_reindex_secs = -full_reindex_interval_secs # Ensure re-indexing happens on launch
  
  def get_parser(self):
    if self.parser == None:
      settings = sublime.load_settings('JaiTools.sublime-settings')
      
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
  
  def get_completions_from_index_key(self, index_key):
    completions = None
    
    if isinstance(index_key, str):
      # index_key is a file path.
      ui_name = os.path.basename(index_key) # rwtodo: this should be the module name if the file is part of a standard module. Not sure about user modules.
      completions = self.get_parser().get_completions_from_file(index_key, ui_name)
    else:
      # index_key is a buffer ID (int). This means the Jai code only exists in an unsaved view.
      # The API can't get text from the buffer directly, so find a view associated with it (if any).
      for view in sublime.active_window().views():
        if view.buffer_id() == index_key:
          jai_text = get_view_contents(view)
          completions = self.get_parser().get_completions_from_text(jai_text, 'unsaved')
          break
    
    return completions
  
  def index_view(self, view, is_async):
    if not view_is_jai(view):
      return
      
    # If a full re-index hasn't been performed recently (see the value of
    # full_reindex_interval_secs), and this function will not block the user (an async event),
    # re-index everything in order to:
    #  - Gather completions from files that are in the project but aren't open
    #  - Remove deleted files (the API doesn't provide an event for file deletions)
    #  - Index any file changes that were made outside of Sublime Text
    if is_async and time.time() - self.last_full_reindex_secs > self.full_reindex_interval_secs:
      self.reindex_everything()
      return
    
    index_key = self.get_view_index_key(view)
    
    completions = self.get_completions_from_index_key(index_key)
    
    if completions != None:
      self.completion_index[index_key] = completions
  
  def reindex_everything(self):
    if self.reindex_in_progress:
      return
    else:
      self.reindex_in_progress = True
    
    print('JaiTools: Starting re-indexing of completions')
    self.last_full_reindex_secs = time.time()
    
    start_time = time.time()
    
    new_completion_index = {}
    all_index_keys = self.get_all_index_keys()
    
    for index_key in all_index_keys:
      completions = self.get_completions_from_index_key(index_key)
      
      if completions != None:
        new_completion_index[index_key] = completions
    
    self.completion_index = new_completion_index
    
    duration_ms = int((time.time() - start_time) * 1000)
    print('JaiTools: Full re-indexing of completions took ' + str(duration_ms) + 'ms')
    self.reindex_in_progress = False
    
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





