import random


pieceScore = {'K':0,'Q':10,'R':5,'B':3,'N':3,'P':1}
CheckMate = 1000
StaleMate = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]


def findBestMove(gs,validMoves):
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
    return bestPlayerMove

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
