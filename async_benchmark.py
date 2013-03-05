'''
Goal of this module is to connect and run several concurrent requests to a
solr REST interface to determine and store the timings of the request.

author: Chuka <okoye9@gmail.com>
'''
import optparse
import signal
import random
import time
import logging
import string
import urllib2
import urllib
from multiprocessing import Process, Queue

###############Benchmark Proper#################
class Benchmark(object):
   
   def __init__(self, i, queue, num_req=1000, nodes='nodes.txt'):
      self.process_id = i
      self.requests = int(num_req)
      self.solr_urls = []
      self.q = queue
      for node in open(nodes):
         self.solr_urls.append(self._solr_url(node.strip()))
      print 'solr node list: ', self.solr_urls 
      print 'Benchmark instantiated'

   def start(self):
      print 'Benchmark started'
      self._benchmark()

   def _solr_url(self, node, port=8983, args='solr/wiki.solr'):
      '''construct solr url object'''
      return 'http://%s:%s/%s/select/?'%(node, port, args)
   
   def _benchmark(self):
      '''
      spawn request_no of solr requests
      '''
      import gevent
      from gevent import monkey; monkey.patch_socket()

      greenlets = []
      for i in xrange(self.requests):
         greenlets.append(gevent.spawn(self._request))

      print 'now waiting for greenlet completion...'
      gevent.joinall(greenlets)
      print 'all greenlets completed'

   def _request(self):
      '''
      each of this is run in a greenlet thread.
      actual request maker. records start time, end time and appends
      '''
      url = random.sample(self.solr_urls, 1)[0]
      diff = lambda past: time.time() - past
      term = random.sample(['california', 'facebook', 'microsoft', 'wikipedia',
      'obama'], 1)[0]
      encoded_args = urllib.urlencode({'q':term, 'wt':'json'})
      start = diff(0)
      result = urllib2.urlopen(url+encoded_args) 
      delta_time = diff(start)
      value = "%s\t%s"%(result.getcode(), delta_time)
      self.q.put(value, block=False)
      
###############Process Management################
if __name__ == '__main__':
   parser = optparse.OptionParser()
   parser.add_option('-r', '--requests', help='no of concurrent requests',
                     dest='requests', default=1000)
   parser.add_option('-p', '--processes', help='no of processes',
                     dest='processes', default=4)
   parser.add_option('-n', '--nodes', help='nodes list file', 
                     dest='nodes', default='nodes.txt')
   parser.add_option('-o', '--output', help='output filename',
                     dest='output', default=None)
   parser.add_option('-c', '--cluster', help='cluster size',
                     dest='cluster', default=None)
   (opts, args) = parser.parse_args()

   #Process management stuff
   processes = []
   queue = Queue(int(opts.requests) * int(opts.processes))
   for i in xrange(int(opts.processes)):
      benchmark = Benchmark(i, queue, num_req=int(opts.requests), 
               nodes=opts.nodes)
      processes.append(Process(target=benchmark.start))
      processes[-1].start()
   
   #Signal handlers
   def shutdown(signum, stackframe):
      for proc in processes:
         proc.terminate()
   signal.signal(signal.SIGTERM, shutdown)

   #Post Processing
   if not opts.output:
      output_file = ''.join(random.sample(string.letters+string.digits, 10))+'.bench'
      if opts.cluster:
         output_file = opts.cluster+'_'+output_file
   else:
      output_file = opts.output
   try:
      for proc in processes:
         proc.join()
      print 'writing output to file' 
      with open(output_file, "w") as f:
         while not queue.empty():
            f.write('%s\n'%queue.get(block=False))
   except KeyboardInterrupt as ki:
      print 'executing shutdown procedure..'
      for proc in processes:
         proc.terminate()
