'''
compute some basic statistics and charts

author: Chuka <okoye9@gmail.com>
'''
import optparse
from os import listdir
from scipy import stats as sci
from itertools import groupby
from statlib import stats

def sort(buffers):
   '''helper function to sort process data'''
   splitter1 = lambda x: x.split('\t')[0].split(':')[0]
   splitter2 = lambda y: y.split('\t')[1].split(':')[1]
   
   for k1, group1 in groupby(sorted(buffers, key=splitter1), key=splitter1):
      for k2, group2 in groupby(sorted(group1, key=splitter2), key=splitter2):
         for value in group2:
            yield value.strip()


class Statistician(object):
   
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

   def compute(self, values):
      '''
      compute all available descriptive stats
      '''
      return '%f\t%f\t%f'%(self.mean(values),
                           self.std(values),
                           self.percentile(90, values))

def main(directory, output):
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
      results.append('%s\t%s'%(f, stats.compute(buff)))
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
   (opts, args) = parser.parse_args()
   main(opts.direc, opts.output)
