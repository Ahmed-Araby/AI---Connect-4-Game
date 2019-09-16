'''
NOTES and [TO DO]:
    - board[r][c]!=0 have no use  it will be !=0 always  --- remove it
    - combine horizontal and vertical iterations at one loop
    - vertical win checking have only one case
    - test winning part again
    - during events handling we do all of them "if" to get the chance to handle all of them
    - I define the board with the board structure and coloumn of last droped piece and last list that help me in droping pieces [ Important ]
    - for off diagonal winning he says main diagonal and vice versus because the board is reversed for the user interface
    - 16/9 adding alpha beta .............. .................  it made the algo go deeper and became damen faster

Questions :
    - why functions see the variables bellow it
    - what is the things that get passed by reference in python
    - could the game end with DRAW ( no winner )

'''

import numpy as np
import pygame
import sys
import copy
import math

# GLOBAL VARIABLES
# colors
BLACK = (0 , 0 , 0)
BLUE =(0 , 0 , 255) # RGB
RED = (255 , 0, 0)
YELLOW = (255 , 255, 0)

# main part
hard=4 # how hard the game is
rows=6
cols=7
win_sz=4
last=[0]*cols  # help me to place pieces in fast manner
game_over=False

# screan information
SQUARESIZE=100 # pixel
RADIUS=SQUARESIZE//2-5
WIDTH=cols*SQUARESIZE
HEIGHT=(rows+1)*SQUARESIZE  # extra 1 for circle to be droped
SIZE=(WIDTH , HEIGHT)
# END of Global Variables


# AI part (min max algorithm and alpha beta algorithm)
# MIT LECTURE and ASSIGNMENT
# I need more understanding of alpha beta pruning algorithm

class player:
    def __init__(self , id , type , name):
        self.id=id
        self.type=type
        self.name=name
        return
class node:
    def __init__(self , board , c , last):
        self.last=copy.deepcopy(last)
        self.c=c
        self.board=copy.deepcopy(board)

class game_solver:
    def __init__(self):
        pass
    def min_max(self, state , depth , player1 , player2 , alpha , beta):  # alpha max value for maximizer , beta min value for minimizer ..
        term=self.is_terminal(state)
        if depth==0 or term==True:
            if term==True:
                if player1==1: # player id = 2 is a winner
                    return -100 , state.c
                else:
                    return 100 , state.c
            return 0 , state.c
        res=0
        best_col=0
        moves=self.get_moves(state , player1)
        # maximizing player
        if player1==1:
            res=-100000
            for move in moves:
                t1 , t2=self.min_max(move , depth-1 , player2 ,player1 , alpha , beta)
                if t1>res:
                    res=t1
                    best_col=move.c
                    alpha=max(alpha , res)
                if alpha>=beta:   # alpha beta pruning
                    break

        # minimizing player
        else:
            res=100000
            for move in moves:
                t1 , t2=self.min_max(move , depth-1 , player2 ,player1 , alpha , beta)
                if t1<res:
                    res=t1
                    best_col=move.c
                    beta=min(beta , res)
                if alpha>=beta:  # alpha beta pruning
                    break

        return res , best_col

    def get_moves(self , state , player):
        moves=[]
        for i in range(cols):
            if valid_pos(i , state.board , cols):
                new_board=copy.deepcopy(state.board)
                l=copy.deepcopy(state.last)
                r=l[i]
                l[i]+=1
                new_board[r][i]=player
                new_state=node(new_board , i  , l)
                moves.append(copy.deepcopy(new_state))
        return moves  # does this get returned by reference  *******************************************

    def is_terminal(self , state):
        if state.c==-1:
            return False
        win , how=winner.is_winning(state.board , state.c , state.last)
        if win==True:
            return True
        return False

    def evaluate(self , state):
        return False

# game logic functions
def build_board(n , m):
    board=np.zeros((n , m))
    return board

