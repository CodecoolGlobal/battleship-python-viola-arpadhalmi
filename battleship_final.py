import string
import os
import random
from time import sleep


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


def ai_random():
    global board_size
    row = random.randint(0, board_size-1)
    col = random.randint(0, board_size-1)
    return row, col


def ai_random_direction():
    direction = ['v', 'h']
    dir = random.choice(direction)
    return dir



def get_board_size():
    alphabet = string.ascii_lowercase
    size = input('please choose a size between 5 - 9: ')
    if len(size) == 1 and size not in alphabet and int(size) in list(range(5, 10)):
        return int(size)
    else:
        print(bcolors.WARNING + 'invalid input' + bcolors.ENDC)
        return get_board_size()


board_size = get_board_size()

def ai_translate(row, col):
    alphabet = string.ascii_uppercase
    coords_letters = {i: letter for i, letter in enumerate(alphabet)}
    coords_numbers = {j: j+1 for j in range(board_size)}
    translated_row = coords_letters[row]
    translated_col = coords_numbers[int(col)]
    return translated_row, translated_col


# -------- WHEN PLACING SHIPS-----
def print_board(board):
    num = 1
    print('\n')
    list_of_nums = []
    for row in board:
        list_of_nums.append(str(num))
        num += 1
    string_of_nums = ' '.join(list_of_nums)
    print(f'    {bcolors.BOLD}{string_of_nums}{bcolors.ENDC}')
    print('  ' + num * '--')
    ch = 'A'
    for row in board:
        print(f"{bcolors.BOLD}{ch}{bcolors.ENDC} | {' '.join(row)}")
        ch = chr(ord(ch) + 1)
# -----  SHOOTING STARTS ------


def print_board_yield(board):
    num = 1
    yield('\n')
    list_of_nums = []
    for row in board:
        list_of_nums.append(str(num))
        num += 1
    string_of_nums = ' '.join(list_of_nums)
    yield(f'    {bcolors.BOLD}{string_of_nums}{bcolors.ENDC}')
    yield('  ' + num * '--')
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


def want_quit(move):
    if move == "Q":
        print('\n'+bcolors.GREEN + 'Good bye! Thanks for playing!' + bcolors.ENDC + '\n')
        exit()


def translate_coords(coordinates, size):
    alphabet = string.ascii_uppercase
    coords_letters = {letter: i for i, letter in enumerate(alphabet)}
    coords_numbers = {j+1: j for j in range(size)}
    translated_row = coords_letters[coordinates[0]]
    translated_col = coords_numbers[int(coordinates[1])]
    return translated_row, translated_col


# size = 9
# board =  [['0']*size for x in range(size)]

def get_coordinates_ship(board):

    global board_size

    letters = 'ABCDEFGHI'
    numbers = '123456789'

    move = input('Please, give a coordinate ( ABC... | 123... ): ').upper()
    want_quit(move)
    if len(move) == 2 and (move[0] in letters[0:board_size] and move[1] in numbers[0:board_size]):
        coords = translate_coords(move, board_size)
        return coords[0], coords[1]

    else:
        print(bcolors.WARNING + 'invalid input' + bcolors.ENDC)
        return get_coordinates_ship(board)


# print(get_coordinates_ship(board))
# ------ FIELD VALIDATION-------
def validate_is_empty(board, row, col):
    return board[row][col] == '0'


# ----  ONE BLOCK SHIPS----
# ----- INNER SHIP -----

def validate_inner_ships_area(board, row, col):

    return board[row-1][col] == '0' and board[row+1][col] == '0' \
        and board[row][col-1] == '0' and board[row][col+1] == '0'
# ------- CORNER SHIPS ------
# 0.0, 4.4, 0.4, 4.0 -> free? [0.1,1.0], [3.4,4.3], [0.3,1.4], [3.0, 4.1]


def validate_00_corner_ships_area(board, row, col):
    return board[row][col+1] == '0' and board[row+1][0] == '0'


def validate_44_corner_ships_area(board, row, col):
    return board[row-1][col] == '0' and board[row][col-1] == '0'


