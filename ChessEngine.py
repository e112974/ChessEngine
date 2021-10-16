# -------------------------------------------------------- #
#                      GameState class                     #
# -------------------------------------------------------- #

class GameState():
    def __init__(self):
        self.board = [
            ["B_R","B_N","B_B","B_Q","B_K","B_B","B_N","B_R"],
            ["B_P","B_P","B_P","B_P","B_P","B_P","B_P","B_P"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["W_P","W_P","W_P","W_P","W_P","W_P","W_P","W_P"],
            ["W_R","W_N","W_B","W_Q","W_K","W_B","W_N","W_R"],
        ]
        self.Turn         = 'White'
        self.MoveLog      = []
        self.CheckMate    = False
        self.StaleMate    = False
        self.WhiteCastled = False
        self.BlackCastled = False
        self.KingInCheck  = False

    # ---------------------------------------------------- #
    #                  MovePiece function                  #
    # ---------------------------------------------------- #
    
    def MovePiece():
        pass
 
    # ---------------------------------------------------- #
    #                  UndoMove function                   #
    # ---------------------------------------------------- #
    
    def UndoMove():
        pass
       
    # ---------------------------------------------------- #
    #              CalculateAllMoves function              #
    # ---------------------------------------------------- #
    
    def CalculateAllMoves():
        pass
