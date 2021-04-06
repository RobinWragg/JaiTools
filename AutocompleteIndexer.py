from .Common import *
from .CompletionParser import *
import sublime_plugin
import time

# rwtodo: Use module names instead of filenames for the UI name if the completion came from a module.
# rwtodo: ensure a buffer and a file path of the same code can't exist in the cache. That would result in duplicated completions. Maybe just watch for the file save event and delete the buffer then.
# rwtodo: it appears that files that are open but not located in one of the project folders are not parsed. When this is fixed, ensure that files which are not included in the project folders are removed from the cache when they are closed.
# rwtodo: Sublime Text doesn't resize the completions popup correctly if we give it too many completions. Gather completions from all open files, and the files/modules referenced by all #import and #load statements in the active file. Remove completions from the list if they don't contain the prefix given by on_query_completions.

class AutocompleteIndexer(sublime_plugin.EventListener):
  completion_index = {} # rwtodo: rename to completion_cache, and rename index_key to cache_key etc
  parser = CompletionParser()
  
  def get_all_index_keys(self):
    index_keys = set()
    
    # Grab the index keys of all open jai views
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
      completions = self.parser.get_completions_from_file(index_key, ui_name)
      
    else:
      # index_key is a buffer ID (int). This means the Jai code only exists in an unsaved view.
      # The API can't get text from the buffer directly, so find a view associated with it (if any).
      for view in sublime.active_window().views():
        if view.buffer_id() == index_key:
          jai_text = get_view_contents(view)
          completions = self.parser.get_completions_from_text(jai_text, 'unsaved')
          break
    
    return completions
  
  def index_view(self, view, is_async):
    if not view_is_jai(view):
      return
    
    index_key = self.get_view_index_key(view)
    
    completions = self.get_completions_from_index_key(index_key)
    
    if completions != None:
      self.completion_index[index_key] = completions
  
  def initialize_index(self):
    # Gather completions from all views.
    
    print('JaiTools: Starting re-indexing completions...')
    
    start_time = time.time()
    
    new_completion_index = {}
    all_index_keys = self.get_all_index_keys()
    
    for index_key in all_index_keys:
      completions = self.get_completions_from_index_key(index_key)
      
      if completions != None:
        new_completion_index[index_key] = completions
    
    self.completion_index = new_completion_index
    
    duration_ms = int((time.time() - start_time) * 1000)
    print('JaiTools: Full re-indexing completions took ' + str(duration_ms) + 'ms')
  
  def on_post_save_async(self, view):
    if not view_is_jai(view):
      return None
    
    # If the view's buffer ID is a key in the index, it needs to be replaced with the view's file path.
    # This is done by deleting the buffer ID and re-indexing the view.
    if view.buffer_id() in self.completion_index:
      del self.completion_index[view.buffer_id()]
    
    self.index_view(view, True)
  
  def on_activated_async(self, view):
    if not view_is_jai(view):
      return None
    
    self.initialize_index()
  
  def on_deactivated_async(self, view):
    if not view_is_jai(view):
      return None
      
    self.index_view(view, True)
  
  def on_query_completions(self, view, prefix, locations):
    if not view_is_jai(view):
      return None
    
    self.index_view(view, False)
    
    completions = []
    for key in self.completion_index.keys():
      completions += self.completion_index[key]
    
    return completions





