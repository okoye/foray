'''
compute some basic statistics and charts

author: Chuka <okoye9@gmail.com>
'''
import optparse
from os import listdir
from scipy import stats as sci
from itertools import groupby
from statlib import stats

class Statistician(object):
  
   def __init__(self):
      pass  

   def mean(self, values):
      '''
      compute mean of passed set of values
      '''
      return stats.mean(values)

   def cleaned_mean(self, values):
      '''
      compute mean of all values that fall within 2 s.d
      '''
      pass

   def cleaned_percentile(values):
      pass

   def cleaned_std(values):
      pass

   def std(self, values):
      '''
      compute standard deviation of values
      '''
      return stats.stdev(values)

   def percentile(self, tile, values):
      '''
      compute the 'tile'-percentile value of values
      '''
      return sci.scoreatpercentile(values, tile)

   def compute(self, values, skip_500s=False, 
                  clean_data=False):
      '''
      compute all available descriptive stats
      '''
      if skip_500s:
         cleaned_values = [e for e in values if e != 500.0]
         values = cleaned_values
         print 'skipped 500 errors'
      if clean_data:
         std = self.std(values)
         mean = self.mean(values)
         inrange = lambda x: x < mean+(std*2) and x > mean-(std*2)
         cleaned_values = [e for e in values if inrange(e)]
         values = cleaned_values
         print 'using cleaned data'
      return '%f\t%f\t%f'%(self.mean(values),
                           self.std(values),
                           self.percentile(90, values))

def main(directory, output, clean=False):
   print 'processing files in', directory
   stats = Statistician()
   buff = list()
   results = list()
   results.append('logid\tmean\tstdev\t90percentile')
   
   for f in listdir(directory): 
      #load file into memory
      for l in open('/'.join([directory, f])):
         buff.append(float(l.split('\t')[1]))
      #compute stats for file
      results.append('%s\t%s'%(f, stats.compute(buff, 
               skip_500s=True, clean_data=clean)))
   print 'finished computing results', len(results)
   with open(output, 'w') as f:
      for line in results:
         f.write('%s\n'%line)

if __name__ == '__main__':
   parser = optparse.OptionParser()
   parser.add_option('-d', '--directory', help='directory containing files',
                     dest='direc', default='./')
   parser.add_option('-o', '--output', help='output dir',
                     dest='output', default='output.txt')
   parser.add_option('-c', '--clean', help='compute on cleaned data',
                     dest='clean', default=False)
   (opts, args) = parser.parse_args()
   main(opts.direc, opts.output, clean=opts.clean)
