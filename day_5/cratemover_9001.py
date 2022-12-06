# Follow the rearrangement procedures, then provide the crates on top of each stack,
# Multiple crates can be moved at a time, so their order is preserved.

with open("day_5/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

stacks_unfiltered = []
procedures_unfiltered = []
stacks = []
procedures = []

# Get the unfiltered crates and unfiltered operations
for index in range(len(input)):
    if len(input[index]) == 0:
        stacks_unfiltered = input[:index - 1]
        procedures_unfiltered = input[index + 1:]
        break

# Reverse the crate order, so the bottom of the stacks are first
stacks_unfiltered.reverse()

# Put stacks into a more useful data structure (list):
# Each element of the list is another list. The front of the list represents the bottom 
# of the stack.
for row in stacks_unfiltered:
    newrow = [row[i:i+3] for i in range(0, len(row), 4)]
    
    for index, item in enumerate(newrow):
        if len(stacks) < index + 1:
            stacks.append([])
        
        # No need to include the 'empty' crates (the whitespace in the input)
        if len(item.lstrip()) != 0:
            stacks[index].append(item)

# Put procedures into a more useful data structure (list):
# Each element of the list is another list. The first number is how many crates to move.
# The second number is the source stack. The third number is the destination stack.
for row in procedures_unfiltered:
    newrow = row.split(' ')
    procedures.append([int(newrow[n]) for n in [1, 3, 5]])

# Perform the procedures as instructed
for procedure in procedures:

    # First parse the move count, source stack and destination stack.
    count = procedure[0]
    src = procedure[1] - 1
    dst = procedure[2] - 1
    
    # tmp holds the crates must be moved. They are moved in the same order to the destination.
    tmp = stacks[src][-1*count:]
    
    # Add the crates the destination, and remove them from the source
    for t in tmp:
        stacks[dst].append(t)
        stacks[src].pop()

# Print the top crates: Recall that the top crates are at the end of 
# each list.
top_crates = ""
for stack in stacks:
    crate = stack[-1][1]
    top_crates += crate

print("Top crates: %s" % top_crates)