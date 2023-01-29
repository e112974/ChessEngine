# -------------------- import modules -------------------- #
import pygame
import ChessEngine

# ----------------- set board dimensions ----------------- #
BoardWidth = BoardHeight = 800
MoveLogPanelWidth        = 200
MoveLogPanelHeight       = BoardHeight
Nrows = Ncols            = 8
SqSize                   = BoardHeight // Nrows
PieceImages              = {}

# ---------------------- load images --------------------- #
pieces = ["B_R","B_N","B_B","B_Q","B_K","B_P","W_R","W_N","W_B","W_Q","W_K","W_P"]
for piece in pieces:
    PieceImages[piece] = pygame.transform.scale(
                         pygame.image.load('images/' + piece + '.png'),(SqSize,SqSize))

# -------------------------------------------------------- #
#         function to highlight legal moves on board       #
# -------------------------------------------------------- #  
        
def HighlightSquares(screen,GameState,AllValidMoves,SelectedSquare):
    if SelectedSquare != ():                                  # check at least one move is made
        row,col = SelectedSquare                              # get row & col of last selected square
        SelectedPieceColor = GameState.board[row][col][0]     
        if SelectedPieceColor == GameState.Turn:
            Surface = pygame.Surface((SqSize,SqSize))               # 
            Surface.set_alpha(100)                                  # transparency value -> 0 for transparent
            Surface.fill(pygame.Color('blue'))                   
            screen.blit(Surface,(col*SqSize,row*SqSize)) 
            Surface.fill(pygame.Color('yellow'))
            for move in AllValidMoves:                              # loop over all legal moves
                if move.StartRow == row and move.StartCol == col:   # if move starts from selected square
                    screen.blit(Surface,(SqSize*move.EndCol,SqSize*move.EndRow))  # then highlight the move square
                            
# -------------------------------------------------------- #
#                 draw game state function                 #
# -------------------------------------------------------- #

def DrawGameState(screen,GameState,AllValidMoves,SelectedSquare,MoveLogFont):
    DrawBoard(screen)
    HighlightSquares(screen,GameState,AllValidMoves,SelectedSquare)
    DrawPieces(screen,GameState.board)
    DisplayMoveLog(screen,GameState,MoveLogFont)

# -------------------------------------------------------- #
#                    draw board function                   #
# -------------------------------------------------------- #
        
def DrawBoard(screen):
    colors = [pygame.Color("white"), pygame.Color("brown")]
    for row in range(Nrows):
        for col in range(Nrows):
            color = colors[((row+col) % 2)]
            pygame.draw.rect(screen,color,pygame.Rect(col*SqSize,row*SqSize,SqSize,SqSize))

# -------------------------------------------------------- #
#                        draw pieces                       #
# -------------------------------------------------------- #

def DrawPieces(screen,board):
    for row in range(Nrows):
        for col in range(Nrows):
            piece = board[row][col]
            if piece != "--":
                screen.blit(PieceImages[piece],pygame.Rect(col*SqSize,row*SqSize,SqSize,SqSize))

# -------------------------------------------------------- #
#           show result at the end of game                 #
# -------------------------------------------------------- #

def ShowGameEndText(screen,text):
    font = pygame.font.SysFont('Helvetica',128,True,False)
    textObject = font.render(text,0,pygame.Color('Gray'))
    textLocation = pygame.Rect(0,0,BoardWidth,BoardHeight).move(BoardWidth/2-textObject.get_width()/2, \
                    BoardHeight/2-textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject = font.render(text,0,pygame.Color('Black'))
    screen.blit(textObject,textLocation.move(2,2))
    
# -------------------------------------------------------- #
#                    write move log                        #
# -------------------------------------------------------- #
    
def DisplayMoveLog(screen,GameState,font):
    # position & size of log box
    MoveLogRect = pygame.Rect(BoardWidth,0,MoveLogPanelWidth,MoveLogPanelHeight)
    # create box to write the log
    pygame.draw.rect(screen,pygame.Color('black'),MoveLogRect)
    # recover the log so far
    MoveLog = GameState.MoveLog
    # initialize move texts
    MoveTexts = []
    # loop over log
    for i in range(0,len(MoveLog),2):
        # 
        moveString = str(i//2 + 1) + '.' + ChessEngine.Move.ChessNotation(MoveLog[i]) + ' '
        if i+1 < len(MoveLog):  # make sure black made a move
            moveString += ChessEngine.Move.ChessNotation(MoveLog[i+1])
        MoveTexts.append(moveString)
    movesPerRow = 3
    padding = 5
    lineSpacing = 1
    textY = padding
    for i in range(0,len(MoveTexts),movesPerRow):
        text = ' '
        for j in range(movesPerRow):
            if i+j < len(MoveTexts):
                text += MoveTexts[i+j] + '  '
        textObject = font.render(text,True,pygame.Color('white'))
        textLocation = MoveLogRect.move(padding,textY)
        screen.blit(textObject,textLocation)
        textY += textObject.get_height() + lineSpacing