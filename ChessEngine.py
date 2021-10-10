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
        self.moveFunctions = {'P': self.getPawnMoves,   'R': self.getRookMoves,
                              'B': self.getBishopMoves, 'N': self.getKnightMoves,
                              'K': self.getKingMoves,   'Q': self.getQueenMoves}
        self.WhiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight = CastleRights(True,True,True,True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks,
                                             self.currentCastlingRight.wqs,
                                             self.currentCastlingRight.bks,
                                             self.currentCastlingRight.bqs)]

    def makeMove(self,move):
        
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.WhiteToMove = not self.WhiteToMove
        if move.pieceMoved == 'W_K':
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMoved == 'B_K':
            self.blackKingLocation = (move.endRow,move.endCol)
            
        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + '_Q'
            
        # enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'
            
        # update enpassantPossible variable
        if move.pieceMoved[2] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2,move.startCol)
        else:
            self.enpassantPossible = ()

        # castle move
        if move.isCastleMove:
            if move.endCol + 1 <= 7 and move.endCol - 2 >= 0:
                if move.endCol - move.startCol == 2:  # king side castle
                    self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'
                else: # queen side
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                    self.board[move.endRow][move.endCol-2] = '--'
        
        self.enpassantPossibleLog.append(self.enpassantPossible)
        
        # update Castling Rights - whenever a rook or a king moves
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks,
                                             self.currentCastlingRight.wqs,
                                             self.currentCastlingRight.bks,
                                             self.currentCastlingRight.bqs))
        
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.WhiteToMove = not self.WhiteToMove
            if move.pieceMoved == 'W_K':
                self.whiteKingLocation = (move.startRow,move.startCol)
            elif move.pieceMoved == 'B_K':
                self.blackKingLocation = (move.startRow,move.startCol)
            # undo enpassantMove
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                
        self.enpassantPossibleLog.pop()
        self.enpassantPossible = self.enpassantPossibleLog[-1]
        
        # undo castling rights
        self.castleRightsLog.pop()  # get rid of castling rights of the move we are undoing
        newRights = self.castleRightsLog[-1]
        self.currentCastlingRight = CastleRights(newRights.wks,newRights.bks,newRights.wqs,newRights.bqs)    
        # undo castle move
        if move.isCastleMove:
            if move.endCol + 1 <= 7 and move.endCol - 2 >= 0:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'
                
        self.checkMate = False
        self.staleMate = False
                         
    def updateCastleRights(self,move):
        if move.pieceMoved == 'W_K':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'B_K':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'W_R':
            if move.startRow == 7:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'B_R':
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastlingRight.bks = False      
                    
        # if rock is captured
        if move.pieceCaptured == 'W_R':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'B_R':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False
                              
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks, \
                                        self.currentCastlingRight.bks,self.currentCastlingRight.bqs)
        # 1. first generate all the moves
        moves = self.getAllPossibleMoves()
        if self.WhiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0],self.whiteKingLocation[1],moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0],self.blackKingLocation[1],moves)        
        # 2. make the move
        for i in range(len(moves)-1,-1,-1):  # when removing from list, go backwards in indices
            self.makeMove(moves[i])
        # 3. make the opponents move
            # we need to switch turns here makemove function will switch turns anyway
            self.WhiteToMove = not self.WhiteToMove
            if self.inCheck(): # 4. for each opponent move, check if king is attacked
                moves.remove(moves[i]) # if the king is attacked, not a valid move
            self.WhiteToMove = not self.WhiteToMove
            self.undoMove()
        if len(moves) == 0:   # either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else: 
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
            
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves

    def inCheck(self):
        if self.WhiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])

    def squareUnderAttack(self,r,c):
        self.WhiteToMove = not self.WhiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.WhiteToMove = not self.WhiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'W' and self.WhiteToMove) or (turn == 'B' and not self.WhiteToMove):
                    piece = self.board[r][c][2]
                    self.moveFunctions[piece](r,c,moves)
        return moves

    def getPawnMoves(self,r,c,moves):
        # -----------------------        
        # Moves for WHITE PAWNS
        # -----------------------
        if self.WhiteToMove:
            if self.board[r-1][c] == '--':
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] =='--':
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'B':
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c-1),self.board,isEnpassantMove = True))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'B':
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c+1),self.board,isEnpassantMove = True))
        # -----------------------        
        # Moves for BLACK PAWNS
        # -----------------------
        else:
            if self.board[r+1][c] == '--':
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] =='--':
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'W':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c-1),self.board,isEnpassantMove = True))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'W':
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                elif (r+1,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c+1),self.board,isEnpassantMove = True))
                    
    def getKnightMoves(self,r,c,moves):
        
        # -----------------------        
        # Moves for WHITE KNIGHT
        # -----------------------
        if self.WhiteToMove:
            # check movement: 2UP 
            row = r - 2
            if row >= 0:
                # check movement: 1LEFT
                col = c - 1 
                if col >= 0:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'B':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 1RIGHT
                col = c + 1 
                if col <= 7:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'B':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 2DOWN 
            row = r + 2
            if row <= 7:
                # check movement: 1LEFT
                col = c - 1 
                if col >= 0:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'B':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 1RIGHT
                col = c + 1 
                if col <= 7:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'B':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 2LEFT
            col = c - 2
            if col >= 0:
                # check movement: 1UP
                row = r - 1 
                if row >= 0:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'B':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 1DOWN
                row = r + 1 
                if row <= 7:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'B':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 2RIGHT
            col = c + 2
            if col <= 7:
                # check movement: 1UP
                row = r - 1 
                if row >= 0:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'B':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 1DOWN
                row = r + 1 
                if row <= 7:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'B':
                        moves.append(Move((r,c),(row,col),self.board))
       # -----------------------        
        # Moves for BLACK KNIGHT
        # -----------------------
        elif not self.WhiteToMove:
            # check movement: 2UP 
            row = r - 2
            if row >= 0:
                # check movement: 1LEFT
                col = c - 1 
                if col >= 0:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'W':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 1RIGHT
                col = c + 1 
                if col <= 7:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'W':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 2DOWN 
            row = r + 2
            if row <= 7:
                # check movement: 1LEFT
                col = c - 1 
                if col >= 0:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'W':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 1RIGHT
                col = c + 1 
                if col <= 7:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'W':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 2LEFT
            col = c - 2
            if col >= 0:
                # check movement: 1UP
                row = r - 1 
                if row >= 0:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'W':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 1DOWN
                row = r + 1 
                if row <= 7:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'W':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 2RIGHT
            col = c + 2
            if col <= 7:
                # check movement: 1UP
                row = r - 1 
                if row >= 0:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'W':
                        moves.append(Move((r,c),(row,col),self.board))
            # check movement: 1DOWN
                row = r + 1 
                if row <= 7:
                    if self.board[row][col] =='--':
                        moves.append(Move((r,c),(row,col),self.board))
                    elif self.board[row][col][0] == 'W':
                        moves.append(Move((r,c),(row,col),self.board))

    def getBishopMoves(self,r,c,moves):
        # -----------------------        
        # Moves for WHITE BISHOP
        # -----------------------
        if self.WhiteToMove:
            # check movement: UP & LEFT
            row = r - 1
            col = c - 1
            while row >= 0 and col >= 0:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'W':
                    break
                elif self.board[row][col][0] == 'B':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                row -= 1  
                col -= 1
            # check movement: UP & RIGHT
            row = r - 1
            col = c + 1
            while row >= 0 and col <= 7:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'W':
                    break
                elif self.board[row][col][0] == 'B':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                row -= 1  
                col += 1
            # check movement: DOWN & RIGHT
            row = r + 1
            col = c + 1
            while row <= 7 and col <= 7:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'W':
                    break
                elif self.board[row][col][0] == 'B':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                row += 1  
                col += 1
            # check movement: DOWN & LEFT
            row = r + 1
            col = c - 1
            while row <= 7 and col >= 0:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'W':
                    break
                elif self.board[row][col][0] == 'B':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                row += 1  
                col -= 1
        # -----------------------        
        # Moves for BLACK BISHOP
        # -----------------------
        else:
            # check movement: UP & LEFT
            row = r - 1
            col = c - 1
            while row >= 0 and col >= 0:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'B':
                    break
                elif self.board[row][col][0] == 'W':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                row -= 1  
                col -= 1
            # check movement: UP & RIGHT
            row = r - 1
            col = c + 1
            while row >= 0 and col <= 7:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'B':
                    break
                elif self.board[row][col][0] == 'W':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                row -= 1  
                col += 1
            # check movement: DOWN & RIGHT
            row = r + 1
            col = c + 1
            while row <= 7 and col <= 7:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'B':
                    break
                elif self.board[row][col][0] == 'W':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                row += 1  
                col += 1
            # check movement: DOWN & LEFT
            row = r + 1
            col = c - 1
            while row <= 7 and col >= 0:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'B':
                    break
                elif self.board[row][col][0] == 'W':
                    moves.append(Move((r,c),(row,col),self.board))
                    break
                row += 1  
                col -= 1

    def getRookMoves(self,r,c,moves):
        # -----------------------        
        # Moves for WHITE ROOK
        # -----------------------
        if self.WhiteToMove:
            # check movement: UP
            row = r - 1
            while row >= 0: 
                if self.board[row][c] =='--':
                    moves.append(Move((r,c),(row,c),self.board))
                elif self.board[row][c][0] == 'W':
                    break
                elif self.board[row][c][0] == 'B':
                    moves.append(Move((r,c),(row,c),self.board))
                    break
                row -= 1  
             # check movement: DOWN
            row = r + 1
            while row <= 7: 
                if self.board[row][c] =='--':
                    moves.append(Move((r,c),(row,c),self.board))
                elif self.board[row][c][0] == 'W':
                    break
                elif self.board[row][c][0] == 'B':
                    moves.append(Move((r,c),(row,c),self.board))
                    break
                row += 1  
             # check movement: LEFT
            col = c - 1
            while col >= 0:  
                if self.board[r][col] =='--':
                    moves.append(Move((r,c),(r,col),self.board))
                elif self.board[r][col][0] == 'W':
                    break
                elif self.board[r][col][0] == 'B':
                    moves.append(Move((r,c),(r,col),self.board))
                    break
                col -= 1
             # check movement: RIGHT
            col = c + 1
            while col <= 7:
                if self.board[r][col] =='--':
                    moves.append(Move((r,c),(r,col),self.board))
                elif self.board[r][col][0] == 'W':
                    break
                elif self.board[r][col][0] == 'B':
                    moves.append(Move((r,c),(r,col),self.board))
                    break
                col += 1 
        # -----------------------        
        # Moves for BLACK ROOK
        # -----------------------
        else:                
            # check movement: UP
            row = r - 1
            while row >= 0: 
                if self.board[row][c] =='--':
                    moves.append(Move((r,c),(row,c),self.board))
                elif self.board[row][c][0] == 'B':
                    break
                elif self.board[row][c][0] == 'W':
                    moves.append(Move((r,c),(row,c),self.board))
                    break
                row -= 1  
             # check movement: DOWN
            row = r + 1
            while row <= 7: 
                if self.board[row][c] =='--':
                    moves.append(Move((r,c),(row,c),self.board))
                elif self.board[row][c][0] == 'B':
                    break
                elif self.board[row][c][0] == 'W':
                    moves.append(Move((r,c),(row,c),self.board))
                    break
                row += 1  
             # check movement: LEFT
            col = c - 1
            while col >= 0:  
                if self.board[r][col] =='--':
                    moves.append(Move((r,c),(r,col),self.board))
                elif self.board[r][col][0] == 'B':
                    break
                elif self.board[r][col][0] == 'W':
                    moves.append(Move((r,c),(r,col),self.board))
                    break
                col -= 1
             # check movement: RIGHT
            col = c + 1
            while col <= 7:
                if self.board[r][col] =='--':
                    moves.append(Move((r,c),(r,col),self.board))
                elif self.board[r][col][0] == 'B':
                    break
                elif self.board[r][col][0] == 'W':
                    moves.append(Move((r,c),(r,col),self.board))
                    break
                col += 1 

    def getKingMoves(self,r,c,moves):
        # -----------------------        
        # Moves for WHITE KING
        # -----------------------
        if self.WhiteToMove:
            # check movement: UP
            row = r - 1
            if row >= 0: 
                if self.board[row][c] =='--':
                    moves.append(Move((r,c),(row,c),self.board))
                elif self.board[row][c][0] == 'B':
                    moves.append(Move((r,c),(row,c),self.board))
             # check movement: DOWN
            row = r + 1
            if row <= 7: 
                if self.board[row][c] =='--':
                    moves.append(Move((r,c),(row,c),self.board))
                elif self.board[row][c][0] == 'B':
                    moves.append(Move((r,c),(row,c),self.board))
             # check movement: LEFT
            col = c - 1
            if col >= 0:  
                if self.board[r][col] =='--':
                    moves.append(Move((r,c),(r,col),self.board))
                elif self.board[r][col][0] == 'B':
                    moves.append(Move((r,c),(r,col),self.board))
             # check movement: RIGHT
            col = c + 1
            if col <= 7:
                if self.board[r][col] =='--':
                    moves.append(Move((r,c),(r,col),self.board))
                elif self.board[r][col][0] == 'B':
                    moves.append(Move((r,c),(r,col),self.board))
            # check movement: UP & LEFT
            row = r - 1
            col = c - 1
            if row >= 0 and col >= 0:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'B':
                    moves.append(Move((r,c),(row,col),self.board))
            # check movement: UP & RIGHT
            row = r - 1
            col = c + 1
            if row >= 0 and col <= 7:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'B':
                    moves.append(Move((r,c),(row,col),self.board))
            # check movement: DOWN & RIGHT
            row = r + 1
            col = c + 1
            if row <= 7 and col <= 7:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'B':
                    moves.append(Move((r,c),(row,col),self.board))
            # check movement: DOWN & LEFT
            row = r + 1
            col = c - 1
            if row <= 7 and col >= 0:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'B':
                    moves.append(Move((r,c),(row,col),self.board))              
        # -----------------------        
        # Moves for BLACK KING
        # -----------------------
        else:
            # check movement: UP
            row = r - 1
            if row >= 0: 
                if self.board[row][c] =='--':
                    moves.append(Move((r,c),(row,c),self.board))
                elif self.board[row][c][0] == 'W':
                    moves.append(Move((r,c),(row,c),self.board))
             # check movement: DOWN
            row = r + 1
            if row <= 7: 
                if self.board[row][c] =='--':
                    moves.append(Move((r,c),(row,c),self.board))
                elif self.board[row][c][0] == 'W':
                    moves.append(Move((r,c),(row,c),self.board))
             # check movement: LEFT
            col = c - 1
            if col >= 0:  
                if self.board[r][col] =='--':
                    moves.append(Move((r,c),(r,col),self.board))
                elif self.board[r][col][0] == 'W':
                    moves.append(Move((r,c),(r,col),self.board))
             # check movement: RIGHT
            col = c + 1
            if col <= 7:
                if self.board[r][col] =='--':
                    moves.append(Move((r,c),(r,col),self.board))
                elif self.board[r][col][0] == 'W':
                    moves.append(Move((r,c),(r,col),self.board))
            # check movement: UP & LEFT
            row = r - 1
            col = c - 1
            if row >= 0 and col >= 0:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'W':
                    moves.append(Move((r,c),(row,col),self.board))
            # check movement: UP & RIGHT
            row = r - 1
            col = c + 1
            if row >= 0 and col <= 7:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'W':
                    moves.append(Move((r,c),(row,col),self.board))
            # check movement: DOWN & RIGHT
            row = r + 1
            col = c + 1
            if row <= 7 and col <= 7:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'W':
                    moves.append(Move((r,c),(row,col),self.board))
            # check movement: DOWN & LEFT
            row = r + 1
            col = c - 1
            if row <= 7 and col >= 0:
                if self.board[row][col] =='--':
                    moves.append(Move((r,c),(row,col),self.board))
                elif self.board[row][col][0] == 'W':
                    moves.append(Move((r,c),(row,col),self.board))  

    def getCastleMoves(self,r,c,moves):
        if self.squareUnderAttack(r,c):
            return
        if (self.WhiteToMove and self.currentCastlingRight.wks) or \
           (not self.WhiteToMove and self.currentCastlingRight.bks):
               self.getKingSideCastleMoves(r,c,moves)
        if (self.WhiteToMove and self.currentCastlingRight.wqs) or \
           (not self.WhiteToMove and self.currentCastlingRight.bqs):
               self.getQueenSideCastleMoves(r,c,moves)
                 
    def getKingSideCastleMoves(self,r,c,moves):
        if c+2 <= 7:
            if self.board[r][c+1] == '--' and self.board[r][c+2]:
                if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
                    moves.append(Move((r,c),(r,c+2),self.board,isCastleMove=True))

    def getQueenSideCastleMoves(self,r,c,moves):
        if self.board[r][c-1] == '--' and \
            self.board[r][c-2] == '--' and \
            self.board[r][c-3] == '--':
                if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2):
                    moves.append(Move((r,c),(r,c-2),self.board,isCastleMove=True))

    def getQueenMoves(self,r,c,moves):
        
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)


