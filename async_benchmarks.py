import gevent

def benchmark():
   print 'benchmark is running!'

g1 = gevent.spawn(benchmark)
g2 = gevent.spawn(benchmark)
greenlets = []
for i in xrange(1000):
   greenlets.append(gevent.spawn(benchmark))

print 'finished spawning greenlets'

gevent.joinall(greenlets)
print 'program ended'