def validate_04_corner_ships_area(board, row, col):
    return board[row][col-1] == '0' and board[row+1][col] == '0'


def validate_40_corner_ships_area(board, row, col):
    return board[row-1][col] == '0' and board[row][col+1] == '0'
# ------- WALL SHIPS--------
# 0.1, 0.2, 0.3  upper board -- free? [0.0,0.2,1.1], [0.1,0.3,1.2], [0.2,0.4,1.3]


def validate_upper_wall_ships(board, row, col):
    return board[row][col-1] == board[row][col+1] == board[row+1][col] == '0'


#  1.0,2.0,3.0   left board -- free? [0.0,1.1,2.0], [1.0,2.1,3.0], [2.0,3.1,4.0]
def validate_left_wall_ships(board, row, col):
    return board[row-1][col] == board[row][col+1] == board[row+1][col] == '0'


# 4.1, 4.2, 4.3  bottom board -- free? [4.0, 3.1, 4.2], [4.1,3.2,4.3], [4.2, 3.3, 4.4]
def validate_bottom_wall_ships(board, row, col):
    return board[row][col-1] == board[row-1][col] == board[row][col+1] == '0'


# 1.4, 2.4, 3.4 right board -- free? [0.4, 1.3, 2.4], [1.4, 2.3, 3.4], [2.4, 3.3, 4.4]
def validate_right_wall_ships(board, row, col):
    return board[row-1][col] == board[row][col-1] == board[row+1][col] == '0'


# ------ validate and place -----
def validate_and_place_inner(board, row, col, mode=1):
    if mode == 1:
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
    else:
        is_validate_area = validate_inner_ships_area(board, row, col)
        is_validate_empty = validate_is_empty(board, row, col)
        if is_validate_area and is_validate_empty:
            board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
            print_board(board)
            return True
        else:
            return False


def validate_and_place_corner_ships(valid_corner, board, row, col, mode=1):
    if mode == 1:
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
    else:
        is_corner_valid = valid_corner
        is_empty = validate_is_empty(board, row, col)
        if is_corner_valid and is_empty:
            board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
            print_board(board)
            return True
        else:
            return False


def validate_and_place_wall_ships(valid_wall, board, row, col, mode=1):
    if mode == 1:
        wall_validate = valid_wall
        is_empty = validate_is_empty(board, row, col)
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
    else:
        wall_validate = valid_wall
        is_empty = validate_is_empty(board, row, col)
        if wall_validate and is_empty:
            board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
            print_board(board)
            return True
        return False


def validate_and_place_vertical_ships(ship_around, board, row, col, mode=1):
    global board_size
    grid = board_size
    if mode == 1:
        is_valid = row+1 < grid and board[row][col] == board[row+1][col] == '0'
        if is_valid and ship_around:
            board[row][col] = bcolors.Purple + "X" + bcolors.ENDC
            board[row+1][col] = bcolors.Purple + "X" + bcolors.ENDC
            print_board(board)
            return True
        else:
            print(bcolors.WARNING + 'you can\'t place ship here!' + bcolors.ENDC)
            return False
    else:
        is_valid = row+1 < grid and board[row][col] == board[row+1][col] == '0'
        if is_valid and ship_around:
            board[row][col] = bcolors.Purple + "X" + bcolors.ENDC
            board[row+1][col] = bcolors.Purple + "X" + bcolors.ENDC
            print_board(board)
            return True
        return False


def validate_and_place_horizontal_ships(ship_around, board, row, col, mode=1):
    global board_size
    grid = board_size
    if mode == 1:
        is_valid = col+1 < grid and board[row][col] == board[row][col+1] == '0'
        if is_valid and ship_around:
            board[row][col] = bcolors.Purple + "X" + bcolors.ENDC
            board[row][col+1] = bcolors.Purple + "X" + bcolors.ENDC
            print_board(board)
            return True
        else:
            print(bcolors.WARNING + 'you can\'t place ship here!' + bcolors.ENDC)
            return False
    else:
        is_valid = col+1 < grid and board[row][col] == board[row][col+1] == '0'
        if is_valid and ship_around:
            board[row][col] = bcolors.Purple + "X" + bcolors.ENDC
            board[row][col+1] = bcolors.Purple + "X" + bcolors.ENDC
            print_board(board)
            return True
        else:
            return False


