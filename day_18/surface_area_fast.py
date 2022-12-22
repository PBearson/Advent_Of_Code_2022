# Calculate the surface area of the lava droplet, which is made up of unit cubes

# This solution has O(n) speed complexity but O(x*y*z) space complexity, where x
# is the largest x coordinate in our input, y is the largest y coordinate, etc.

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

    # Return the final surface area
    return surface_area

cubes = parse_input(input)
droplet = initialize_droplet_matrix(cubes)
sa = get_surface_area(cubes, droplet)
print("Surface area: %d" % sa)