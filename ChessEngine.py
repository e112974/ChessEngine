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
        self.WhiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False

