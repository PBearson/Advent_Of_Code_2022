# Find the top 3 Elves with the most calories and report the total number of calories

with open("day_1/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

calorie_counts = []

# For each Elf, find the number of calories and append that number to the calorie_counts list
calories = 0
for i in input:
    if len(i) == 0:
        calorie_counts.append(calories)
        calories = 0
    else:
        calories += int(i)

# Sort the list
calorie_counts.sort()

# Get the sum of the top 3
top_three = calorie_counts[-3:]
total = sum(top_three)
print(f"Total calories: {total}")