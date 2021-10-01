from pygame.draw import rect
import ChessEngine
import pygame as p

p.init()
Width = Height = 1024
Dimension = 8
SqSize = Height // Dimension
MaxFPS = 15
Images = {}


def loadImages():
    pieces = ["B_R","B_N","B_B","B_Q","B_K","B_P","W_R","W_N","W_B","W_Q","W_K","W_P"]
    for piece in pieces:
        Images[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'),(SqSize,SqSize))

def main():
    p.init()
    screen = p.display.set_mode((Width,Height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    #validMoves = gs.getAllPossibleMoves()
    moveMade  = False
    loadImages()
    running = True
    sqSelected = ()    # tuple(row,col)
    playerClicks = []  # two tuples [(6,4) (4,4)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SqSize
                row = location[1]//SqSize
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    validMoves = gs.getAllPossibleMoves()
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        DrawGameState(screen,gs)
        clock.tick(MaxFPS)
        p.display.flip()


def DrawGameState(screen,gs):
    DrawBoard(screen)
    DrawPieces(screen,gs.board)

def DrawBoard(screen):
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
