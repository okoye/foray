'''
emit only words of length 3 and above
'''
from sys import argv, exit, stdin

if '-h' in argv or 'usage' in argv:
   print 'reads input from stdin and prints to stdout'
   exit()

for line in stdin:
   if len(line) >= 3:
      print line.strip()
