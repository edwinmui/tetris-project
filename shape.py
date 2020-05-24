import pygame, sys
"""
Shape class
"""

class Shape:
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


class Piece(Shape):
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

def get_shape():
    MIDDLE_GRID_X = 5   # X value referencing the middle of the grid
    TOP_GRID_Y = 0      # Y value referencing the top of the grid
    # returns a random shape
    return Piece(MIDDLE_GRID_X, TOP_GRID_Y, random.choice(shapes))

def convert_shape_format(shape):
    """
    EFFECTS: Converts the shapes, which are currently strings, into visual
            in-game Tetris blocks 
    """
    # constant vars to help format shapes
    OFFSET_LEFT = 2
    OFFSET_UP = 4
    positions = []
    # figures out the current rotation of the shape
    shape_format = shape.shape[shape.rotation % get_num_shape_rotates(shape)]

    # iterates through every line of shape
    for x, line in enumerate(shape_format):
        row = list(line)
        for y, col in enumerate(row):
            # checks if a block exists at the current string
            if col == '0':
                # adds it to our list of current shape positions
                positions.append((shape.x + x, shape.y + y))
    
    # offsets positions of shapes to deal with initial incorrect offset
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - OFFSET_LEFT, pos[1] - OFFSET_UP)

    return positions

def draw_next_shape(shape, surface):
    """
    EFFECTS: Shows the upcoming piece on the right side of the screen
    """
    font = pygame.font.SysFont('centurygothic', 30)
    # displays text indicating next shape area
    label = font.render('Next Shape', 1, WHITE)
    #offset constants to make the next shape look better
    SHAPE_RIGHT_OFFSET = 50
    SHAPE_UP_OFFSET = 100

    sx = top_left_x + PLAY_WIDTH + SHAPE_RIGHT_OFFSET
    sy = top_left_y + PLAY_HEIGHT/2 - SHAPE_UP_OFFSET
    shape_format = shape.shape[shape.rotation 
                                     % get_num_shape_rotates(shape)]

    # draws the actual tetris block
    for i, line in enumerate(shape_format):
        for j, col in enumerate(line):
            if col == '0':
                pygame.draw.rect(surface, shape.color, 
            (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 
                0)

    TITLE_RIGHT_OFFSET = 10
    TITLE_UP_OFFSET = 30
    surface.blit(label, (sx + TITLE_RIGHT_OFFSET, sy - TITLE_UP_OFFSET))