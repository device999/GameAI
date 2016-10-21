__author__ = 'Marina'
import numpy as np

class TreeNode():

    def __init__(self, nodeId, utility):

        self.nodeId = nodeId
        self.parent = None
        self.successors = None
        self.utility = utility
        self.mmv = None
        self.maxutil = None

    def getNodeId(self):
        return self.nodeId

    def getParent(self):
        return self.parent

    def getSuccessors(self):
        return self.successors

    def getUtility(self):
        return self.utility

    def getMmv(self):
        return self.mmv

    def getMaxutil(self):
        return self.maxutil

    def insertChildren(self, node, successors):
        self.successors = successors
        for n in successors:
            n.parent = node

    def maxStep(self, node):
        node.mmv = -np.inf
        node.maxutil = -np.inf
        if node.getUtility() != None:
            node.mmv = node.getUtility()
        else:
            for n in node.getSuccessors():
                node.mmv = max(node.mmv, n.minStep(n))
                if n.getUtility()!= None:
                    node.maxutil = max(node.maxutil, n.getUtility())
                    print("#### ", node.maxutil)
                else:
                    node.maxutil = max(node.maxutil, n.maxutil)
        return node.mmv

    def minStep(self, node):
        node.mmv = np.inf
        node.maxutil = -np.inf
        if node.getUtility() != None:
            node.mmv = node.getUtility()
        else:
            for n in node.getSuccessors():
                node.mmv = min(node.mmv, n.maxStep(n))
                if n.getUtility()!= None:
                    node.maxutil = max(node.maxutil, n.getUtility())
                else:
                    node.maxutil = max(node.maxutil, n.maxutil)
        return node.mmv

    def printTree(self, node):

        print("current node ", node.getNodeId())

        if node.getSuccessors() != None:
            print("node has children, exploring children...")
            for child in node.getSuccessors():
                print("|nodeId: ", child.getNodeId(), " |parent: ", child.getParent().getNodeId(), " |utility: ", child.getUtility(), " |mmv: ", child.getMmv(), " |maxutil: ", child.getMaxutil())

                node.printTree(child)
        else:
            print("node is a leaf")

    def bestMaxStrategy(self, node):
        print("PATH ", node.getNodeId())

        localmaxutil = -np.inf
        bestchild = None

        if node.getSuccessors() != None:
            for child in node.getSuccessors():
                if node.getMmv() == child.getMmv() and child.getMaxutil() > localmaxutil:
                    localmaxutil = child.getMaxutil()
                    bestchild = child
            bestchild.bestMaxStrategy(bestchild)