def valid_pos(col , board, cols):
    if col<0 or col>=cols:
        return 0
    return board[5][col]==0


'''
def take_input(player , cols):  # for console purpose
    valid=False
    while not valid:
        col = int(input("player {} enter your choice \n ".format(player)))
        col-=1  # 0 indexing
        if valid_pos(col, board , cols):
            valid = True
        else:
            print("not a valid position to drop a piece try again \n")
    return col

'''


def place_piece(col , board , player):
    if col<0 or col>=cols or last[col]==rows:
        return
    index=last[col]
    board[index][col]=player
    last[col]+=1
    return

def display_board(board):
    print(np.flip(board , 0))   # flip over the x axis
    return



class winning:
    def __init__(self):
        self.last=[]


    def h_win(self ,board ,c):
        r=self.last[c]-1
        cnt=0
        # left horizontal
        for i in range(1 , win_sz):
            if c-i<0:
                break
            if board[r][c]!=0 and board[r][c]==board[r][c-i]:
                cnt+=1
            else: # this was the BUG   ******
                break

        # right part
        for i in range(1, win_sz):
            if c+i>=cols:
                break
            if board[r][c]!=0 and board[r][c]==board[r][c+i]:
                cnt+=1
            else: # this was the BUG   ******
                break

        if cnt>=3:
            return True
        return False

    def v_win(self ,board ,c):
        r=self.last[c]-1
        cnt=0
        # no need for upper case
        # lower winning
        for i in range(1, win_sz):
            if r-i<0:
                break
            if board[r][c]!=0 and board[r][c]==board[r-i][c]:
                cnt+=1
            else: # this was the BUG   ******
                break
        if cnt>=3:
            return True
        return False

    def main_diagonal_win(self ,board ,c):
        r=self.last[c]-1
        cnt=0

        # upper part
        for i in range(1 , win_sz):
            if not (r-i>=0 and c-i>=0):
                break
            if board[r][c]!=0 and board[r][c]==board[r-i][c-i]:
                cnt+=1
            else: # this was the BUG   ******
                break

        # lower part
        for i in range(1 ,win_sz):
            if r+i>=rows or c+i>=cols:
                break
            if board[r][c]!=0 and board[r][c]==board[r+i][c+i]:
                cnt+=1
            else: # this was the BUG   ******
                break

        if cnt>=3:
            return True
        return False

    def off_diagonal_win(self ,board ,c):
        r=self.last[c]-1
        cnt=0
        # upper part
        # increase coloumn and decrease row
        for i in range(1 , win_sz):
            if r-i<0 or c+i>=cols:
                break
            if board[r][c]!=0 and board[r][c]==board[r-i][c+i]:
                cnt+=1
            else: # this was the BUG   ******
                break

        # lower part
        # increase row and decrease coloumn
        for i in range(1 , win_sz):
            if r+i>=rows or c-i<0:
                break
            if board[r][c]!=0 and board[r][c]==board[r+i][c-i]:
                cnt+=1
            else: # this was the BUG   ******
                break


        if cnt>=3:
            return True
        return False

    def is_winning(self , board , c , last):
        self.last = copy.deepcopy(last)

        if self.h_win(board, c )==True:
            return True , "HORIZONTAL"
        if self.v_win(board, c) == True:
            return True , "VERTICAL"
        if self.main_diagonal_win(board, c) == True:
            return True , "MAIN DIAGONAl"
        if self.off_diagonal_win(board, c) == True:
            return True , "OFF DIAGONAL"

        '''
            we need to handle draw case 
        '''
        return False , "NO WINNER"





