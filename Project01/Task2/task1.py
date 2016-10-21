import numpy as np
import operator
import matplotlib.pyplot as plt


def move_still_possible(S):
    return not (S[S==0].size == 0)

#Random move, move function returns new game state
def move_at_random(S, p):
    xs, ys = np.where(S==0)

    i = np.random.permutation(np.arange(xs.size))[0]

    S[xs[i], ys[i]] = p

    return S

# Function that counts the amount of winning combinations

def winning_move_cnt(S, p):
    cnt= np.sum(np.sum(S, axis=0) * p == 3) + \
         np.sum(np.sum(S, axis=1) * p == 3) + \
         int((np.sum(np.diag(S)) * p) == 3) +\
         int((np.sum(np.diag(np.rot90(S))) * p) == 3)
    return cnt
# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}


# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print (B)

#main function to play game n-times, where X uses move1 and O - move2
def playGame(move1, move2, n=1):
    # initialize 3x3 tic tac toe board
    #game_res = dict.fromkeys(['-1','0','1'],list()) #--this produces a weird dublication bug =(
    game_res = {-1:[],0:[],1:[]}
    for i in range(n):

        gameState = np.zeros((3,3), dtype=int)
        # initialize player number, move counter
        player = 1
        mvcntr = 1

        # initialize flag that indicates win
        noWinnerYet = True
        while move_still_possible(gameState) and noWinnerYet:
            # Make move depending on game config
            gameState = move1(gameState, player) if player == 1 else move2(gameState, player)

            # evaluate game state
            if winning_move_cnt(gameState, player):
                game_res[player].append(gameState) #= gameState
                noWinnerYet = False

            # switch player and increase move counter
            player *= -1
            mvcntr +=  1
        if noWinnerYet:
             game_res[0].append(gameState)
    return game_res

#For statistical approach, game is played multiple of times
# and analizaed for the points with the highest win impact

def analyzeGame(n=1):
    points = [(x, y) for x in range(3) for y in range(3)]
    point_cnt = dict.fromkeys(points, 0)
    results = playGame(move_at_random,move_at_random, n)
    print([len(results[i]) for i in [-1, 0, 1]])
    win_cnt = len(results[-1]) + len(results[1])
    for k,v in results.items():
        if k != '0':
            for field in v:
                a = np.where(field==k)
                for i in range(len(a[0])):
                    point_cnt[(a[0][i], a[1][i])] +=1/win_cnt
    return point_cnt

#Move based on statistical analysis, task 2.1

def adjustedMove(S, p):
    for key, value in MOVE_RATE:
        #print("%s wins with prob %s" % (key, value))
        if S[key] == 0:
            S[key] = p
            return S

# Heuristic move implementation, based on the quality function, that encounters the amount of
# possible winning positions, task 2.2

def heuristicMove(S, p):

    #utility function, estimates the amount of possible winning game states
    def calculateWinStates(tmpS,p ):
        Sp1 = tmpS.copy()
        Sp2 = tmpS.copy()
        Sp1[Sp1==0]=p
        Sp2[Sp2 == 0] = -1*p
        return winning_move_cnt(Sp1,p) - winning_move_cnt(Sp2,-1*p)

    x,y = np.where(S==0)
    point_odds = -10000
    # iterative estimation of empty fields
    for point in [(x[i],y[i]) for i in range(len(x))]:
        #trigger to check if rival can win in next step
        tmp = S.copy()
        tmp[point] = -1*p
        if winning_move_cnt(tmp, -1*p):
            S[point] = p
            return S

        tmp = S.copy()
        tmp[point] = p
        if calculateWinStates(tmp,p) > point_odds:
            bestPoint = point
    S[bestPoint] = p
    return S

# function to build pair-wise barcharts in order to see the initial move impact

def plotPairs(res1,res2, name1, name2):

    N = 3
    a1 = [len(res1[i]) for i in [-1,0,1]]
    a2 = [len(res2[i]) for i in [-1,0,1]]
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, a1, width, color='r')
    rects2 = ax.bar(ind + width, a2, width, color='y')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('observations')
    ax.set_title('Game results')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(('O', 'draw', 'X'))
    ax.legend((rects1[0], rects2[0]), (name1, name2), loc=2)

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)
    plt.show()

if __name__ == '__main__':
    #couple of steps to build a coefs for statistical move
    test = analyzeGame(1000)
    MOVE_RATE = sorted(test.items(), key=operator.itemgetter(1),reverse = True)

    #different result calculation for further visualization
    res1 = playGame(move_at_random, move_at_random, 1000)
    res11 = playGame(move_at_random, move_at_random, 1000)
    res2 = playGame(adjustedMove, move_at_random, 1000)
    res21 = playGame(move_at_random, adjustedMove,  1000)
    res3 = playGame(heuristicMove, move_at_random, 1000)
    res31 = playGame(move_at_random, heuristicMove,  1000)
    res4 = playGame(adjustedMove, heuristicMove, 1000)
    res41 = playGame(heuristicMove,  adjustedMove, 1000)

    #calls of vis function to get the plots
    plotPairs(res1,res11,  'random-random','random-random')
    plotPairs(res2,res21, 'X - statistics; O - random', 'X-random; O - statistics')
    plotPairs(res3,res31, 'X - heuristic move; O - random', 'X - random; O - heuristic move')
    plotPairs(res4,res41, 'X - statistics; O - heuristic move', 'X-heuristic move; O - statistics')
