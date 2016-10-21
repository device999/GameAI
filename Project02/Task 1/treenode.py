# treenode class with default getters and setters
class TreeNode(object):
    def __init__(self, S):
        self.S = S
        self.child = []
        self.parent = None

    def setParent(self,parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def setState(self,S):
        self.S = S

    def getState(self):
        return self.S

    def addChild(self, obj):
        self.child.append(obj)

    def getChild(self):
        return self.child

    def getChildCnt(self):
        return len(self.child)

    def hasChild(self):
        return bool(len(self.child) != 0)
