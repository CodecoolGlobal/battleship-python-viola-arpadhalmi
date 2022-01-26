import string

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


board =  [['0']*5 for x in range(5)]
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
    coords_letters = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4}
    coords_numbers = {'1':0, '2':1, '3':2, '4':3, '5':4}

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
    if board[row][col] == '0': return True
    else: return False


def validate_inner_ships_area(board, row, col): # col,row !=0 and col,row !=4
    up = row - 1
    down = row + 1
    left = col - 1
    right = col + 1
    if board[up][col] == '0' and board[down][col] == '0' and board[row][left] == '0' and board[row][right] == '0':
         return True
    else: return False



# ------- CORNER SHIPS ------
 # 0.0, 4.4, 0.4, 4.0 -> free? [0.1,1.0], [3.4,4.3], [0.3,1.4], [3.0, 4.1]
def validate_00_corner_ships_area(board):
    if board[0][1] == '0' and board[1][0] == '0':return True
    else: return False
    

def validate_44_corner_ships_area(board): 
    if board[3][4] == '0' and board[4][3] == '0':return True
    else: return False

    
def validate_04_corner_ships_area(board):
    if board[0][3] == '0' and board[1][4] == '0':return True
    else: return False

    
def validate_40_corner_ships_area(board): 
    if board[3][0] == '0' and board[4][1] == '0':return True
    else: return False
    

# ------- WALL SHIPS--------

# 0.1, 0.2, 0.3  upper board -- free? [0.0,0.2,1.1], [0.1,0.3,1.2], [0.2,0.4,1.3]
def validate_upper_wall_ships(board):
    first = board[0][0] ==  board[0][2] ==  board[1][1] == '0'
    second = board[0][1] == board[0][3] == board[1][2]  == '0'
    third = board[0][2] == board[0][4] == board[1][3] == '0'
    print(first, second, third)
    if first and second and third:
        return True
    else: return False
  


#  1.0,2.0,3.0   left board -- free? [0.0,1.1,2.0], [1.0,2.1,3.0], [2.0,3.1,4.0]
def validate_left_wall_ships(board):
    first = board[0][0] == '0' and board[1][1] == '0' and board[2][0]
    second = board[1][0] == '0' and board[2][1] == '0' and board[3][0]
    third = board[2][0] == '0' and board[3][1] == '0' and board[4][0]
    if first and second and third:
        return True
    else: return False
        


# 4.1, 4.2, 4.3  bottom board -- free? [4.0, 3.1, 4.2], [4.1,3.2,4.3], [4.2, 3.3, 4.4]
def validate_bottom_wall_ships(board):
    first = board[4][0] == '0' and board[3][1] == '0' and board[4][2]
    second = board[4][1] == '0' and board[3][2] == '0' and board[4][3]
    third =  board[4][2] == '0' and board[3][3] == '0' and board[4][4]
    if first and second and third:
        return True
    else: return False



# 1.4, 2.4, 3.4 right board -- free? [0.4, 1.3, 2.4], [1.4, 2.3, 3.4], [2.4, 3.3, 4.4]
def validate_right_wall_ships(board):
    first = board[0][4] == '0' and board[1][3] == '0' and board[2][4]
    second = board[1][4] == '0' and board[2][3] == '0' and board[3][4]
    third = board[2][4] == '0' and board[3][3] == '0' and board[4][4]
    if first and second and third:
        return True
    else: return False



# ------ validate and place -----

def validate_and_place_inner(board, row, col):
    is_validate_area = validate_inner_ships_area(board, row, col)
    is_validate_empty = validate_is_empty(board, row, col)
    if is_validate_area and is_validate_empty:
        player1_b[row][col] = bcolors.Blue + "X" + bcolors.ENDC
        print_board(board)
    else:
        print(bcolors.WARNING + 'you can\'t place your ship here' + bcolors.ENDC)
        return placing_ships(board)


