import pygame
import sys
from grid import get_grid_height

"""
                                GAME FILE
Contains all functions necessary to handle core game logic such as checking if
the user loses, tracking the previous highest score , etc.
"""

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

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)
GREY = (120, 120, 120)


def check_lost(positions):
    """
    EFFECTS: Returns whether any of the currently placed blocks in the passed-
             in locked_positions dictionary are above the screen, 
             a.k.a. resulting in a loss
    """
    # loops through all positions and checks if y position is still less than 1
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def max_score():
    with open('scores.txt', 'r') as r_file:
        lines = r_file.readlines()
        score = lines[0].strip()
    return score


def update_score(new_score):
    # obtains the current highest score
    old_score = max_score()

    # updates score if new scores is higher than old score
    with open('scores.txt', 'w') as w_file:
        if int(new_score) > int(old_score):
            w_file.write(str(new_score))
        else:
            w_file.write(str(old_score))


def clear_rows(grid, locked_positions):
    """
    MODIFIES: grid, locked
    EFFECTS:  Removes all rows of the grid that are full based on locked 
              positions, meaning no empty squares exist, and returns the number 
              of rows cleared
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
                          key=lambda x: x[1], reverse=True):
            x, y = key
            # if row is above the deleted row, shift it down
            if y < deleted_index:
                # updates locked positions with the shifted key
                new_key = (x, y + deleted_index)
                locked_positions[new_key] = locked_positions.pop(key)

    # returns the number of rows the player clears
    return cleared_rows
