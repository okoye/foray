'''
compute some basic statistics and charts

author: Chuka <okoye9@gmail.com>
'''
import numpy as np
from scipy import stats
from itertools import groupby

def sort(buffers):
   splitter1 = lambda x: x.split('\t')[0].split(':')[0]
   splitter2 = lambda y: y.split('\t')[1].split(':')[1]
   
   for k1, group1 in groupby(sorted(buffers, key=splitter1), key=splitter1):
      for k2, group2 in groupby(sorted(group1, key=splitter2), key=splitter2):
         for value in group2:
            yield value.strip()

class Statistician(object):
   
   def __init__(self, input_file=None):
      assert(input_file is not None)
      setattr(self, 'input', input_file)

   def mean(self, values):
      '''
      compute mean of passed set of values
      '''
      pass

   def std(self, values):
      '''
      compute standard deviation of values
      '''
      pass

   def percentile(self, tile, values):
      '''
      compute the 'tile'-percentile value of values
      '''
      return stats.scoreatpercentile(values, tile)

   def _parse(self, line, major_sep='\t', minor_sep=':'):
      key, value = line.split(major_sep)
      proc, req = key.split(minor_sep)
      return (int(proc), int(req), float(value))

   def compute(self):
      matrix = list()
      for line in open(self.input):
         process, request, value = self._parse(line)
         matrix[request, process] = value
         matrix.append((process, request, value))
      

if __name__ == '__main__':
   Statistician(input_file='../results/7NodeRun.log',
                  rows=250,
                  cols=8).compute()