# ---- 2 BLOCKS SHIPS ----
# ---- INNERS ----
def validate_inner_ship_vertical(board, row, col):
    if board[row-1][col] == '0' and board[row][col+1] == '0' \
        and board[row+1][col+1] == '0' and board[row+2][col] == '0'\
            and board[row][col-1] == '0' and board[row+1][col-1] == '0':
        return True
    else:
        return False


def validate_inner_ship_horizontal(board, row, col):
    if board[row-1][col] == '0' and board[row-1][col+1] == '0' \
        and board[row][col+2] == '0' and board[row+1][col] == '0'\
            and board[row+1][col+1] == '0' and board[row][col-1] == '0':
        return True
    else:
        return False

# --- CORNERS -----
# ---- vertical ----


def validate_00_corner_ship_vertical(board, row, col):
    return board[row][col+1] == '0' and board[row+1][col+1] == '0' and board[row+2][col] == '0'


def validate_30_corner_ship_vertical(board, row, col):
    return board[row-1][col] == '0' and board[row][col+1] == '0' and board[row+1][col+1] == '0'


def validate_04_corner_ship_vertical(board, row, col):
    return board[row][col-1] == '0' and board[row+1][col-1] == '0' and board[row+2][col] == '0'


def validate_34_corner_ship_vertical(board, row, col):
    return board[row-1][col] == '0' and board[row][col-1] == '0' and board[row+1][col-1] == '0'


def validate_00_corner_ship_horizontal(board, row, col):
    return board[row+1][col] == '0' and board[row+1][col+1] == '0' and board[row+2][col] == '0'


def validate_40_corner_ship_horizontal(board, row, col):
    return board[row-1][col] == '0' and board[row-1][col+1] == '0' and board[row][col+2] == '0'


def validate_03_corner_ship_horizontal(board, row, col):
    return board[row][col-1] == '0' and board[row+1][col] == '0' and board[row+1][col+1] == '0'


def validate_43_corner_ship_horizontal(board, row, col):
    return board[row][col-1] == '0' and board[row-1][col] == '0' and board[row-1][col+1] == '0'


def hoizontal_upper_edges(board, row, col):
    return board[row][col-1] == '0' and board[row+1][col] == '0' \
        and board[row+1][col+1] == '0' and board[row][col+2] == '0'


def horizontal_left_edges(board, row, col):
    return board[row-1][col] == '0' and board[row-1][col+1] == '0' \
        and board[row][col+2] == '0' and board[row+1][col] == '0' and board[row+1][col+1] == '0'


def horizontal_bottom_edges(board, row, col):
    return board[row][col-1] == '0' and board[row-1][col] == '0' \
        and board[row-1][col+1] == '0' and board[row][col+2] == '0'


def horizontal_right_edges(board, row, col):
    return board[row-1][col+1] == '0' and board[row-1][col] == '0' \
        and board[row][col-1] == '0' and board[row+1][col] == '0' and board[row+1][col+1] == '0'


def vertical_upper_edges(board, row, col):
    return board[row][col-1] == '0' and board[row+1][col-1] == '0' \
        and board[row+2][col] == '0' and board[row+1][col+1] == '0' and board[row][col+1] == '0'


def vertical_left_edges(board, row, col):
    return board[row-1][col] == '0' and board[row][col+1] == '0' \
        and board[row+1][col+1] == '0' and board[row+2][col] == '0'


def vertical_bottom_edges(board, row, col):
    return board[row][col-1] == '0' and board[row+1][col-1] == '0' \
        and board[row-1][col] == '0' and board[row][col+1] == '0' and board[row+1][col+1] == '0'


