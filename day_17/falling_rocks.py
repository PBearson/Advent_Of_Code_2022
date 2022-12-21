# Find the height of the stack of rocks after 2022 rocks have stopped falling

with open("day_17/sample_input.txt", "r") as f:
    input = f.read().splitlines()

# Initialize the room. The width is exactly 7 units wide. The maximum height
# cannot be more than 8088 units tall, since that is the length of the longest 
# rock.
def initialize_room():
    room_width = 7
    room_height = 4 * 2022

    room_row = ['.'] * room_width
    room = [room_row] * room_height

    return room

# Get the next rock type based on the number of rocks dropped so far. The next rock
# type is identified by a string, which are as follows:
# - "W": wide (4 units in a row)
# - "+": plus (3 units long, 3 units wide)
# - "L": backwards L (3 units long, 3 units wide, joined at the bottom-right corner)
# - "T": tall (4 units in a column)
# - "O": big (2 by 2)
def get_next_rock(rocks_dropped):
    index = rocks_dropped % 5

    if index == 0:
        return "W"
    elif index == 1:
        return "+"
    elif index == 2:
        return "L"
    elif index == 3:
        return "T"
    return "O"

# Check if a unit in the room is empty
def is_empty(room, pos_x, pos_y):
    return room[pos_y][pos_x] == '.'

# Return True if moving left would lead to an out-of-bounds.
# Since the rock X position is already relative to its left-most
# position, checking this bound is straightforward.  
def move_left_is_out_of_bounds(rock_type, rock_x):
    return rock_x == 0

# Return True if moving right would lead to an out-of-bounds
def move_right_is_out_of_bounds(rock_type, rock_x, max_x):

    # For wide type: Check X + 3
    if rock_type == "W":
        return rock_x + 3 == max_x

    # For + and L type: Check X + 2
    if rock_type in "+L":
        return rock_x + 2 == max_x

    # For tall type: Check X
    if rock_type == "T":
        return rock_x == max_x

    # For big type: Check X + 1
    if rock_type == "O":
        return rock_type + 1 == max_x 
    

def move_down_is_out_of_bounds(rock_type, rock_y, max_y):
    
    # For all types except + type: Check Y
    if rock_type in "WLTO":
        return rock_y == max_y

    # For + type: Check Y + 1
    if rock_type == "+":
        return rock_y + 1 == max_y


# If the rock tries to move left, make sure it does not collide with the wall
# or other rocks
def can_move_left(room, rock_type, rock_x, rock_y):

    # Is moving left out of bounds?
    if move_left_is_out_of_bounds(rock_type, rock_x):
        return False

    # For wide type: Check (X, Y)
    if rock_type == "W":
        return is_empty(room, rock_x - 1, rock_y)

    # For + type: check (X, Y), (X + 1, Y - 1), and (X + 1, Y + 1)
    if rock_type == "+":
        check1 = is_empty(room, rock_x - 1, rock_y)
        check2 = is_empty(room, rock_x, rock_y - 1)
        check3 = is_empty(room, rock_x, rock_y - 1)
        return check1 and check2 and check3

    # For backwards L type: check (X, Y), (X + 2, Y - 1), and (X + 2, Y - 2)
    if rock_type == "L":
        check1 = is_empty(room, rock_x - 1, rock_y)
        check2 = is_empty(room, rock_x + 1, rock_y - 1)
        check3 = is_empty(room, rock_x + 1, rock_y - 2)
        return check1 and check2 and check3

    # For tall type: check (X, Y) through (X, Y - 3)
    if rock_type == "T":
        check1 = is_empty(room, rock_x - 1, rock_y)
        check2 = is_empty(room, rock_x - 1, rock_y - 1)
        check3 = is_empty(room, rock_x - 1, rock_y - 2)
        check4 = is_empty(room, rock_x - 1, rock_y - 3)
        return check1 and check2 and check3 and check4

    # For big type: check (X, Y) and (X, Y - 1)
    if rock_type == "O":
        check1 = is_empty(room, rock_x - 1, rock_y)
        check2 = is_empty(room, rock_x - 1, rock_y - 1)
        return check1 and check2

# If the rock tries to move right, make sure it does not collide with the wall
# or other rocks
def can_move_right(room, rock_type, rock_x, rock_y):

    # Is moving right out of bounds?
    if move_right_is_out_of_bounds(rock_type, rock_x, len(room[0])):
        return False

    # For wide type: check (X + 3, Y)
    if rock_type == "W":
       return is_empty(room, rock_x + 4, rock_y)

    # For + type: check (X + 2, Y), (X + 1, Y + 1), and (X + 1, Y - 1)
    if rock_type == "+":
        check1 = is_empty(room, rock_x + 3, rock_y)
        check2 = is_empty(room, rock_x + 2, rock_y + 1)
        check3 = is_empty(room, rock_x + 2, rock_y - 1)
        return check1 and check2 and check3

    # For backward L type: check (X + 2, Y), (X + 2, Y - 1), and (X + 2, Y - 2)
    if rock_type == "L":
        check1 = is_empty(room, rock_x + 3, rock_y)
        check2 = is_empty(room, rock_x + 3, rock_y - 1)
        check3 = is_empty(room, rock_x + 3, rock_y - 2)
        return check1 and check2 and check3

    # For tall type: check (X, Y) through (X, Y - 3)
    if rock_type == "T":
        check1 = is_empty(room, rock_x + 1, rock_y)
        check2 = is_empty(room, rock_x + 1, rock_y - 1)
        check3 = is_empty(room, rock_x + 1, rock_y - 2)
        check4 = is_empty(room, rock_x + 1, rock_y - 3)
        return check1 and check2 and check3 and check4

    # For big type: Check (X + 1, Y) and (X + 1, Y - 1)
    if rock_type == "O":
        check1 = is_empty(rock_x + 1, rock_y)
        check2 = is_empty(rock_x + 1, rock_y - 1)
        return check1 and check2

# If the rock tries to move down, make sure it does not collide with the floor
# or other rocks
def can_move_down(room, rock_type, rock_x, rock_y):

    # Is moving down out of bounds?
    if move_down_is_out_of_bounds(rock_type, rock_y, len(room)):
        return False

    return True

def drop_next_rock(room, jetstream, jetstream_position, rocks_dropped, max_height):

    # Get the next rock
    next_rock = get_next_rock(rocks_dropped)

    # Spawn rock. It spawns 2 units from the left wall and 3 units "above" the
    # max height. 
    rock_x, rock_y = (2, len(room) - max_height - 4)

    print(next_rock, rock_x, rock_y)
    print(can_move_left(room, next_rock, rock_x, rock_y))


jetstream = input[0]
room = initialize_room()

drop_next_rock(room, jetstream, 0, 0, 0)