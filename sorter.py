import sys
from itertools import groupby

#sorts first by process id then sorts by thread id

buf = list()
#first store object
for line in sys.stdin:
   buf.append(line)

#now start sorting
skey1 = lambda x: x.split('\t')[0].split(':')[0]
skey2 = lambda y: y.split('\t')[0].split(':')[1]

for k1, group1 in groupby(sorted(buf, key=skey1), key=skey1):
   for k2, group2 in groupby(sorted(group1, key=skey2), key=skey2):
      for value in group2:
         print value.strip()
   print "#########"
