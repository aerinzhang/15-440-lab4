#!/usr/bin/env python                                                                                                                     
import optparse
import random
from mpi4py import MPI
import PointSequential as PS

optparser = optparse.OptionParser()
optparser.add_option("-k", "--k", dest="k", type="int", help="number of clusters")
optparser.add_option("-e", "--e", dest="e", type="float", help="threshold for convergence")
optparser.add_option("-i", "--input", dest="input", help="input file path")
optparser.add_option("-o", "--output", dest="output", help="output file path")
(opts, _) = optparser.parse_args()

# assign each point its cluster number
# returns a list of tuples like (clusterNum, (x,y))
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
	return membership

# given the new assignment of clusters, calculate the new centroids
def updateCentroids(membership, k):
	clusters = [[] for _ in xrange(k)]
	for pair in membership:
		clusters[pair[0]] += [pair[1]]
	newCen = []
	for cluster in clusters:
		sizeOfC = len(cluster)
		if (sizeOfC > 0):
			x = (sum([point[0] for point in cluster])) / sizeOfC
			y = (sum([point[1] for point in cluster])) / sizeOfC
			newCen += [(x, y)]
	return newCen

#randomly selects initial centroids
def getInitialCentroids(points, k):
	cen = []
	while (k != 0):
		index = random.randint(0, len(points)-1)
		c = points[index]
		cen += [c]
		k -= 1
		points.remove(c)
	print cen
	return cen

def kMeans(k, e, i, o):
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()

	#rank = 0 divides the points and scatters to each data
	if rank == 0:
		f = open(i, "r")
		points = []
		for line in f.readlines():
			pointStr = line.strip().split(' ')
			point = (float(pointStr[0]), float(pointStr[1]))
			points.append(point)
		f.close()
		chunkSize = len(points)/size
		chunk = [points[i*chunkSize: min((i+1)*chunkSize, len(points))] for i in range(size)]
		#pick centroids and then broadcast
		newCen = getInitialCentroids(points, k)
	else:
		newCen = None
		chunk = None
	newCen = comm.bcast(newCen, root=0)
	chunk = comm.scatter(chunk, root=0)
	# every other node gets the broadcasted list from ranko
	# each node then computes membership based on that centroids
	oldCen = [(0,0)]*k
	membership = [-1]*len(chunk)
	allMembership = []
	while(PS.diffCentroids(oldCen, newCen) > e):
		oldCen = newCen[:]
		membership = assignMembership(chunk, newCen)
		allMembers = comm.gather(membership, root=0)
		#flatten the list of lists
		if (rank == 0):
			allMembership = []
			#flatten the list of lists
			for member in allMembers:
				# based on newmembership calculate new centroids 
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
	import cProfile
	#cProfile.run("kMeans(3, 0.0001, 'Pointk3p100000.txt', 'tst.txt')")
	cProfile.run("kMeans(opts.k, opts.e, opts.input, opts.output)")
