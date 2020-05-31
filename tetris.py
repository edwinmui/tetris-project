import pygame
import sys
# imports all necessary tetris modules
from shape import *
from grid import *
from game import *

"""
                                TETRIS FILE
Contains all the necessary game logic and driver functions needed to execute
the game.
"""

def main(win):
    """
        REQUIRES: win is a valid pygame surface that can be drawn on
        MODIFIES: win
        EFFECTS: Plays the tetris game
    """
    global grid

    locked_positions = {}   # format e.g. "(x, y):(255, 0, 0) = (row, col):(255, 0, 0)"
    grid = create_grid(locked_positions)    # format e.g. "grid = [x][y] = [row][col]""

    change_piece = False
    run = True
    curr_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    score = 0
    fall_speed = 0.27       # initial speed at which blocks fall
    INCREASE_LEVEL = 5      # num seconds before increasing fall speed
    MAX_SPEED = 0.12        # the maximum speed a block can fall
    INCREASE_SPEED = 0.005      # the amount of speed a block is incr. by / lvl
    MILLISECOND = 1000

    # continues to run the game untl the user quits
    while run:
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

                if event.key == pygame.K_RIGHT:
                    # moves piece right
                    curr_piece.x += 1
                    if not(valid_space(curr_piece, grid)):
                        curr_piece.x -= 1

                if event.key == pygame.K_UP:
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
            # updates the next piece and change piece bool
            next_piece = get_shape()
            change_piece = False
            # checks if any rows need to be cleared and adds to total score
            score += clear_rows(grid, locked_positions) * 10

        # draw the game window
        draw_window(win, grid, score)
        # draws the next shape on the right side of screen
        draw_next_shape(next_piece, win)
        # updates the screen
        pygame.display.update()

        # if user LOST
        if check_lost(locked_positions):
            YOU_LOST_FONT_SIZE = 80
            draw_text_middle('YOU LOST!', YOU_LOST_FONT_SIZE, WHITE, win)
            pygame.display.update()
            pygame.time.delay(MILLISECOND * 2)
            run = False
            update_score(score)


def main_menu(win):
    pygame.font.init()
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
