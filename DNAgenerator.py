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

def createCentroids(k, l):
	cList = []
	radius = int(r/(k**(0.5)))
	while (len(cList) < k):
		newCentroid = ((random.random()*r, random.random()*r),
					int(random.random()*radius))
		if (checkCentroids(cList, newCentroid)):
			cList += [newCentroid]
	return cList

def checkTwoCentroids(c1, c2):
	((x1, y1), r1) = c1
	((x2, y2), r2) = c2
	if (((x1-x2)**2 + (y1-y2)**2))**(0.5) <= r1+r2:
		return False
	else:
		return True

def checkCentroids(known, new):
	for each in known:
		#if two centroids are too close
		if checkTwoCentroids(each, new):
			return False
	return True

def pointsAroundCentroid(c, p):
	pointSet = set()
	((x, y), r) = c
	while (len(pointSet) < p):
		angle = random.random()*(2*math.pi)
		rad = random.random()*r
		newPoint = (x+rad*math.sin(angle), y+rad*math.cos(angle))
		pointSet.add(newPoint)
	return pointSet

def similarityOfStrands(d1, d2):
	sim = 0
	for i in xrange(len(d1)):
		if (d1[i] == d2[i]):
			sim += 1
	return sim

def createCentroids(k, l):
	cList = []
	diffRad = random.randint(1, l)
	while(len(cList) < k):
		newCentroid = (createStrand(l), diffRad)
		if ():
			cList += [newCentroid]
	return cList

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