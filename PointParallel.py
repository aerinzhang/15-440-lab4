#!/usr/bin/env python                                                                                                                     
import optparse
<<<<<<< HEAD
import math
import random
from mpi4py import MPI
=======
from mpi4py import MPI
import PointSequential as PS
>>>>>>> 78db129c0356b85ec3068b19d765002473afd7c6

optparser = optparse.OptionParser()
optparser.add_option("-k", "--k", dest="k", type="int", help="number of clusters")
optparser.add_option("-e", "--e", dest="e", type="int", help="threshold for convergence")
optparser.add_option("-i", "--input", dest="input", help="input file path")
optparser.add_option("-o", "--output", dest="output", help="output file path")
(opts, _) = optparser.parse_args()

<<<<<<< HEAD
def distance(p1, p2):
    return (((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)) ** 0.5

def getInitialCentroids(points, k):
    ntries = int (2 + math.log(k))
    n = len(points)
    centroids = [points[random.randint(0, n-1)]]  
    D       = [distance(point, centers[0])**2 for point in points] 
    Dsum    = reduce (lambda x, y : x + y, D)  
    for _ in xrange(k - 1):  
        bestDsum = bestIdx = -1  
        for _ in range(ntries):  
            randVal = random.random() * Dsum  
            for i in range(n):  
                if randVal <= D[i]:  
                    break  
                else:  
                    randVal -= D[i]    
            tmpDsum = reduce(lambda x, y : x + y,  
                             (min(D[j], distance(points[j], points[i]) ** 2) for j in xrange(n)))  
            if bestDsum < 0 or tmpDsum < bestDsum:  
                bestDsum, bestIdx  = tmpDsum, i  
        Dsum = bestDsum  
        centroids.append (points[bestIdx])  
    return centroids

# compute average centroid from points in a cluster
def getNewCentroids(clusters):
    centroids = []
    for points in clusters:
        p = len(points)
        if (p > 0):
            x = (sum([point[0] for point in points])) / p
            y = (sum([point[1] for point in points])) / p
            centroids.append((x, y))
    return centroids

# compute point clusters
def getClusters(points, centroids):
    k = len(centroids)
    clusters = [[] for _ in xrange(k)]
    for point in points:
        minDistance = float("inf")
        for c in xrange(k):
            d = distance(point, centroids[c])
            if (d < minDistance):
                minDistance = d
                minCluster = c
        clusters[minCluster].append(point)
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
    comm = MPI.COMM_WORLD

    myrank = comm.Get_rank()
    numProcs = comm.Get_size()
    # read data points into list of tuples (x, y)
    f = open(i, "r")
    points = []
    for line in f.readlines():
        pointStr = line.strip().split(' ')
        point = (float(pointStr[0]), float(pointStr[1]))
        points.append(point)
    f.close()
    # run kMeans
    initialCentroids = getInitialCentroids(points, k)
    oldCentroids = initialCentroids
    clusters = getClusters(points, initialCentroids)
    newCentroids = getNewCentroids(clusters)
    while (diffCentroids(oldCentroids, newCentroids) > e):
        oldCentroids = copyOf(newCentroids)
        clusters = getClusters(points, newCentroids)
        newCentroids = getNewCentroids(clusters)
    fo = open(o, "w+") 
    for c in newCentroids:
        fo.write("%f %f\n" % (c[0], c[1]))
    fo.close()
    
#kMeans(3, 0.0001, "input.txt", "output.txt")
kMeans(opts.k, opts.e, opts.input, opts.output)
=======
def assignMembership(points, centroids):
	k = len(centroids)
	membership = []
	for point in points:
		minDistance = float("inf")
		for c in xrange(k):
			d = PS.distance(point, centroids[c])
			if (d < minDistance):
				minDistance = d
				minCluster = c
		#format (clusterNum, (x,y))
		membership.append((minCluster, point))
		#print membership
	return membership

def updateCentroids(membership, k):
	clusters = [[] for _ in xrange(k)]
	#print membership
	for pair in membership:
		#print pair
		clusters[pair[0]] += [pair[1]]
	newCen = []
	for cluster in clusters:
		sizeOfC = len(cluster)
		if (sizeOfC > 0):
			x = (sum([point[0] for point in cluster])) / sizeOfC
			y = (sum([point[1] for point in cluster])) / sizeOfC
			newCen += [(x, y)]
	return newCen

def run(k, e, i, o):
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()
	f = open(i, "r")
	points = []
	for line in f.readlines():
		pointStr = line.strip().split(' ')
		point = (float(pointStr[0]), float(pointStr[1]))
		points.append(point)
	f.close()
	chunkSize = len(points)/size
	# if rank == 0 pick centroids and then broadcast
	# every other node gets the broadcasted list from ranko
	# each node then computes membership based on that centroids
	# based on newmembership calculate new centroids 
	if (rank == 0):
		newCen = PS.getInitialCentroids(points[0:chunkSize], k)
	else:
		newCen = None
	newCen = comm.bcast(newCen, root=0)
	oldCen = [(0,0)]*k
	membership = [-1]*chunkSize
	allMembership = []
	while(PS.diffCentroids(oldCen, newCen) > e):
		oldCen = newCen[:]
		if (rank == size - 1):
			chunk = points[rank*chunkSize:(rank+1)*chunkSize]
		else:
			chunk = points[rank*chunkSize:]
		membership = assignMembership(chunk, newCen)
		#if (rank == 0):
		allMembers = comm.gather(membership, root=0)
		#flatten the list of lists
		if (rank == 0):
		#allMembers = comm.scatter(allMembers, root=0)
			allMembership = []
			for member in allMembers:
				allMembership.extend(member)
			newCen = updateCentroids(allMembership, k)
		newCen = comm.bcast(newCen, root=0)

	#write output file
	if (rank == 0):
		fo = open(o, "w+")
		for c in newCen:
			fo.write("%f %f\n" % (c[0], c[1]))
		fo.close()
	return 42
if __name__ == "__main__":
	run(3, 0.0001, 'Pointk3p100000.txt', 'tst.txt')
	#run(opts.k, opts.e, opts.input, opts.output)
>>>>>>> 78db129c0356b85ec3068b19d765002473afd7c6
