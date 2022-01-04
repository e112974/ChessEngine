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
        self.Turn              = 'W'
        self.MoveLog           = []
        self.WhiteKingLocation = (7,4)
        self.BlackKingLocation = (0,4)
        self.CheckMate         = False
        self.StaleMate         = False
        self.WhiteCastled      = False
        self.BlackCastled      = False
        # set move functions dictionary
        self.MoveFunctions = {'P': self.PawnMoves,   'R': self.RookMoves,
                              'B': self.BishopMoves, 'N': self.KnightMoves,
                              'K': self.KingMoves,   'Q': self.QueenMoves}
        
    # ---------------------------------------------------- #
    #                  MovePiece function                  #
    # ---------------------------------------------------- #
    
    def MakeMove(self,Move):
        self.board[Move.StartRow][Move.StartCol] = "--"                     # set the start square to empty 
        self.board[Move.EndRow][Move.EndCol] = Move.PieceMoved              # set the final square to the moved piece
        self.MoveLog.append(Move)                                           # add move to the log
        self.Turn = 'B' if self.Turn == 'W' else 'W'  # update turn ('W' or 'B') 
        # update king locations, this is later used within 
        # CheckAttackedSquare function to check if kings are
        # attacked after a move  
        if Move.PieceMoved == 'W_K':
            self.WhiteKingLocation = (Move.EndRow,Move.EndCol)
        elif Move.PieceMoved == 'B_K':
            self.BlackKingLocation = (Move.EndRow,Move.EndCol) 
        # pawn promotion
        if Move.PawnPromotion:
            self.board[Move.EndRow][Move.EndCol] = Move.PieceMoved[0] + '_Q'    # change promoted pawn to queen
        
    # ---------------------------------------------------- #
    #                  UndoMove function                   #
    # ---------------------------------------------------- #
    
    def UndoMove(self):
        if len(self.MoveLog) != 0:                                       # check at least one move is made 
            move = self.MoveLog.pop()                                    # drop last move from log
            self.board[move.StartRow][move.StartCol] = move.PieceMoved   # change start square to moved piece
            self.board[move.EndRow][move.EndCol] = move.PieceCaptured    # change final square to empty or captured piece
            self.Turn = 'B' if self.Turn == 'W' else 'W'                 # update turn
            if move.PieceMoved == 'W_K':
                self.WhiteKingLocation = (move.StartRow,move.StartCol)
            elif move.PieceMoved == 'B_K':
                self.BlackKingLocation = (move.StartRow,move.StartCol)

    # ---------------------------------------------------- #
    #          Calculate list of all possible moves        #
    # ---------------------------------------------------- #
    
    def CalculateAllPossibleMoves(self):
        # initialize variables 
        AllPossibleMoves = []
        # loop over rows and cols on the board 
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] != '--':
                    Piece      = self.board[row][col][2]
                    PieceColor = self.board[row][col][0]
                    # following line executes the function which calculates the moves
                    # for the current piece type (function is retrieved using dictionary
                    # defined above)
                    if PieceColor == self.Turn:
                        self.MoveFunctions[Piece](PieceColor,row,col,AllPossibleMoves)
        return AllPossibleMoves
    
    # ---------------------------------------------------- #
    #          Calculate list of all possible moves        #
    # ---------------------------------------------------- #
    
    def CalculateAllValidMoves(self):
        # initialize variables 
        self.CheckMate   = False
        # get all possible moves 
        AllPossibleMoves = self.CalculateAllPossibleMoves()
        # loop over all possible moves 
        # loop backwards using indices to be able to remove moves from list
        # using remove function 
        for i in range(len(AllPossibleMoves)-1,-1,-1):
            self.MakeMove(AllPossibleMoves[i])                    
            # now calculate all opponent moves
            OpponentMoves = self.CalculateAllPossibleMoves()    
            # get king's location depending on whose turn it is           
            if self.Turn == 'W':
                KingRow = self.BlackKingLocation[0]
                KingCol = self.BlackKingLocation[1]                
            else:
                KingRow = self.WhiteKingLocation[0]
                KingCol = self.WhiteKingLocation[1]
            # try all opponent moves one-by-one
            for move in OpponentMoves:
                # if any opponent move attacks the king, remove it from
                # the list of valid moves
                if move.EndRow == KingRow and move.EndCol == KingCol:
                    AllPossibleMoves.remove(AllPossibleMoves[i])
                    break
            self.UndoMove()
        if len(AllPossibleMoves) == 0:   # either checkmate or stalemate
            self.CheckMate = True           
        return AllPossibleMoves
    
    # ---------------------------------------------------- #
    #      check the target square function                #
    # ---------------------------------------------------- #
    
    def CheckSquareUnderAttack(self,TargetRow,TargetCol):
        self.Turn = 'B' if self.Turn == 'W' else 'W'          
        OpponentMoves = self.CalculateAllPossibleMoves()
        self.Turn = 'B' if self.Turn == 'W' else 'W' 
        for move in OpponentMoves:
            if move.EndRow == TargetRow and move.EndCol == TargetCol:
                return True
        return False
    
    # ---------------------------------------------------- #
    #      check the target square function                #
    # ---------------------------------------------------- #
  
    def CheckSquare(self,PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves):
        # this flag is used to break the loop within the move functions
        BreakFlag = False
        MovingPiece = self.board[PieceRow][PieceCol]
        TargetPieceColor = self.board[CheckRow][CheckCol][0]
        # if target square is empty -> it is a legal move
        if self.board[CheckRow][CheckCol] == '--':
            AllValidMoves.append(Move((PieceRow,PieceCol),(CheckRow,CheckCol),self.board))
        else:
            # if target square is not empty, then the move is only legal if target piece is 
            # opposite color
            if PieceColor != TargetPieceColor:
                AllValidMoves.append(Move((PieceRow,PieceCol),(CheckRow,CheckCol),self.board))
            # set flag to true to finish the loop in move function    
            BreakFlag = True
        return BreakFlag
    
    # ---------------------------------------------------- #
    #      Calculate Moves for each piece                  #
    # ---------------------------------------------------- #
    
    def PawnMoves(self,PieceColor,PieceRow,PieceCol,AllValidMoves):
        # moving direction is up (i.e. -1, since rows decrease as going up) for 'W'
        # and down for 'B'
        Direction = -1 if self.Turn == 'W' else 1 
        CheckCol = PieceCol     
        # if first move of pawn, then they can jump double, this is assigned
        # by calling the function twice and incrementing the row in between the calls
        if (self.Turn == 'W' and PieceRow == 6) or (self.Turn == 'B' and PieceRow == 1):
            CheckRow = PieceRow + Direction
            TargetSquare = self.board[CheckRow][CheckCol]
            if (TargetSquare == '--'):
                self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)
            CheckRow = CheckRow + Direction
            TargetSquare = self.board[CheckRow][CheckCol]
            if (TargetSquare == '--'):
                self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves)           
        else:
            CheckRow = PieceRow + Direction
            TargetSquare = self.board[CheckRow][CheckCol]
            if CheckRow >= 0 and CheckRow <= 7 and (TargetSquare == '--'): 
                self.CheckSquare(PieceColor,PieceRow,PieceCol,CheckRow,CheckCol,AllValidMoves) 
        # check capturing piece: DIAGONAL
        CheckCol = PieceCol
        Directions = [-1,1]   
        for i in Directions:
            CheckCol = PieceCol + i
            CheckRow = PieceRow + Direction
            # check that target square is within bounds
            if CheckRow >= 0 and CheckRow <= 7 and CheckCol >= 0 and CheckCol <= 7: 
                # check color of captured piece
                TargetPieceColor = self.board[CheckRow][CheckCol][0]
                # if target square is not empty & piece is opposite color
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
        # get initial position 
        self.StartRow      = StartSq[0]
        self.StartCol      = StartSq[1]
        #  get final position 
        self.EndRow        = EndSq[0]
        self.EndCol        = EndSq[1]
        # get moved & captured info 
        self.PieceMoved        = board[self.StartRow][self.StartCol]
        self.PieceCaptured     = board[self.EndRow][self.EndCol]
        self.PieceCapturedFlag = self.PieceCaptured != '--'
        # calculate move ID 
        self.moveID = self.StartRow * 1000 + self.StartCol * 100 + self.EndRow * 10 + self.EndCol
        #  calculate move ID 
        self.PawnPromotion = (self.PieceMoved == 'W_P' and self.EndRow == 0) or \
                             (self.PieceMoved == 'B_P' and self.EndRow == 7)
        self.CastleMove = False
    # implement comparison method for this class    
    # note that this method is necessary to compare the objects of this class
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def ChessNotation(self):
        # castle move
        if self.CastleMove:
            return 'O-O' if self.endCol == 6 else 'O-O-O'
        EndSquare = self.getRankFile(self.EndRow,self.EndCol)
        # pawn moves
        if self.PieceMoved[2] == 'P':
            if self.PieceCapturedFlag:
                return self.colsToFiles[self.StartCol] + 'x' + EndSquare    
            else: 
                return EndSquare
        # TODO: pawn promotions
        # TODO: two pieces move same square
        # TODO: specify chess moves
        
        # piece moves
        moveString = self.PieceMoved[2]
        if self.PieceCapturedFlag:
            moveString += 'x'
        return moveString + EndSquare

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    