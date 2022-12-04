# Find the number of assignment pairs where at least one number overlaps

with open("day_4/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

total_overlaps = 0

# Iterate through all pairs
for pair in input:

    # Get the ID ranges of each pair
    r1, r2 = pair.split(",")
    r1_low, r1_high = [int(r) for r in r1.split("-")]
    r2_low, r2_high = [int(r) for r in r2.split("-")]

    # Check for overlap
    if r1_high >= r2_low and r1_low <= r2_high:
        total_overlaps += 1

print("Total pairs with overlap: %d" % total_overlaps)