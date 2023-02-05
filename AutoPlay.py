# -------------------- import modules -------------------- #
from ChessEngine import *

# ---------------------------------------------------- #
#                  Points for Each Piece               #
# ---------------------------------------------------- #

PiecePoints = {'K':0,'Q':8,'R':5,'B':3,'N':3,'P':1}

# ---------------------------------------------------- #
#          Points for PIECES considering POSITION      #
# ---------------------------------------------------- #

KnightPoints = [[1,1,1,1,1,1,1,1],
                [1,2,2,2,2,2,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,2,2,2,2,2,1],
                [1,1,1,1,1,1,1,1]]

BishopPoints = [[4,3,2,1,1,2,3,4],
                [3,4,4,2,2,3,4,3],
                [2,3,4,3,3,4,3,2],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [2,3,4,3,3,4,3,2],
                [3,4,3,2,2,3,4,3],
                [4,3,2,1,1,2,3,4]]

QueenPoints =  [[1,1,1,3,1,1,1,1],
                [1,2,3,3,3,1,1,1],
                [1,4,3,3,3,4,2,1],
                [1,2,3,3,3,2,2,1],
                [1,2,3,3,3,2,2,1],
                [1,4,3,3,3,4,2,1],
                [1,2,2,3,3,1,1,1],
                [1,1,1,3,1,1,1,1]]

RookPoints =   [[4,3,4,4,4,4,3,4],
                [4,4,4,4,4,4,4,4],
                [1,1,2,3,3,2,1,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,1,2,2,2,2,1,1],
                [4,4,4,4,4,4,4,4],
                [4,3,4,4,4,4,3,4]]

WhitePawnPoints = [[8,8,8,8,8,8,8,8],
                   [8,8,8,8,8,8,8,8],
                   [5,6,6,7,7,6,6,5],
                   [2,3,3,5,5,3,3,2],
                   [1,2,3,4,4,3,2,1],
                   [1,1,2,3,3,2,1,1],
                   [1,1,1,0,0,1,1,1],
                   [0,0,0,0,0,0,0,0]]

BlackPawnPoints = [ [0,0,0,0,0,0,0,0],
                    [1,1,1,0,0,1,1,1],
                    [1,1,2,3,3,2,1,1],
                    [1,2,3,4,4,3,2,1],
                    [2,3,3,5,5,3,3,2],
                    [5,6,6,7,7,6,6,5],
                    [8,8,8,8,8,8,8,8],
                    [8,8,8,8,8,8,8,8]]

# ---------------------------------------------------- #
#          Dictinoary to assign position points        #
# ---------------------------------------------------- #

PiecePositionPoints = {'N': KnightPoints,'R': RookPoints, 'Q': QueenPoints, 'B': BishopPoints,
                       'B_P': BlackPawnPoints, 'W_P': WhitePawnPoints}

# ---------------------------------------------------- #
#          Initialize Checkmate & Stalemate scores     #
# ---------------------------------------------------- #

CheckMate = 1000
StaleMate = 0.0

# ---------------------------------------------------- #
#          Set Depth of Auto Play                      #
# ---------------------------------------------------- #

Depth = 5

# ---------------------------------------------------- #
#          CalculateBestMove Function                  #
# ---------------------------------------------------- #

def CalculateBestMove(GameState):
    # calculate all valid moves
    AllValidMoves = GameState.CalculateAllValidMoves()
    # set flag
    ActualMoveFlag = False
    # initialize best score
    BestScore = -CheckMate if GameState.Turn == 'W' else CheckMate
    # try every valid move
    for move in AllValidMoves:
        # try the move
        GameState.MakeMove(move,ActualMoveFlag)  
        # calculate all counter-valid moves
        AllValidMoves = GameState.CalculateAllValidMoves()
        # initialize best counter score
        BestCounterScore = -CheckMate if GameState.Turn == 'W' else CheckMate
        # try every valid counter move
        for CounterMove in AllValidMoves:
            # try the move
            GameState.MakeMove(CounterMove,ActualMoveFlag)  
            # calculate board score
            CounterScore = ScoreBoard(GameState)
            # if a better move is found than the current best one, 
            # then replace the best move
            if (GameState.Turn == 'W' and CounterScore < BestCounterScore) \
                or (GameState.Turn == 'B' and CounterScore > BestCounterScore):
                BestCounterScore = CounterScore
                BestCounterMove  = CounterMove
            # unde move
            GameState.UndoMove()    
        # tmake best counter move
        GameState.MakeMove(BestCounterMove,ActualMoveFlag)      
        # calculate board score
        Score = ScoreBoard(GameState)
        # if a better move is found than the current best one, 
        # then replace the best move
        if (GameState.Turn == 'W' and Score > BestScore) \
            or (GameState.Turn == 'B' and Score < BestScore):
            BestScore = Score
            BestMove = move
        # unde move    
        GameState.UndoMove()    
        GameState.UndoMove()   
    # return Best Move
    return BestMove

# ---------------------------------------------------- #
#                  ScoreBoard function                 #
# ---------------------------------------------------- #
# 
# Score is calculated based on the position of the piece and/or
# the value of capture piece
# Note: A POSITIVE score is good for WHITE and a NEGATIVE score is good for BLACK
def ScoreBoard(GameState):
    # check if checkmate or stalemate is reached
    if GameState.CheckMate:
        if GameState.Turn == 'W':
            return -CheckMate   # black wins
        else:
            return CheckMate    # white wins
    elif GameState.StaleMate:
        return StaleMate
    # initialize score 
    Score = 0
    # loop over every ROW on board
    for row in range(len(GameState.board)):
        # loop over every COL on board
        for col in range(len(GameState.board[row])):
            # Check Square
            Square = GameState.board[row][col]
            # proceed only if square is not empty
            if Square != '--':
                # calculate position score
                PiecePositionScore = 0
                # only king has no  position score
                if Square[2] != 'K':
                    # for pawns we need to check the color as well
                    if Square[2] == 'P':
                        PiecePositionScore = PiecePositionPoints[Square][row][col]
                    else:
                        PiecePositionScore = PiecePositionPoints[Square[2]][row][col]
                # calculate the total score 
                # total score = position score + value of any captured piece
                if Square[0] == 'W':
                    Score += PiecePoints[Square[2]] + PiecePositionScore * 0.1
                elif Square[0] == 'B':
                    Score -= PiecePoints[Square[2]] + PiecePositionScore * 0.1
    return Score   