def vertical_right_edges(board, row, col):
    return board[row+1][col] == '0' and board[row][col-1] == '0' \
        and board[row+1][col-1] == '0' and board[row+2][col] == '0'


# ----- PLACE ONE BLOCK -----

# ------- VALIDATE PLACE 1 BLOCK SHIP ------

def place_one_block(board, mode=1):
    global board_size

    if mode == 1:
        row, col = get_coordinates_ship(board)
    else:
        row, col = ai_random()

    # inners  
    if row in list(range(1, board_size-1)) and col in list(range(1,board_size-1)):
        return validate_and_place_inner(board, row, col, mode)

     # edges
    elif row == 0 and col in list(range(1, board_size-1)):
        return validate_and_place_wall_ships(validate_upper_wall_ships(board, row, col), board, row, col, mode)
    elif col == 0 and row in list(range(1, board_size-1)):
        return validate_and_place_wall_ships(validate_left_wall_ships(board, row, col), board, row, col, mode)
    elif row in list(range(4, board_size)) and col in list(range(1,board_size-1)):
        return validate_and_place_wall_ships(validate_bottom_wall_ships(board, row, col), board, row, col, mode)
    elif row in list(range(1, board_size-1)) and col in list(range(4,board_size)):
        return validate_and_place_wall_ships(validate_right_wall_ships(board, row, col), board, row, col, mode)

    # corners
    elif row == 0 and col == 0:
        return validate_and_place_corner_ships(validate_00_corner_ships_area(board, row, col), board, row, col, mode)
    elif row == 0 and col in list(range(4,board_size)):
        return validate_and_place_corner_ships(validate_04_corner_ships_area(board, row, col), board, row, col, mode)
    elif row in list(range(4,board_size)) and col == 0:
        return validate_and_place_corner_ships(validate_40_corner_ships_area(board, row, col), board, row, col, mode)
    elif row in list(range(4,board_size)) and col in list(range(4, board_size)):
        return validate_and_place_corner_ships(validate_44_corner_ships_area(board, row, col), board, row, col, mode)


    else:
        return False


# ------VALIDATE AND PLACE TWO BLOCK SHIPS-------



