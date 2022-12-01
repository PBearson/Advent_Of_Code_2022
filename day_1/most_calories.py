# Find the Elf with the most calories and report the number of calories

with open("day_1/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

max_calories = 0
calories = 0
for i in input:
    if len(i) == 0:
        if calories > max_calories:
            max_calories = calories
        calories = 0
    else:
        calories += int(i)

print(f"The most calories is {max_calories}")