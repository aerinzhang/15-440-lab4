#!/usr/bin/env python                                                                                                                     
import optparse
import sys
import random

optparser = optparse.OptionParser()
optparser.add_option("-k", "--value-of-k", dest="kValue", type="int", help="number of clusters")
optparser.add_option("-p", "--value-of-p", dest="pValue", type="int", help="number of data in a cluster")
optparser.add_option("-o", "--output", dest="output", default="data/output.txt", help="location of output file")
optparser.add_option("-l", "--length-of-DNA", dest="dLength", default=20, type="int", help="length of DNA strand")
(opts, _) = optparser.parse_args()

def DNAgenerator(outfile, p, k):
	o = open(outfile, "w+")
	bases = ["A", "C", "G", "T"]
	for i in xrange(p*k):
		seq = []
		for j in xrange(20):
			seq += [bases[random.randint(0, 3)]]
		o.write(''.join(seq)+'\n')

DNAgenerator(opts.output, opts.pValue, opts.kValue)