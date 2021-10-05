#-------------------------------
# import modules
#-------------------------------
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
    validMoves = gs.getValidMoves()
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
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            
        DrawGameState(screen,gs,validMoves,sqSelected)
        clock.tick(MaxFPS)
        p.display.flip()


# highlight square selected and moves for piece selected

def HighlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected != ():
        r,c = sqSelected
        if gs.board[r][c][0] == ('W' if gs.WhiteToMove else 'B'):
            # highlight selected square
            s = p.Surface((SqSize,SqSize))
            s.set_alpha(100)  # transparency value -> 0 for transparent
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SqSize,r*SqSize))
            # highlight moves
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,(SqSize*move.endCol,SqSize*move.endRow))    

def DrawGameState(screen,gs,validMoves,sqSelected):
    DrawBoard(screen)
    HighlightSquares(screen,gs,validMoves,sqSelected)
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

# animating pieces
def animateMove(move,screen,board,clock):
    global colors
    coords = []   # list of coords that animation move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10    # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r,c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        DrawBoard(screen)
        DrawPieces(screen,board)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SqSize,move.endRow*SqSize,SqSize,SqSize)
        p.draw.rect(screen,color,endSquare)
        # draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(Images[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(Images[move.pieceMoved],p.Rect(c*SqSize,r*SqSize,SqSize,SqSize))
        p.display.flip()
        clock.tick(60)
    
    
if __name__ == "__main__":
    main()
