# Find the common item between the compartments in each rucksack, and calculate its priority. Do this 
# for all rucksacks and sum all the priorities.

import string

with open("day_3/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

item_types = string.ascii_letters

total_priority = 0

# Iterate through all rucksacks
for rucksack in input:
    compartment_len = int(len(rucksack) / 2)
    compartment_a = rucksack[:compartment_len]
    compartment_b = rucksack[compartment_len:]
    
    # Find the common item using a simple search
    common_item = ""
    for item in compartment_a:
        if item in compartment_b:
            common_item = item
            break

    # Get the priority of the common item
    priority = item_types.find(common_item) + 1
    total_priority += priority

print("Sum of priorities: %d" % total_priority)