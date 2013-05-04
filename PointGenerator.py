#!/usr/bin/env python                                                                                                                     
import optparse
import sys
import random
import math

optparser = optparse.OptionParser()
optparser.add_option("-k", "--value-of-k", dest="kValue", type="int", help="number of clusters")
optparser.add_option("-p", "--value-of-p", dest="pValue", type="int", help="number of data in a cluster")
optparser.add_option("-o", "--output", dest="output", help="location of output file")
optparser.add_option("-r", "--range", dest="range", default=10000, type="int", help="range of coordinates")
(opts, _) = optparser.parse_args()


def createCentroids(k, r):
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



def PointGenerator(outfile, p, k, r):
	o = open(outfile, "w+")
	# generate centroids list
	cList = createCentroids(k, r)
	for i in xrange(k):
		#for each centroids, generate p data points
		c = cList[i]
		pSet = pointsAroundCentroid(c, p)
		while (len(pSet) != 0):
			(x, y) = pSet.pop()
			o.write("%f %f\n"%(x,y))
	o.close()
	return 42
PointGenerator(opts.output, opts.pValue, opts.kValue, opts.range)