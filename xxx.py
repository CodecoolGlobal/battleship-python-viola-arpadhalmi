import string
import os
from time import sleep
import random
import ai

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


# when placing ships
def print_board(board):
    print(bcolors.BOLD + '  | 1 2 3 4 5' + bcolors.ENDC)
    print('--------------')
    ch = 'A'
    for row in board:
        print(f"{bcolors.BOLD}{ch}{bcolors.ENDC} | {' '.join(row)}")
        ch = chr(ord(ch) + 1)


# when the play starts
def print_board_yield(board):
    yield(bcolors.BOLD + '  | 1 2 3 4 5' + bcolors.ENDC)
    yield('--------------')
    ch = 'A'
    for row in board:
        yield(f"{bcolors.BOLD}{ch}{bcolors.ENDC} | {' '.join(row)}")
        ch = chr(ord(ch) + 1)


def get_direction():
    dir = ['V', 'H']
    try:
        direction = input('please give a direction (v, h): ').upper()
        if direction in dir:
            return direction
        else:
            return get_direction()
    except ValueError:
        print(bcolors.WARNING + 'Please choose between V or H' + bcolors.ENDC) 
        return get_direction()


def get_length():
    len = ['1', '2']
    try:
        length = input('please give ship size (1, 2): ')
        if length in len:
            return int(length)
        else:
            return get_length()
    except ValueError:
        print(bcolors.WARNING + 'Please choose between 1 or 2' + bcolors.ENDC)
        return get_length()


def get_coordinates_ship(board):
    coords_letters = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    coords_numbers = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4}
    row, column = True, True
    try:
        row, column = input('give me a coordinate (A,B,C,D,E--1,2,3,4,5): ').upper()

        if row in coords_letters and column in coords_numbers:
            return coords_letters[row], coords_numbers[column]
        else:
            print(bcolors.WARNING + 'invalid input' + bcolors.ENDC)
            return get_coordinates_ship(board)
    except ValueError:
        print(bcolors.WARNING + 'invalid input!' + bcolors.ENDC)
        return get_coordinates_ship(board)


# ------ FIELD VALIDATION-------
def validate_is_empty(board, row, col):
    return board[row][col] == '0'


def validate_inner_ships_area(board, row, col): # col,row !=0 and col,row !=4
    up = row - 1
    down = row + 1
    left = col - 1
    right = col + 1
    return board[up][col] == '0' and board[down][col] == '0' \
        and board[row][left] == '0' and board[row][right] == '0'


# ------- CORNER SHIPS ------
# 0.0, 4.4, 0.4, 4.0 -> free? [0.1,1.0], [3.4,4.3], [0.3,1.4], [3.0, 4.1]
def validate_00_corner_ships_area(board):
    return board[0][1] == '0' and board[1][0] == '0'


def validate_44_corner_ships_area(board): 
    return board[3][4] == '0' and board[4][3] == '0'


def validate_04_corner_ships_area(board):
    return board[0][3] == '0' and board[1][4] == '0'

  
def validate_40_corner_ships_area(board):
    return board[3][0] == '0' and board[4][1] == '0'
# ------- WALL SHIPS--------


# 0.1, 0.2, 0.3  upper board -- free? [0.0,0.2,1.1], [0.1,0.3,1.2], [0.2,0.4,1.3]
def validate_upper_wall_ships(board, row, col):
    if row == 0 and col == 1:
        first = board[0][0] == board[0][2] == board[1][1] == '0'
        return first
    elif row == 0 and col == 2:
        second = board[0][1] == board[0][3] == board[1][2]  == '0'
        return second
    elif row == 0 and col == 3:
        third = board[0][2] == board[0][4] == board[1][3] == '0'
        return third


#  1.0,2.0,3.0   left board -- free? [0.0,1.1,2.0], [1.0,2.1,3.0], [2.0,3.1,4.0]
def validate_left_wall_ships(board, row, col):
    if row == 1 and col == 0:
        first = board[0][0] == board[1][1] == board[2][0] == '0'
        return first
    if row == 2 and col == 0:
        second = board[1][0] == board[2][1] == board[3][0] == '0'
        return second
    if row == 3 and col == 0:
        third = board[2][0] == board[3][1] == board[4][0] == '0'
        return third


