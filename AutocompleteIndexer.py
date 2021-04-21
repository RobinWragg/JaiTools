import sublime
import sublime_plugin
import os
from .autocomplete_parser import get_completions

# rwtodo: Use module names instead of filenames for the UI name if the completion came from a module.
# rwtodo: ensure a buffer and a file path of the same code can't exist in the cache. That would result in duplicated completions. Maybe just watch for the file save event and delete the buffer then.
# rwtodo: it appears that files that are open but not located in one of the project folders are not parsed. When this is fixed, ensure that files which are not included in the project folders are removed from the cache when they are closed.
# rwtodo: Sublime Text doesn't resize the completions popup correctly if we give it too many completions. Gather completions from all open files, and the files/modules referenced by all #import and #load statements in the active file. Remove completions from the list if they don't contain the prefix given by on_query_completions.

class AutocompleteIndexer(sublime_plugin.EventListener):
  completion_index = {} # rwtodo: rename to completion_cache, and rename index_key to cache_key etc
  max_trigger_length = -1
  
  def get_file_contents(self, file_path):
    file_view = sublime.active_window().find_open_file(file_path)
    
    # Load from the view buffer if it exists
    if file_view == None:
      with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    else:
      return self.get_view_contents(file_view)
      
  def get_view_contents(self, view):
    pattern = '[\w\W]*'
    
    buffer_region = view.find(pattern, 0)
    
    if buffer_region == None:
      return ''
    else:
      return view.substr(buffer_region)
      
  def view_is_jai(self, view):
    settings = view.settings()
    
    if settings != None:
      syntax = settings.get('syntax')
      if syntax != None:
        if syntax.find('Jai.sublime-syntax') >= 0:
          return True

    path = view.file_name()
    
    if path != None and path[-4:].lower() == '.jai':
      return True
      
    return False
  
  def get_all_index_keys(self):
    index_keys = set()
    
    # Grab the index keys of all open jai views
    for view in sublime.active_window().views():
      if self.view_is_jai(view):
        index_keys.add(self.get_view_index_key(view))
    
    return index_keys
  
  def get_view_index_key(self, view):
    file_path = view.file_name()
    
    if file_path == None:
      return view.buffer_id()
    else:
      return file_path
  
  def get_completions_from_index_key(self, index_key):
    if self.max_trigger_length == -1:
      # rwtodo: add a menu option to open JaiTools.sublime-settings the same way Package Control does it.
      settings = sublime.load_settings('JaiTools.sublime-settings')
      self.max_trigger_length = settings.get('completions_popup_max_width', 1000)
    
    completions = None
    
    if isinstance(index_key, str):
      # index_key is a file path.
      ui_name = os.path.basename(index_key) # rwtodo: this should be the module name if the file is part of a standard module. Not sure about user modules.
      text = self.get_file_contents(index_key)
      completions = get_completions(text, ui_name, self.max_trigger_length)
    else:
      # index_key is a buffer ID (int). This means the Jai code only exists in an unsaved view.
      # The API can't get text from the buffer directly, so find a view associated with it (if any).
      for view in sublime.active_window().views():
        if view.buffer_id() == index_key:
          jai_text = self.get_view_contents(view)
          completions = get_completions(jai_text, '(unsaved)', self.max_trigger_length)
          break
    
    return completions
  
  def index_view(self, view, is_async):
    if not self.view_is_jai(view):
      return
    
    index_key = self.get_view_index_key(view)
    
    completions = self.get_completions_from_index_key(index_key)
    
    if completions != None:
      self.completion_index[index_key] = completions
  
  def initialize_index(self):
    # Gather completions from all views.
    new_completion_index = {}
    all_index_keys = self.get_all_index_keys()
    
    for index_key in all_index_keys:
      completions = self.get_completions_from_index_key(index_key)
      
      if completions != None:
        new_completion_index[index_key] = completions
    
    self.completion_index = new_completion_index
  
  def on_post_save_async(self, view):
    if not self.view_is_jai(view):
      return None
    
    # If the view's buffer ID is a key in the index, it needs to be replaced with the view's file path.
    # This is done by deleting the buffer ID and re-indexing the view.
    if view.buffer_id() in self.completion_index:
      del self.completion_index[view.buffer_id()]
    
    self.index_view(view, True)
  
  def on_activated_async(self, view):
    if not self.view_is_jai(view):
      return None
    
    self.initialize_index()
  
  def on_deactivated_async(self, view):
    if not self.view_is_jai(view):
      return None
      
    self.index_view(view, True)
  
  def on_query_completions(self, view, prefix, locations):
    if not self.view_is_jai(view):
      return None
    
    self.index_view(view, False)
    
    completions = []
    for key in self.completion_index.keys():
      completions += self.completion_index[key]
    
    return completions





