# Calculate the number of visible trees from outside the grid

with open("day_8/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

visible_trees = 0

# Return whether the tree is an edge
def is_edge(x, y, x_len, y_len):
    left_edge = x == 0
    top_edge = y == 0
    right_edge = x == x_len - 1
    bottom_edge = y == y_len - 1

    return left_edge or top_edge or right_edge or bottom_edge

# Return whether the given tree can be seen from outside by comparing 
# its height to the neighbors' heights
def visible_from_direction(height, neighbors):
    return height > max(neighbors)

y_len = len(input)
x_len = len(input[0])

# Iterate through each row (y) and column (x)
for y in range(len(input)):
    for x in range(len(input[y])):

        # Check if edge
        if is_edge(x, y, x_len, y_len):
            visible_trees += 1
            continue

        # Get neighbors
        left_neighbors = input[y][:x]
        right_neighbors = input[y][x+1:]
        top_neighbors = [r[x] for r in input[:y]]
        bottom_neighbors = [r[x] for r in input[y+1:]]

        # Get visibility
        visible_left = visible_from_direction(input[y][x], left_neighbors)
        visible_right = visible_from_direction(input[y][x], right_neighbors)
        visible_top = visible_from_direction(input[y][x], top_neighbors)
        visible_bottom = visible_from_direction(input[y][x], bottom_neighbors)

        # Check the visibility
        if visible_left or visible_right or visible_top or visible_bottom:
            visible_trees += 1

print("Number of visible trees: %d" % visible_trees)