def place_two_block(board, mode=1):

    global board_size
    if mode == 1:
        direction = get_direction()
        row, col = get_coordinates_ship(board)
    else:
        direction = ai_random_direction()
        direction = direction.upper()
        row, col = ai_random()


    if direction == 'H':

         # inner ships
        if row in list(range(1, board_size-1)) and col in list(range(1, board_size-2)):
            return validate_and_place_horizontal_ships(validate_inner_ship_horizontal(board, row, col), board, row, col, mode)

        # edges
        if row == 0 and col in list(range(1, board_size-2)):
            return validate_and_place_horizontal_ships(hoizontal_upper_edges(board, row, col), board, row, col, mode)
        
        elif row in list(range(1, board_size-1)) and col == 0:
            return validate_and_place_horizontal_ships(horizontal_left_edges(board, row, col), board, row, col, mode)

        elif row in list(range(1, board_size-1)) and col in list(range(3, board_size-1)):
            return validate_and_place_horizontal_ships(horizontal_right_edges(board, row, col), board, row, col, mode)
       
        elif row in list(range(4, board_size)) and col in list(range(1, board_size-2)):
            return validate_and_place_horizontal_ships(horizontal_bottom_edges(board, row, col), board, row, col, mode)
        # corner ships
        elif row == 0 and col == 0:
            return validate_and_place_horizontal_ships(validate_00_corner_ship_horizontal(board, row, col), board, row, col, mode)
        
        elif row in list(range(4, board_size)) and col == 0:
            return validate_and_place_horizontal_ships(validate_40_corner_ship_horizontal(board, row, col), board, row, col, mode)
    
        elif row == 0 and col in list(range(3, board_size-1)):
            return validate_and_place_horizontal_ships(validate_03_corner_ship_horizontal(board, row, col), board, row, col, mode)
        
        elif row in list(range(4, board_size)) and col in list(range(3, board_size-1)):
            return validate_and_place_horizontal_ships(validate_43_corner_ship_horizontal(board, row, col), board, row, col, mode)
      


        elif row in list(range(0, board_size)) and col in list(range(4, board_size)):
            print(bcolors.WARNING + 'You can\'t place ship here' + bcolors.ENDC)
            return place_two_block(board, mode)

    elif direction == 'V':
             # inner ships
        if row in list(range(1, board_size-2)) and col in list(range(1, board_size-1)):
            return validate_and_place_vertical_ships(validate_inner_ship_vertical(board, row, col),board, row, col, mode)
        
         # edges
        if row in list(range(1, board_size-2)) and col == 0:
            return validate_and_place_vertical_ships(vertical_left_edges(board, row, col), board, row, col, mode)

        elif row in list(range(3, board_size-1)) and col in list(range(1, board_size-1)):
            return validate_and_place_vertical_ships(vertical_bottom_edges(board, row, col), board, row, col, mode)

        elif row in list(range(1, board_size-2)) and col in list(range(4, board_size)):
            return validate_and_place_vertical_ships(vertical_right_edges(board, row, col), board, row, col, mode)

        elif row == 0 and col in list(range(1, board_size-1)):
            return validate_and_place_vertical_ships(vertical_upper_edges(board, row, col), board, row, col, mode)
        # corner ships

        elif row == 0 and col == 0:
            return validate_and_place_vertical_ships(validate_00_corner_ship_vertical(board,row, col), board, row, col, mode)

        elif row in list(range(3, board_size-1)) and col == 0:
            return validate_and_place_vertical_ships(validate_30_corner_ship_vertical(board,row, col), board, row, col, mode)

        elif row == 0 and col in list(range(4, board_size)):
            return validate_and_place_vertical_ships(validate_04_corner_ship_vertical(board,row, col), board, row, col, mode)

        elif row in list(range(3, board_size-8)) and col in list(range(4, board_size)):
            return validate_and_place_vertical_ships(validate_34_corner_ship_vertical(board,row, col), board, row, col, mode)
        
    

        elif row in list(range(4, board_size)) and col in list(range(0, board_size)):
            print(bcolors.WARNING + 'You can\'t place ship here' + bcolors.ENDC)
            return place_two_block(board, mode)
    
    else: return False


def placing_ships(player_board, ships_1, ships_2, mode, ship1, ship2):
    print_board(player_board)
    valid = True
    while ships_1 > 0:
        print(f'\n You got {ship1} pieces of one-block ships.')
        print(f'{bcolors.CYAN} {ships_1} {bcolors.ENDC} piece(s) of one block ship left\n')
        if valid:
            placing = place_one_block(player_board, mode)
            if placing:
                ships_1 -= 1
        else:
            return place_one_block(player_board, mode)

    while ships_2 > 0:
        print(f'\n You got {ship2} pieces of two-block ships.')
        print(f'{bcolors.Purple} {ships_2}{bcolors.ENDC} piece(s) of one block ship left\n')

        if valid:
            placing2 = place_two_block(player_board, mode)
            if placing2:
                ships_2 -= 1
        else:
            return place_two_block(player_board, mode)
    return player_board


