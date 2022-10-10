import random

pieceScore = {"K":0 , "Q":10,"R":5,"B":3,"N":3,"p":1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 1




def findBestMoveMinMax(gs,validMoves):
    global nextMove
    nextMove = None 
    findMoveMinMax(gs, validMoves , DEPTH, gs.whiteToMove)
    return nextMove

def findBestMoveNegaMax(game_state, valid_moves):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveNegaMax(game_state, valid_moves, DEPTH, 1 if game_state.whiteToMove else -1)
    return next_move 



def findMoveNegaMax(gs, valid_moves, depth, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(gs)

    max_score = -CHECKMATE
    for move in valid_moves:
        gs.makeMove(move)
        next_moves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, next_moves, depth - 1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undoMove()
    return max_score


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
    return score


def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]