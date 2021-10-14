#-------------------------------
# import modules
#-------------------------------
from pygame.draw import rect
from pygame.font import SysFont
import ChessEngine
import pygame as p

p.init()
BoardWidth = BoardHeight = 1024
MoveLogPanelWidth = 400
MoveLogPanelHeight = BoardHeight
Dimension = 8
SqSize = BoardHeight // Dimension
MaxFPS = 15
Images = {}


def loadImages():
    pieces = ["B_R","B_N","B_B","B_Q","B_K","B_P","W_R","W_N","W_B","W_Q","W_K","W_P"]
    for piece in pieces:
        Images[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'),(SqSize,SqSize))

def main():
    p.init()
    screen = p.display.set_mode((BoardWidth+MoveLogPanelWidth,BoardHeight))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont('Arial',24,False,False)
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False           
        DrawGameState(screen,gs,moveLogFont)


def DrawGameState(screen,gs,moveLogFont):
    DrawBoard(screen)
    DrawPieces(screen,gs.board)

        
def DrawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("brown")]
    for row in range(Dimension):
        for col in range(Dimension):
            color = colors[((row+col) % 2)]
            p.draw.rect(screen,color,p.Rect(col*SqSize,row*SqSize,SqSize,SqSize))

def DrawPieces(screen,board):
    for row in range(Dimension):
        for col in range(Dimension):
            piece = board[row][col]
            if piece != "--":
                screen.blit(Images[piece],p.Rect(col*SqSize,row*SqSize,SqSize,SqSize))

if __name__ == "__main__":
    main()