# 4.1, 4.2, 4.3  bottom board -- free? [4.0, 3.1, 4.2], [4.1,3.2,4.3], [4.2, 3.3, 4.4]
def validate_bottom_wall_ships(board, row, col):
    if row == 4 and col == 1:
        first = board[4][0] == board[3][1] == board[4][2] == '0'
        return first
    if row == 4 and col == 2:
        second = board[4][1] == board[3][2] == board[4][3] == '0'
        return second
    if row == 4 and col == 3:
        third = board[4][2] == board[3][3] == board[4][4] == '0'
        return third


# 1.4, 2.4, 3.4 right board -- free? [0.4, 1.3, 2.4], [1.4, 2.3, 3.4], [2.4, 3.3, 4.4]
def validate_right_wall_ships(board, row, col):
    if row == 1 and col == 4:
        first = board[0][4] == board[1][3] ==  board[2][4] == '0'
        return first
    if row == 2 and col == 4:
        second = board[1][4] == board[2][3] == board[3][4] == '0'
        return second
    if row == 3 and col == 4:
        third = board[2][4] == board[3][3] == board[4][4] == '0'
        return third

# ------ validate and place -----


def validate_and_place_inner(board, row, col):
    is_validate_area = validate_inner_ships_area(board, row, col)
    is_validate_empty = validate_is_empty(board, row, col)
    if is_validate_area and is_validate_empty:
        board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
        print_board(board)
        return True
    elif not is_validate_area:
        print(bcolors.WARNING + 'ships are too close!' + bcolors.ENDC)
        return False
    elif not is_validate_empty:
        print(bcolors.WARNING + 'this slot is taken!' + bcolors.ENDC)
        return False


def validate_and_place_corner_ships(valid_corner, board, row, col):
    is_corner_valid = valid_corner
    is_empty = validate_is_empty(board, row, col)
    if is_corner_valid and is_empty:
        board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
        print_board(board)
        return True
    elif not is_corner_valid:
        print(bcolors.WARNING + 'ships are too close!' + bcolors.ENDC)
        return False
    elif not is_empty:
        print(bcolors.WARNING + 'this slot is taken!' + bcolors.ENDC)
        return False


def validate_and_place_wall_ships(valid_wall, board, row, col):
    wall_validate = valid_wall
    is_empty = validate_is_empty(board, row,col)
    if wall_validate and is_empty:
        board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
        print_board(board)
        return True
    elif not wall_validate:
        print(bcolors.WARNING + 'ships are too close!' + bcolors.ENDC)
        return False
    elif not is_empty:
        print(bcolors.WARNING + 'this slot is taken!' + bcolors.ENDC)
        return False


def validate_and_place_vertical_ships(board, row, col):
    grid = 5
    is_valid = row+1 < grid and board[row][col] == board[row+1][col] == '0'
    if is_valid:
        board[row][col] = bcolors.Purple + "X" + bcolors.ENDC
        board[row+1][col] = bcolors.Purple + "X" + bcolors.ENDC
        print_board(board)
        return True
    else:
        print(bcolors.WARNING + 'you can\'t place ship here!' + bcolors.ENDC)
        return False


def validate_and_place_horizontal_ships(board, row, col):
    grid = 5
    is_valid = col+1 < grid and board[row][col] == board[row][col+1] == '0'
    if is_valid:
        board[row][col] = bcolors.Purple + "X" + bcolors.ENDC
        board[row][col+1] = bcolors.Purple + "X" + bcolors.ENDC
        print_board(board)
        return True
    else:
        print(bcolors.WARNING + 'you can\'t place ship here!!' + bcolors.ENDC)
        return False


def place_one_block(board):

    row, col = get_coordinates_ship(board)
    # if it's inner ship
    if row != 0 and row != 4 and col != 0 and col !=4:
        return validate_and_place_inner(board, row, col)

    # if it's in corner
    elif row == 0 and col == 0:
        return validate_and_place_corner_ships(validate_00_corner_ships_area(board), board, row, col)
    elif row == 0 and col == 4:
        return validate_and_place_corner_ships(validate_04_corner_ships_area(board), board, row, col)
    elif row == 4 and col == 0:
        return validate_and_place_corner_ships(validate_40_corner_ships_area(board), board, row, col)
    elif row == 4 and col == 4:
        return validate_and_place_corner_ships(validate_44_corner_ships_area(board), board, row, col)
    # edges
    elif row == 0 and (col == 1 or col == 2 or col == 3):
        return validate_and_place_wall_ships(validate_upper_wall_ships(board, row, col), board, row, col)
    elif col == 0 and (row == 1 or row == 2 or row == 3):
        return validate_and_place_wall_ships(validate_left_wall_ships(board, row, col), board, row, col)
    elif row == 4 and (col == 1 or col == 2 or col == 3):
        return validate_and_place_wall_ships(validate_bottom_wall_ships(board, row, col), board, row, col)
    elif col == 4 and (row == 1 or row == 2 or row == 3):
        return validate_and_place_wall_ships(validate_right_wall_ships(board, row, col), board, row, col)
    else:
        return False


