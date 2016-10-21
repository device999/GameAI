# task 2.1 
# tic tac teo game tree states
# combinational agruments 

import numpy as np
import copy as objCopy
import sys

# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

#global variable to 
totalNodeOfGameTree = 0
totalGameWinByPlayer_X = 0
totalGameDrawCount = 0
totalNodesHavingChilds = 0

# two players of the game
PLAYER_X = 1
PLAYER_O =-1


def move_still_possible(S):
    return not (S[S==0].size == 0)


def move_was_winning_move(S, p):
    if np.max((np.sum(S, axis=0)) * p) == 3:
        return True

    if np.max((np.sum(S, axis=1)) * p) == 3:
        return True

    if (np.sum(np.diag(S)) * p) == 3:
        return True

    if (np.sum(np.diag(np.rot90(S))) * p) == 3:
        return True

    return False


# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B



# A simple game tree node. It hold all the possible state of the game

class Game(object):
    def __init__(self, gameState):
        self.gameState = gameState
        self.children = []
        self.parent = None

    def set_parent(self,parent):
        self.parent = parent
    
    def set_game_state(self,gameState):
        self.gameState = gameState
    
    def get_parent(self):
        return self.parent
                
    def add_children(self, obj):
        self.children.append(obj)
       
    def get_children(self):
        return self.children
    
    def get_children_count(self):
        return len(self.children)
     
    def print_tree_size(self):
        print 'tree size is %d' %(len(self.children))           
    
    def get_game_state(self):
        return self.gameState
    
    def print_tree(self):
        for c in self.children:
            print (c.gameState)
     
    def has_children(self):
        if len(self.children) ==  0 :
            return False
        return True                
 
   
def calculate_average_branching_fector(node):
    if (node.has_children()):
        global totalNodesHavingChilds
        totalNodesHavingChilds += 1
        children = node.get_children()
        #print 'expended node has child: %d'%(node.get_children_count())
        for child in children:
            calculate_average_branching_fector(child)
   

def create_new_game_node(parent, savedGameState):
    newGameNode = Game(savedGameState)
    newGameNode.set_parent(parent)
    parent.add_children(newGameNode)
    parent.set_game_state(savedGameState)
    return newGameNode            
    

def generate_game_tree(gameTreeNode, player):
    gameState = gameTreeNode.get_game_state()
    xs, ys = np.where(gameState == 0)
    
    # initialize flag that indicates win
    noWinnerYet = True

    for i in range(xs.size):
        savedGameState =objCopy.copy(gameState)

        if noWinnerYet:    
            savedGameState[xs[i]][ys[i]] = player
            
            #create the new game node and store it into the parent
            newGameNode = create_new_game_node(gameTreeNode, savedGameState)
            
            global totalNodeOfGameTree
            totalNodeOfGameTree += 1
            #simulate as a progress ...
            sys.stdout.write("\rTotal Game Tree Node Count: %d" %totalNodeOfGameTree)
            
            if move_was_winning_move(savedGameState, player):
                if player == PLAYER_X:
                    global totalGameWinByPlayer_X
                    totalGameWinByPlayer_X += 1
                    noWinnerYet = False
                # if a game is finished then that tree branching is stop
                return 
            else:
                generate_game_tree(newGameNode, player*-1)
        
    if noWinnerYet:
        global totalGameDrawCount;
        totalGameDrawCount +=1;
                
if __name__ == '__main__':
    
    # initialize 3x3 tic tac toe board
    gameState = np.zeros((3,3), dtype=int)
    
    # initialize player number, move counter
    player = PLAYER_X

    #initialize the game tree
    gameTree = Game(gameState)
    #generate game tree
    generate_game_tree(gameTree,player)

    #print '\ntotal node count :%d' %totalNodeOfGameTree
    print '\nTotal win by player X :%d' %totalGameWinByPlayer_X
    
    print 'Total draw count :%d' %totalGameDrawCount
    
    calculate_average_branching_fector(gameTree)
    #print 'Total Node count having childs :%d'%totalNodesHavingChilds
    print 'Average branching factor: %f' %(float(totalNodeOfGameTree)/totalNodesHavingChilds)
