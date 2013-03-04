env.user = ''
env.password = ''

def _nodes(filename='nodes.txt'):
   nodes = []
   for line in open(filename):
      nodes.append(line.strip())
   return nodes[0]

def prepare_solr():
   '''
   First copy data to be indexed to a node
   Add schema
   Call index script with correct parameters
   '''
   put('/tmp/*.bz', '/tmp/')
   with cd('/usr/share/dse-demos/wikipedia'):
      run('./1-add-schema.sh')
      run('./2-index.sh --wikifile `ls /tmp/*.bz2`')

