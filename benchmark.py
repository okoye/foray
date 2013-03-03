'''
Goal of this module is to connect and run several concurrent requests to a
solr REST interface to determine and store the timings of the request.

author: Chuka <okoye9@gmail.com>
'''
import optparse
import signal
import pysolr
import gevent
import random
from datetime import datetime
from gevent import monkey; monkey.patch_socket()

###############Benchmark Proper#################
class Benchmark(object):
   
   def __init__(self, i, num_req=1000, nodes='nodes.txt'):
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
      #for i in xrange(self.requests):
      #   greenlets.append(gevent.spawn(self._request))
      #   print 'spawning greenlet %i'%i
      g1 = gevent.spawn(self._request)
      g2 = gevent.spawn(self._request)

      print 'now waiting for greenlet completion...'
      #gevent.joinall(greenlets)
      gevent.joinall([g1, g2])

   def _request(self):
      '''
      each of this is run in a greenlet thread.
      actual request maker. records start time, end time and appends
      '''
      pass
      #random.sample(self.solr_urls, 1)[0]
      #for i in xrange(2):
      #   print 'pinging solr %d'%i

###############Process Management################
if __name__ == '__main__':
   parser = optparse.OptionParser()
   parser.add_option('-r', '--requests', help='no of concurrent requests',
                     dest='requests', default=1000)
   parser.add_option('-p', '--processes', help='no of processes',
                     dest='processes', default=1)
   parser.add_option('-n', '--nodes', help='nodes list file', 
                     dest='nodes', default='nodes.txt')
   (opts, args) = parser.parse_args()

   benchmark = Benchmark(num_req=opts.requests, nodes=opts.nodes)
   benchmark.start()

   #add process management stuff again
