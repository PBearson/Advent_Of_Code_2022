# Count the number of unique positions that the tail of the rope visits.

with open("day_9/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

head_position = [0, 0]
tail_position = [0, 0]

# Unique tail visits is instantiated with the initial tail position
unique_tail_visits = set(tuple(tail_position))

# Return whether the head is at least one space close to the tail
def head_close_to_tail():
    global head_position, tail_position

    x_bounded = abs(head_position[0] - tail_position[0]) <= 1
    y_bounded = abs(head_position[1] - tail_position[1]) <= 1
    bounded = x_bounded and y_bounded
    return bounded

# Move the tail exactly one space
def move_tail_once():
    global head_position, tail_position

    # Diagonal move top left
    if head_position[0] < tail_position[0] and head_position[1] < tail_position[1]:
        tail_position[0] -= 1
        tail_position[1] -= 1

    # Diagonal move top right
    elif head_position[0] < tail_position[0] and head_position[1] > tail_position[1]:
        tail_position[0] -= 1
        tail_position[1] += 1

    # Diagonal move bottom left
    elif head_position[0] > tail_position[0] and head_position[1] < tail_position[1]:
        tail_position[0] += 1
        tail_position[1] -= 1

    # Diagonal move bottom right
    elif head_position[0] > tail_position[0] and head_position[1] > tail_position[1]:
        tail_position[0] += 1
        tail_position[1] += 1

    # Move left
    elif head_position[0] < tail_position[0]:
        tail_position[0] -= 1

    # Move right
    elif head_position[0] > tail_position[0]:
        tail_position[0] += 1

    # Move top
    elif head_position[1] < tail_position[1]:
        tail_position[1] -= 1

    # Move bottom
    elif head_position[1] > tail_position[1]:
        tail_position[1] += 1

# Loop through all the inputs
for command in input:

    # Get the direction and number of steps
    direction, count = command.split(" ")
    count = int(count)

    # Update head position
    if direction == "R":
        head_position[0] += count
    elif direction == "L":
        head_position[0] -= count
    elif direction == "U":
        head_position[1] -= count
    else:
        head_position[1] += count

    # Move the tail as long as it is far from the head. Update the 
    # unique tail visits as needed.
    while not head_close_to_tail():
        move_tail_once()
        unique_tail_visits.add(tuple(tail_position))

print("Unique tail visits: %d" % len(unique_tail_visits))