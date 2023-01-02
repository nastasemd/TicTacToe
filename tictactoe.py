import pygame as pg
import os
import numpy as np
import random

Path = os.path.dirname(os.path.abspath(__file__))

# Initializing
pg.init()
screen = pg.display.set_mode((800, 600))
BG = (60, 120, 250)
screen.fill(BG)

# Title, icon and images
pg.display.set_caption("Tic Tac Toe")
icon = pg.image.load(os.path.join(Path, 'images\icon.png'))
pg.display.set_icon(icon)

boardImg = pg.image.load(os.path.join(Path, 'images\\board.png'))
OImg = pg.image.load(os.path.join(Path, 'images\O.png'))
XImg = pg.image.load(os.path.join(Path, 'images\X.png'))

# Clickable areas (Squares where you can place stuff)
squarePos = [(220, 120), (335, 120), (450, 120),
      (220, 235), (335, 235), (450, 235),
      (220, 350), (335, 350), (450, 350)]
      
areas = []
for i in range(len(squarePos)):
    areas.append(pg.Rect(squarePos[i][0], squarePos[i][1], 110, 110))

def drawBoard():
    screen.blit(boardImg, (220, 120))
    for i in range(len(b)):
        if b[i] == 'O':
            screen.blit(OImg, (squarePos[i][0], squarePos[i][1]))
        elif b[i] == 'X':
            screen.blit(XImg, (squarePos[i][0], squarePos[i][1]))

# Text and buttons
font = pg.font.Font("freesansbold.ttf", 32)
gameOverText = ""
RestartButton = pg.Rect(50, 150, 130, 50)
RestartButtonText = font.render('Restart', True, 'white')
githubText = "github.com/nastasemd"
def showText():
    topText = font.render("Tic Tac Toe", True, (255, 255, 255))
    github = font.render(githubText, True, (255, 255, 255))
    screen.blit(topText, (290, 40))
    screen.blit(github, (435, 565))
    if gameOverText == "Player won!":
        gText = font.render(gameOverText, True, (0, 255, 0))
        screen.blit(gText, (30, 90))
    elif gameOverText == "CPU won!":
        gText = font.render(gameOverText, True, (255, 0, 0))
        screen.blit(gText, (30, 90))
    elif gameOverText == "Tied game!":
        gText = font.render(gameOverText, True, (255, 255, 0))
        screen.blit(gText, (30, 90))
    if gameOver:
        mx,my = pg.mouse.get_pos()
        if RestartButton.x <= mx <= RestartButton.x + 130 and RestartButton.y <= my <= RestartButton.y + 50:
            pg.draw.rect(screen, (180, 180, 180), RestartButton)
        else:
            pg.draw.rect(screen, (110, 110, 110), RestartButton)
        screen.blit(RestartButtonText, (RestartButton.x + 5, RestartButton.y + 5))

# Game logic
clock = pg.time.Clock()
playerTurn = True
difficulty = 0
gameOver = False
b = np.array(9 * [""])

def checkGameEnd(gameOver, playerTurn):
    global gameOverText
    if gameOver:
        return True
    checks = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    if not "" in b:
        gameOver = True
        gameOverText = "Tied game!"
        
    for i in range(len(checks)):
        if checkWin(checks[i][0], checks[i][1], checks[i][2]):
            gameOver = True
            if playerTurn:
                gameOverText = "Player won!"
            else:
                gameOverText = "CPU won!"
    
    return gameOver

def checkWin(x, y, z):
    if (b[x] == b[y] and b[x] == b[z] and b[x] != ""):
        return True

# Game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(len(areas)):
                    if areas[i].collidepoint(event.pos) and gameOver == False and b[i] == "":
                        if playerTurn:
                            print('Player placed O into square ' + str(i) + '.')
                            b[i] = 'O'
                            gameOver = checkGameEnd(gameOver, playerTurn)
                            if gameOver == False:
                                playerTurn = False
                if RestartButton.collidepoint(event.pos):
                    gameOver = False
                    b = np.array(9 * [""])
                    playerTurn = True
                    gameOverText = ""
    screen.fill(BG)
    drawBoard()
    showText()
    pg.display.update()
    if not playerTurn and gameOver == False:
        pg.time.wait(300)
        r = random.randint(0, 8)
        while(b[r] != ""):
            r = random.randint(0, 8)
        print('CPU placed X into square ' + str(r) + '.')
        b[r] = 'X'
        gameOver = checkGameEnd(gameOver, playerTurn)
        if gameOver == False:
            playerTurn = True
        screen.fill(BG)
        drawBoard()
        showText()
        pg.display.update()
        clock.tick(60)
    