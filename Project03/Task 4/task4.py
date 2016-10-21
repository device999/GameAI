from kmeans import *
from optparse import OptionParser
from somNewTer import *
import random
from math import sqrt

parser = OptionParser()

#TODO add comments

def getActions(path):
    return np.array([path[i+1] - path[i] for i in range(len(path)-1)])

def getJointProb(somClust, actClust, nsom, nact ):
    probMatrix = np.zeros((nsom, nact))
    for i in range(len(actClust)):
        probMatrix[somClust[i], actClust[i]] +=1
    return probMatrix / np.sum(probMatrix)

def getPath(probMtrx, somCenters, actionCenters, pathClust, niter):
    state = random.sample(list(pathClust), 1)[0]
    path = []
    pos = np.copy(somCenters[state])
    for i in range(niter):
        path.append(pos)
        pos = np.copy(pos + actionCenters[np.argmax(probMtrx[state])])
        state = np.argmin([dist(pos, k) for k in somCenters])
    return np.array(path)

def plotit(points, data):
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc_data = ax.scatter(data[:, 0], data[:, 1], data[:, 2], zorder=1, c='r', alpha=1)
    ax.plot(points[:, 0], points[:, 1], points[:, 2], c='b')
    #sc_centers = ax.scatter(center[:, 0], center[:, 1], center[:, 2], zorder=4, s=100, marker='o', c='b', alpha=1)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.pause(5)
    plt.show()

if __name__ == '__main__':
    parser.add_option("-a", "--actionclusters",
                      dest="actionclusters", default=False, #action="store_false",
                      help="input value for actions clusters amount")

    parser.add_option("-n", "--somneurons",
                      dest="somneurons", default=False,  # action="store_false",
                      help="input value for actions clusters amount")
    parser.add_option("-i", "--nitersom",
                      dest="nitersom", default=False,  # action="store_false",
                      help="input number of iterations for SOM learning")

    parser.add_option("-D", "--datapath",
                      dest="datapath", default=False,  # action="store_false",
                      help="enter input data for SOM")

    parser.add_option("-p", "--pathiter",
                      dest="pathiter", default=False,  # action="store_false",
                      help="enter number of iterations for optimal path")

    (options, args) = parser.parse_args()

    somCenters = main('api', int(options.nitersom), int(options.somneurons), options.datapath)
    path = np.loadtxt(options.datapath, dtype=float,comments='#',delimiter=",")
    actions = getActions(path)
    actionCenters, actionClust = kmeans(actions, int(options.actionclusters))
    pathClust = getClosest(somCenters,path)
    probMtrx = getJointProb(pathClust, actionClust, len(somCenters), int(options.actionclusters))
    optPath = getPath(probMtrx,somCenters, actionCenters, pathClust, int(options.pathiter))
    #plotit(somCenters, path)
    plotit(np.array(optPath), path)
