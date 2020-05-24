"""
This file contains all of the Tetris shapes formats needed for game to function
"""


class ShapeFormat:
    # SHAPE FORMATS
    S = [['.....',
          '......',
          '..00..',
          '.00...',
          '.....'],
         ['.....',
          '..0..',
          '..00.',
          '...0.',
          '.....']]

    Z = [['.....',
          '.....',
          '.00..',
          '..00.',
          '.....'],
         ['.....',
          '..0..',
          '.00..',
          '.0...',
          '.....']]

    I = [['..0..',
          '..0..',
          '..0..',
          '..0..',
          '.....'],
         ['.....',
          '0000.',
          '.....',
          '.....',
          '.....']]

    O = [['.....',
          '.....',
          '.00..',
          '.00..',
          '.....']]

    J = [['.....',
          '.0...',
          '.000.',
          '.....',
          '.....'],
         ['.....',
          '..00.',
          '..0..',
          '..0..',
          '.....'],
         ['.....',
          '.....',
          '.000.',
          '...0.',
          '.....'],
         ['.....',
          '..0..',
          '..0..',
          '.00..',
          '.....']]

    L = [['.....',
          '...0.',
          '.000.',
          '.....',
          '.....'],
         ['.....',
          '..0..',
          '..0..',
          '..00.',
          '.....'],
         ['.....',
          '.....',
          '.000.',
          '.0...',
          '.....'],
         ['.....',
          '.00..',
          '..0..',
          '..0..',
          '.....']]

    T = [['.....',
          '..0..',
          '.000.',
          '.....',
          '.....'],
         ['.....',
          '..0..',
          '..00.',
          '..0..',
          '.....'],
         ['.....',
          '.....',
          '.000.',
          '..0..',
          '.....'],
         ['.....',
          '..0..',
          '.00..',
          '..0..',
          '.....']]

    # index 0 - 6 represent shape
    shapes = [S, Z, I, O, J, L, T]
    shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0),
                    (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(ShapeFormat):
    """ Represents a single piece """

    def __init__(self, col, row, shape):
        """ Initializes a single piece """
        self.x = col
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        # numbers from 0-3, default set to zero
        self.rotation = 0


def get_num_shape_rotates(shape):
    # returns the number of rotations a shape has
    return len(shape.shape)


def get_num_shape_rotates(shape):
    # returns the number of rotations a shape has
    return len(shape.shape)
