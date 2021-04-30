import sublime
import sublime_plugin
import os
from .autocomplete_parser import get_completions

class Autocompleter(sublime_plugin.EventListener):
  completion_cache = {}
  cache_initialized = False
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
  
  def get_all_cache_keys(self):
    cache_keys = set()
    
    # Grab the cache keys of all open jai views
    for view in sublime.active_window().views():
      if self.view_is_jai(view):
        cache_keys.add(self.get_view_cache_key(view))
    
    return cache_keys
  
  def get_view_cache_key(self, view):
    file_path = view.file_name()
    
    if file_path == None:
      return view.buffer_id()
    else:
      return file_path
  
  def get_view_by_buffer_id(self, buffer_id):
    for view in sublime.active_window().views():
      if view.buffer_id() == buffer_id:
        return view
    return None
  
  def get_completions_from_cache_key(self, cache_key):
    if self.max_trigger_length == -1:
      # rwtodo: add a menu option to open JaiTools.sublime-settings the same way Package Control does it.
      settings = sublime.load_settings('JaiTools.sublime-settings')
      self.max_trigger_length = settings.get('completions_popup_max_width', 1000)
    
    completions = None
    
    if isinstance(cache_key, str):
      # cache_key is a file path.
      ui_name = os.path.basename(cache_key)
      text = self.get_file_contents(cache_key)
      completions = get_completions(text, ui_name, False, self.max_trigger_length)
    else:
      # cache_key is a buffer ID (int). This means the Jai code only exists in an unsaved view.
      # The API can't get text from the buffer directly, so find a view associated with it (if any).
      view = self.get_view_by_buffer_id(cache_key)
      if view:
        jai_text = self.get_view_contents(view)
        completions = get_completions(jai_text, '(unsaved)', False, self.max_trigger_length)
    
    return completions
  
  def get_completions_from_view(self, view):
    if not self.view_is_jai(view):
      return
    
    cache_key = self.get_view_cache_key(view)
    
    completions = self.get_completions_from_cache_key(cache_key)
    
    if completions != None:
      self.completion_cache[cache_key] = completions
  
  def initialize_cache(self):
    # Gather completions from all views.
    new_completion_cache = {}
    all_cache_keys = self.get_all_cache_keys()
    
    for cache_key in all_cache_keys:
      completions = self.get_completions_from_cache_key(cache_key)
      
      if completions != None:
        new_completion_cache[cache_key] = completions
    
    self.completion_cache = new_completion_cache
    self.cache_initialized = True
  
  def on_post_save_async(self, view):
    if not self.view_is_jai(view):
      return None
    
    # If the view's buffer ID is a key in the cache, it needs to be replaced with the view's file path.
    # This is done by deleting the buffer ID and re-cacheing the view.
    if view.buffer_id() in self.completion_cache:
      del self.completion_cache[view.buffer_id()]
    
    self.get_completions_from_view(view)
  
  def on_activated_async(self, view):
    if not self.view_is_jai(view):
      return
    
    if not self.cache_initialized:
      self.initialize_cache()
  
  def on_deactivated_async(self, view):
    if not self.view_is_jai(view):
      return
    
    self.get_completions_from_view(view)
  
  def on_query_completions(self, view, prefix, locations):
    if not self.view_is_jai(view):
      return None
    
    active_view_key = self.get_view_cache_key(view)
    
    # Delete completions from the cache if the view isn't open anymore
    keys_to_delete = []
    for key in self.completion_cache.keys():
      if isinstance(key, str):
        if view.window().find_open_file(key) == None:
          keys_to_delete.append(key)
      else:
        if self.get_view_by_buffer_id(key) == None:
          keys_to_delete.append(key)
    for key in keys_to_delete:
      del self.completion_cache[key]
    
    # Gather completions into one list
    completions = []
    for key in self.completion_cache.keys():
      if key == active_view_key:
        continue
      completions += self.completion_cache[key]
    
    # Add the active view's completions to the completions list
    jai_text = self.get_view_contents(view)
    completions += get_completions(jai_text, 'rwtodo', True, self.max_trigger_length)
    
    # rwtodo: filter out identifiers that don't contain 'prefix'. Design the cache to make this fast.
    
    return completions





