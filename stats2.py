
import numpy as np
from scipy import stats

def parse(line, majo, mino):
   key, value = line.split(majo)
   proc, req = key.split(mino)
   return (int(proc), int(req), float(value))

def main(input_file):
   readings = []
   for line in open(input_file):
      readings.append(parse(line, '\t', ':'))

   #now, compute 90th percentile value
   l = lambda z: z[2]
   p = stats.scoreatpercentile(map(l, readings), 99)
   print p
      


if __name__ == '__main__':
   main('/Users/dokoye/Desktop/dump/benchmark_data/4_400.log')
