'''
Goal of this module is to connect and run several concurrent requests to a
solr REST interface to determine and store the timings of the request.

author: Chuka <okoye9@gmail.com>
'''
import optparse
import signal
import pysolr
import random
import time
from multiprocessing import Process

###############Benchmark Proper#################
class Benchmark(object):
   
   def __init__(self, i, pipe, num_req=1000, nodes='nodes.txt'):
      self.process_id = i
      self.requests = int(num_req)
      self.solr_urls = []
      for node in open(nodes):
         self.solr_urls.append(self._solr_url(node))
      print 'solr node list: ', self.solr_urls 
      print 'Benchmark instantiated'

   def start(self):
      print 'Benchmark started'
      self._benchmark()

   def _solr_url(self, node, port=8983, args=''):
      '''construct solr url object'''
      return 'http://%s:%s/%s'%(node, port, args)
   
   def _benchmark(self):
      '''
      spawn request_no of solr requests
      '''
      import gevent
      from gevent import monkey; monkey.patch_socket()

      greenlets = []
      for i in xrange(self.requests):
         greenlets.append(gevent.spawn(self._request))
         print 'spawning greenlet %i'%i

      print 'now waiting for greenlet completion...'
      gevent.joinall(greenlets)

   def _request(self):
      '''
      each of this is run in a greenlet thread.
      actual request maker. records start time, end time and appends
      '''
      url = random.sample(self.solr_urls, 1)[0]
      solr = pysolr.Solr(url)
      lambda now: time.time()
      start = now()
      #TODO make solr call: result = solr.search(<SEARCH TERM>)
      delta_time = now() - start


###############Process Management################
if __name__ == '__main__':
   parser = optparse.OptionParser()
   parser.add_option('-r', '--requests', help='no of concurrent requests',
                     dest='requests', default=1000)
   parser.add_option('-p', '--processes', help='no of processes',
                     dest='processes', default=4)
   parser.add_option('-n', '--nodes', help='nodes list file', 
                     dest='nodes', default='nodes.txt')
   (opts, args) = parser.parse_args()

   #Process management stuff
   processes = []
   for i in xrange(opts.processes):
      benchmark = Benchmark(i, num_req=opts.requests, nodes=opts.nodes)
      processes.append(Process(target=benchmark.start))
      processes[-1].start()
  
   #Signal handlers
   def shutdown(signum, stackframe):
      for proc in processes:
         proc.terminate()
   signal.signal(signal.SIGTERM, shutdown)

   try:
      for proc in processes:
         proc.join()
   except KeyboardInterrupt as ki:
      for proc in processes:
         proc.terminate()