def validate_and_place_corner_ships(valid_corner, board, row, col):
    is_corner_valid = valid_corner
    is_empty = validate_is_empty(board, row, col)
    if is_corner_valid and is_empty:
        board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
        print_board(board)
    else:
        print(bcolors.WARNING + 'you can\'t place your ship here' + bcolors.ENDC)
        return placing_ships(board)


def validate_and_place_wall_ships(valid_wall, board, row, col):
    wall_validate = valid_wall
    print(wall_validate)
    is_empty = validate_is_empty(board, row,col)
    print(is_empty)
    if wall_validate and is_empty:
        board[row][col] = bcolors.Blue + "X" + bcolors.ENDC
        print_board(board)
    else:
        print(bcolors.WARNING + '0wall you can\'t place your ship here' + bcolors.ENDC)
        return placing_ships(board)

# ----- validators -----

corner_validators = [
    validate_00_corner_ships_area(player1_b), 
    validate_04_corner_ships_area(player1_b), 
    validate_40_corner_ships_area(player1_b), 
    validate_44_corner_ships_area(player1_b)
    ]

wall_validators = [
    validate_upper_wall_ships(player1_b), 
    validate_left_wall_ships(player1_b), 
    validate_bottom_wall_ships(player1_b), 
    validate_right_wall_ships(player1_b)
    ]



player1_ship_1 = 3
player1_ship_2 = 2

player2_ship_1 = 3
player2_ship_2 = 2


def placing_ships(player1_b):
    global player1_ship_1
    global player1_ship_2
    print_board(player1_b)   
    lenght = get_length()
    direction = get_direction()
    while player1_ship_1 > 0:
        if lenght == 1:
            row, col = get_coordinates_ship(player1_b)
            # if it's inner ship
            if row != 0 and row != 4 and col !=0 and col!=4:
                validate_and_place_inner(player1_b,row,col)
                player1_ship_1-=1

            # if it's in corner 
            elif row == 0 and col == 0:
                validate_and_place_corner_ships(corner_validators[0], player1_b, row, col)
                player1_ship_1-=1

            elif row == 0 and col == 4:
                validate_and_place_corner_ships(corner_validators[1],player1_b, row, col)
                player1_ship_1-=1

            elif row == 4 and col == 0:
                validate_and_place_corner_ships(corner_validators[2],player1_b, row, col)
                player1_ship_1-=1
               
            elif row == 4 and col == 4:
                validate_and_place_corner_ships(corner_validators[3],player1_b, row, col)
                player1_ship_1-=1

            # -- upper board
            elif row == 0 and (col == 1 or col == 2 or col == 3):
                validate_and_place_wall_ships(wall_validators[0],player1_b, row, col)
                player1_ship_1-=1
            # -- left board
            elif col == 0 and (row == 1 or row == 2 or row == 3):
                validate_and_place_wall_ships(wall_validators[1],player1_b, row, col)
                player1_ship_1-=1
            # -- bottom board
            elif row == 4 and (col == 1 or col == 2 or col == 3):
                validate_and_place_wall_ships(wall_validators[2],player1_b, row, col)
                player1_ship_1-=1
            # -- right board
            elif col == 0 and (row == 1 or row == 2 or row == 3):
                validate_and_place_wall_ships(wall_validators[3],player1_b, row, col)
                player1_ship_1-=1

def translate_coords(coordinates, size=5):
    alphabet = string.ascii_uppercase
    coords_letters = {letter: i for i, letter in enumerate(alphabet)}
    coords_numbers = {j+1: j for j in range(size)}
    translated_row = coords_letters[coordinates[0]]
    translated_col = coords_numbers[int(coordinates[1])]
    return translated_row, translated_col

# player_1_ship_1 = ['A1', 'C3'] 
# player_1_ship_2 = [['A2', 'A3'], ['B1','C1']]
# for i in range(len(player_1_ship_2)):
#    for j in range(len(player_1_ship_2[i])):
    # if coordinate in player_1_ship2[i]:
    #    if player_1_ship2[i][j] == 'H':
    #       player_1_ship2[i] = ['S', 'S']     
    #    else:
    #    player_1_ship_2[i][j] = 'H'
