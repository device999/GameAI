This is description of the source code:
In this code i implemented 13 functions and 1 main loop.
The name of the functions and their description will be given below:
i will start from main loop and will continue with description every function:
plus i will provide in the source short information about each function individually

So it starts from the main loop:
we create a grid "a" as numpy array with sizes of global variables LINE and column
line,column,step,enemy and winner used in our main cycle
arrays goodmove and badmove needed for statistics
while	checkFullness(a)!=1	and	winner==0:
checkFullness function checks whether our grid (a) is not full
this function gives two outputs whether 1 or 2:
1 when our grid is full and 2 when we have some steps to play
winner is 0,because we don't have anyone who won the game,
winner can be either 0,1 or 2
0 draw
1 First player won
2 Second player won
While we are in condition we have to define who's step it is
either player 1 or player 2, therefore we use function turn()
it has one input=>step , which is so called counter and defines 
turn by simply finding the remainder of our step divided by 2
if it 0 =>player 1
		enemy=>2
else =>
player= 2
enemy = 1
After knowing the player,we are using brute force search
to find the point which can lead us to victory or we have to
cover the point which help opponent to win.
Therefore i implemented function called
nextMove(a,{player or enemy})
in defence method, function checks all grid (a,enemy) for 
opponents positions,
there are 4 functions which checks grid for 4 connections
checkUpandDown(grid,line,column,player) checks vertical or
up and down neighbors of the element
checkRightandLeft(--/same input as previous--) checks horizontal
or right and left neighbors of the element
checkDiagonalRightUpLeftDown(same input) checks right diagonal
checkDiagonalLeftUpRightDown(same input) checks left diagonal
for horizontal and diagonal checking there is some cases in which for example :
we have a line a[3][0,1,2],but a[4][3] is so for winning a[4][3] must be filled and only
after that we can input our point to win.So we are checking the below line if it empty ,then we play 
but in case it is not we are awared of being losed or won.
so the function checkDownNeighbor,checks whether the down field is empty or not.
After this processes done ,we can enter our value or assign randomly.{You can comment or uncomment the code on line 245,246}
Then statistics mode proceeds,we calculate the bad or good move.I will explain more detailly in the presentation.
268 - 286 is the important part of our programm ,
so first when we add value it must fall into the last line in our case is 5 and the column is chosen by us.
if that line is already full we have to put it into its up neighbor,but we have to check whether it is also full or not
therefore we need cycle while it will go upwards untill there will be no free up or the column will not end, in second case
program will ask to reply replying that the column is full and there are presented also break points accordingly.
In case there is no value in the line so we are simply assigning the choice of the player to the line,
variables line and column are needed for further working, they are helping checkingFunctions.
so when we made our move and we can proceed to the checkingFunctions,considering initial layer we are checking its neighbors
all across the grid.so if it has more than 3 neighbors value of the variable is assigned either to 1 or 2 depending on the player
and exiting the main while loop.
thats it! :)