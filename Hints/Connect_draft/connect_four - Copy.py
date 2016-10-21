import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import time

class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()
         
    def __exit__(self, type, value, traceback):
        print "Elapsed time: {:.3f} sec".format(time.time() - self._startTime)
        print format(time.time() - self._startTime)

def evaluationFun(line, p):
    new_line = np.copy(line)
    new_line[new_line==0] = p
    if not terminalCheck(new_line, p):
        # there is no chance for p to win through this line
        return 0

    if layerComputation(line, p, 4):
        # (#rows * 4 + #cols * 4 + #diags*4) * 2
        return 100.0
    elif layerComputation(line, p, 3):
        return 3
    elif layerComputation(line, p, 2):
        return 2
    elif layerComputation(line, p, 1):
        return 1

    return 1.0
   
def evaluate(S, p):
    value = 0.0
    # count rows
    for rowIdx in range(S.shape[0]):
        row = S[rowIdx, :]
        value += evaluationFun(row, p)
        value -= evaluationFun(row, -p)

    # count cols
    for colIdx in range(S.shape[1]):
        column = S[:, colIdx]
        value += evaluationFun(column, p)
        value -= evaluationFun(column, -p)

    # count diagonals
    for i in range(-2, 4):
        value += evaluationFun(S.diagonal(i), p)
        value -= evaluationFun(S.diagonal(i), -p)

    rotatedS = np.rot90(S)
    for i in range(-3, 3):
        value += evaluationFun(rotatedS.diagonal(i), p)
        value -= evaluationFun(rotatedS.diagonal(i), -p)

    return value

def checkFullness(S):
    return not (S[S==0].size == 0)

def possibleMoves(S):
    possibleMoves = []
    for colIdx in range(S.shape[1]):
        column = S[:, colIdx]
        zeroIndexes = np.where(column == 0)[0]
        if zeroIndexes.size > 0:
            rowIdx = zeroIndexes.max()
            possibleMoves.append((rowIdx, colIdx))
    return possibleMoves

# find the next best move
def minmax(S, p, depth, maximize=True):
    possibleMove = possibleMoves(S)
    if 0 == depth or 0 == len(possibleMove):
        if maximize:
            return (evaluate(S, p), )
        else:
            return (evaluate(S, -p), )

    if terminalMovement(S, -p):
       if maximize:
           return (-np.inf, )
       else:
           return (np.inf, )

    best_move = possibleMove[0]
    if maximize:
        mmv = -np.inf
        for move in possibleMove:
            next_S = np.copy(S)
            next_S[move] = p
            next_mmv = minmax(next_S, -p, depth - 1, False)[0]
            if mmv < next_mmv:
                best_move = move
                mmv = next_mmv
    else:
        mmv = np.inf
        for move in possibleMove:
            next_S = np.copy(S)
            next_S[move] = p
            next_mmv = minmax(next_S, -p, depth - 1, True)[0]
            if mmv > next_mmv:
                best_move = move
                mmv = next_mmv


    return (mmv, best_move)

def minmaxMovement(S, p, depth):
    S[minmax(S, p, depth)[1]] = p
    return S

def randomMovement(S, p):
    possibleMove = possibleMoves(S)
    i = np.random.randint(len(possibleMove))
    
    S[possibleMove[i]] = p

    return S

def layerComputation(vector, p, n):
    for i in range(vector.size - n + 1):
        if vector[i] == p and vector[i:(i+n)].sum() == n * p:
            return True
    return False

def terminalCheck(vector, p):
    return layerComputation(vector, p, 4)

def terminalMovement(S, p):
    for rowIdx in range(S.shape[0]):
        row = S[rowIdx, :]
        if terminalCheck(row, p):
            return True

    for colIdx in range(S.shape[1]):
        column = S[:, colIdx]
        if terminalCheck(column, p):
            return True

    # check diagonals with length at least 4
    for i in range(-2, 4):
        if terminalCheck(S.diagonal(i), p):
            return True

    rotatedS = np.rot90(S)
    for i in range(-3, 3):
        if terminalCheck(rotatedS.diagonal(i), p):
            return True

    return False



# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:'0'}

# print game state matrix using symbols
def terminalVisualisation(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B



def start(playedGames, depth):
    # tournament statistics
    game = {1:0, -1:0, 0:0}

    for epoch in range(playedGames):
        # initialize 6x7 tic tac toe board
        gameState = np.zeros((6, 7), dtype=int)

        # initialize player number, move counter
        player = 1
        counter = 1

        # initialize flag that indicates win
        noWinnerYet = True
    
        while checkFullness(gameState) and noWinnerYet:
            # get player symbol
            name = symbols[player]
            # print '%s falls' % name

            if player == 1:
              # apply depth restricted search to do best move
              gameState = minmaxMovement(gameState, player, depth)
            else:
              # let player move at random
              gameState = randomMovement(gameState, player)

            # print current game state
            #terminalVisualisation(gameState)
        
            # evaluate game state
            if terminalMovement(gameState, player):
                # print 'player %s wins after %d moves' % (name, mvcntr)
                noWinnerYet = False

                # update tournament statistics
                # respective to the winner
                game[player] =game[player]+ 1
            # switch player and increase move counter
            if player==1:
                player = -1
            else:
                player = 1
            counter =counter +1


        if noWinnerYet:
            game[0] =game[0] + 1
            print 'draw' 

    print '\nWins and draws after %s sample:' % playedGames
    return game

def graphStatistics(tournament, playedGames, depth):
    data = []
    legends = []
    if tournament[-1]:
        data.append([-1] * tournament[-1])
        legends.append('We lost')
    if tournament[0]:
        data.append([0] * tournament[0])
        legends.append('Draw')
    if tournament[1]:
        data.append([1] * tournament[1])
        legends.append('We won')
    n, bins, patches = plt.hist(data, 1)
    plt.ylabel('Number of games')
    plt.title('Statistics after %s games where depth is %s' % (playedGames, depth))
    plt.legend(patches, legends)
    plt.show()

def proportion(totalNumber,findNumber):
    return (findNumber*100)/totalNumber

def pieWinLostDraw(tour,numberOfGames,threeDepth):
# make a square figure and axes
    figure(1, figsize=(6,6))
    ax = axes([0.1, 0.1,0.8, 0.8])

# The slices will be ordered and plotted counter-clockwise.
    labels = 'Wins', 'Draws', 'Losts'
    fracs = [proportion(numberOfGames,tour[1]),proportion(numberOfGames,tour[0]), proportion(numberOfGames,tour[-1])]
    explode=(0, 0.05, 0)

    pie(fracs, explode=explode, labels=labels,autopct='%1.1f%%', shadow=True, startangle=90)
                # The default startangle is 0, which would start
                # the Frogs slice on the x-axis.  With startangle=90,
                # everything is rotated counter-clockwise by 90 degrees,
                # so the plotting starts on the positive y-axis.

    title('Statistics after %s games where depth is %s' % (numberOfGames, threeDepth), bbox={'facecolor':'0.8', 'pad':5})

    show()


if __name__ == '__main__':
    playedGames = 5
    result = []
    for depth in range(1, 4):
        print "\n using depth = ", depth
        with Profiler() as p:
            game = start(playedGames, depth)
            result.append(game)

    print "\nResult ", result
    playedGames = len(result)
    i = 0
    while i<playedGames:
        graphStatistics(result[i], playedGames, i+1)
        pieWinLostDraw(result[i],playedGames,i+1)
        i = i + 1
