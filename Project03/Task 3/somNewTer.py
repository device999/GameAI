import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import random
import math
import sys
import csv
import time

def updateSOMNeighborLine(learningRate,sigma,i,winnerIndice, pattern, neighborValue, gl, MAXDIST):
    graph_dist = lambda gl, i1, i2: min(int(gl- max(i1, i2) + min(i1, i2)), abs(i1 - i2))
    result = learningRate*math.exp(-np.abs(graph_dist(gl, i, winnerIndice)*(dist(pattern,neighborValue)/MAXDIST))/(2*sigma))*(neighborValue - pattern)

    return pattern + result


def dist(x,y):
    return np.sqrt(np.sum(pow(x-y, 2)))


def main(method, niter = 1000, amountCl = 50, datapath = 'C:/q3dm1-path1.csv'):
    path = np.loadtxt(datapath,dtype=np.float,comments='#',delimiter=",")
    secondPath = path[:,0:3].astype(np.float)

    mxDot = np.array([float(max(path[:,i])) for i in range(path.shape[1])])
    mnDot = np.array([float(min(path[:,i])) for i in range(path.shape[1])])
    MAXDIST = dist(mnDot, mxDot)

    center = np.array([[random.uniform(mnDot[i], mxDot[i]) for i in range(path.shape[1])] for n in range(amountCl)])

    distance = np.zeros(amountCl)
    if method =='viz':
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        sc_data = ax.scatter(secondPath[:,0], secondPath[:,1], secondPath[:,2], zorder=1, c='r', alpha=1)
        ax.plot(center[:,0], center[:,1], center[:,2], c='b')
        sc_centers = ax.scatter(center[:,0], center[:,1], center[:,2], zorder=4, s=100, marker='o',c='b', alpha=1)
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        fig.show()

    for k in range(niter):
        learningRate = (1-float(k)/float(niter))**3
        sigma = math.exp(-float(k)/float(niter))
        randomPoint = secondPath[np.random.randint(0, np.shape(secondPath)[0]),:]

        for x in range(len(distance)):
            distance[x] = dist(randomPoint,center[x])

        winnerIndice = np.argmin(distance)

        for i in range(len(center)):
            center[i] = updateSOMNeighborLine(learningRate,sigma,i,winnerIndice,center[i],randomPoint, len(path),MAXDIST)

        if method=='viz' and divmod(k, 100)[1]==0:
            plt.pause(0.0001)
            sc_centers._offsets3d = (center[:, 0], center[:, 1], center[:, 2])
            plt.draw()
            plt.show()

    if method=='api':
        return center
    elif method =='dataexport':
        import os
        with open(os.path[0]+'/out.csv', 'w') as fl:
            np.savetxt(fl, center, delimiter=';')

if __name__ == "__main__":
    main('viz')
