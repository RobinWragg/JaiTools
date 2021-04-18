import cProfile
import sys
import os
import re

# This is a hack to import autocomplete_parser from the parent directory, because Python.
sys.path.append('..')
from autocomplete_parser import *

jai_file_path = os.path.expanduser('~/Downloads/jai-beta-053/modules/Sound_Player/module.jai')

with open(jai_file_path, 'r') as f:
  jai_text = f.read()

jai_file_basename = os.path.basename(jai_file_path)

def get_completions_repeatedly():
  # Call get_completions() several times to get a more accurate profile.
  for i in range(100):
    get_completions(jai_text, jai_file_basename)

cProfile.run('get_completions_repeatedly()', sort='cumtime')

# regex_declarations = re.findall(r'\w+\s*::', jai_text)
# parser_declarations = get_completions(jai_text, jai_file_basename)
# print('regex declarations: ' + str(len(regex_declarations)))
# print('parser declarations: ' + str(len(parser_declarations)))

# for d in regex_declarations[:10]:
#   print(d)
# print()
# for d in parser_declarations[:10]:
#   print(d)

