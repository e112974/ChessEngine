import random
from typing import Counter

pieceScore = {'K':0,'Q':10,'R':5,'B':3,'N':3,'P':1}
CheckMate = 1000
StaleMate = 0
MaxDepth = 2

def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]


# minmax without recursion
""" def findBestMoveNoRecursion(gs,validMoves):
    turnMultiplier = 1 if gs.WhiteToMove else -1
    opponentMinMaxScore = CheckMate   # we are trying to minimize our opponent's best move
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.staleMate:
            opponentMaxScore = StaleMate
        elif gs.checkMate:
            opponentMaxScore = -CheckMate 
        else:
            opponentMaxScore = -CheckMate
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = CheckMate
                elif gs.staleMate:
                    score = StaleMate
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove """


def findBestMove(gs,validMoves):
    global nextMove,counter
    nextMove = None
    counter = 0
    #findMoveMinMax(gs,validMoves,MaxDepth,gs.WhiteToMove)
    #findMoveNegaMax(gs,validMoves,MaxDepth,1 if gs.WhiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs,validMoves,MaxDepth,-CheckMate,CheckMate,1 if gs.WhiteToMove else -1)
    print(counter)
    return nextMove

def findMoveMinMax(gs,validMoves,Depth,whiteToMove):
    global nextMove
    if Depth == 0:
        return scoreMaterial(gs.board)
    if whiteToMove:
        maxScore = -CheckMate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs,nextMoves,Depth-1,False)
            if score > maxScore:
                maxScore = score
                if Depth == MaxDepth:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CheckMate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs,nextMoves,Depth-1,False)
            if score < minScore:
                minScore = score
                if Depth == MaxDepth:
                    nextMove = move
            gs.undoMove()
        return minScore

def findMoveNegaMax(gs,validMoves,Depth,turnMultiplier):
    global nextMove,counter
    counter += 1
    if Depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CheckMate
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs,nextMoves,Depth-1,-turnMultiplier)
        if score > maxScore:
            maxScore = score
            if Depth == MaxDepth:
                nextMove = move
        gs.undoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(gs,validMoves,Depth,alpha,beta,turnMultiplier):
    global nextMove, counter
    counter += 1
    if Depth == 0:
        return turnMultiplier * scoreBoard(gs)
    # move ordering - implement later
    maxScore = -CheckMate
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs,nextMoves,Depth-1,-beta,-alpha,-turnMultiplier)
        if score > maxScore:
            maxScore = score
            if Depth == MaxDepth:
                nextMove = move
        gs.undoMove()
        # implementation of alpha & beta
        if maxScore > alpha: #pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

# a positive score is good white, a negative score is good for black
def scoreBoard(gs):
    if gs.checkMate:
        if gs.WhiteToMove:
            return -CheckMate   # black wins
        else:
            return CheckMate    # white wins
    elif gs.staleMate:
        return StaleMate
     
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'W':
                score += pieceScore[square[2]]
            elif square[0] == 'B':
                score -= pieceScore[square[2]]
    return score    

# score the board based on material
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'W':
                score += pieceScore[square[2]]
            elif square[0] == 'B':
                score -= pieceScore[square[2]]
    return score
