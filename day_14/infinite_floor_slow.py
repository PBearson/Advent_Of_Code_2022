# Find how many units of sand come to rest before sand reaches the source. The floor is infinite.

# This is the slow and dumb way. We make the floor really wide (to the point that out-of-bounds is impossible)
# and we run the simulation like before.

with open("day_14/input.txt", "r") as f:
    input = f.read().splitlines()

# Transform the input into a list of sublists, where each sublist has the following structure:
# [[X, Y], [X, Y], [X, Y]]
def transform_input(input):
    parsed_input = []
    for scan in input:
        points = scan.split(" -> ")
        points = [p.split(",") for p in points]
        for p in points:
            p[0] = int(p[0])
            p[1] = int(p[1])
        parsed_input.append(points)
    return parsed_input

# Return 4 integers: smallest X unit, largest X unit, and largest largest Y unit.
# We already know smallest Y unit (500, 0)
def get_room_dimensions(scans):
    small_x = small_y = 2 ** 32
    large_x = large_y = 0

    # Get the room dimensions by finding the smallest and largest points
    for scan in scans:

        # Find smallest X and largest X
        x_points = [s[0] for s in scan]
        small_x = min(min(x_points), small_x)
        large_x = max(max(x_points), large_x)

        # Find largest Y
        y_points = [s[1] for s in scan]
        large_y = max(max(y_points), large_y)

    return (small_x, large_x, large_y)

# Given the room dimensions and the scans, return a matrix of points, where each
# point is either a '.' (air) or a '#' (rock). Also return the sand source.
def draw_room(scans, min_x, max_x, max_y):
    room = []

    max_y += 2
    min_x -= 500
    max_x += 500
    print(min_x, max_x)

    # Create the initially empty room, except for the floor of rocks
    for y in range(0, max_y + 1):
        space = '.'
        if y == max_y:
            space = '#'
        row = [space] * (max_x - min_x + 1)
        room.append(row)

    # Create the rocks
    for scan in scans:
        for i in range(len(scan) - 1):
            rock1 = scan[i]
            rock2 = scan[i + 1]

            # Swap rocks if necessary, since iteration depends on smaller values coming first
            if rock1[0] > rock2[0] or rock1[1] > rock2[1]:
                rock1, rock2 = rock2, rock1 
              
            for rx in range(rock1[0], rock2[0] + 1):
                for ry in range(rock1[1], rock2[1] + 1):
                    dx = rx - min_x
                    dy = ry
                    room[dy][dx] = '#'

    # Get the sand position, relative to the matrix indices
    sandx = 500 - min_x
    sandy = 0
    sand = [sandx, sandy]
    
    return room, sand

# Draws the room, including the sand source
def draw_room_pretty(room, sand):

    room[0][sand[0]] = '+'
    for i, r in enumerate(room):
        print(i, "".join(r))

# Find the next position for one unit of sand. 
# Draw it. Return whether the sand was drawn or not.
def sand_step(room, sand):
    x_pos, y_pos = sand

    # If bottom 3 positions are filled, then the sand has reached the top and we are done.
    pos1 = room[y_pos + 1][x_pos - 1]
    pos2 = room[y_pos + 1][x_pos]
    pos3 = room[y_pos + 1][x_pos + 1]
    if pos1 == 'O' and pos2 == 'O' and pos3 == 'O':
        return False

    # Move the sand.
    while True:

        # Can we move down?
        if y_pos == len(room) - 1 or room[y_pos + 1][x_pos] == '.':
            y_pos += 1
            continue

        # Can we move diagonally left?
        if x_pos == 0 or room[y_pos + 1][x_pos - 1] == '.':
            x_pos -= 1
            y_pos += 1
            continue

        # Can we move diagonally right?
        if x_pos == len(room) - 1 or room[y_pos + 1][x_pos + 1] == '.':
            x_pos += 1
            y_pos += 1
            continue

        # Cannot move
        break

    room[y_pos][x_pos] = 'O'
    return True

# Run the sand simulation. Return the number of sand units drawn.
def run_sand_sim(room, sand):
    units = 0

    # Keep stepping until sand_step returns False
    while True:
        units += 1
        sand_drawn = sand_step(room, sand)
        if not sand_drawn:
            break
    return units

scans = transform_input(input)
x1, x2, y = get_room_dimensions(scans)
room, sand = draw_room(scans, x1, x2, y)

sand_count = run_sand_sim(room, sand)

draw_room_pretty(room, sand)

print("Sand count: %d" % sand_count)