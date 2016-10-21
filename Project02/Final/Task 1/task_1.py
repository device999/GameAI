import numpy as np
import copy as objCopy
import sys
from treenode import TreeNode
#globals
totalNodeCnt = 0
winByXCnt = 0
totalGameDrawCnt = 0
totalParentNodesCnt = 0
totalChildCnt = 0

def move_still_possible(S):
    return not (S[S==0].size == 0)


def winning_move_cnt(S, p):
    cnt= np.sum(np.sum(S, axis=0) * p == 3) + \
         np.sum(np.sum(S, axis=1) * p == 3) + \
         int((np.sum(np.diag(S)) * p) == 3) +\
         int((np.sum(np.diag(np.rot90(S))) * p) == 3)
    return cnt > 0

##recursive parent node calculation

def calc_parent_nodes(node):
    if node.hasChild():
        global totalParentNodesCnt
        totalParentNodesCnt += 1
        children = node.getChild()
        global totalChildCnt 
        totalChildCnt +=len(children)
        for child in children:
            calc_parent_nodes(child)


def create_new_node(parent, saved_state):
    newNode = TreeNode(saved_state)
    newNode.setParent(parent)
    parent.addChild(newNode)
    parent.setState(saved_state)
    return newNode


def generate_game_tree(gameTreeNode, player):
    # initialize win flag
    noWinnerYet = True

    S = gameTreeNode.getState()
    xs, ys = np.where(S == 0)

    for i in range(xs.size):
        savedS = objCopy.copy(S)
        if noWinnerYet:
            savedS[xs[i]][ys[i]] = player
            newGameNode = create_new_node(gameTreeNode, savedS)

            global totalNodeCnt
            totalNodeCnt += 1

            if winning_move_cnt(savedS, player):
                if player == 1:
                    global winByXCnt
                    winByXCnt += 1
                    noWinnerYet = False
                return
            else:
                generate_game_tree(newGameNode, player*-1)

    if noWinnerYet:
        global totalGameDrawCnt
        totalGameDrawCnt +=1

if __name__ == '__main__':

    # initialize 3x3 tic tac toe board
    S = np.zeros((3,3), dtype=int)

    # initialize player number, move counter
    player = 1

    #initialize the game tree
    gameTree = TreeNode(S)

    #generate game tree
    generate_game_tree(gameTree,player)

    print ('Total node count :%d' % totalNodeCnt)
    print ('Total win X player win count :%d' % winByXCnt)
    print ('Total draw count :%d' % totalGameDrawCnt)

    calc_parent_nodes(gameTree)
    print ('Total parent node count :%d'% totalParentNodesCnt)
    print ('Average branching factor: %f' %  (float(totalChildCnt)/totalParentNodesCnt))