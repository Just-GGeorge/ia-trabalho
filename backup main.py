"""
arquivo main responsavel para receber e tratar os inputs e mostrar display
"""

import pygame as p 
import jogoEngine

WIDTH = HEIGHT  = 512
DIMENSION = 11
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES ={}

def loadImages():
    pieces = ['wR','wK','bR']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))

        #podemos acesar imagem atraves 'IMAGES['wp']'


def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = jogoEngine.GameState()

    validMoves = gs.getValidMoves()
    moveMade = False # variavel flag para quando movimento é feito

    loadImages()
    running = True
    sqSelected = () # definir o quadrado qual usuario cliclou inicia como nenhum
    playerClicks = [] #mantem o registro dos clicks mover peao que inicial está (4,4) para (5,4) 0 = x 1 = y
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN :
                location = p.mouse.get_pos() # (x,y) posicao do mouse na tela
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row , col) : #checar se usuario cliclou no mesmo quadrado duas vezes "mover peça para msm lugar"
                    sqSelected = () # para de selecionar peça
                    playerClicks = [] # limpa registros de clicks
                
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) #salvar posição do primeiro e  segundo click

                if len(playerClicks)  == 2: # segundo click do jogador
                    move = jogoEngine.Move(playerClicks[0],playerClicks[1], gs.board)
                    print(move.getChessNotations())#para debug
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () #resetar os click do usuario
                    playerClicks = [] 

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #"defaz ultimo movimento se aperta z"
                    gs.undoMove()
                    moveMade = True

            if moveMade:
                validMoves = gs.getValidMoves()
                moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
responsavel pelas representações graficas
'''

def drawGameState(screen,gs):
    drawBoard(screen) # desenha os quadrado do tabuleiro
    drawPieces(screen, gs.board)

'''
desenha os quadrados
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) %2)]
            p.draw.rect(screen,color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))

'''
desenha as peças
'''

def drawPieces(screen,board):
    for r in range (DIMENSION):
        for c in range (DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

if __name__ == "__main__":
    main()
