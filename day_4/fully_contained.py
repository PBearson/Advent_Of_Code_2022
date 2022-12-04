# Find the number of assignment pairs where one range fully contains the other

with open("day_4/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

total_pairs = 0

# Iterate through all pairs
for pair in input:

    # Get the ID ranges of each pair
    r1, r2 = pair.split(",")
    r1_low, r1_high = [int(r) for r in r1.split("-")]
    r2_low, r2_high = [int(r) for r in r2.split("-")]
    
    # Check for containment
    r1_contains_r2 = r1_low <= r2_low and r1_high >= r2_high
    r2_contains_r1 = r2_low <= r1_low and r2_high >= r1_high

    if r1_contains_r2 or r2_contains_r1:
        total_pairs += 1

print("Total contained pairs: %d" % total_pairs)