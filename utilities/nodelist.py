'''
using the output of cassandra's nodetool ring info, emit to std out
the ips of various nodes in the cluster
'''
from sys import argv, exit, stdin

if '-h' in argv or 'usage' in argv:
   print 'reads input from stdin and prints to stdout'
   exit()


for line in stdin:
   value = line.split()[0]
   if '.' in value:
      print value
