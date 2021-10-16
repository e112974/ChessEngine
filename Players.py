# -------------------------------------------------------- #
#                       Player class                       #
# -------------------------------------------------------- #

class Player():
    def __init__(self, Name, Color, Type, AIdepth, AImethod):
      self.Name           = Name
      self.Color          = Color
      self.Type           = Type
      self.Time           = 0.0
      self.MoveLog        = []
      self.CapturedPieces = []
      self.Castled        = False
      self.InCheck        = False