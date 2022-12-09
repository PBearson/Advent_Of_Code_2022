# Get the highest scenic score possible for any tree in the grid

with open("day_8/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

max_scenic_score = 0

# Return whether the tree is an edge
def is_edge(x, y, x_len, y_len):
    left_edge = x == 0
    top_edge = y == 0
    right_edge = x == x_len - 1
    bottom_edge = y == y_len - 1

    return left_edge or top_edge or right_edge or bottom_edge

# Return the number of visible neighbor trees.
# We assume neighbors are in ordered from closest to furthest.
# There is no need to check the last neighbor since there is nothing
# afterwards to check.
def number_visible_trees(height, neighbors):
    num_visible = 1
    for n in neighbors[:-1]:
        if height <= n:
            break
        num_visible += 1
    return num_visible

y_len = len(input)
x_len = len(input[0])

# Iterate through each row (y) and column (x)
for y in range(len(input)):
    for x in range(len(input[y])):

        # Edge trees have scenic scores of 0
        if is_edge(x, y, x_len, y_len):
            continue

        # Get left neighbors - reverse their order since we want to check closest neighbors first
        left_neighbors = input[y][:x]
        left_neighbors = left_neighbors[::-1]

        # Get right neighbors
        right_neighbors = input[y][x+1:]

        # Get top neighbors - reverse their order since we want to check closest neighbors first
        top_neighbors = [r[x] for r in input[:y]]
        top_neighbors.reverse()

        # Get bottom neighbors
        bottom_neighbors = [r[x] for r in input[y+1:]]

        # Get the number of visible trees in each direction
        visible_left = number_visible_trees(input[y][x], left_neighbors)
        visible_right = number_visible_trees(input[y][x], right_neighbors)
        visible_top = number_visible_trees(input[y][x], top_neighbors)
        visible_bottom = number_visible_trees(input[y][x], bottom_neighbors)

        # Get the scenic score
        scenic_score = visible_left * visible_right * visible_top * visible_bottom

        # Update the max scenic score as needed
        max_scenic_score = max(max_scenic_score, scenic_score)

print("The maximum scenic score is %d" % max_scenic_score)