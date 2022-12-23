# Calculate the external surface area of the lava droplet, which is made up of unit cubes


with open("day_18/input.txt", "r") as f:
    input = f.read().splitlines()

# From the input, get a list of cubes (each cube being a (x, y, z) tuple)
def parse_input(input):
    cubes = []

    for cube in input:
        cube = cube.split(",")
        cube = [int(c) for c in cube]
        cubes.append(cube)

    return cubes

# Get a matrix of bounds (x, y, z), where x is the largest x coordinate in our input,
# y is the largest y coordinate, etc. 
def initialize_droplet_matrix(cubes):

    # Get the bounds. Add 1 to avoid IndexError
    x_bound = max([c[0] for c in cubes]) + 1
    y_bound = max([c[1] for c in cubes]) + 1
    z_bound = max([c[2] for c in cubes]) + 1

    # Initialize the matrix
    matrix = [[[0 for z in range(z_bound)] for y in range(y_bound)] for x in range(x_bound)]

    return matrix

# Given a cube and droplet (i.e., a cluster of cubes), return the number of cubes in the droplet
# that are adjacent to our cube
def get_num_adjacent_cubes(cube, droplet):
    num_adjacent_cubes = 0
    x, y, z = cube
    x_bound = len(droplet) - 1
    y_bound = len(droplet[0]) - 1
    z_bound = len(droplet[0][0]) - 1

    # Check x adjacency
    if x > 0 and droplet[x - 1][y][z] == 1:
        num_adjacent_cubes += 1
    if x < x_bound and droplet[x + 1][y][z] == 1:
        num_adjacent_cubes += 1

    # Check y adjacency
    if y > 0 and droplet[x][y - 1][z] == 1:
        num_adjacent_cubes += 1
    if y < y_bound and droplet[x][y + 1][z] == 1:
        num_adjacent_cubes += 1

    # Check y adjacency
    if z > 0 and droplet[x][y][z - 1] == 1:
        num_adjacent_cubes += 1
    if z < z_bound and droplet[x][y][z + 1] == 1:
        num_adjacent_cubes += 1

    return num_adjacent_cubes

# Given a cube (empty or not), check if it is internal by checking if other rocks surround it on all sides
def cube_is_internal(cube, droplet):
    x_bound = len(droplet)
    y_bound = len(droplet[0])
    z_bound = len(droplet[0][0])
    x, y, z = cube

    x_before = False
    x_after = False
    for n in range(x_bound):
        if n == x:
            continue

        x_neighbor = droplet[n][y][z]
        
        if x_neighbor:
            if n < x:
                x_before = True
            else:
                x_after = True

    y_before = False
    y_after = False
    for n in range(y_bound):
        if n == y:
            continue

        y_neighbor = droplet[x][n][z]
        
        if y_neighbor == 1:
            if n < y:
                y_before = True
            else:
                y_after = True

    z_before = False
    z_after = False
    for n in range(z_bound):
        if n == z:
            continue

        z_neighbor = droplet[x][y][n]
        
        if z_neighbor == 1:
            if n < z:
                z_before = True
            else:
                z_after = True

    return x_before and x_after and y_before and y_after and z_before and z_after

# Count the number of surfaces 'touching' an air pocket 
def get_air_pocket_touches(droplet):
    x_bound = len(droplet) - 1
    y_bound = len(droplet[0]) - 1
    z_bound = len(droplet[0][0]) - 1
    air_pocket_touches = 0

    for x in range(1, x_bound):
        for y in range(1, y_bound):
            for z in range(1, z_bound):

                # Ignore non-airgaps
                if droplet[x][y][z] != 0:
                    continue

                # Make sure gap is actually internal, i.e., there should be rocks surrounding all sides, some finite number of units away
                if not cube_is_internal((x, y, z), droplet):
                    continue

                # Count the number of adjacent rocks.
                adjacent_rocks = [droplet[x - 1][y][z], droplet[x + 1][y][z], droplet[x][y - 1][z], droplet[x][y + 1][z], droplet[x][y][z - 1], droplet[x][y][z + 1]]
                adjacent_rocks = [ar for ar in adjacent_rocks if ar == 1]
                air_pocket_touches += len(adjacent_rocks)
                
    return air_pocket_touches

# Get the surface area of the droplet
def get_surface_area(cubes, droplet):
    surface_area = 0

    # Look at each cube in our input
    for cube in cubes:

        # Find the number of adjacent cubes
        num_adjacent_cubes = get_num_adjacent_cubes(cube, droplet)

        # The base surface area increases by 6 sides. For each adjacent cube, the surface area 
        # decreases by 2 sides
        surface_area += 6 - (2 * num_adjacent_cubes)

        # Add this cube to the droplet
        x, y, z = cube
        droplet[x][y][z] = 1

    # Remove internal surfaces, i.e., those which 'touch' an internal air pocket
    surface_area -= get_air_pocket_touches(droplet) 

    # Return the final surface area
    return surface_area

cubes = parse_input(input)
droplet = initialize_droplet_matrix(cubes)
sa = get_surface_area(cubes, droplet)
print("Surface area: %d" % sa)