class CastleRights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
        
class Move():

    ranksToRows = {'1':7, '2':6, '3':5, '4':4,
                   '5':3, '6':2, '7':1, '8':0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}   # reverse the pairs
    filesToCols = {'a':0, 'b':1, 'c':2, 'd':3,
                   'e':4, 'f':5, 'g':6, 'h':7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow   = endSq[0]
        self.endCol   = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'W_P' and self.endRow == 0) or (self.pieceMoved == 'B_P' and self.endRow == 7)
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'W_P' if self.pieceMoved == 'B_P' else 'B_P'
        self.isCaptured = self.pieceCaptured != '--'
        self.isCastleMove = isCastleMove
        
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
    # overriding str() function
    def __str__(self):
        # castle move
        if self.isCastleMove:
            return 'O-O' if self.endCol == 6 else 'O-O-O'
        
        endSquare = self.getRankFile(self.endRow,self.endCol)
        # pawn moves
        if self.pieceMoved[2] == 'P':
            if self.isCaptured:
                return self.colsToFiles[self.startCol] + 'x' + endSquare    
            else: 
                return endSquare
        # TODO: pawn promotions
        # TODO: two pieces move same square
        # TODO: specify chess moves
        
        # piece moves
        moveString = self.pieceMoved[2]
        if self.isCaptured:
            moveString += 'x'
        return moveString + endSquare
            