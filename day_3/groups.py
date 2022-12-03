# Find the common item between the groups of rucksacks, and calculate its priority. Do this 
# for all groups and sum all the priorities.

import string

with open("day_3/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

item_types = string.ascii_letters

total_priority = 0

# Iterate through all groups
for index in range(0, len(input), 3):
    rucksack_1 = input[index]
    rucksack_2 = input[index + 1]
    rucksack_3 = input[index + 2]

    # Findt he common item using a simple search
    common_item = ""
    for item in rucksack_1:
        if item in rucksack_2 and item in rucksack_3:
            common_item = item
            break

    # Get the priority of the common item
    priority = item_types.find(common_item) + 1
    total_priority += priority

print("Sum of priorities: %d" % total_priority)