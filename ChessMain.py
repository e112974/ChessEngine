# -------------------- import modules -------------------- #
import ChessEngine
import pygame
import Players
from Utilities import *
from pygame._sdl2.video import Window
from MenuAndButtons import *

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
#                  define RunTheGame function              #
# -------------------------------------------------------- #
# note: defining the core script here as a function called "main"
# enables using the functions defined below. If we did not do 
# that it would execute the script from top to bottom without
# first defining the function
# in this way, it first just registers the function names, 
# reaches to the bottom of this file and then the "__name__ == "__main__" "
# part at the end runs this main function

def RunTheGame():
    # ----------------- initialize pygame ---------------- #
    pygame.init()
    # -------------------- set game window -------------------- #
    Screen = pygame.display.set_mode((BoardWidth+MoveLogPanelWidth,BoardHeight)) # set size of window
    window = Window.from_display_module()   
    window.position = (1400,300)   # set position of window
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
    # --------- create a button --------- #
    ButtonWidth = 10
    b0 = Button((BoardWidth + MoveLogPanelWidth/2,BoardHeight-30), \
        "Click me now", ButtonWidth, "green on yellow",command=on_click)
    # --------- draw/update board --------- #      
    DrawGameState(Screen,GameState,AllValidMoves,SelectedSquare,MoveLogFont) 
    # -------------------------------------------------------- #
    #         MAIN LOOP - RUNNING GAME                         #
    # -------------------------------------------------------- #  
    while RunningFlag:
        for Event in pygame.event.get():    # check the mouse clicks
            if Event.type == pygame.QUIT:   # if user clicks quit
                RunningFlag = False         # set flag
                # --------- draw/update board --------- #    
                DrawGameState(Screen,GameState,AllValidMoves,SelectedSquare,MoveLogFont) 
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
                            GameState.MakeMove(SelectedMove,True)     # if so, make the move
                            ClickedSquares = []                       # set clicked squares back to empty
                            MoveMade = True                           # set flag
                            break
                    if not MoveMade:                                 # if not a legal move
                        ClickedSquares = [SelectedSquare]            # then ignore last clicked (2nd square)
                # --------- draw/update board --------- #      
                DrawGameState(Screen,GameState,AllValidMoves,SelectedSquare,MoveLogFont) 
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
                # --------- draw/update board --------- #       
                DrawGameState(Screen,GameState,AllValidMoves,SelectedSquare,MoveLogFont) 
        # --------- check if mate or stalemate --------- #                      
        if GameState.CheckMate or GameState.StaleMate:
            if GameState.CheckMate:
                text = 'White Wins!!' if GameState.Turn == 'B' else 'Black Wins!!'
            elif GameState.StaleMate:
                text = 'It is a Draw!!'
            ShowGameEndText(Screen,text)  
            GameOver = True

        b0.update()
        # -------------------- show -------------------- # 
        pygame.display.flip()
         # ----------- calculate new valid moves after move is made-------- #   
        if MoveMade:
            AllValidMoves = GameState.CalculateAllValidMoves()     # update list of valid moves
            MoveMade = False                                       # update flag       
         
# -------------------------------------------------------- #
#              execute RunTheGame function                 #
# -------------------------------------------------------- #

RunTheGame()
