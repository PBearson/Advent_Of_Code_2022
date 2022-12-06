# Find how many characters need to be processed before the first message is detected.

with open("day_6/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

characters = input[0]
processed = 0

# Get each contiguous sequence of 14 characters and check if they are unique
for i in range(len(characters) - 13):
    marker = characters[i:i+14]
    if len(set(marker)) == 14:
        processed = i + 14
        break

print("Processed %d characters" % processed)