# Find how many units of sand come to rest before sand reaches the source. The floor is infinite.

# This is the fast way. It inspects each row of the cave exactly once and calculates the number of sand units
# that will fit there.

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
    max_y += 2
    room = []

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
    for r in room:
        print("".join(r))


# Count the number of sand units that can fit, row by row. The first row has 1 unit.
# Every row can fit up to 2 more units than the previous row. Sand cannot go in a space
# if it is occupied by a rock. Gaps are created when 3 or more units of rock are adjacent
# on the same row. If the rock length is N, then the gap size under that rock is N - 2; the
# gap size under that is N - 4, then N - 6, and so on, until the gap is closed.
# Return the count.
def count_sand(room, sand):
    count = 0
    for i in range(len(room) - 1):
        row = room[i]
        rowcount = 1 + (i * 2) - len([r for r in row if r == '#'])
        
        # Check top 3 spaces; sand cannot fit if the top 3 spaces are rocks
        if i > 0:
            for j in range(1, len(row) - 1):

                # Get the top 3 spaces
                pos1 = room[i - 1][j - 1]
                pos2 = room[i - 1][j]
                pos3 = room[i - 1][j + 1]

                # If this is an empty space and the top 3 spaces are rocks, then sand cannot
                # go here. We also replace this space with a rock so that the effect cascades down.
                if room[i][j] == '.' and pos1 == '#' and pos2 == '#' and pos3 == '#':
                    room[i][j] = '#'
                    rowcount -= 1

        count += rowcount

    return count

scans = transform_input(input)
x1, x2, y = get_room_dimensions(scans)
room, sand = draw_room(scans, x1, x2, y)

count = count_sand(room, sand)

print("Sand count: %d" % count)