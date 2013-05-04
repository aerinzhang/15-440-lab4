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

def pointsAroundCentroid(c, p):
	pointSet = set()
	((x, y), r) = c
	while (len(pointSet) < p):
		angle = random.random()*(2*math.pi)
		rad = random.random()*r
		newPoint = (x+rad*math.sin(angle), y+rad*math.cos(angle))
		pointSet.add(newPoint)
	return pointSet

def diffOfStrands(d1, d2):
	diff = 0
	for i in xrange(len(d1)):
		if (d1[i] != d2[i]):
			diff += 1
	return diff

def checkTwoStrands(d1, d2):
	(s1, r1) = d1
	(s2, r2) = d2
	return False if (diffOfStrands(s1, s2) <= (r1+r2)) else True

def createCentroids(k, l):
	cList = []
	diffRad = int(l/(k**(0.5)))
	while(len(cList) < k):
		newCentroid = (createStrand(l), random.randint(1, diffRad))
		if (checkCentroids(cList, newCentroid)):
			cList += [newCentroid]
	return cList

def checkCentroids(known, new):
	for each in known:
		if (checkTwoStrands(each, new)):
			return False
	return True

def createStrand(l):
	bases = ["A", "C", "G", "T"]
	seq = []
	for i in xrange(l):
		seq += [bases[random.randint(0, 3)]]
	return ''.join(seq)

	[bases[random.randint(0, 3)]]

def DNAGenerator(outfile, p, k):
	o = open(outfile, "w+")
	for i in xrange(p*k):
		o.write(''.join(seq)+'\n')
	o.close()
	return 42
DNAGenerator(opts.output, opts.pValue, opts.kValue)