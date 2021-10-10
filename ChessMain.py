#-------------------------------
# import modules
#-------------------------------
from pygame.draw import rect
from pygame.font import SysFont
import ChessEngine, SmartMoveFinder
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
    validMoves = gs.getValidMoves()
    moveMade  = False
    animate = False  # flag variable when a move is animated
    loadImages()
    running = True
    sqSelected = ()    # tuple(row,col)
    playerClicks = []  # two tuples [(6,4) (4,4)]
    gameOver = False
    playerOne = False  # if human playing white, this will be true, if AI playing for false
    playerTwo = False
    while running:
        humanTurn = (gs.WhiteToMove and playerOne) or (not gs.WhiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0]//SqSize
                    row = location[1]//SqSize
                    if sqSelected == (row,col) or col >= 8:
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
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r:    # reset the board when r is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
        
        # AI move finder
        if not gameOver and not humanTurn:
            AImove = SmartMoveFinder.findBestMove(gs,validMoves)
            if AImove is None:
                AImove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AImove)
            moveMade = True
            animate = True
                    
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            
        DrawGameState(screen,gs,validMoves,sqSelected,moveLogFont)
        
        if gs.checkMate or gs.staleMate:
            gameOver = True
            if gs.staleMate:
                text = 'It is a Draw!!'
            else:
                text = 'Black Wins!!' if gs.WhiteToMove else 'White Wins!!'
            drawEndGameText(screen,text)

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

def DrawGameState(screen,gs,validMoves,sqSelected,moveLogFont):
    DrawBoard(screen)
    HighlightSquares(screen,gs,validMoves,sqSelected)
    DrawPieces(screen,gs.board)
    drawMoveLog(screen,gs,moveLogFont)
    
def drawMoveLog(screen,gs,font):
    moveLogRect = p.Rect(BoardWidth,0,MoveLogPanelWidth,MoveLogPanelHeight)
    p.draw.rect(screen,p.Color('black'),moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0,len(moveLog),2):
        moveString = str(i//2 + 1) + '.' + str(moveLog[i]) + ' '
        if i+1 < len(moveLog):  # make sure black made a move
            moveString += str(moveLog[i+1])
        moveTexts.append(moveString)
    movesPerRow = 3
    padding = 5
    lineSpacing = 1
    textY = padding
    for i in range(0,len(moveTexts),movesPerRow):
        text = ' '
        for j in range(movesPerRow):
            if i+j < len(moveTexts):
                text += moveTexts[i+j] + '  '
        textObject = font.render(text,True,p.Color('white'))
        textLocation = moveLogRect.move(padding,textY)
        screen.blit(textObject,textLocation)
        textY += textObject.get_height() + lineSpacing
        
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
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'B' else move.endRow - 1
                endSquare = p.Rect(move.endCol*SqSize,enPassantRow*SqSize,SqSize,SqSize)
            screen.blit(Images[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(Images[move.pieceMoved],p.Rect(c*SqSize,r*SqSize,SqSize,SqSize))
        p.display.flip()
        clock.tick(120)   
    
def drawEndGameText(screen,text):
    font = p.font.SysFont('Helvetica',128,True,False)
    textObject = font.render(text,0,p.Color('Gray'))
    textLocation = p.Rect(0,0,BoardWidth,BoardHeight).move(BoardWidth/2-textObject.get_width()/2, \
                    BoardHeight/2-textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject = font.render(text,0,p.Color('Black'))
    screen.blit(textObject,textLocation.move(2,2))
    
if __name__ == "__main__":
    main()
