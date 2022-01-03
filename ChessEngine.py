# -------------------------------------------------------- #
#                      GameState class                     #
# -------------------------------------------------------- #

class GameState():
    def __init__(self):
        self.board = [
            ["B_R","B_N","B_B","B_Q","B_K","B_B","B_N","B_R"],
            ["B_P","B_P","B_P","B_P","B_P","B_P","B_P","B_P"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "B_Q", "--", "--"],
            ["--", "--", "W_Q", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["W_P","W_P","W_P","W_P","W_P","W_P","W_P","W_P"],
            ["W_R","W_N","W_B","W_Q","W_K","W_B","W_N","W_R"],
        ]
        # set properties
        self.Turn         = 'W'
        self.MoveLog      = []
        self.CheckMate    = False
        self.StaleMate    = False
        self.WhiteCastled = False
        self.BlackCastled = False
        self.KingInCheck  = False
        # set move functions dictionary
        self.MoveFunctions = {'P': self.PawnMoves,   'R': self.RookMoves,
                              'B': self.BishopMoves, 'N': self.KnightMoves,
                              'K': self.KingMoves,   'Q': self.QueenMoves}
        
    # ---------------------------------------------------- #
    #                  MovePiece function                  #
    # ---------------------------------------------------- #
    
    def MakeMove(self,Move):
        self.board[Move.StartRow][Move.StartCol] = "--"
        self.board[Move.EndRow][Move.EndCol] = Move.PieceMoved
        self.MoveLog.append(Move)
        self.Turn = 'B' if self.Turn == 'W' else 'W'
        
    # ---------------------------------------------------- #
    #                  UndoMove function                   #
    # ---------------------------------------------------- #
    
    def UndoMove(self):
        pass
       
    # ---------------------------------------------------- #
    #          Update list of valid moves function         #
    # ---------------------------------------------------- #
    
    def CalculateAllMoves(self):
        # --------------- initialize array --------------- #
        AllValidMoves = []
        # ----- loop over rows and cols on the board ----- #
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] != '--':
                    Piece      = self.board[row][col][2]
                    PieceColor = self.board[row][col][0]
                    if PieceColor == self.Turn:
                        self.MoveFunctions[Piece](PieceColor,row,col,AllValidMoves)
        return AllValidMoves
    
    # ---------------------------------------------------- #
    #      Calculate Moves for each piece function         #
    # ---------------------------------------------------- #
    
    def PawnMoves(self,PieceColor,PieceRow,PieceCol,AllValidMoves):
        pass
    
    def KingMoves(self,PieceColor,PieceRow,PieceCol,AllValidMoves):
        pass
    
    def RookMoves(self,PieceColor,PieceRow,PieceCol,AllValidMoves):
        # -----------------------        
        # Moves for ROOK
        # -----------------------
        Directions = [-1,1]         
        # check movement: UP & DOWN
        for i in Directions:
            row = PieceRow + i
            while row >= 0 and row <= 7: 
                if self.board[row][PieceCol] == '--':
                    AllValidMoves.append(Move((PieceRow,PieceCol),(row,PieceCol),self.board))
                else:
                    if PieceColor == self.Turn:
                        break
                    else:
                        AllValidMoves.append(Move((PieceRow,PieceCol),(row,PieceCol),self.board))
                        break
                row = row + i  
        # check movement: LEFT & RIGHT
        for i in Directions:
            col = PieceCol + i
            while col >= 0 and col <= 7:
                if self.board[PieceRow][col] == '--':
                    AllValidMoves.append(Move((PieceRow,PieceCol),(PieceRow,col),self.board))
                else:
                    if PieceColor == self.Turn:
                        break
                    else:
                        AllValidMoves.append(Move((PieceRow,PieceCol),(PieceRow,col),self.board))
                        break
                col = col + i 
                 
    def QueenMoves(self,PieceColor,PieceRow,PieceCol,AllValidMoves):
        self.BishopMoves(PieceColor,PieceRow,PieceCol,AllValidMoves)
        self.RookMoves(PieceColor,PieceRow,PieceCol,AllValidMoves)
        
    def BishopMoves(self,PieceColor,PieceRow,PieceCol,AllValidMoves):
        # -----------------------        
        # Moves for BISHOP
        # -----------------------
        Directions = [-1,1]   
        # check movement: UP - LEFT & DOWN - RIGHT
        for i in Directions:
            row = PieceRow + i
            col = PieceCol + i
            while row >= 0 and row <= 7 and col >= 0 and col <= 7:
                if self.board[row][col] =='--':
                    AllValidMoves.append(Move((PieceRow,PieceCol),(row,col),self.board))
                else:
                    if PieceColor == self.Turn:
                        break
                    else:
                        AllValidMoves.append(Move((PieceRow,PieceCol),(row,col),self.board))
                        break
                row = row + i  
                col = col + i
        # check movement: UP - RIGHT & DOWN - LEFT
        for i in Directions:                
            row = PieceRow + i
            col = PieceCol - i
            while row >= 0 and row <= 7 and col >= 0 and col <= 7:
                if self.board[row][col] =='--':
                    AllValidMoves.append(Move((PieceRow,PieceCol),(row,col),self.board))
                else:
                    if PieceColor == self.Turn:
                        break
                    else:
                        AllValidMoves.append(Move((PieceRow,PieceCol),(row,col),self.board))
                        break
                row = row + i  
                col = col - i
    
    def KnightMoves(self,PieceColor,PieceRow,PieceCol,AllValidMoves):
        pass  
    
class Move():

    ranksToRows = {'1':7, '2':6, '3':5, '4':4,
                   '5':3, '6':2, '7':1, '8':0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}   # reverse the pairs
    filesToCols = {'a':0, 'b':1, 'c':2, 'd':3,
                   'e':4, 'f':5, 'g':6, 'h':7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, StartSq, EndSq, board):
        # -------------- get initial position ------------ #
        self.StartRow      = StartSq[0]
        self.StartCol      = StartSq[1]
        # -------------- get final position -------------- #
        self.EndRow        = EndSq[0]
        self.EndCol        = EndSq[1]
        # ----------- get moved & captured info ---------- #
        self.PieceMoved    = board[self.StartRow][self.StartCol]
        self.PieceCaptured = board[self.EndRow][self.EndCol]
        # ----------- calculate move ID ---------- #
        self.moveID = self.StartRow * 1000 + self.StartCol * 100 + self.EndRow * 10 + self.EndCol

    # ----------- implement comparison method for this class ---------- #    
    # note that this method is necessary to compare the objects of this class
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False