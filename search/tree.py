LEFT = "LEFT"
MIDDLE = "MIDDLE"
RIGHT = "RIGHT"

class tree:
    def __init__(self, board, parent, group):
        self.left = None
        self.middle = None
        self.right = None
        self.board = board
        self.parent = parent
        self.group = group
    
    def insert(self, node, side):
        if side == LEFT:
            self.left = node
        elif side == RIGHT:
            self.right = node
        else:
            self.middle = node

