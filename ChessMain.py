# -------------------- import modules -------------------- #
import ChessEngine
import pygame
import Players

# ----------------- set board dimensions ----------------- #
BoardWidth = BoardHeight = 1024
MoveLogPanelWidth        = 400
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
#                       main function                      #
# -------------------------------------------------------- #

def main():
    # ----------------- initialize pygame ---------------- #
    pygame.init()
    # -------------------- set screen -------------------- #
    Screen = pygame.display.set_mode((BoardWidth+MoveLogPanelWidth,BoardHeight))
    Screen.fill(pygame.Color("white"))
    # --------------------- set clock -------------------- #
    Clock = pygame.time.Clock()
    # -------------------- set log font ------------------ #
    MoveLogFont = pygame.font.SysFont('Arial',24,False,False)
    # ----------------- create gamestate ----------------- #
    GameState = ChessEngine.GameState()
    # ---------- initialize variables -------------------- #
    RunningFlag    = True
    GameOver       = False
    MoveMade       = False
    ClickedSquares = []  # two tuples [(6,4) (4,4)]
    SelectedSquare = ()  # single tuples (6,4) 
    # --------- calculate all inital valid moves --------- #
    AllValidMoves = GameState.CalculateAllValidMoves()
    # -------------------------------------------------------- #
    #         MAIN LOOP - RUNNING GAME                         #
    # -------------------------------------------------------- #  
    while RunningFlag:
        for Event in pygame.event.get():    # check the mouse clicks
            if Event.type == pygame.QUIT:   # if user clicks quit
                RunningFlag = False         # set flag
            # --------- MOUSE CLICKED --------- #
            elif Event.type == pygame.MOUSEBUTTONDOWN:     # if user clicks on the board
                ClickLocation = pygame.mouse.get_pos()     # get click coords
                col = ClickLocation[0]//SqSize             # determine row & col
                row = ClickLocation[1]//SqSize
                # following checks are necessary to correctly identify the start & end
                # squares for a piece to move
                #
                # ignore click if previously clicked square or outside board boundary
                if SelectedSquare == (row,col) or col >= 8: 
                    SelectedSquare = ()
                    ClickedSquares = []
                # ignore click if it is the first click on an empty square    
                elif len(ClickedSquares) < 1 and GameState.board[row][col] == '--':
                    SelectedSquare = ()
                    ClickedSquares = []                   
                else:
                    SelectedSquare = (row,col)
                    ClickedSquares.append(SelectedSquare)        # add to the list of clicked squares
                # if two selected squares are registered correctly
                if len(ClickedSquares) == 2:     
                    StartSquare  = ClickedSquares[0]
                    EndSquare    = ClickedSquares[1]                
                    SelectedMove = ChessEngine.Move(StartSquare,EndSquare,GameState.board)      
                    for i in range(len(AllValidMoves)):          # check if selected move is a legal move
                        if SelectedMove == AllValidMoves[i]:
                            GameState.MakeMove(SelectedMove)     # if so, make the move
                            ClickedSquares = []                  # set clicked squares back to empty
                            MoveMade = True                      # set flag
                    if not MoveMade:                                 # if not a legal move
                        ClickedSquares = [SelectedSquare]            # then ignore last clicked (2nd square)
            # --------- KEY PRESSED --------- #
            elif Event.type == pygame.KEYDOWN:                       # if user presses a key
                # Undo Last Move 
                if Event.key == pygame.K_z:                          # if pressed key is "z"           
                    GameState.UndoMove()                             # undo last move
                    MoveMade = True                                  # set flag
                # Reset board
                if Event.key == pygame.K_r:                          # if pressed key is "r"
                    GameState = ChessEngine.GameState()
                    AllValidMoves = GameState.CalculateAllMoves()
                    SelectedSquare = ()
                    ClickedSquares = []  
                    MoveMade = False         
        # -------------------- draw updated game board status  ------------ #    
        DrawGameState(Screen,GameState,AllValidMoves,SelectedSquare,MoveLogFont)  
        # -------------------- stop game if check mate -------------------- #                       
        if GameState.CheckMate or GameState.StaleMate:
            if GameState.CheckMate:
                text = 'White Wins!!' if GameState.Turn == 'B' else 'Black Wins!!'
            elif GameState.StaleMate:
                text = 'It is a Draw!!'
            ShowGameEndText(Screen,text)  
            GameOver = True
        # -------------------- show -------------------- # 
        pygame.display.flip()
         # ----------- calculate new valid moves after move is made-------- #   
        if MoveMade:
            AllValidMoves = GameState.CalculateAllValidMoves()     # update list of valid moves
            MoveMade = False                                       # update flag       
  
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

def DrawGameState(Screen,GameState,AllValidMoves,SelectedSquare,MoveLogFont):
    DrawBoard(Screen)
    HighlightSquares(Screen,GameState,AllValidMoves,SelectedSquare)
    DrawPieces(Screen,GameState.board)
    DisplayMoveLog(Screen,GameState,MoveLogFont)

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

def ShowGameEndText(Screen,text):
    font = pygame.font.SysFont('Helvetica',128,True,False)
    textObject = font.render(text,0,pygame.Color('Gray'))
    textLocation = pygame.Rect(0,0,BoardWidth,BoardHeight).move(BoardWidth/2-textObject.get_width()/2, \
                    BoardHeight/2-textObject.get_height()/2)
    Screen.blit(textObject,textLocation)
    textObject = font.render(text,0,pygame.Color('Black'))
    Screen.blit(textObject,textLocation.move(2,2))
    
# -------------------------------------------------------- #
#                    write move log                        #
# -------------------------------------------------------- #
    
def DisplayMoveLog(Screen,GameState,font):
    MoveLogRect = pygame.Rect(BoardWidth,0,MoveLogPanelWidth,MoveLogPanelHeight)
    pygame.draw.rect(Screen,pygame.Color('black'),MoveLogRect)
    MoveLog = GameState.MoveLog
    MoveTexts = []
    for i in range(0,len(MoveLog),2):
        moveString = str(i//2 + 1) + '.' + ChessEngine.Move.ChessNotation(MoveLog[i]) + ' '
        #if i+1 < len(MoveLog):  # make sure black made a move
            #moveString += str(MoveLog[i+1])
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
        Screen.blit(textObject,textLocation)
        textY += textObject.get_height() + lineSpacing
        
# -------------------------------------------------------- #
#                    main function                         #
# -------------------------------------------------------- #

if __name__ == "__main__":
    main()
