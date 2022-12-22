# Calculate the surface area of the lava droplet, which is made up of unit cubes

# This solution is O(n^2), so not quite optimal.

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

# Given a cube and droplet (i.e., a cluster of cubes), return the number of cubes in the droplet
# that are adjacent to our cube
def get_num_adjacent_cubes(cube, droplet):
    num_adjacent_cubes = 0

    # Check adjacency for each droplet unit. Cubes are adjacenct if any 2 coordinates are identical,
    # and the last coordinate is off by exactly 1.
    for d in droplet:
        # x and y and identical, z is off by 1
        z_offset = cube[0] == d[0] and cube[1] == d[1] and abs(cube[2] - d[2]) == 1

        # x and z are identical, y is off by 1
        y_offset = cube[0] == d[0] and cube[2] == d[2] and abs(cube[1] - d[1]) == 1

        # y and z are identical, x is off by 1
        x_offset = cube[1] == d[1] and cube[2] == d[2] and abs(cube[0] - d[0]) == 1

        # If the cube is adjacent to this droplet unit, then append it
        if x_offset or y_offset or z_offset:
            num_adjacent_cubes += 1

    return num_adjacent_cubes

# Get the surface area of the droplet
def get_surface_area(cubes):
    droplet = []
    surface_area = 0

    # Look at each cube in our input
    for cube in cubes:

        # Find the number of adjacent cubes
        num_adjacent_cubes = get_num_adjacent_cubes(cube, droplet)

        # The base surface area increases by 6 sides. For each adjacent cube, the surface area 
        # decreases by 2 sides
        surface_area += 6 - (2 * num_adjacent_cubes)

        # Add this cube to the droplet
        droplet.append(cube)

    # Return the final surface area
    return surface_area

cubes = parse_input(input)
sa = get_surface_area(cubes)
print("Surface area: %d" % sa)