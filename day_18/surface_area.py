# Calculate the surface area of the lava droplet, which is made up of unit cubes

with open("day_18/input.txt", "r") as f:
    input = f.read().splitlines()

def parse_input(input):
    cubes = []

    for cube in input:
        cube = cube.split(",")
        cube = [int(c) for c in cube]
        cubes.append(cube)

    return cubes

# Given a cube and droplet (i.e., a cluster of cubes), return a list of cubes in the droplet
# that are adjacent to our cube
def get_adjacent_cubes(cube, droplet):
    adjacent_cubes = []

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
            adjacent_cubes.append(d)

    return adjacent_cubes

# Get the surface area of the droplet
def get_surface_area(cubes):
    droplet = []
    surface_area = 0

    # Look at each cube in our input
    for cube in cubes:
        
        # First add the surface area of the cube to the droplet
        surface_area += 6

        # Find the number of adjacent cubes
        adjacent_cubes = get_adjacent_cubes(cube, droplet)

        # For each adjacent cube, the surface area decreases by 2 sides
        surface_area -= 2 * len(adjacent_cubes)

        # Add this cube to the droplet
        droplet.append(cube)

    # Return the final surface area
    return surface_area

cubes = parse_input(input)
sa = get_surface_area(cubes)
print("Surface area: %d" % sa)