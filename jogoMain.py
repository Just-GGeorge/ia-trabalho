"""
arquivo main responsavel para receber e tratar os inputs e mostrar display
"""

import pygame as p 
import jogoEngine , SmartMoveFinder

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
    playerOne = True #False a IA joga True o jogador joga
    playerTwo = False
    gameOver = False
    while running:
        humanturn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handle
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() # (x,y) posicao do mouse na tela
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row , col) : #checar se usuario cliclou no mesmo quadrado duas vezes "mover peça para msm lugar"
                        sqSelected = () # para de selecionar peça
                        playerClicks = [] # limpa registros de clicks  

                    else:
                        sqSelected = (row , col)
                        playerClicks.append(sqSelected) #salvar posição do primeiro e  segundo click
                        
                    if len(playerClicks)  == 2: # segundo click do jogador
                        move = jogoEngine.Move(playerClicks[0],playerClicks[1], gs.board)
                        print(move.getChessNotations())#para debug
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () #resetar os click do usuario
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            #key hanldes
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #"defaz ultimo movimento se aperta z"
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = jogoEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
            
        #IA move
        if not gameOver and not humanturn:
            AIMove = SmartMoveFinder.findBestMoveNegaMaxAlphaBeta(gs,validMoves)
            if AIMove is None:
                AImove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves = gs.getValidMoves()
            moveMade = False
        
        drawGameState(screen,gs,validMoves, sqSelected)

        if gs.checkMate :
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Mercenarios ganharam rei capturado')
            else:
                drawText(screen, 'Soldados ganharam rei chegou no refugio')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'StaleMate')

        if gs.ReiInCheck:
            gameOver = True
            if not gs.whiteToMove:
                drawText(screen, 'Mercenarios ganharam rei capturado')
            else:
                drawText(screen, 'Soldados ganharam rei chegou no refugio')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'StaleMate')
        
        clock.tick(MAX_FPS)
        p.display.flip()



'''
faz highlight dos quadrados possiveis para movimentar
'''

def highlightSquares(screen,gs,validMoves,sqSelected):
    
    if (len(gs.moveLog)) > 0:
        last_move = gs.moveLog[-1]
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('yellow'))
        screen.blit(s, (last_move.endCol * SQ_SIZE, last_move.endRow * SQ_SIZE))

    if sqSelected != ():
        r , c = sqSelected
        if gs.board[r][c][0] == ('w' if  gs.whiteToMove else 'b'): # quadrado selecionado é uma peça q pode mover
            #highlight selected square
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100) #valor transparencia 0 tranparente 255 opaco
            s.fill(p.Color("blue"))
            screen.blit(s,(c*SQ_SIZE, r*SQ_SIZE))
            #hightligh moves from square
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c :
                    screen.blit(s,(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


'''
responsavel pelas representações graficas
'''

def drawGameState(screen,gs,validMoves, sqSelected):
    drawBoard(screen) # desenha os quadrado do tabuleiro
    highlightSquares(screen,gs,validMoves, sqSelected)
    drawPieces(screen, gs.board)

'''
desenha os quadrados
'''
def drawBoard(screen):
    global colors

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


def animateMove(move,screen,board,clock):
    global colors
    #coords = [] #lista das cordenadas que animação ira acontecer
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol

    framesPerSquare = 10 # frames para mover por quadrado
    frameCount = (abs(dR)+ abs(dC)) * framesPerSquare

    for frame in range(frameCount + 1):
        r , c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen,board)
        # apaga peça que foi movida da sua posicao final

        color = colors[(move.endRow + move.endCol)% 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE , SQ_SIZE)
        p.draw.rect(screen , color , endSquare)

        #desenha a peça

        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #desenha peça movendo
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)

'''
função escrever texto
'''

def drawText(screen,text):
    font = p.font.SysFont("Helvitca",32, True,False)
    textObject = font.render(text, 0 , p.Color('Gray'))
    textLocation = p.Rect(0,0, WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2 , HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

    textObject = font.render(text, 0 , p.Color('Black'))
    screen.blit(textObject, textLocation.move(2,2))



if __name__ == "__main__":
    main()
