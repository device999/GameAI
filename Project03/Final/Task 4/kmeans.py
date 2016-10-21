
import numpy as np
import logging


def calcD (centers, data):
    distsqrd = (centers[: , np.newaxis,:]- data)**2
    return np.sum(np.min (np.sum(distsqrd,axis =2), axis =0))

def getClosest(centers, data):
    distances = np.sqrt(np.sum((centers[:, np.newaxis, :] - data) ** 2, axis=2))
    closest = np.argmin(distances, axis=0)
    return closest

def kmeans(data,k=3,n=5,t=0.0001):
    #InitializecentersandlistJtotrackperformancemetric
    centers = np.array(data[np.random.choice(range(data.shape[0]), k, replace=False),:],dtype=float)
    D=[]
    _iter = 0
    #Repeat n times
    #for iter in range(n):
    # or another option to calc convergence, uncomment/comment the line above
    while (len(D) < 3) or (D[-1] - D[-2]) > t:
        _iter+=1
    #calculating closest distances

        closest = getClosest(centers, data)
    #Calculate overall sum of dist
        D.append(calcD(data,centers))
    #Update cluster centers
        for i in range(k):
            centers[i,:]=data[closest==i,:].mean(axis=0, dtype = float)
    return centers, closest


