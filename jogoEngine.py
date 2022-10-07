""""
mantem informações atuais do jogo de xadrez, para determinar os estados que encontramos
"""

class  GameState():
    def __init__(self):
        # O tabuleiro 8 por 8 representado por listas de 2 dimensionais, cada elemento do tabuleir representado 2 simbolos
        # primeiro caracter é a cor b = preto e w = white
        # Segundo tipo de peça p = peao , Q = rainha , K = rei , B = bispo , R = torre , N = cavalo
        # a string "--" representa espaço vazio ou seha nao tem nenhuma eça sobre ela
        self.board = [

            ["--","--","--","bR","bR","bR","bR","bR","--","--","--"],
            ["--","--","--","--","--","bR","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--","--","--","--"],
            ["bR","--","--","--","--","wR","--","--","--","--","bR"],
            ["bR","--","--","--","wR","wR","wR","--","--","--","bR"],
            ["bR","bR","--","wR","wR","wK","wR","wR","--","bR","bR"],
            ["bR","--","--","--","wR","wR","wR","--","--","--","bR"],
            ["bR","--","--","--","--","wR","--","--","--","--","bR"],
            ["--","--","--","--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","bR","--","--","--","--","--"],
            ["--","--","--","bR","bR","bR","bR","bR","--","--","--"]]

        self.moveFunctions =  {'R':self.getRookMoves , 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

        self.whiteKingLocation = (5,5)

    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Log do movimento para poder cancelar voltar movimento
        self.ameaca_captura(move)
        self.whiteToMove = not self.whiteToMove # trocar qual player vai jogar

        #atualiza posicao do rei
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow,move.endCol)
            #print("atualizou o rei", self.whiteKingLocation)
        

    def confirma_captura(self,linha,coluna):
        enemyColor = "w" if self.whiteToMove else "b"
        contador = 0
        
        for i in range(len(linha)):
            if (linha[i] + 1) < 11:
                
                if self.board[linha[i]+1][coluna[i]][0] == enemyColor:
                    contador += 1
            if (linha[i] - 1) >= 0: 
                if self.board[linha[i]-1][coluna[i]][0] == enemyColor:
                    contador += 1
            if (coluna[i] + 1) < 11:
                if self.board[linha[i]][coluna[i]-1][0] == enemyColor:
                    contador += 1
                if self.board[linha[i]][coluna[i]+1][0] == enemyColor:
                    contador += 1
            if contador >= 2:
                self.board[linha[i]][coluna[i]] = "--"
            contador = 0

    def ameaca_captura(self,move):
        log = self.moveLog[-1]
        linha = [move.endRow][0]
        coluna = [move.endCol][0]
        linha_verifica = []
        coluna_verifica = []
        enemyColor = "b" if self.whiteToMove else "w"
        flag_captura = False
        if (linha + 1) < 11:
            if self.board[linha+1][coluna][0] == enemyColor:
                flag_captura = True
                linha_verifica.append(linha+1)
                coluna_verifica.append(coluna)
        if (linha - 1) >= 0: 
            if self.board[linha-1][coluna][0] == enemyColor:
                flag_captura = True
                linha_verifica.append(linha-1)
                coluna_verifica.append(coluna)
        if (coluna + 1) < 11:
            if self.board[linha][coluna-1][0] == enemyColor:
                flag_captura = True
                linha_verifica.append(linha)
                coluna_verifica.append(coluna-1)

            if self.board[linha][coluna+1][0] == enemyColor:
                flag_captura = True
                linha_verifica.append(linha)
                coluna_verifica.append(coluna+1)
        if flag_captura:
            self.confirma_captura(linha_verifica,coluna_verifica)  
        linha_verifica = []
        coluna_verifica = []

#se quiser arruma para volta movimento de peça que foi de base força ae eu do futuro
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop() # remove ultimo elemento e passa valor para variavel se estiver sendo atribuida como esse caso
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove 

    
    '''
    movimentos considerando checks mates
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() # por enquanto

    '''
    movimentos que nao consideram checks mate
    '''
    def getAllPossibleMoves(self):
        moves = []

        for r in range(len(self.board)): # linhas 
            for c in range (len(self.board[r])): # colunas
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) # vai chamar função de movimentos de acordo com tipo da peça
        return moves

    '''
    get todos movimentos do peão, para linha e coluna e salva em lista
    '''

    def getRookMoves(self,r,c,moves):
        #print("Valor de R e C que recebi",r,c)
        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range (1,len(self.board)):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 11 and 0 <= endCol < 11:
                    if (endRow,endCol) not in ((0,0),(0,10),(10,0),(10,10),(5,5)):
                        endPiece = self.board[endRow][endCol]
                        
                    else:
                        break
                    if endPiece == "--": # espaço vazio
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    #elif endPiece[0] == enemyColor: # movimento para capturar
                        #moves.append(Move((r,c),(endRow,endCol),self.board))
                        #break
                    else:
                        break
                else:
                    break
            
    def getKingMoves(self,r,c,moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range (1,len(self.board)):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 11 and 0 <= endCol < 11:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # espaço vazio
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    #elif endPiece[0] == enemyColor: # movimento para capturar
                        #moves.append(Move((r,c),(endRow,endCol),self.board))
                        #break
                    else:
                        break
                else:
                    break

class Move():

    # mapa chaves para valores
    # chave : valor

    rankToRows = {"1":10,"2":9,"3":8,"4":7,"5":6,"6":5,"7":4,"8":3,"9":2,"10":1,"11":0}
    



    rowToRanks = {v: k for k , v in rankToRows.items()}
    
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,"i":8,"j":9,"k":10}


    colsToFiles = {v: k for k , v in filesToCols.items()}


    def __init__(self, startSq , endSq , board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID= self.startRow * 100000 + self.startCol * 10000 + self.endRow * 1000 + 10 * self.endCol

    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotations(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowToRanks[r]