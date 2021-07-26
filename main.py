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
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


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
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    # Represents a tetris piece in the game
    # Has x and y coordinates
    # Has the color
    # Has the rotation
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape 
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    # Creates a 2x2 list
    # The list represents the color value of each cell in the grid
    # If there is a locked position, that means we need to change it as it shouldn't be (0,0,0)
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c

    return grid

def convert_shape_format(shape):
    # Takes in a piece object (called shape)
    # 1. Format
    # Format represents a list that contains the correct rotation/orientation of the current piece at hand
    # If a piece has 4 different kinds of rotations, then format works by doing the following :
    # If the piece is in the first state of rotation, then it will be 0 % 4 which is 0, etc.
    # 2. First For Loop
    # Adds the location of the 0s in the shape, we need to add i and j to the shape.x since it gives us the true coords


    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)] 

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + i, shape.y + j))
    
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    # The line below first creates accepted_pos
    # accepted_pos is a 2d list that has tuples of grid coordinates of the 10x20 rectangle
    accepted_pos = [ [(j, i) for j in range(10) if grid[i][j] == (0,0,0)]  for i in range(20) ]  

    # The line below converts accepted_pos into a single list that has all the grid coordinates
    # accepted_pos stands for accepted positions which serves as a reference of which coordinates are correct
    accepted_pos = [j for sub in accepted_pos for j in sub]

    # Formatted is a list that contains coordinates of a shape that is on the game board
    formatted = convert_shape_format(shape) 

    # This for loop serves as a way to check if the coordinates are in a valid spot
    for pos in formatted:
        if pos not in accepted_pos:
            if pos [1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos 
        if y < 1:
            return True
    
    return False 

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(surface, text, size, color):  
    font = pygame.font.SysFont('comicsans', size, bold = True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))
   
def draw_grid(surface, grid):
    # Draws the the grey grid of the game
    # Does this by looping through every single part of the grid
    # First for loop draws horizontal lines
    # Second for loop draws vertical lines

    sx = top_left_x # Top left x coordinate of the play area
    sy = top_left_y # Top left y coordinate of the play area

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx + play_width, sy + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j*block_size, sy), (sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):
    inc = 0
    # Loops thru grid backwards
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try : 
                    del locked[(j,i)]
                except:
                    continue
    
    if inc > 0:
        # Given a list that looks like [(0,1), (0,0)] --> [(0,0), (0,1)]
        # Get all the posistions that have the same y value in together in the same order
        for key in sorted(list(locked), key = lambda x:x[1])[::-1]:
            x, y = key
            if y < ind :
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    
    return inc



def draw_next_shape(shape, surface):
    # Draws the next shape on the screen and shows the user what it is 
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape:', 1, (255,255,255))

    # This part will focus on drawing the particular label we have created above
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100 

    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
    
    surface.blit(label, (sx + 10, sy - 30))

def update_score(new_score):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > new_score:
            f.write(str(score))
        else: 
            f.write(str(new_score))

def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    
    return score

def draw_window(surface, grid, score=0, last_score = 0):
    # Draws the game window
    # Fills a window with black
    # Draws the play area

    surface.fill((0,0,0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255,255,255))
    
    surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2, 30))

    # Current Score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100 

    surface.blit(label, (sx + 20, sy + 160))

    label = font.render('High Score: ' + str(last_score), 1, (255,255,255))
    
    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface,grid)
    # pygame.display.update()

def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27 # How long it takes for a shape to start falling
    level_time = 0 # How much time has passed
    score = 0 

    draw_window (win, grid)

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime() # Gets the amount of time since clock.tick(), fall_time is in the units of miliseconds
        level_time += clock.get_rawtime()
        clock.tick() # A function that is called once per frame, limits runspeed of a game and makes sure that it runs consistently on all machines

        # At 5 seconds.. (moves faster)
        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1 # moves down the piece by 1
            if not(valid_space(current_piece,grid)) and current_piece.y > 0:
                current_piece.y -= 1
                # We either hit a new piece or have hit the bottom
                # Change piece means that now we need to change a new piece 
                change_piece = True 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                pygame.display.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            # We don't need to update a color of a piece if the piece hasn't showed up at row 0
            if y > -1:
                grid[y][x] = current_piece.color

        # Checking if change_piece is true which basically means if a piece has been locked
        if change_piece:
            for pos in shape_pos: 
                p = (pos[0], pos[1])
                # 1. What is locked_posistions? 
                # locked_posistion is a dictionary in a form like the following :
                # {(1,2):(255,255,255)}
                # Basically a coordinate, and a color associated with said coordinate
                # 2. What does a locked posistion mean?
                # Simply a locked posistion or a posistion that will not move anymore
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10


        
        draw_window (win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # Checking if we have actually lost the game
        # If the game has been lost, the while loop will cancel and jump to the area outside of this while loop
        if check_lost(locked_positions):
            draw_text_middle(win, 'YOU LOST!', 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False 
            update_score(score)


def main_menu(win):
    run = True 
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            if event.type == pygame.KEYDOWN: 
                main(win)
        
    pygame.display.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game