# graphics part  using Pygame library
def draw_board(SCREEN , x , board , player):
    # positions here are (x , y)  -> (col , row )   like my CV lib    in pixels as coordinates
    # surface , color , shape parameters
    SCREEN.fill((0 , 0 , 0)) # clear the screen
    co=BLACK
    if game_over:
        co=BLACK
    elif player==1:
        co=RED
    else:
        co=YELLOW
    pygame.draw.rect(SCREEN , BLUE , (0 , SQUARESIZE, WIDTH , HEIGHT))
    pygame.draw.circle(SCREEN, co, (x, SQUARESIZE // 2), RADIUS)  # circle that follow the mouse

    flipped_board=np.flip(board , 0)
    for i in range(1 , rows+1):
        for j in range(0 , cols):
            # surface , color , center(integer only) , radius
            # radius-5 so that circles don't touch
            if flipped_board[i-1][j]==0:
                pygame.draw.circle(SCREEN, BLACK, (j * SQUARESIZE + SQUARESIZE // 2, i * SQUARESIZE + SQUARESIZE // 2), SQUARESIZE // 2 - 5)
            elif flipped_board[i-1][j]==1:
                pygame.draw.circle(SCREEN, RED , (j * SQUARESIZE + SQUARESIZE // 2, i * SQUARESIZE + SQUARESIZE // 2), SQUARESIZE // 2 - 5)
            elif flipped_board[i-1][j]==2:
                pygame.draw.circle(SCREEN, YELLOW, (j * SQUARESIZE + SQUARESIZE // 2, i * SQUARESIZE + SQUARESIZE // 2), SQUARESIZE // 2 - 5)

    pygame.display.update()

    return


board=build_board(rows , cols)
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH , HEIGHT))  # why do we hold it in SCREEN  ->> it's a reference to draw on it
turn=1
player1=player(1 , 1 , "Ahmed Araby")  # human
player2=player(2 , -1 , "AI")  # computer
cur_player=player1
other_player=player2
solver=game_solver()
winner=winning()
# game loop
x=0 # in case it were computer turn it will be noe defined so this helps

while True:
    if game_over:
        draw_board(SCREEN , x , board , turn )
    elif cur_player.type==-1:  # computer run (AI algorithm)
        state=node(board , -1 ,last)
        val , col=solver.min_max(state , 6 , cur_player.id , other_player.id , -math.inf , math.inf)  # alpha , beta

        # play part try to encapculate it   **************************
        place_piece(col, board, turn)
        display_board(board)  # console thing
        win , how =winner.is_winning(board, col, last)
        if win==True:
            print("player {} wins -- {}".format(turn , how))
            game_over = True
        else:
            turn = 3 - turn  # alternate between players turns  3-1=1   , 3-2=1 ans so on
            # exchange players  , put it into a function
            tmp = copy.deepcopy(cur_player)
            cur_player = copy.deepcopy(other_player)
            other_player = copy.deepcopy(tmp)


    else:  # human
        for event in pygame.event.get():

            if event.type==pygame.QUIT:  # exit
                sys.exit() # I guess it have 0 parm by default

            if event.type == pygame.MOUSEBUTTONDOWN:  # clicking to drop a piece
                #print(event.pos)
                x=event.pos[0]
                col = x//100  # [0 , 7)
                if col==7:
                    col-=1
                place_piece(col, board, turn)
                display_board(board)  # console thing
                win , how=winner.is_winning(board,col , last)
                if win==True:
                    print("player {} wins -- {}".format(turn , how))
                    game_over = True
                else:
                    turn = 3 - turn  # alternate between players turns  3-1=1   , 3-2=1 ans so on
                    # exchange players  , put it into a function
                    tmp=copy.deepcopy(cur_player)
                    cur_player=copy.deepcopy(other_player)
                    other_player=copy.deepcopy(tmp)

            if event.type == pygame.MOUSEMOTION:
                #print(event.pos)
                x=int(event.pos[0])  # it's a tuple
                # edit the position
                if x<SQUARESIZE/2:
                    x=50
                if WIDTH-x<50:
                    x-=50-(WIDTH-x)

    draw_board(SCREEN , x , board , turn)  # only need to be called once