#                  

def validate_shoot(board, row, col):
    if (board[row][col-1] == '0' and board[row][row +1] == '0' and board[row-1][col] == '0' and board[row +1][col] == '0') or \
    (board[row][col-1] == 'H' or board[row][row +1] == 'H' or board[row-1][col] == 'H' or board[row +1][col] == 'H'):
        board[row][col] = 'S'
        if 'H' == board[row][col -1]:
            board[row][col] = 'S'
        elif 'H' == board[row][col +1]:
            board[row][col +1] = 'S'
        elif 'H' == board[row -1][col]:
            board[row -1][col] = 'S'
        elif 'H' == board[row + 1][col]:
            board[row + 1][col] = 'S'
        print('You\'ve sunk a ship!')
    elif (board[row][col-1] == '0' and board[row][row +1] == '0' and board[row-1][col] == '0' and board[row +1][col] == '0') and \
    (board[row][col-1] == '0' and board[row][row +1] == '0' and board[row-1][col] == '0' or board[row +1][col] == '0'):
        board[row][col] = 'S'
        print('You\'ve sunk a ship!')
    else:
        board[row][col] = 'H'
        print('You\'ve hit a ship!')



def shooting(board):
    #while coord not valid:
    coordinate = input('Where do you want to shoot?\n').upper()
    row = translate_coords(coordinate)[0]
    col = translate_coords(coordinate)[1]
        #validate_coord(coordinate)
    if board[row][col] == '0':
        board[row][col] = 'M'
        print('You\'ve missed!')
    elif board[row][col] == 'X':
        validate_shoot(board, row, col)



if __name__ == '__main__':
    placing_ships(player1_b)
    while True:
        print('Player 1 pls shoot')
        shooting(player1_b)
        print_board(player1_b)
    # print('Player 2 pls shoot')
    # shooting(board, player)


# placing ships

# player 1 place ships

# 1 block ships = 3
# 2 block ships = 2
# board = print_board(player1)
# length = get the length (1,2) --> return 1 or 2 --> reduce the number of that size ships
# direction = get_direction (V, H)

# while 1_block > 0 and 2_block > 0:

#       if length == 1:
#           coords = ask ship1 coords from user
#           validate coords (if it == '0' and if there are any ship up, down, right, left !out of board range) return true or false
#           if true 
#                place the ship on board
#                1 block -= 
#           else: ask ship1 coords from user
#
#       if length == 2:
#           start-point-row, start-point-col = ask ship2 coords from user 
#           grid = 5
#           validate 2 blocks with 2 functions
#             if V :
#                if start-row + length >= grid --> return true or false
#                   validator1 = if board[start-row][start-col] == '0' and board[start-row + 1][start-col] == '0' --> true or false
#                   validator2 = if there are any ship up, down, right, left !! out of board range) --> true or false
#                   if all validators == true:
#                        place ship
#                        2 block-=1 
#                   else:
#                       print('you can not place here your ship)
#                       return ask ship2 coords from user
#                 else:
#                      print('there is no space to place here your ship')
#                      return ask ship2 coords from user
#               
#             if H :
#                if start-col + length >= grid:
#                    validator1 = if board[start-row][start-col] == '0' and board[start-row][start-col + 1] == '0':
#                    validator2 = if there are any ship up, down, right, left !! out of board range) true or false
#                    if all validators == true:
#                       place ship
#                       2 block-=1
#                    else:
#                       print('you can not place here your ship)
#                       return ask ship2 coords from user
#                else:
#                     print('there is no space to place here your ship')
#                     return ask ship2 coords from user

#  'waiting for the other player (press any button then next player starts placing)
# 1 block ships = 3
# 2 block ships = 2
# print_board(player2)
# .....



# shooting
# display the two hidden boards
# 

