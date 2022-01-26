import os
import random
import xxx

class bcolors:
    Purple = '\033[95m'
    Blue = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


board = [['0']*5 for x in range(5)]
player1_b = [['0']*5 for x in range(5)]
player2_b = [['0']*5 for x in range(5)]
player1_hidden_b = [['0']*5 for x in range(5)]
player2_hidden_b = [['0']*5 for x in range(5)]

def ai_main_place_ships():
    player_1_one_block = 3
    player_1_two_block = 2
    player_2_one_block = 3
    player_2_two_block = 2

    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    ai_board = ai_placing_ships(player2_b, player_2_one_block, player_2_two_block)
    print(f'\nPLAYER 1 MOVES\n')
    player_1_board = xxx.placing_ships(player1_b, player_1_one_block, player_1_two_block)
    os.system(command)

    print("AI's placement phase...")

    input('Please press enter to continue....')
    os.system(command)
    return player_1_board, ai_board


def ai_random():
    random_col = random.randint(0,4)
    random_row = random.randint(0,4)
    print(random_col, random_row)
    return random_row, random_col

def ai_validate_and_place_inner(board, row, col):
    is_validate_area = xxx.validate_inner_ships_area(board, row, col)
    is_validate_empty = xxx.validate_is_empty(board, row, col)
    if is_validate_area and is_validate_empty:
        board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
        xxx.print_board(board)
        return True


def ai_placing_ships(player_board, ships_1, ships_2):
    valid = True
    while ships_1 > 0:
        if valid:
            placing = ai_place_one_block(player_board)
        if placing:
            ships_1 -= 1
        else:
            return ai_place_one_block(player_board)

    while ships_2 > 0:
        if valid:
            placing2 = ai_place_two_block(player_board)
            if placing2:
                ships_2 -= 1
    return player_board


def ai_place_two_block(board):
    while True:
        row, col = ai_random()
        directions = ['v','h']
        random_direction = random.choice(directions)
        if random_direction == 'V':
            return ai_validate_and_place_vertical_ships(board, row, col)
        elif random_direction == 'H':
            return ai_validate_and_place_horizontal_ships(board, row, col)
        else:
            return False

def ai_validate_and_place_inner(board, row, col):
    is_validate_area = xxx.validate_inner_ships_area(board, row, col)
    is_validate_empty = xxx.validate_is_empty(board, row, col)
    if is_validate_area and is_validate_empty:
        board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
        xxx.print_board(board)
        return True

def ai_validate_and_place_wall_ships(valid_wall, board, row, col):
    wall_validate = valid_wall
    is_empty = xxx.validate_is_empty(board, row,col)
    if wall_validate and is_empty:
        board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
        xxx.print_board(board)
        return True

def ai_validate_and_place_vertical_ships(board, row, col):
    grid = 5
    is_valid = row+1 < grid and board[row][col] == board[row+1][col] == '0'
    if is_valid:
        board[row][col] = bcolors.Purple + "X" + bcolors.ENDC
        board[row+1][col] = bcolors.Purple + "X" + bcolors.ENDC
        xxx.print_board(board)
        return True

def ai_validate_and_place_horizontal_ships(board, row, col):
    grid = 5
    is_valid = col+1 < grid and board[row][col] == board[row][col+1] == '0'
    if is_valid:
        board[row][col] = bcolors.Purple + "X" + bcolors.ENDC
        board[row][col+1] = bcolors.Purple + "X" + bcolors.ENDC
        xxx.print_board(board)
        return True


def ai_validate_and_place_corner_ships(valid_corner, board, row, col):
    is_corner_valid = valid_corner
    is_empty = xxx.validate_is_empty(board, row, col)
    if is_corner_valid and is_empty:
        board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
        xxx.print_board(board)
        return True

def ai_place_one_block(board):
    while True:
        row, col = ai_random()
        #row, col = ai_main_place_ships(board)
        # if it's inner ship
        if row != 0 and row != 4 and col != 0 and col != 4:
            return ai_validate_and_place_inner(board, row, col)

        # if it's in corner
        elif row == 0 and col == 0:
            return ai_validate_and_place_corner_ships(xxx.validate_00_corner_ships_area(board), board, row, col)
        elif row == 0 and col == 4:
            return ai_validate_and_place_corner_ships(xxx.validate_04_corner_ships_area(board), board, row, col)
        elif row == 4 and col == 0:
            return ai_validate_and_place_corner_ships(xxx.validate_40_corner_ships_area(board), board, row, col)
        elif row == 4 and col == 4:
            return ai_validate_and_place_corner_ships(xxx.validate_44_corner_ships_area(board), board, row, col)
        # edges
        elif row == 0 and (col == 1 or col == 2 or col == 3):
            return ai_validate_and_place_wall_ships(xxx.validate_upper_wall_ships(board, row, col), board, row, col)
        elif col == 0 and (row == 1 or row == 2 or row == 3):
            return ai_validate_and_place_wall_ships(xxx.validate_left_wall_ships(board, row, col), board, row, col)
        elif row == 4 and (col == 1 or col == 2 or col == 3):
            return ai_validate_and_place_wall_ships(xxx.validate_bottom_wall_ships(board, row, col), board, row, col)
        elif col == 4 and (row == 1 or row == 2 or row == 3):
            return ai_validate_and_place_wall_ships(xxx.validate_right_wall_ships(board, row, col), board, row, col)
        else:
            return False