def validate_inner_ship_two(board, row, col, dir):
    if dir == 'V':
        up = row + 1
        right1 = col + 1
        right2 = row + 1, col + 1
        down = row + 2
        left1 = col-1
        left2 = row + 1, col - 1

    if dir == 'H':
        up1 = row - 1
        up2 = row - 1, col + 1
        right = col + 2
        down1 = row + 1
        down2 = row + 1, col + 1
        left = col - 1


def place_two_block(board):
    direction = get_direction()
    row, col = get_coordinates_ship(board)
    if direction == 'V':
        return validate_and_place_vertical_ships(board, row, col)
    elif direction == 'H':
        return validate_and_place_horizontal_ships(board, row, col)
    else:
        return False


def placing_ships(player_board, ships_1, ships_2):
    print_board(player_board)
    valid = True
    while ships_1 > 0:
        if valid:
            placing = place_one_block(player_board)
        if placing:
            ships_1 -= 1
        else:
            return place_one_block(player_board)

    while ships_2 > 0:
        if valid:
            placing2 = place_two_block(player_board)
            if placing2:
                ships_2 -= 1
    return player_board



def main_placing_ships():
    player_1_one_block = 3
    player_1_two_block = 2
    player_2_one_block = 3
    player_2_two_block = 2

    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    
    print(f'\nPLAYER 1 MOVES\n')
    player_1_board = placing_ships(player1_b, player_1_one_block, player_1_two_block)
    os.system(command)

    print("Next player's placement phase...")

    input('Please press enter to continue....')
    os.system(command)

    print(f'\nPLAYER 2 MOVES\n')
    player_2_board = placing_ships(player2_b, player_2_one_block , player_2_two_block)
    os.system(command)

    return player_1_board, player_2_board
# f'player 1\n{print_board(player_1_board_with_ships)}'
# f'player 2\n{print_board(player_2_board_with_ships)}'

# if player_1_board_with_ships[0][0] == bcolors.Purple + "X" + bcolors.ENDC or bcolors.Blue + "X" + bcolors.ENDC:
#     print('SINK')
#     player1_hidden_b[0][0] = bcolors.FAIL + 'H' + bcolors.ENDC


def validate_ship2_shoot(board, row, col, display_board):
    h = bcolors.FAIL + 'H' + bcolors.ENDC
    s = bcolors.FAIL + 'S' + bcolors.ENDC
    try:
        board[row][col] = h
        display_board[row][col] = h
        if board[row][col - 1] == h:
            board[row][col - 1] = s
            board[row][col] = s
            display_board[row][col - 1] = s
            display_board[row][col] = s
            print("You've sunk a ship!")
        elif board[row][col + 1] == h:
            board[row][col + 1] = s
            board[row][col] = s
            display_board[row][col + 1] = s
            display_board[row][col] = s
            print("You've sunk a ship!")
        elif board[row-1][col] == h:
            display_board[row-1][col] = s
            display_board[row][col] = s
            board[row-1][col] = s
            board[row][col] = s
            print("You've sunk a ship!")
        elif board[row + 1][col] == h:
            board[row + 1][col] = s
            board[row][col] = s
            display_board[row + 1][col] = s
            display_board[row][col] = s
            print("You've sunk a ship!")
    except IndexError:
        pass


def check_win(board):
    for i in range(5):
        for j in range(5):
            if board[i][j] == bcolors.Purple + 'X' + bcolors.ENDC or board[i][j] == bcolors.Blue + 'X' + bcolors.ENDC:
                return False
    return True


# def check_win(board):

#     purple = any(bcolors.Purple + 'X' + bcolors.ENDC in b for b in board)
#     blue = any(bcolors.Blue + 'X' + bcolors.ENDC in b for b in board)
#     if purple or blue:
#         return False
#     else: return True
# demo_board1 = [['0', '0', '0', '0', '0'],
# [bcolors.Blue + 'X' + bcolors.ENDC, '0', '0', '0', '0'],
# ['0', '0', '0', bcolors.Purple + 'X' + bcolors.ENDC, bcolors.Purple + 'X' + bcolors.ENDC],
# [bcolors.Blue + 'X' + bcolors.ENDC, '0', '0', '0', '0'],
# ['0', '0', '0', bcolors.Purple + 'X' + bcolors.ENDC, bcolors.Purple + 'X' + bcolors.ENDC]
# ]

