# -------------------------------------------------------- #
#                      GameState class                     #
# -------------------------------------------------------- #

class GameState():
    def __init__(self):
        self.board = [
            ["B_R","B_N","B_B","B_Q","B_K","B_B","B_N","B_R"],
            ["B_P","B_P","B_P","B_P","B_P","B_P","B_P","B_P"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
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
        # pawn promotion
        if Move.PawnPromotion:
            self.board[Move.EndRow][Move.EndCol] = Move.PieceMoved[0] + '_Q'
        
    # ---------------------------------------------------- #
    #                  UndoMove function                   #
    # ---------------------------------------------------- #
    
    def UndoMove(self):
        if len(self.MoveLog) != 0:
            move = self.MoveLog.pop()
            self.board[move.StartRow][move.StartCol] = move.PieceMoved
            self.board[move.EndRow][move.EndCol] = move.PieceCaptured
            self.Turn = 'B' if self.Turn == 'W' else 'W'
       
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
        Direction = -1 if self.Turn == 'W' else 1
        # check movement: UP & DOWN
        CheckCol = PieceCol
        if (self.Turn == 'W' and PieceRow == 6) or (self.Turn == 'B' and PieceRow == 1):
            CheckRow = PieceRow + Direction
            self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)
            CheckRow = CheckRow + Direction
            self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)           
        else:
            CheckRow = PieceRow + Direction
            if CheckRow >= 0 and CheckRow <= 7: 
                self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves) 
        # check capturing piece: DIAGONAL
        CheckCol = PieceCol
        Directions = [-1,1]   
        for i in Directions:
            CheckCol = PieceCol + i
            CheckRow = PieceRow + Direction
            if CheckRow >= 0 and CheckRow <= 7 and CheckCol >= 0 and CheckCol <= 7: 
                TargetPieceColor = self.board[CheckRow][CheckCol][0]
                if (TargetPieceColor != '-') and (PieceColor != TargetPieceColor):
                    AllValidMoves.append(Move((PieceRow,PieceCol),(CheckRow,CheckCol),self.board))
            
    def KingMoves(self,PieceColor,PieceRow,PieceCol,AllValidMoves):
        Directions = [-1,1]   
        # check movement: UP & DOWN
        CheckCol = PieceCol
        for i in Directions:
            CheckRow = PieceRow + i
            if CheckRow >= 0 and CheckRow <= 7: 
                self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)        
        # check movement: LEFT & RIGHT
        CheckRow = PieceRow
        for i in Directions:
            CheckCol = PieceCol + i
            if CheckCol >= 0 and CheckCol <= 7:
                self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)
        # check movement: UP - LEFT & DOWN - RIGHT
        for i in Directions:
            CheckRow = PieceRow + i
            CheckCol = PieceCol + i
            if CheckRow >= 0 and CheckRow <= 7 and CheckCol >= 0 and CheckCol <= 7:
                self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)
        # check movement: UP - RIGHT & DOWN - LEFT
        for i in Directions:                
            CheckRow = PieceRow + i
            CheckCol = PieceCol - i
            if CheckRow >= 0 and CheckRow <= 7 and CheckCol >= 0 and CheckCol <= 7:
                self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)
    
    def CheckSquare(self,PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves):
        BreakFlag = False
        TargetPieceColor = self.board[CheckRow][CheckCol][0]
        if self.board[CheckRow][CheckCol] == '--':
            AllValidMoves.append(Move((PieceRow,PieceCol),(CheckRow,CheckCol),self.board))
        else:
            if PieceColor == TargetPieceColor:
                BreakFlag = True
            else:
                AllValidMoves.append(Move((PieceRow,PieceCol),(CheckRow,CheckCol),self.board))
                BreakFlag = True
        return BreakFlag
            
    def RookMoves(self,PieceColor,PieceRow,PieceCol,AllValidMoves):
        Directions = [-1,1]     
        # check movement: UP & DOWN
        CheckCol = PieceCol
        for i in Directions:
            BreakFlag = False    
            CheckRow = PieceRow + i
            while (CheckRow >= 0 and CheckRow <= 7) and (not BreakFlag): 
                BreakFlag = self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)
                CheckRow = CheckRow + i         
        # check movement: LEFT & RIGHT
        CheckRow = PieceRow
        for i in Directions:
            BreakFlag  = False
            CheckCol = PieceCol + i
            while (CheckCol >= 0 and CheckCol <= 7) and (not BreakFlag):
                BreakFlag = self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)
                CheckCol = CheckCol + i 
                 
    def QueenMoves(self,PieceColor,PieceRow,PieceCol,AllValidMoves):
        self.BishopMoves(PieceColor,PieceRow,PieceCol,AllValidMoves)
        self.RookMoves(PieceColor,PieceRow,PieceCol,AllValidMoves)
        
    def BishopMoves(self,PieceColor,PieceRow,PieceCol,AllValidMoves):
        Directions = [-1,1]   
        # check movement: UP - LEFT & DOWN - RIGHT
        for i in Directions:
            BreakFlag  = False
            CheckRow = PieceRow + i
            CheckCol = PieceCol + i
            while (CheckRow >= 0 and CheckRow <= 7 and CheckCol >= 0 and CheckCol <= 7) and (not BreakFlag):
                BreakFlag = self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)
                CheckRow = CheckRow + i  
                CheckCol = CheckCol + i
        # check movement: UP - RIGHT & DOWN - LEFT
        for i in Directions:  
            BreakFlag  = False              
            CheckRow = PieceRow + i
            CheckCol = PieceCol - i
            while (CheckRow >= 0 and CheckRow <= 7 and CheckCol >= 0 and CheckCol <= 7) and (not BreakFlag):
                BreakFlag = self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)
                CheckRow = CheckRow + i  
                CheckCol = CheckCol - i
    
    def KnightMoves(self,PieceColor,PieceRow,PieceCol,AllValidMoves):
        Directions = [-1,1]         
        # check movement: UP & DOWN
        for j in Directions:
            CheckRow = PieceRow
            CheckCol = PieceCol + 2*j
            for i in Directions:
                CheckRow = PieceRow + i
                if CheckRow >= 0 and CheckRow <= 7 and CheckCol >= 0 and CheckCol <= 7: 
                    self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)        
        # check movement: RIGHT & LEFT
        for j in Directions:
            CheckCol = PieceCol
            CheckRow = PieceRow + 2*j
            for i in Directions:
                CheckCol = PieceCol + i
                if CheckRow >= 0 and CheckRow <= 7 and CheckCol >= 0 and CheckCol <= 7: 
                    self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)   
    
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
        # ----------- calculate move ID ---------- #
        self.PawnPromotion = (self.PieceMoved == 'W_P' and self.EndRow == 0) or \
                             (self.PieceMoved == 'B_P' and self.EndRow == 7)
    # ----------- implement comparison method for this class ---------- #    
    # note that this method is necessary to compare the objects of this class
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False