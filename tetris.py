import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
S_WIDTH = 800
S_HEIGHT = 700
PLAY_WIDTH = 300  # meaning 300 // 10 = 30 width per block
PLAY_HEIGHT = 600  # meaning 600 // 20 = 20 height per block
BLOCK_SIZE = 30
GRID_HEIGHT = 20    # the max valid height of a grid
GRID_WIDTH = 10     # the max valid width of a grid

top_left_x = (S_WIDTH - PLAY_WIDTH) // 2    # 250
top_left_y = S_HEIGHT - PLAY_HEIGHT         # 100

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DARK_BLUE = (0,0,128)
WHITE = (255,255,255)
BLACK = (0,0,0)
PINK = (255,200,200)
GREY = (120, 120, 120)


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

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), 
    (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape

class Piece(object):
    """ Represents a single piece """

    def __init__(self, col, row, shape):
        """ Initializes a single piece """
        self.x = col
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        # numbers from 0-3, default set to zero
        self.rotation = 0

def get_grid_width(grid):
    # returns the width of the grid
    return len(grid[0])

def get_grid_height(grid):
    # returns the length of the grid
    return len(grid)

def create_grid(locked_positions={}):
    """ 
    EFFECTS: Creates and returns a newly constructed grid, which is a 
                2D array of colors meant to represent a Tetris grid
    """
    # creates a blank grid
    grid = [ [(0, 0, 0) for col in range(GRID_WIDTH)]
                        for row in range(GRID_HEIGHT) ]
    # looks through grid and checks if key exists in each slot
    for row in range(get_grid_height(grid)):
        for col in range(get_grid_width(grid)):
            if (col, row) in locked_positions:
                c = locked_positions[(col, row)]
                grid[row][col] = c                                                # POSSIBLE BUG!!!!! FIX LATER
    return grid

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
    format = shape.shape[shape.rotation % len(shape.shape)]

    # iterates through every line of shape and executes based on
    for x, line in enumerate(format):
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

def valid_space(shape, grid):
    """
    REFUIRES: shape is a valid tetris shape, and grid is a valid tetris grid
    EFFECTS:  Returns whether the current shape is at a valid space within the
              provided grid
    """
    # creates a list of all accepted positions
    accepted_pos = [ [(col, row) for col in range(get_grid_width(grid)) 
                                if grid[row][col] == (0, 0, 0)]
                            for row in range(get_grid_height(grid)) ]
    # flattens out the above 2D list into a 1D list that can iterated over
    accepted_pos = [col for sub in accepted_pos for col in sub]
    # formats the positions of shape to be compared
    formatted_shape_pos = convert_shape_format(shape)
    # checks if converted shape is accepted
    for pos in formatted_shape_pos:
        if pos not in accepted_pos:
            # checks if the shape is not above the grid; if above grid, OK
            if pos[1] >= 0:
                return False

    return True

def check_lost(positions):
    """
    EFFECTS: Returns whether any of the currently placed blocks in the passed-
             in locked_positions dictionary are above the screen, 
             a.k.a. resulting in a loss
    """
    # loops through all positions and checks if y position is still less than 1
    for pos in positions:
        for x, y in pos:
            if y < 1:
                return True
    return False

def get_shape():
    # returns a random shape
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):  
    pass
   
def draw_grid(surface, grid):
    # draws the gridlines onto the window
    sx = top_left_x
    sy = top_left_y

    # draws horizontal line across every row
    for row in range(get_grid_height(grid)):
        pygame.draw.line(surface, GREY, (sx, sy + row * BLOCK_SIZE), 
                                      (sx + PLAY_WIDTH, sy + row * BLOCK_SIZE))

    # draws vertical line across entire col
    for col in range(get_grid_width(grid)):
        pygame.draw.line(surface, GREY, 
                    (sx + col * BLOCK_SIZE, sy),
                    (sx + col * BLOCK_SIZE, sy + PLAY_HEIGHT))

def clear_rows(grid, locked):
    pass

def draw_next_shape(shape, surface):
    pass

def draw_window(surface, grid):
    # fills the surface with blank RGB values
    surface.fill(0, 0, 0)

    pygame.font.init()
    font = pygame.font.SysFont('centurygothic', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    # gets to the middle of the grid
    surface.blit(label, (top_left_x + PLAY_WIDTH/2 - (label.get_width()/2), 30))

    # draws the rectangles on the surface
    for row in range(get_grid_height(grid)):
        for col in range(get_grid_width(grid)):
            pygame.draw.rect(surface, grid[row][col], 
            (top_left_x + col * BLOCK_SIZE, top_left_y + row * BLOCK_SIZE, 
            BLOCK_SIZE, BLOCK_SIZE), 0)

    # creates a red border around the play area
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y,
                        PLAY_WIDTH, PLAY_HEIGHT), 4)

    # draws the grid
    draw_grid(surface, grid)
    # updates the screen
    pygame.display.update()

def main(win):

    locked_positions = {}
    grid = create_grid()

    change_piece = False
    run = True
    curr_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    MILLISECOND = 1000

    # continues to run the game untl the user quits
    while run:
        # updates the grid based on prev locked positions of tetris blocks
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()

        if fall_time / MILLISECOND > fall_speed:
            fall_time = 0
            curr_piece.y += 1
            # checks if falling piece hits bottom or another piece
            if not(valid_space(curr_piece, grid)) and curr_piece.y > 0:
                # if hits bottom or another piece, switches to the next piece
                curr_piece.y -= 1
                change_piece = True


        for event in pygame.event.get():
            # if the user wants to quit, exits the program
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            # checks what the user presses down a key
            if event.type == pygame.KEYDOWN:
                # checks different cases and verifies that movement is valid
                if event.key == pygame.K_LEFT:
                    curr_piece.x -= 1
                    if not(valid_space(curr_piece, grid)):
                        curr_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    curr_piece.x += 1
                    if not(valid_space(curr_piece, grid)):
                        curr_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    curr_piece.y += 1
                    if not(valid_space(curr_piece, grid)):
                        curr_piece.y -= 1

                if event.key == pygame.K_UP:
                    curr_piece.rotation += 1
                    if not(valid_space(curr_piece, grid)):
                        curr_piece.rotation -= 1

    shape_positions = convert_shape_format(curr_piece)

    # draws the shape onto the grid
    for i in range(len(shape_positions)):
        col, row = shape_positions[i]
        # if piece is not above the screen
        if row > -1:
            grid[row][col] = curr_piece.color

    # if piece hits ground, updates locked-grid with corresp piece pos and color
    if change_piece:
        for pos in shape_positions:
            p = (pos[0], pos[1])
            locked_positions[p] = curr_piece.color
        # updates the current piece
        curr_piece = next_piece
        #updates the next piece and change piece bool
        next_piece = get_shape()
        change_piece = False

    draw_window(win, grid)

    # check if user lost
    if check_lost(locked_positions):
        run = False

                    
def main_menu(win):
    main(win)
    pass

win = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game