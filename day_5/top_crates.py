# Follow the rearrangement procedures, then provide the crates on top of each stack

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

# Put stacks into a more useful data structure (list):
# Each element of the list is another list. The front of the list represents the top 
# of the stack.
for row in stacks_unfiltered:
    newrow = [row[i:i+3] for i in range(0, len(row), 4)]
    
    for index, item in enumerate(newrow):
        if len(stacks) < index + 1:
            stacks.append([])
        stacks[index].append(item)

# Put procedures into a more useful data structure (list):
# Each element of the list is another list. The first number is how many crates to move.
# The second number is the source stack. The third number is the destination stack.
for row in procedures_unfiltered:
    newrow = row.split(' ')
    procedures.append([int(newrow[n]) for n in [1, 3, 5]])

# sanity check
print(procedures)