import pygame as pg
import sys
import os

BOX_SIZE = 50

PLAYER = "@"
TARGET = "."
SPACE = " "
BINGO = "*"
WALL = "#"
BOX = "$"

board = []
targets = []
all_fonts = pg.font.get_fonts()
root = os.path.dirname(os.path.abspath(__file__))

def restartLevel():
    global board
    global targets
    board = []
    targets = []
    initBoard()
    initTargets()

def checkWin():
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == TARGET or (board[i][j] == BOX and isTarget(i, j)):
                return False
    return True

def drawWinMessage(screen):
    font = pg.font.SysFont("comicsansms", 20)
    text = font.render('BINGO!', True, (255, 255, 255))
    text_rect = text.get_rect(center=(getScreenSize()[0] // 2, getScreenSize()[1] // 2))
    screen.blit(text, text_rect)

def initBoard():
    with open(root+"/game.txt", "r") as f:
        for line in f.read().splitlines():
            board.append(list(line))

def initTargets():
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == TARGET:
                targets.append([i, j])

def isTarget(row, col):
    for target in targets:
        if target[0] == row and target[1] == col:
            return True
    return False

def getPlayerPosition():
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == PLAYER:
                return i, j

def moveLeft():
    movePlayer(0, -1)
def moveRight():
    movePlayer(0, 1)
def moveDown():
    movePlayer(1, 0)
def moveUp():
    movePlayer(-1, 0)

def doMove(row, col, i, j):
    board[row+i][col+j] = PLAYER
    if isTarget(row, col):
        board[row][col] = TARGET
    else:
        board[row][col] = SPACE

def drawRestartMessage(screen):
    pg.font.init()
    font = pg.font.SysFont("comicsansms", 20)
    text = font.render('Нажмите R для перезапуска', True, (0, 0, 75))
    text_rect = text.get_rect(center=(getScreenSize()[0] // 2, getScreenSize()[1] - 20))
    screen.blit(text, text_rect)

def drawBoard(screen):
    img_wall = pg.image.load(root+'/wall.png').convert()
    img_box = pg.image.load(root+'/box.png').convert()
    img_bingo = pg.image.load(root+'/bingo.png').convert()
    img_target = pg.image.load(root+'/target.png').convert()
    img_space = pg.image.load(root+'/space.png').convert()
    img_player = pg.image.load(root+'/player.png').convert()
    images = {
        WALL: img_wall,
        SPACE: img_space,
        BOX: img_box,
        TARGET: img_target,
        PLAYER: img_player,
        BINGO: img_bingo
    }
    for i in range(len(board)):
        for j in range(len(board[i])):
            screen.blit(images[board[i][j]], (j*BOX_SIZE, i*BOX_SIZE))
    pg.display.update()
def movePlayer(i, j):
    row, col = getPlayerPosition()
    m, n = i*2, j*2
    if board[row+i][col+j] == SPACE:
        doMove(row, col, i, j)
    elif board[row+i][col+j] == TARGET:
        doMove(row, col, i, j)
    elif board[row+i][col+j] == BOX:
        if board[row+m][col+n] == SPACE:
            board[row+m][col+n] = BOX
            doMove(row, col, i, j)
        elif board[row+m][col+n] == TARGET:
            board[row+m][col+n] = BINGO
            doMove(row, col, i, j)
    elif board[row+i][col+j] == BINGO:
        if board[row+m][col+n] == SPACE:
            board[row+m][col+n] = BOX
            doMove(row, col, i, j)
        elif board[row+m][col+n] == TARGET:
            board[row+m][col+n] = BINGO
            doMove(row, col, i, j)
    else:
        pass

def getScreenSize():
    j = 0
    for i in range(len(board)):
        j = len(board[i]) if len(board[i]) > j else j
    return  j * BOX_SIZE, len(board) * BOX_SIZE

def main():
   board = initBoard()
   targets = initTargets()
   pg.display.init()
   pg.display.set_caption("Ящики")
   screen = pg.display.set_mode(getScreenSize())
   screen.fill((0, 0, 0))
   while True:
       for event in pg.event.get():
           if event.type == pg.KEYDOWN:
               if event.key == pg.K_r:
                   restartLevel()
               if event.key == pg.K_LEFT:
                   moveLeft()
               elif event.key == pg.K_RIGHT:
                   moveRight()
               elif event.key == pg.K_DOWN:
                   moveDown()
               elif event.key == pg.K_UP:
                   moveUp()
               elif event.key == pg.K_ESCAPE:
                   pg.quit()
                   sys.exit()
           elif event.type == pg.QUIT:
               pg.quit()
               sys.exit()
           drawBoard(screen)
           drawRestartMessage(screen)
           if checkWin():
                drawWinMessage(screen)
           pg.display.update()

if __name__ == "__main__":
    main()
