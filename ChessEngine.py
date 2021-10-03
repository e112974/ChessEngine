class GameState():
    def __init__(self):
        self.board = [
            ["B_R","B_N","B_B","B_Q","B_K","B_B","B_N","B_R"],
            ["B_P","B_P","B_P","B_P","B_P","B_P","B_P","B_P"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "W_N", "--", "--"],
            ["--", "--", "--", "B_N", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["W_P","W_P","W_P","W_P","W_P","W_P","W_P","W_P"],
            ["W_R","W_N","W_B","W_K","W_Q","W_B","W_N","W_R"],
        ]
        self.moveFunctions = {'P': self.getPawnMoves,   'R': self.getRookMoves,
                              'B': self.getBishopMoves, 'N': self.getKnightMoves,
                              'K': self.getKingMoves,   'Q': self.getQueenMoves}
        self.WhiteToMove = True
        self.moveLog = []

    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.WhiteToMove = not self.WhiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endRow] = move.pieceCaptured
            self.WhiteToMove = not self.WhiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

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
        if self.WhiteToMove:
            if self.board[r-1][c] == '--':
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] =='--':
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'B':
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'B':
                    moves.append(Move((r,c),(r-1,c+1),self.board))
        else:
            if self.board[r+1][c] == '--':
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] =='--':
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'W':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'W':
                    moves.append(Move((r,c),(r+1,c+1),self.board))


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
        if not self.WhiteToMove:
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
        elif not self.WhiteToMove:                
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
        if not self.WhiteToMove:
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

    def getQueenMoves(self,r,c,moves):
        # -----------------------        
        # Moves for WHITE QUEEN
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
        # Moves for BLACK QUEEN
        # -----------------------
        elif not self.WhiteToMove:                
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


class Move():

    ranksToRows = {'1':7, '2':6, '3':5, '4':4,
                   '5':3, '6':2, '7':1, '8':0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}   # reverse the pairs
    filesToCols = {'a':0, 'b':1, 'c':2, 'd':3,
                   'e':4, 'f':5, 'g':6, 'h':7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow   = endSq[0]
        self.endCol   = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]