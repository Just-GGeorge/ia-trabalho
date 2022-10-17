import random

pieceScore = {"K":0 ,"R":5}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2
DIST = 99



def findBestMoveMinMax(gs,validMoves):
    global nextMove
    nextMove = None 
    findMoveMinMax(gs, validMoves , DEPTH, gs.whiteToMove)
    return nextMove
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove 
    if depth == 0:
        return scoreBoard(gs)

    if  whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score =  findMoveMinMax(gs,nextMoves, depth -1 , False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move

            gs.undoMove()
        return maxScore
    else:
        minScore =  CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score =  findMoveMinMax(gs,nextMoves, depth -1 , True)

            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

   
def findBestMoveNegaMaxAlphaBeta(game_state, valid_moves):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if game_state.whiteToMove else -1)
    return next_move 


def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)

    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score



def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins

    elif gs.staleMate:
        return STALEMATE

    score = 0 

    for row in gs.board:
        for square in row:
            if square[0] == "w":
                score = score + pieceScore[square[1]]
            elif square[1] == "b":
                score -= pieceScore[square[1]]

    extra = kingToRefuge(gs)
    if gs.whiteToMove:
        return score +(score - extra )
    else:
        return score

def kingToRefuge(gs):
    global DIST
    rei = gs.whiteKingLocation
    if gs.whiteToMove:
        for i in gs.refugio:
            if ((i[0] - rei[0]) + (i[1] - rei[1])) < DIST:
                DIST = abs (i[0] - rei[0]) + abs (i[1] - rei[1])
                return DIST
    else:
        return 0


def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]