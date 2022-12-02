# Calculate the score of the Rock Paper Scissors tournament if the player follows the stategy guide.
# Rock -> Scissors -> Paper -> Rock
# Rules:
#   A / X = Rock
#   B / Y = Paper
#   C / Z = Scissors
#   Rock = 1 point. Paper = 2 points. Scissors = 3 points.
#   Loss = 0 points. Draw = 3 points. Win = 6 points.

with open("day_2/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

key = {
    'A X': 4, # rock = 1, draw = 3
    'A Y': 8, # paper = 2, win = 6
    'A Z': 3, # rock = 3, loss = 0
    'B X': 1, # rock = 1, loss = 0
    'B Y': 5, # paper = 2, draw = 3
    'B Z': 9, # scissors = 3, win = 6
    'C X': 7, # rock = 1, win = 6
    'C Y': 2, # paper = 2, loss = 0
    'C Z': 6 # scissors = 3, draw = 3
}

score = sum([key[i] for i in input])

print("Score: %d" % score)