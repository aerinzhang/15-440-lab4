#!/usr/bin/env python                                                                                                                     
import optparse
import sys
import random

optparser = optparse.OptionParser()
optparser.add_option("-k", "--value-of-k", dest="kValue", type="int", help="number of clusters")
optparser.add_option("-p", "--value-of-p", dest="pValue", type="int", help="number of data in a cluster")
optparser.add_option("-o", "--output", dest="output", help="location of output file")
optparser.add_option("-r", "--range", dest="range", default=10000, type="int", help="range of coordinates")
(opts, _) = optparser.parse_args()

def PointGenerator(outfile, p, k, r):
	o = open(outfile, "w+")
	for i in xrange(p*k):
		(x,y) = (random.randint(0, r), random.randint(0, r))
		o.write("%d %d\n"%(x,y))

PointGenerator(opts.output, opts.pValue, opts.kValue, opts.range)