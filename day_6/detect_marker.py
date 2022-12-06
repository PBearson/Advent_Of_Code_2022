# Find how many characters need to be processed before the first start-of-packet marker is detected.

with open("day_6/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

characters = input[0]
processed = 0

# Get each contiguous sequence of 4 characters and check if they are unique
for i in range(len(characters) - 3):
    marker = characters[i:i+4]
    if len(set(marker)) == 4:
        processed = i + 4
        break

print("Processed %d characters" % processed)