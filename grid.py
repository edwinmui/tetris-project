import pygame, sys
"""
Grid class
"""

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
    grid = [ [EMPTY_SQUARE for col in range(GRID_WIDTH)]
                        for row in range(GRID_HEIGHT) ]
    # looks through grid and checks if key exists in each slot
    for row in range(get_grid_height(grid)):
        for col in range(get_grid_width(grid)):
            if (col, row) in locked_positions:
                c = locked_positions[(col, row)]
                grid[row][col] = c                                              
    return grid

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

def draw_text_middle(text, size, color, surface): 
    """
    MODIFIES: surface
    EFFECTS:  Draws the provided text in the middle of the screen
    """ 
    font = pygame.font.SysFont("centurygothic", size, bold = True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + PLAY_WIDTH/2 - label.get_width()/2, 
    top_left_y + PLAY_HEIGHT/2 - label.get_height()/2))

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
    label2 = font.render('Score: ' + str(score), 1, WHITE)
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

    # creates a red border around the play area
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y,
                        PLAY_WIDTH, PLAY_HEIGHT), 4)

    # draws the grid
    draw_grid(surface, grid)