# Calculate the score of the Rock Paper Scissors tournament if the player follows the stategy guide.
# Rock -> Scissors -> Paper -> Rock
# Revised Rules:
#   A = Opponent plays Rock
#   B = Opponent plays Paper
#   C = Opponent playes Scissors
#   X = Player needs to lose
#   Y = Player needs to draw
#   Z = player needs to win
#   Rock = 1 point. Paper = 2 points. Scissors = 3 points.
#   Loss = 0 points. Draw = 3 points. Win = 6 points.

with open("day_2/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

key = {
    'A X': 3, # Loss = 0, scissors = 3
    'A Y': 4, # Draw = 3, rock = 1
    'A Z': 8, # Win = 6, paper = 2
    'B X': 1, # Loss = 0, rock = 1
    'B Y': 5, # Draw = 3, paper = 2
    'B Z': 9, # Win = 6, scissors = 3
    'C X': 2, # Loss = 0, paper = 2
    'C Y': 6, # Draw = 3, scissors = 3
    'C Z': 7, # Win = 6, rock = 1
}

score = sum([key[i] for i in input])

print("Score: %d" % score)