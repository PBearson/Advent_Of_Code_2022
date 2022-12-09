# Count the number of unique positions that the tail of the rope visits.
# This rope is longer: 10 knots instead of 2 knots.

with open("day_9/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

# Create a list of positions for the rope. Index 0 indicates the head's position.
rope_position = []
for _ in range(10):
    rope_position.append([0, 0])

# Unique tail visits is instantiated with the initial tail position
unique_tail_visits = set()
unique_tail_visits.add(tuple(rope_position[0]))

print(unique_tail_visits, len(unique_tail_visits))

# Return whether one knot is at least one space close to another knot
def knots_close(knot_1, knot_2):
    x_bounded = abs(knot_1[0] - knot_2[0]) <= 1
    y_bounded = abs(knot_1[1] - knot_2[1]) <= 1
    bounded = x_bounded and y_bounded
    return bounded

def all_knots_close():
    global rope_position

    count = 0
    for i in range(len(rope_position) - 1):
        count += knots_close(rope_position[i], rope_position[i+1])
    
    return count == 9

# Move a knot exactly one space. Knot 2 gets moved, depending on knot 1's position.
def move_knot_once(knot_1, knot_2):

    # Diagonal move top left
    if knot_1[0] < knot_2[0] and knot_1[1] < knot_2[1]:
        knot_2[0] -= 1
        knot_2[1] -= 1

    # Diagonal move top right
    elif knot_1[0] < knot_2[0] and knot_1[1] > knot_2[1]:
        knot_2[0] -= 1
        knot_2[1] += 1

    # Diagonal move bottom left
    elif knot_1[0] > knot_2[0] and knot_1[1] < knot_2[1]:
        knot_2[0] += 1
        knot_2[1] -= 1

    # Diagonal move bottom right
    elif knot_1[0] > knot_2[0] and knot_1[1] > knot_2[1]:
        knot_2[0] += 1
        knot_2[1] += 1

    # Move left
    elif knot_1[0] < knot_2[0]:
        knot_2[0] -= 1

    # Move right
    elif knot_1[0] > knot_2[0]:
        knot_2[0] += 1

    # Move top
    elif knot_1[1] < knot_2[1]:
        knot_2[1] -= 1

    # Move bottom
    elif knot_1[1] > knot_2[1]:
        knot_2[1] += 1

    # Return the new knot position
    return knot_2

# Loop through all the inputs
for command in input:

    # Get the direction and number of steps
    direction, count = command.split(" ")
    count = int(count)

    # Update head position
    if direction == "R":
        rope_position[0][0] += count
    elif direction == "L":
        rope_position[0][0] -= count
    elif direction == "U":
        rope_position[0][1] -= count
    else:
        rope_position[0][1] += count

    # Update the other knots as long as the head knot is not close enough
    while not knots_close(rope_position[0], rope_position[1]):
        for i in range(len(rope_position) - 1):
            knot_1 = rope_position[i]
            knot_2 = rope_position[i + 1]

            # Update each child knot as needed
            if not knots_close(knot_1, knot_2):
                rope_position[i + 1] = move_knot_once(knot_1, knot_2)

            # Update the unique tail visits as needed
            unique_tail_visits.add(tuple(rope_position[9]))

print("Unique tail visits: %d" % len(unique_tail_visits))