'''
compute some basic statistics and charts

author: Chuka <okoye9@gmail.com>
'''
import numpy as np
from scipy import stats

#TODO: support args to program

class Statistician(object):
   
   def __init__(self, input_file=None, rows=0, cols=0):
      assert(input_file is not None)
      assert(rows > 0 and cols > 0)
      setattr(self, 'input', input_file)
      setattr(self, 'rows', rows)
      setattr(self, 'cols', cols)

   def graph(self, values):
      '''
      generates a line graph given a list of tuples (x, y)
      '''
      pass

   def describe(self, values, title=None):
      '''
      generate some statistic for the passed set of values
      '''
      mean = np.mean(values)
      std = np.std(values)
      var = np.var(values)

      print '###############Statistics for %s #############'%title
      print 'Mean: %s'%mean
      print 'Standard Deviation: %s'%std
      print 'Variance: %s'%var
      

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