def main_placing_ships(mode=1):

    global board_size

    player1_b = [['0']*board_size for x in range(board_size)]
    player2_b = [['0']*board_size for x in range(board_size)]
    player1_hidden_b = [['0']*board_size for x in range(board_size)]
    player2_hidden_b = [['0']*board_size for x in range(board_size)]


    
    player_1_one_block = 3
    player_1_two_block = 2
    player_2_one_block = 3
    player_2_two_block = 2

    player_1_one_blockx = 3
    player_1_two_blockx = 2
    player_2_one_blockx = 3
    player_2_two_blockx = 2

    if board_size in [6,7]:
        player_1_one_block = 4
        player_1_two_block = 3
        player_2_one_block = 4
        player_2_two_block = 3

        player_1_one_blockx = 4
        player_1_two_blockx = 3
        player_2_one_blockx = 4
        player_2_two_blockx = 3



    if board_size in [8,9]:
        player_1_one_block = 5
        player_1_two_block = 4
        player_2_one_block = 5
        player_2_two_block = 4

        player_1_one_blockx = 5
        player_1_two_blockx = 4
        player_2_one_blockx = 5
        player_2_two_blockx = 4

    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    if mode == 1:
        print(f'{bcolors.BOLD} \nPLAYER 1 MOVES\n {bcolors.ENDC}')
        player_1_board = placing_ships(player1_b, player_1_one_block, player_1_two_block, mode, player_1_one_blockx, player_1_two_blockx)
        os.system(command)

        print("Next player's placement phase...")

        input('Please press enter to continue....')
        os.system(command)

        print(f'{bcolors.BOLD} \nPLAYER 2 MOVES\n {bcolors.ENDC}')
        player_2_board = placing_ships(player2_b, player_2_one_block, player_2_two_block, mode, player_1_one_blockx, player_1_two_blockx)
        os.system(command)
    else:
        player_2_board = placing_ships(player2_b, player_2_one_block, player_2_two_block, mode, player_1_one_blockx, player_1_two_blockx)
        os.system(command)
        print('\nPLAYER 1 MOVES\n')
        player_1_board = placing_ships(player1_b, player_1_one_block, player_1_two_block, 1, player_1_one_blockx, player_1_two_blockx)

    return player_1_board, player_2_board, player1_hidden_b, player2_hidden_b


def check_win(board):
    purple = bcolors.Purple + 'X' + bcolors.ENDC
    blue = bcolors.Blue + 'X' + bcolors.ENDC
    for i in range(5):
        for j in range(5):
            if board[i][j] == purple or board[i][j] == blue:
                return False
    return True


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


def player_turn(board, display_board, mode=1):
    if mode == 1:
        row, col = get_coordinates_ship(board)
        if board[row][col] == bcolors.Blue + "X" + bcolors.ENDC:
            print('You\'ve sunk a 1 block ship')
            board[row][col] = bcolors.FAIL + 'S' + bcolors.ENDC
            display_board[row][col] = bcolors.FAIL + 'S' + bcolors.ENDC
        elif board[row][col] == bcolors.Purple + "X" + bcolors.ENDC:
            validate_ship2_shoot(board, row, col, display_board)
            print('You\'ve hit a 2 block ship')
        elif board[row][col] == '0':
            board[row][col] = bcolors.WARNING + "M" + bcolors.ENDC
            display_board[row][col] = bcolors.WARNING + 'M' + bcolors.ENDC
            print('You\'ve missed!')
        else:
            print('Useless move!')
    else:
        row, col = ai_random()
        translate_row = ai_translate(row, col)[0]
        translate_col = ai_translate(row, col)[1]
        print(f'AI\'s move was: {translate_row}{translate_col}')
        if board[row][col] == bcolors.Blue + "X" + bcolors.ENDC:
            print('The AI sunk a 1 block ship!')
            board[row][col] = bcolors.FAIL + 'S' + bcolors.ENDC
            display_board[row][col] = bcolors.FAIL + 'S' + bcolors.ENDC
        elif board[row][col] == bcolors.Purple + "X" + bcolors.ENDC:
            validate_ship2_shoot(board, row, col, display_board)
            print('The AI hit a 2 block ship')
        elif board[row][col] == '0':
            board[row][col] = bcolors.WARNING + "M" + bcolors.ENDC
            display_board[row][col] = bcolors.WARNING + 'M' + bcolors.ENDC
            print('The AI missed!')
        else:
            print('The AI made a stupid move :)')


