# import modules
import ChessEngine
import pygame

# initialize pygame module
pygame.init()

#-------------------------------
# import modules
#-------------------------------
BoardWidth = BoardHeight = 1024
MoveLogPanelWidth = 400
MoveLogPanelHeight = BoardHeight
Dimension = 8
SqSize = BoardHeight // Dimension
Images = {}


def loadImages():
    pieces = ["B_R","B_N","B_B","B_Q","B_K","B_P","W_R","W_N","W_B","W_Q","W_K","W_P"]
    for piece in pieces:
        Images[piece] = pygame.transform.scale(pygame.image.load('images/' + piece + '.png'),(SqSize,SqSize))

def main():
    pygame.init()
    screen = pygame.display.set_mode((BoardWidth+MoveLogPanelWidth,BoardHeight))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    moveLogFont = pygame.font.SysFont('Arial',24,False,False)
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False           
        DrawGameState(screen,gs,moveLogFont)
        pygame.display.flip()
        
def DrawGameState(screen,gs,moveLogFont):
    DrawBoard(screen)
    DrawPieces(screen,gs.board)

        
def DrawBoard(screen):
    global colors
    colors = [pygame.Color("white"), pygame.Color("brown")]
    for row in range(Dimension):
        for col in range(Dimension):
            color = colors[((row+col) % 2)]
            pygame.draw.rect(screen,color,pygame.Rect(col*SqSize,row*SqSize,SqSize,SqSize))

def DrawPieces(screen,board):
    for row in range(Dimension):
        for col in range(Dimension):
            piece = board[row][col]
            if piece != "--":
                screen.blit(Images[piece],pygame.Rect(col*SqSize,row*SqSize,SqSize,SqSize))

if __name__ == "__main__":
    main()
