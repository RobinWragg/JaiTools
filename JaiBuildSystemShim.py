import sys

print(sys.argv[0])
current_jai_file = sys.argv[1]
print('JaiTools: Building project...')
print('JaiTools: No build.jai file found in the project.')
print(f'JaiTools: Running \'jai {current_jai_file}\'...')