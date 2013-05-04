#!/usr/bin/env python                                                                                                                     
import optparse
from mpi4py import MPI
import PointSequential as PS

##optparser = optparse.OptionParser()
##optparser.add_option("-k", "--k", dest="k", type="int", help="number of clusters")
##optparser.add_option("-e", "--e", dest="e", type="float", help="threshold for convergence")
##optparser.add_option("-i", "--input", dest="input", help="input file path")
##optparser.add_option("-o", "--output", dest="output", help="output file path")
##(opts, _) = optparser.parse_args()

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
		newCen = PS.getInitialCentroids(points, k)#[0:chunkSize], k)
	else:
		newCen = None
	newCen = comm.bcast(newCen, root=0)
	oldCen = [(0,0)]*k
	membership = [-1]*chunkSize
	allMembership = []
	while(PS.diffCentroids(oldCen, newCen) > e):
		oldCen = newCen[:]
		if (rank != size - 1):
			chunk = points[rank*chunkSize:(rank+1)*chunkSize]
		else:
			chunk = points[rank*chunkSize:]
		membership = assignMembership(chunk, newCen)
		allMembers = comm.gather(membership, root=0)
		#flatten the list of lists
		if (rank == 0):
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


run(3, 0.0001, 'inputPoints.txt', 'output.txt')

#run(3, 0.0001, 'Pointk3p100000.txt', 'tst.txt')

##if __name__ == "__main__":
##	import cProfile
##	cProfile.run("run(opts.k, opts.e, opts.input, opts.output)")
