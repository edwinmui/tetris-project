import pygame, sys
from pygame.locals import *
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
EMPTY_SQUARE = (0, 0, 0)    # tuple representing an empty block of a grid

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

def get_grid_width(grid):
    # returns the width of the grid
    return len(grid[0])

def get_grid_height(grid):
    # returns the length of the grid
    return len(grid)

def get_num_shape_rotates(shape):
    # returns the number of rotations a shape has
    return len(shape.shape)

def create_grid(locked_positions={}):
    """ 
    EFFECTS: Creates and returns a newly constructed grid, which is a 
                2D array of colors meant to represent a Tetris grid
    """
    # creates a blank grid
    grid = [ [EMPTY_SQUARE for col in range(GRID_WIDTH)]
                        for row in range(GRID_HEIGHT) ]
    # looks through grid and checks if key exists in each slot
    for row in range(get_grid_height(grid)):
        for col in range(get_grid_width(grid)):
            if (col, row) in locked_positions:
                c = locked_positions[(col, row)]
                grid[row][col] = c                                              
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

def valid_space(shape, grid):
    """
    REFUIRES: shape is a valid tetris shape, and grid is a valid tetris grid
    EFFECTS:  Returns whether the current shape is at a valid space within the
              provided grid
    """
    # creates a list of all accepted positions
    accepted_pos = [ [(col, row) for col in range(get_grid_width(grid)) 
                                if grid[row][col] == EMPTY_SQUARE]
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
    MIDDLE_GRID_X = 5
    TOP_GRID_Y = 0
    # returns a random shape
    return Piece(MIDDLE_GRID_X, TOP_GRID_Y, random.choice(shapes))

def draw_text_middle(text, size, color, surface): 
    """
    MODIFIES: surface
    EFFECTS:  Draws the provided text in the middle of the screen
    """ 
    font = pygame.font.SysFont("centurygothic", size, bold = True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + PLAY_WIDTH/2 - label.get_width()/2, 
    top_left_y + PLAY_HEIGHT/2 - label.get_height()/2))
   
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

def clear_rows(grid, locked_positions):
    """
    MODIFIES: grid, locked
    EFFECTS:  Removes all rows of the grid that are full, 
              meaning no empty squares exist
    """
    cleared_rows = 0
    # goes through every row starting from bottom of grid
    for y in range(get_grid_height(grid)-1, -1, -1):
        row = grid[y]
        # checks if there are any empty squares within the row
        if (0, 0, 0) not in row:
            cleared_rows += 1
            deleted_index = y
            # if no empty squares, tries to delete every block within row
            for x in range(len(row)):
                try:
                    del locked_positions[(x, y)]
                except:
                    continue
    
    # if there are rows that need to be deleted
    if cleared_rows > 0:
        # goes through the entire locked positions dictionary backwards
        for key in sorted(list(locked_positions), 
                                            key=lambda x:x[1], reverse = True):
            x, y = key
            # if row is above the deleted row, shift it down 
            if y < deleted_index:
                # updates locked positions with the shifted key
                new_key = (x, y + deleted_index)
                locked_positions[new_key] = locked_positions.pop(key)

    # returns the number of rows the player clears
    return cleared_rows

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

def draw_window(surface, grid, score=0):
    # fills the surface with blank RGB values
    surface.fill(BLACK)

    # draws the Tetris label at top of screen
    pygame.font.init()
    font = pygame.font.SysFont('centurygothic', 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    surface.blit(label, (top_left_x + PLAY_WIDTH/2 - (label.get_width()/2), 30))

    # draws the score on the right size of screen
    font = pygame.font.SysFont('centurygothic', 30)
    label2 = font.render('Score' + str(score), 1, WHITE)
    #offset constants to make the next shape look better
    SHAPE_RIGHT_OFFSET = 70
    SHAPE_DOWN_OFFSET = 60    
    sx = top_left_x + PLAY_WIDTH + SHAPE_RIGHT_OFFSET
    sy = top_left_y + PLAY_HEIGHT/2 + SHAPE_DOWN_OFFSET
    surface.blit(label2, (sx, sy))

    # draws the rectangles on the surface
    for row in range(get_grid_height(grid)):
        for col in range(get_grid_width(grid)):
            pygame.draw.rect(surface, grid[row][col], 
            (top_left_x + col * BLOCK_SIZE, top_left_y + row * BLOCK_SIZE, 
            BLOCK_SIZE, BLOCK_SIZE), 0)

    # draws the grid
    draw_grid(surface, grid)
    # creates a red border around the play area
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y,
                        PLAY_WIDTH, PLAY_HEIGHT), 4)

def main(win):
    """
        REQUIRES: win is a valid pygame surface that can be drawn on
    """
    global grid

    locked_positions = {}   # format e.g. "(x, y):(255, 0, 0)"
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    curr_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    score = 0
    INCREASE_LEVEL = 5      # num seconds before increasing fall speed
    MAX_SPEED = 0.12        # the maximum speed a block can fall
    INCREASE_SPEED = 0.005      # the amount of speed a block is incr. by / lvl
    MILLISECOND = 1000

    # continues to run the game untl the user quits
    while run:
        fall_speed = 0.27
        # updates the grid based on prev locked positions of tetris blocks
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # increases fall speed as game progresses
        if level_time/MILLISECOND > INCREASE_LEVEL:
            # resets level tracker
            level_time = 0
            # the threshold for highest speed a block can attain
            if level_time > MAX_SPEED:
                level_time -= INCREASE_SPEED

        # makes blocks fall down the screen
        if fall_time / MILLISECOND > fall_speed:
            # resets fall time tracker
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
                    # moves piece left
                    curr_piece.x -= 1
                    if not(valid_space(curr_piece, grid)):
                        curr_piece.x += 1   

                elif event.key == pygame.K_RIGHT:
                    # moves piece right
                    curr_piece.x += 1
                    if not(valid_space(curr_piece, grid)):
                        curr_piece.x -= 1

                elif event.key == pygame.K_UP:
                    # rotates piece one iteratoins
                    curr_piece.rotation = (curr_piece.rotation
                        + 1 % len(curr_piece.shape))
                    if not(valid_space(curr_piece, grid)):
                        curr_piece.rotation = (curr_piece.rotation 
                            - 1 % len(curr_piece.shape))

                if event.key == pygame.K_DOWN:
                    # moves piece down
                    curr_piece.y += 1
                    if not(valid_space(curr_piece, grid)):
                        curr_piece.y -= 1

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
        # checks if any rows need to be cleared and adds to total score
        score += clear_rows(grid, locked_positions) * 10

    # draw the game window
    draw_window(win, grid, score)
    # draws the next shape on the right side of screen
    draw_next_shape(next_piece, win)
    #updates the screen
    pygame.display.update()

    # if user LOST
    if check_lost(locked_positions):
        YOU_LOST_FONT_SIZE = 80
        draw_text_middle('YOU LOST!', YOU_LOST_FONT_SIZE, WHITE, win)
        pygame.display.update()
        pygame.time.delay(MILLISECOND * 2)
        run = False
                    
def main_menu(win):
    START_FONT_SIZE = 60
    run = True
    while run:
        # starts with black screen and start-game prompt
        win.fill(BLACK)
        draw_text_middle("Press Any Key to Start", START_FONT_SIZE, WHITE, win)
        pygame.display.update()
        for event in pygame.event.get():
            # quits game if user quits
            if event.type == pygame.QUIT:
                run = False
            # if users presses a key, plays game
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()




win = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption('Tetris')
main_menu(win)