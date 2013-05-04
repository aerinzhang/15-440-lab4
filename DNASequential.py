#!/usr/bin/env python                                                                                                                     
import optparse
import math
import random

optparser = optparse.OptionParser()
optparser.add_option("-k", "--k", dest="k", type="int", help="number of clusters")
optparser.add_option("-e", "--e", dest="e", type="int", help="threshold for convergence")
optparser.add_option("-i", "--input", dest="input", help="input file path")
optparser.add_option("-o", "--output", dest="output", help="output file path")
(opts, _) = optparser.parse_args()

def distance(s1, s2):
    numDiff = 0
    l = len(s1)
    for i in xrange(l):
        if s1[i] != s2[i]:
            numDiff += 1
    return numDiff

def notExisting(centroids, centroid):
    for c in centroids:
        if c == centroid:
            return False
    return True

# generate random centroids
def getInitialCentroids(strands, k):
    centroids = []
    numCentroids = 0
    while (numCentroids < k):
        centroid = random.choice(strands)
        if (notExisting(centroids, centroid)):
            centroids.append(centroid)
            numCentroids += 1
    return centroids

# compute average centroid from most commonly used bases
def getNewCentroids(clusters):
    centroids = []
    for strands in clusters:
        centroid = ""
        for i in xrange(len(strands[0])):
            numA, numG, numC, numT = 0, 0, 0, 0
            for strand in strands:
                if strand[i] == "A": numA += 1
                elif strand[i] == "G": numG += 1
                elif strand[i] == "C": numC +=1
                else: numT += 1
            if (max(numA, numG, numC, numT) == numA): centroid += "A"
            elif (max(numA, numG, numC, numT) == numG): centroid += "G"
            elif (max(numA, numG, numC, numT) == numC): centroid += "C"
            else: centroid += "T"
        centroids.append(centroid)
    return centroids

# compute dna clusters
def getClusters(strands, centroids):
    k = len(centroids)
    clusters = [[] for _ in xrange(k)]
    for strand in strands:
        minDistance = float("inf")
        for c in xrange(k):
            d = distance(strand, centroids[c])
            if (d < minDistance):
                minDistance = d
                minCluster = c
        clusters[minCluster].append(strand)
    return clusters

# compute maximum change in centroids
def diffCentroids(oldCentroids, newCentroids):
    k = len(oldCentroids)
    return max([distance(oldCentroids[c], newCentroids[c]) for c in xrange(k)])

# make deep copy of centroids list
def copyOf(centroids):
    k = len(centroids)
    return [centroids[c] for c in xrange(k)]

def kMeans(k, e, i, o):
    # read data points into list DNA strings
    f = open(i, "r")
    strands = []
    for line in f.readlines():
        strand = line.strip()
        strands.append(strand)
    f.close()
    # run kMeans
    initialCentroids = getInitialCentroids(strands, k)
    oldCentroids = initialCentroids
    clusters = getClusters(strands, initialCentroids)
    newCentroids = getNewCentroids(clusters)
    #print newCentroids
    while (diffCentroids(oldCentroids, newCentroids) > e):
        oldCentroids = copyOf(newCentroids)
        clusters = getClusters(strands, newCentroids)
        newCentroids = getNewCentroids(clusters)
        fo = open(o, "w+") 
    for c in newCentroids:
        fo.write(c + "\n")
    fo.close()
     
#kMeans(10, 0.0001, "dna.txt", "output.txt")
if __name__ == "__main__":
    kMeans(opts.k, opts.e, opts.input, opts.output)
