#!/usr/bin/env python                                                                                                                     
import optparse
from mpi4py import MPI
import DNASequential as DS

optparser = optparse.OptionParser()
optparser.add_option("-k", "--k", dest="k", type="int", help="number of clusters")
optparser.add_option("-e", "--e", dest="e", type="float", help="threshold for convergence")
optparser.add_option("-i", "--input", dest="input", help="input file path")
optparser.add_option("-o", "--output", dest="output", help="output file path")
(opts, _) = optparser.parse_args()

# assigns each strand its cluster number
# returns a list of tuples like (clusterNum, strand)
def assignMembership(strands, centroids):
    k = len(centroids)
    membership = []
    for strand in strands:
        minDistance = float("inf")
        for c in xrange(k):
            d = DS.distance(strand, centroids[c])
            if (d < minDistance):
                minDistance = d
                minCluster = c
        membership.append((minCluster, strand))
    return membership

# given the new assignment of clusters, calculate the new centroids
def updateCentroids(membership, k):
    clusters = [[] for _ in xrange(k)]
    for pair in membership:
        clusters[pair[0]] += [pair[1]]
    newCen = []
    for cluster in clusters:
        centroid = ""
        if (len(cluster)  > 0):
            for i in xrange(len(cluster[0])):
                numA, numG, numC, numT = 0, 0, 0, 0
                for strand in cluster:
                    if strand[i] == "A": numA += 1
                    elif strand[i] == "G": numG += 1
                    elif strand[i] == "C": numC +=1
                    else: numT += 1
                if (max(numA, numG, numC, numT) == numA): centroid += "A"
                elif (max(numA, numG, numC, numT) == numG): centroid += "G"
                elif (max(numA, numG, numC, numT) == numC): centroid += "C"
                else: centroid += "T"
            newCen.append(centroid)
    return newCen

#parallel kmeans
def kMeans(k, e, i, o):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    #when rank = 0, divides the strands and scatters to each node
    if (rank == 0):
        f = open(i, "r")
        strands = []
        for line in f.readlines():
            strand = line.strip()
            strands.append(strand)
        f.close()
        chunkSize = len(strands)/size
        chunk = [strands[i*chunkSize: min((i+1)*chunkSize, len(points))] for i in range(size)]
        #pick centroids and then broadcast
        newCen = DS.getInitialCentroids(strands, k)
    else:
        newCen = None
        chunk = None

    # every other node gets the broadcasted newCen from root
    newCen = comm.bcast(newCen, root=0)
    # every node gets its chunk of data
    chunk = comm.scatter(chunk, root=0)
    oldCen = [""]*k
    membership = [-1]*len(chunk)
    allMembership = []
    # repeat until convergence
    while(DS.diffCentroids(oldCen, newCen) > e):
        oldCen = newCen[:]
        # each node then computes membership based on the current centroids
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
        #broadcast newCentroids to every node
        newCen = comm.bcast(newCen, root=0)

    # write output file
    if (rank == 0):
        fo = open(o, "w+")
        for c in newCen:
            fo.write(c)
        fo.close()

if __name__ == "__main__":
	import cProfile
	cProfile.run("kMeans(opts.k, opts.e, opts.input, opts.output)")