# demo_board2 = [['0', '0', '0', '0', '0'],
# [bcolors.Blue + 'X' + bcolors.ENDC, '0','0','0','0'],
# ['0','0','0',bcolors.Purple + 'X' + bcolors.ENDC,bcolors.Purple + 'X' + bcolors.ENDC],
# [bcolors.Blue + 'X' + bcolors.ENDC,'0','0','0','0'],
# ['0','0','0',bcolors.Purple + 'X' + bcolors.ENDC,bcolors.Purple + 'X' + bcolors.ENDC]
]


def main_menu():
    print('''_           _   _   _           _     _       
| |         | | | | | |         | |   (_)      
| |__   __ _| |_| |_| | ___  ___| |__  _ _ __  
| '_ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \ 
| |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) |
|_.__/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/ 
                                        | |    
                                        |_|    
''')
    mode = input('''Choose a mode! 
    Multiplayer mode - 1 
    Single player mode - 2 ''')
    bullet = 0
    if mode == '1':
        while not 5 <= bullet <= 50:
            try:
                bullet = int(input('Choose turn limit (5-50) '))
            except ValueError:
                print('Please choose a number between 5-50')
        lets_sink(bullet)
    elif mode == '2':
        lets_ai()


def player_turn(board, display_board):
    row, col = get_coordinates_ship(board)

    if board[row][col] == bcolors.Blue + "X" + bcolors.ENDC:
        print('You\'ve sunk a 1 block ship')
        board[row][col] = bcolors.FAIL + 'S' + bcolors.ENDC
        display_board[row][col] = bcolors.FAIL + 'S' + bcolors.ENDC
    elif board[row][col] == bcolors.Purple + "X" + bcolors.ENDC:
        validate_ship2_shoot(board, row, col, display_board)
        print('You\'ve hit a 2 block ship')
    elif board[row][col] == '0':
        board[row][col] = bcolors.GREEN + "M" + bcolors.ENDC
        display_board[row][col] = bcolors.FAIL + 'S' + bcolors.ENDC
        print('You\'ve missed!')
    else:
        print('Useless move!')


def lets_ai():
    ai.ai_main_place_ships()

def lets_sink(bullet):
    main_placing_ships()
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    print(f'{bcolors.BOLD}\nRemaining turns: {bullet}{bcolors.ENDC}\n')
    player = True
    print(f'\n   Player1          Player2\n')

    for left, right in zip(print_board_yield(player1_hidden_b), print_board_yield(player2_hidden_b)):
        print(f'{left}    {right}')

    while bullet > 0:
        if player:
            print(f'{bcolors.BOLD}\nPlayer 1\'s shoot phase!{bcolors.ENDC}')
            player_turn(player2_b, player2_hidden_b)
            sleep(2)
            os.system(command)
        else:
            print(f'{bcolors.BOLD}\nPlayer 2\'s shoot phase!{bcolors.ENDC}')
            player_turn(player1_b, player1_hidden_b)
            sleep(2)
            os.system(command)
        
        player = not player
        bullet -= 1
        print(f'{bcolors.BOLD}\nRemaining turns: {bullet}{bcolors.ENDC}\n')

        for left, right in zip(print_board_yield(player1_hidden_b), print_board_yield(player2_hidden_b)):
            print(f'{left}    {right}')

        if check_win(player1_b):
            print('\nPlayer 2 won')
            break
        elif check_win(player2_b):
            print('\nPlayer 1 won')
            break
        if bullet == 0:
            print('\nIt\'s a tie!')


if __name__ == '__main__':

    # player_1_board_with_ships, player_2_board_with_ships = main_placing_ships()
    try:
        main_menu()
    except KeyboardInterrupt:
        print('\nThanks for playing, goodbye.')


def translate_coords(coordinates, size=5):
    alphabet = string.ascii_uppercase
    coords_letters = {letter: i for i, letter in enumerate(alphabet)}
    coords_numbers = {j+1: j for j in range(size)}
    translated_row = coords_letters[coordinates[0]]
    translated_col = coords_numbers[int(coordinates[1])]
    return translated_row, translated_col
