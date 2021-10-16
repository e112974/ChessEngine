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
    # ---------- initialize flag for status of game ---------- #
    RunningFlag = True
    # -------------------- start game -------------------- #
    while RunningFlag:
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                RunningFlag = False           
        DrawGameState(Screen,GameState,MoveLogFont)
        pygame.display.flip()
        
        
# -------------------------------------------------------- #
#                 draw game state function                 #
# -------------------------------------------------------- #

def DrawGameState(screen,gs,moveLogFont):
    DrawBoard(screen)
    DrawPieces(screen,gs.board)

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
#                         function                         #
# -------------------------------------------------------- #

if __name__ == "__main__":
    main()
