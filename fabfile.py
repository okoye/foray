from fabric.api import *

#environment global information
env.user = ''
env.password = ''

def _fetch_node_list(file_name='nodes.txt'):
   nodes = []
   for line in open(filename):
      nodes.append(line.strip())

   return nodes

def _add_schema(node):
   with cd("/usr/share/dse-demos/wikipedia"):
      run("1-add-schema.sh")

def _index_articles():
   with cd("/usr/share/dse-demos/wikipedia"):
      run("2-index.sh --wikifile \
      enwiki-20111007-pages-articles25.xml-p023725001p026625000.bz2 \
      --limit 10000")

def _validate_solr():
   pass

def setup_solr():
   '''
   the setup process is as follows:
      add necesary schema to solr nodes by executing command
      index the articles with command
      test to make sure everything went well
   '''
   for node in _fetch_node_list():
      _add_schema(node)
      _index_articles(node)
      _validate_solr(node)
