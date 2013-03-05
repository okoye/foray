====
What
====

Purpose of this is to determine at what point DSE (cassandra <=> solr) starts
experiencing performance degradation as the number of nodes in the cluster
increases. 

===
Why
===
As search volume increases and the number of nodes in the cassandra cluster
grows, the number of nodes solr must contact to fully answer a query increases
to:
                     ceiling(n/r) 
where n is the number of nodes in the cluster and r is the number of replicas.
So, this experiment aims to provide some concrete numbers regarding the
performance of solr as cluster size increases.

===
How
===
Assuming query volume is constant (X reqs/sec) is sent to a varying cluster of
cassandra nodes. The standard deviation of the time taken for a response is
computed for each of the requests and all requests times the fall within 2 sds
is considered valid while the rest are discarded. The mean of the valid timings
is regarded as the roundtrip processing time for solr.

=======================
Description of scripts:
=======================
benchmark.py : runs actual benchmarking process. call with -h for more info
fabfile.py : setups and configures cassandra in the cluster

======
Notes:
======
You might need to install to libevent on your platform to run this script
Also, the script requires a file called nodes.txt that contains a list of nodes
to operate on and expects a bz2 file in /tmp containing wikipedia dataset

==========
Statistics Notes:
==========
The statistics module computes the important values of a particular run
including the 
- mean
- std
- 90th percentile value
- skew

Eventually, it emits a regression model describing performance of a fixed
cluster as query volume increases and performance of a cluster as cluster size
increases