def lets_sink(bullet, mode=1):
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    if mode == 1:
        player_1_board_with_ships, player_2_board_with_ships, player1_hidden_b, player2_hidden_b = main_placing_ships()
        os.system(command)
        print(f'{bcolors.BOLD}\nRemaining turns: {bullet}{bcolors.ENDC}\n')
        player = True
        print('\n   Player1          Player2\n')

        for left, right in zip(print_board_yield(player1_hidden_b), print_board_yield(player2_hidden_b)):
            print(f'{left}    {right}')

        while bullet >= 0:
            if player:
                print(f'{bcolors.BOLD}\nPlayer 1\'s shoot phase!{bcolors.ENDC}')
                player_turn(player_2_board_with_ships, player2_hidden_b)
                sleep(2)
                os.system(command)
            else:
                print(f'{bcolors.BOLD}\nPlayer 2\'s shoot phase!{bcolors.ENDC}')
                player_turn(player_1_board_with_ships, player1_hidden_b)
                sleep(2)
                os.system(command)
            
            player = not player
            if not player:
                bullet -= 1
            os.system(command)
            print(f'{bcolors.BOLD}\nRemaining turns: {bullet}{bcolors.ENDC}\n')
            print('\n   Player1          Player2\n')
            for left, right in zip(print_board_yield(player1_hidden_b), print_board_yield(player2_hidden_b)):
                print(f'{left}    {right}')

            if check_win(player_1_board_with_ships):
                os.system(command)
                print('\nPlayer 2 won')
                break
            elif check_win(player_2_board_with_ships):
                os.system(command)
                print('\nPlayer 1 won')
                break
            if bullet == 0:
                os.system(command)
                print('\nIt\'s a tie!')
                break
        print('\n   Player1          Player2\n')
        for left, right in zip(print_board_yield(player_1_board_with_ships), print_board_yield(player_2_board_with_ships)):
            print(f'{left}    {right}')
    else:
        player_1_board_with_ships, player_2_board_with_ships, player1_hidden_b, player2_hidden_b = main_placing_ships(2)
        os.system(command)
        print(f'{bcolors.BOLD}\nRemaining turns: {bullet}{bcolors.ENDC}\n')
        player = True
        print('\n   Player1          AI\n')

        for left, right in zip(print_board_yield(player1_hidden_b), print_board_yield(player2_hidden_b)):
            print(f'{left}    {right}')

        while bullet >= 0:
            if player:
                print(f'{bcolors.BOLD}\nPlayer 1\'s shoot phase!{bcolors.ENDC}')
                player_turn(player_2_board_with_ships, player2_hidden_b)
                sleep(2)
                os.system(command)
            else:
                print(f'{bcolors.BOLD}\nAI\'s shoot phase!{bcolors.ENDC}')
                player_turn(player_1_board_with_ships, player1_hidden_b, 2)
                sleep(2)
                os.system(command)

            player = not player
            if not player:
                bullet -= 1
            print(f'{bcolors.BOLD}\nRemaining turns: {bullet}{bcolors.ENDC}\n')
            print('\n   Player1          AI\n')
            for left, right in zip(print_board_yield(player1_hidden_b), print_board_yield(player2_hidden_b)):
                print(f'{left}    {right}')

            if check_win(player_1_board_with_ships):
                os.system(command)
                print('\nThe AI won')
                break
            elif check_win(player_2_board_with_ships):
                os.system(command)
                print('\nPlayer 1 won')
                break
            if bullet == 0:
                os.system(command)
                print('\nIt\'s a tie!')
                break
        print('\n   Player1          AI\n')
        for left, right in zip(print_board_yield(player_1_board_with_ships),
                    print_board_yield(player_2_board_with_ships)):
                print(f'{left}    {right}')


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
    mode = 0
    while mode not in (1, 2):
        try:
            mode = int(input('''Choose a mode!
            1 - Multiplayer mode
            2 - Single player mode\n'''))
        except ValueError:
            print('Please provide a number (1 or 2).')
    bullet = 0
    if mode == 1:
        while not 5 <= bullet <= 50:
            try:
                bullet = int(input('Choose turn limit (5-50) '))
            except ValueError:
                print('Please choose a number between 5-50')
        lets_sink(bullet)
    elif mode == 2:
        while not 5 <= bullet <= 50:
            try:
                bullet = int(input('Choose turn limit (5-50) '))
            except ValueError:
                print('Please choose a number between 5-50')
        lets_sink(bullet, mode)


if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        want_quit('Q')
