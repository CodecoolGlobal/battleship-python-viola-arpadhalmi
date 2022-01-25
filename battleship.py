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


player1_board = [['0']*5 for x in range(5)]


def custom_boards():
    pass


def menu():
    pass


def print_board(board):
    print(bcolors.BOLD + '  | 1 2 3 4 5' + bcolors.ENDC)
    print('--------------')
    ch = 'A'
    for row in board:
        print(f"{bcolors.BOLD}{ch}{bcolors.ENDC} | {' '.join(row)}")
        ch = chr(ord(ch) + 1)


def print_board_yield(board):
    yield(bcolors.BOLD + '  | 1 2 3 4 5' + bcolors.ENDC)
    yield('--------------')
    ch = 'A'
    for row in board:
        yield(f"{bcolors.BOLD}{ch}{bcolors.ENDC} | {' '.join(row)}")
        ch = chr(ord(ch) + 1)

print_board(player1_board)


def get_direction():
    dir = ['V', 'H']
    try:
        direction = input('please give a direction (v, h): ').upper()
        if direction in dir:
            return direction
        else:
            return get_direction()
    except ValueError:
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
        return get_length()


def get_coordinates_ship1(board):
    coords_letters = {
        'A' : 0,
        'B' : 1,
        'C' : 2,
        'D' : 3,
        'E' : 4,
    }
    coords_numbers = {
        '1' : 0,
        '2' : 1,
        '3' : 2,
        '4' : 3,
        '5' : 4
    }

    # ship_1 = 3
    # ship_2 = 2
    count = 1
    try:
        while count > 0:
            row, column = input('give me a coordinate (A,B,C,D,E--1,2,3,4,5): ').upper()
            if row in coords_letters and column in coords_numbers:
                if board[coords_letters[row]][coords_numbers[column]] == '0':
                    count -= 1
                    # board[coords_letters[row]][coords_numbers[column]] = bcolors.Blue + "X" + bcolors.ENDC
                    return coords_letters[row], coords_numbers[column]
                else:
                    print('this space has already taken, choose another one')
                    return get_coordinates_ship1(board)
            else:
                print(bcolors.WARNING + 'wrong value, give me valid value' + bcolors.ENDC) # ha nincs a megadott értékek között
                return get_coordinates_ship1(board)
    except ValueError:
        print(bcolors.WARNING + 'invalid input!' + bcolors.ENDC) # ha pl több, mint 3 karakter az input
        return get_coordinates_ship1(board)


    
# print(get_coordinates_ship1(player1_board))
print(get_length())




def validate_grid_and_place_ship(board, row, col, dir, len, start_row, end_row, start_col, end_col):
    # check the row or col to see if it is safe to place a ship there
    # return true or false


    all_valid = True
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if board[row][col] != '0':
                all_valid = False
                break
    if all_valid:
      
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                if dir == 'H' and len == 2:
                    board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
                    board[row][col+1] = bcolors.Blue + "X" + bcolors.ENDC
                elif dir == 'V' and len == 2:
                    board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
                    board[row+1][col] = bcolors.Blue + "X" + bcolors.ENDC
                else:
                    board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
                print_board(board)

    return all_valid

    


def try_to_place_ship(row, col, direction, length):
    grid_size = 5
    # based on dir will call a helper method to try and place the ship
    # returns validate_grid... which will be true or false

    start_row, end_row, start_col, end_col = row, row + 1, col, col + 1 # A5--- > 0 1 4 5
   
    if direction == 'H':
        if col + length > grid_size:
            print('too long')
            return False
        start_col = col - length + 1
        end_col = col + length
        
        print('ok')
    elif direction == 'V':
        if row + length > grid_size:
            print('too long')
            return False
        start_row = row - length + 1
        end_row = row + length
        print('ok')

    return validate_grid_and_place_ship(player1_board, row_coord, column_coord, direction, int(length), start_row, end_row, start_col, end_col)



# print(try_to_place_ship(row_coord, column_coord, direction, int(length)))
