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

def kMeans(k, e, i, o):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    f = open(i, "r")
    strands = []
    for line in f.readlines():
        strand = line.strip()
        strands.append(strand)
    f.close()
    chunkSize = len(strands)/size
    # if rank == 0 pick centroids and then broadcast
    # every other node gets the broadcasted list from ranko
    # each node then computes membership based on that centroids
    # based on newmembership calculate new centroids 
    if (rank == 0):
        newCen = DS.getInitialCentroids(strands, k)
    else:
        newCen = None
    newCen = comm.bcast(newCen, root=0)
    oldCen = [""]*k
    membership = [-1]*chunkSize
    allMembership = []
    while(DS.diffCentroids(oldCen, newCen) > e):
        oldCen = newCen[:]
        if (rank != size - 1):
            chunk = strands[rank*chunkSize:(rank+1)*chunkSize]
        else:
            chunk = strands[rank*chunkSize:]
        membership = assignMembership(chunk, newCen)
        allMembers = comm.gather(membership, root=0)
        #flatten the list of lists
        if (rank == 0):
            allMembership = []
            for member in allMembers:
                allMembership.extend(member)
            newCen = updateCentroids(allMembership, k)
        newCen = comm.bcast(newCen, root=0)

    # write output file
    if (rank == 0):
        fo = open(o, "w+")
        for c in newCen:
            fo.write(c)
        fo.close()

#kMeans(10, 0.0001, 'input.txt', 'output.txt')

if __name__ == "__main__":
	import cProfile
	cProfile.run("kMeans(opts.k, opts.e, opts.input, opts.output)")
