#!/usr/bin/env python                                                                                                                     
import optparse
import sys
import random
import math

optparser = optparse.OptionParser()
optparser.add_option("-k", "--value-of-k", dest="kValue", type="int", help="number of clusters")
optparser.add_option("-p", "--value-of-p", dest="pValue", type="int", help="number of data in a cluster")
optparser.add_option("-o", "--output", dest="output", default="output.txt", help="location of output file")
optparser.add_option("-l", "--length-of-DNA", dest="dLength", default=50, type="int", help="length of DNA strand")
(opts, _) = optparser.parse_args()

def pointsAroundCentroid(c, p, l):
	pointSet = set()
	(s, r) = c
	while (len(pointSet) < p-1):
		diff = random.randint(1, r)
		newPoint = modifyCentroid(s, diff)
		pointSet.add(newPoint)
	return pointSet

def modifyCentroid(s, n):
	news = list(s)
	s = list(s)
	#modify i positions
	bases = ["A", "C", "G", "T"]
	while (diffOfStrands(news,s))!= n:
		i = random.randint(0, len(s)-1)
		gene = bases[(bases.index(s[i]) + random.randint(1,3))%4]
		news[i] = gene
	return ''.join(news)


def diffOfStrands(d1, d2):
	diff = 0
	for i in xrange(len(d1)):
		if (d1[i] != d2[i]):
			diff += 1
	return diff

def checkTwoStrandsOverlap(d1, d2):
	(s1, r1) = d1
	(s2, r2) = d2
	return True if (diffOfStrands(s1, s2) <= (r1+r2)) else False

def createCentroids(k, l, p):
	cList = []
	diffRad = round(l*1.0/k)
	while(len(cList) < k):
		minR = max(math.ceil(math.log(p, l)), 1)
		newCentroid = (createStrand(l), random.randint(minR, diffRad))
		if (checkCentroids(cList, newCentroid)):
			cList += [newCentroid]
	return cList

def checkCentroids(known, new):
	for each in known:
		if (checkTwoStrandsOverlap(each, new)):
			return False
	return True

def createStrand(l):
	bases = ["A", "C", "G", "T"]
	seq = []
	for i in xrange(l):
		seq += [bases[random.randint(0, 3)]]
	return ''.join(seq)

def DNAGenerator(outfile, p, k, l):
	o = open(outfile, "w+")
	stem = outfile.split(".")[0]
	oSolution = open(stem+"Sol.txt", "w+")
	#create a list a centroids
	cList = createCentroids(k, l, p)
	#for each center, generates a set of points
	for i in xrange(k):
		strandsSet = pointsAroundCentroid(cList[i], p, l)
		o.write(cList[i][0]+'\n')
		oSolution.write(cList[i][0]+'\n')
		for strand in strandsSet:
			o.write(strand+'\n')
	o.close()
	oSolution.close()
	return 42
if __name__ == "__main__":
	DNAGenerator(opts.output, opts.pValue, opts.kValue, opts.dLength)