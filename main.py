'''
NOTES and [TO DO]:
    - board[r][c]!=0 have no use  it will be !=0 always  --- remove it
    - combine horizontal and vertical iterations at one loop
    - vertical win checking have only one case
    - test winning part again
    - during events handling we do all of them "if" to get the chance to handle all of them


Questions :
    - why functions see the variables bellow it
    - what is the things that get passed by reference in python
    - could the game end with DRAW (no winner )
'''

import numpy as np
import pygame
import sys

# GLOBAL VARIABLES
# colors
BLACK = (0 , 0 , 0)
BLUE =(0 , 0 , 255) # RGB
RED = (255 , 0, 0)
YELLOW = (255 , 255, 0)

# main part
rows=6
cols=7
win_sz=4
last=[0]*cols  # help me to place pieces in fast manner
game_over=False
turn=1

# screan information
SQUARESIZE=100 # pixel
RADIUS=SQUARESIZE//2-5
WIDTH=cols*SQUARESIZE
HEIGHT=(rows+1)*SQUARESIZE  # extra 1 for circle to be droped
SIZE=(WIDTH , HEIGHT)
# END of Global Variables


# AI part (alpha beta algorithm)
# MIT LECTURE and ASSIGNMENT




# game logic functions
def build_board(n , m):
    board=np.zeros((n , m))
    return board

def valid_pos(col , board, cols):
    if col<0 or col>=cols:
        return 0
    return board[5][col]==0


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


def place_piece(col , board , player):   # does python pass arrays by reference
    index=last[col]
    board[index][col]=player
    last[col]+=1
    return

def display_board(board):
    print(np.flip(board , 0))   # flip over the x axis
    return

def h_win(board , rows ,cols , c, win_sz):
    r=last[c]-1
    cnt=0
    # left horizontal
    for i in range(1 , win_sz):
        if c-i<0:
            break
        if board[r][c]!=0 and board[r][c]==board[r][c-i]:
            cnt+=1
    for i in range(1, win_sz):
        if c+i>=cols:
            break
        if board[r][c]!=0 and board[r][c]==board[r][c+i]:
            cnt+=1

    if cnt>=3:
        return True
    return False

def v_win(board , rows , cols , c , win_sz):
    r=last[c]-1
    cnt=0
    '''  # this case will never happen as we drop pieces to bottom first 
    # upper vertical
    for i in range(1 , win_sz):
        if r+i>=rows:
                break
        if board[r][c]!=0 and board[r][c]==board[r+i][c]:
            cnt+=1
    match=max(match , cnt)
    '''
    # lower winning
    for i in range(1, win_sz):
        if r-i<0:
            break
        if board[r][c]!=0 and board[r][c]==board[r-i][c]:
            cnt+=1
    if cnt>=3:
        return True
    return False

def main_diagonal_win(board , rows , cols , c , win_sz):
    r=last[c]-1
    cnt=0

    # upper part
    for i in range(1 , win_sz):
        if not (r-i>=0 and c-i>=0):
            break
        if board[r][c]!=0 and board[r][c]==board[r-i][c-i]:
            cnt+=1

    # lower part
    for i in range(1 ,win_sz):
        if r+i>=rows or c+i>=cols:
            break
        if board[r][c]!=0 and board[r][c]==board[r+i][c+i]:
            cnt+=1

    if cnt>=3:
        return True
    return False

def off_diagonal_win(board , rows , cols , c , win_sz):
    r=last[c]-1
    cnt=0
    # upper part
    # increase coloumn and decrease row
    for i in range(1 , win_sz):
        if r-i<0 or c+i>=cols:
            break
        if board[r][c]!=0 and board[r][c]==board[r-i][c+i]:
            cnt+=1

    # lower part
    # increase row and decrease coloumn
    for i in range(1 , win_sz):
        if r+i>=rows or c-i<0:
            break
        if board[r][c]!=0 and board[r][c]==board[r+i][c-i]:
            cnt+=1

    if cnt>=3:
        return True
    return False

def winning(board , rows , cols , c , win_sz):
    # how does theses functions accesses last ***********************************************************
    if h_win(board , rows , cols , c , win_sz)==True:
        return True
    if v_win(board, rows , cols , c , win_sz) == True:
        return True
    if main_diagonal_win(board, rows , cols , c , win_sz) == True:
        return True
    if off_diagonal_win(board, rows , cols , c , win_sz) == True:
        return True

    return False





board=build_board(rows , cols)
# graphics part  using Pygame library
def draw_board(SCREEN , x , board , player):
    # positions here are (x , y)  -> (col , row )   like my CV lib    in pixels as coordinates
    # surface , color , shape parameters
    SCREEN.fill((0 , 0 , 0)) # clear the screen
    co=BLACK
    if player==1:
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


pygame.init()
SCREEN = pygame.display.set_mode((WIDTH , HEIGHT))  # why do we hold it in SCREEN  ->> it's a reference to draw on it

# game loop
while not game_over:
    # iterator throw the events that pygame capture from my pc
    for event in pygame.event.get():
        if event.type==pygame.QUIT:  # exit
            sys.exit() # I guess it have 0 parm by default

        if event.type == pygame.MOUSEBUTTONDOWN:  # clicking to drop a piece
            print(event.pos)
            x=event.pos[0]
            col = x//100  # [0 , 7)
            if col==7:
                col-=1
            place_piece(col, board, turn)
            display_board(board)  # console thing
            if winning(board, rows, cols, col, win_sz) == True:
                print("player {} wins ".format(turn))
                game_over = True
            else:
                turn = 3 - turn  # alternate between players turns  3-1=1   , 3-2=1 ans so on

        if event.type == pygame.MOUSEMOTION:
            print(event.pos)
            x=int(event.pos[0])  # it's a tuple
            # edit the position
            if x<SQUARESIZE/2:
                x=50
            if WIDTH-x<50:
                x-=50-(WIDTH-x)


    draw_board(SCREEN , x , board , turn)  # only need to be called once