from fabric.api import *
import commands

env.user = 'ubuntu'

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
   bzfile = commands.getoutput('ls /tmp/*.bz2')
   put(bzfile, '/tmp/')
   with cd('/usr/share/dse-demos/wikipedia'):
      run('./1-add-schema.sh')
      run('./2-index.sh --wikifile /tmp/%s'%bzfile)

