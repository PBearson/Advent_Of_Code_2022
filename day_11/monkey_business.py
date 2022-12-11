# Calculate the monkey business by counting the two most active monkeys inspect items over 20 rounds. Multiply those numbers together.

import math

with open("day_11/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

# Monkey class with the following attributes:
#   - items: The list of items carried by this monkey. Each element in the list is the current worry level for that item.
#   - operation: A string to signify the operation on each item, either '*' or '+'
#   - operand: A string to signify how to apply the operation. Can either be a number or 'old'
#   - divTest: An int to use in the divisibility test.
#   - trueTarget: If the item is divisible by divTest, pass the item to this monkey.
#   - FalseTarget: If the item is not divisible by divTest, pass the item to this monkey.
class Monkey:
    def __init__(self, items:list, operation:str, operand:str, divTest:int, trueTarget:int, falseTarget:int):
        self.items = items
        self.operation = operation
        self.operand = operand
        self.divTest = divTest
        self.trueTarget = trueTarget
        self.falseTarget = falseTarget

        # Inspections is the number of inspections done by this monkey
        self.inspections = 0

    # Perform the operations on each item
    def perform_operations(self):
        for i in range(len(self.items)):

            # Get the operand
            if self.operand == 'old':
                operand = self.items[i]
            else:
                operand = int(self.operand)

            # Perform the operation
            if self.operation == '+':
                self.items[i] += operand
            else:
                self.items[i] *= operand

            # Divide by 3 and round down
            self.items[i] = math.floor(self.items[i] / 3)

        # Update the number of inspections
        self.inspections += len(self.items)

    # Test an item for divisibility. Return the target monkey.
    def get_target_monkey(self, item):
        if item % self.divTest == 0:
            return self.trueTarget
        return self.falseTarget

    def __str__(self):
        return f"Monkey attributes:\n\tItems: {self.items}\n\tOperation: new = old {self.operation} {self.operand}\n\tTest: Divisible by {self.divTest}\n\tIf true: throw to monkey {self.trueTarget}\n\tIf false: throw to monkey {self.falseTarget}\n\tInspections: {self.inspections}"

# A list of Monkey objects. The monkey at index 0 is Monkey 0.
monkeys = []

# Initialize the monkeys
def initialize_monkeys():
    global monkeys

    for i in range(0, len(input), 7):
        monkey_info = input[i:i+6]
        monkey_info = [m.lstrip() for m in monkey_info]

        # Get start items
        start_items = monkey_info[1].split(" ")[2:]
        start_items = [s.replace(",", "") for s in start_items]
        start_items = [int(s) for s in start_items]
        
        # Get the operation and operand
        operation, operand = monkey_info[2].split(" ")[-2:]
        
        # Get the division test
        divTest = monkey_info[3].split(" ")[-1]
        divTest = int(divTest)
        
        # Get the target monkey when division test is True
        trueTarget = monkey_info[4].split(" ")[-1]
        trueTarget = int(trueTarget)

        # Get the target monkey when division test is False
        falseTarget = monkey_info[5].split(" ")[-1]
        falseTarget = int(falseTarget)

        # Create the monkey
        monkey = Monkey(start_items, operation, operand, divTest, trueTarget, falseTarget)
        monkeys.append(monkey)

# Run a single round by getting the new worry levels and passing the items to the new monkeys
def run_single_round():
    global monkeys

    for monkey in monkeys:
        # Get the new worry levels 
        monkey.perform_operations()

        # Pass the items to the new monkeys
        for item in monkey.items:
            target_monkey = monkey.get_target_monkey(item)
            monkeys[target_monkey].items.append(item)

        # The monkey will have thrown all its items
        monkey.items = []

# Run 20 rounds
def run_rounds():
    for _ in range(20):
        run_single_round()


# Get the monkeys and run the 20 rounds
initialize_monkeys()
run_rounds()

# Get monkey business
inspections = [m.inspections for m in monkeys]
inspections.sort()
active_a, active_b = inspections[-2:]
monkey_business = active_a * active_b
print("Monkey business: %d" % monkey_business)