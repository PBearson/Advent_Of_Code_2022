# Find how many units of sand come to rest before sand begins to fall into the void below.

with open("day_14/sample_input.txt", "r") as f:
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

    # Create the initially empty room
    for y in range(0, max_y + 1):
        row = ['.'] * (max_x - min_x + 1)
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
    for r in room:
        print("".join(r))

scans = transform_input(input)
x1, x2, y = get_room_dimensions(scans)
room, sand = draw_room(scans, x1, x2, y)

draw_room_pretty(room, sand)