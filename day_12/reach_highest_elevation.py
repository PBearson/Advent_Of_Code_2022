# Find the number of steps it takes to reach the highest elevation E as quickly as possible.

import string

with open("day_12/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

# The start and end positions (which have not been found yet), each as a (row, col) pair
start_position = []
end_position = []

# Distances is a dict where the key is a position and a value is that distance
distances = {}

# Initialize everything:
#   - Find initial positions
#   - Create distances
def initialize():
    global input, start_position, end_position, distances

    # Find the start and end positions. Also intiialize distances to max distances
    max_distance = 2 ** 32
    for row in range(len(input)):
        for col in range(len(input[row])):
            if input[row][col] == 'S':
                start_position = [row, col]
                distances[(row, col)] = 0
            else:
                distances[(row, col)] = max_distance
            if input[row][col] == 'E':
                end_position = [row, col]


# Returns True if the given position can be visited, based on the current position.
def can_visit_position(player_position, visit_position):
    global input

    # Make sure the position is not out of bounds
    if visit_position[0] < 0 or visit_position[0] > len(input) - 1:
        return False
    if visit_position[1] < 0 or visit_position[1] > len(input[0]) - 1:
        return False

    # Compare the heights
    player_height = input[player_position[0]][player_position[1]]
    visit_height = input[visit_position[0]][visit_position[1]]

    all_heights = 'S' + string.ascii_lowercase + 'E'

    height_diff = all_heights.find(visit_height) - all_heights.find(player_height)
    return height_diff <= 1

# Get a list of positions that can be visited, based on the current position.
def get_next_positions(player_position):
    global input

    next_positions = []
    
    # Check left
    left_position = (player_position[0], player_position[1] - 1)
    if can_visit_position(player_position, left_position):
        next_positions.append(left_position)

    # Check right
    right_position = (player_position[0], player_position[1] + 1)
    if can_visit_position(player_position, right_position):
        next_positions.append(right_position)

    # Check above
    above_position = (player_position[0] - 1, player_position[1])
    if can_visit_position(player_position, above_position):
        next_positions.append(above_position)

    # Check below
    below_position = (player_position[0] + 1, player_position[1])
    if can_visit_position(player_position, below_position):
        next_positions.append(below_position)

    return next_positions

# Get the shortest distance from the start position to every other position
def get_distances():
    global distances, start_position

    queue = [tuple(start_position)]
    visited = []

    while len(queue) > 0:
        # Get the next position from the queue
        current_position = queue.pop(0)

        # Update the visited list with the current position
        visited.append(current_position)

        # Get the visitable positions from the current position
        next_positions = get_next_positions(current_position)

        # Iterate through the adjacent positions
        for next_pos in next_positions:

            # Get the new distance for that position
            distances[next_pos] = min(distances[next_pos], distances[current_position] + 1)

            # Add the position to the queue if we have not visited already (and if it's not already in the qeueu)
            if next_pos not in visited and next_pos not in queue:
                queue.append(next_pos)

initialize()
get_distances()
print("Number of steps to highest elevation: %d" % distances[tuple(end_position)])