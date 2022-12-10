# Draw the CRT screen by finding which pixels light up

with open("day_10/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

x_reg = 1
cycle = 0
pixels = []

# Each entry in pipeline is a list: [OP, val, count]
#   - OP is the opcode, either "noop" or "addx"
#   - val is the operand of the opcode: for "noop" it is 0
#   - count is the number of cycles that need to execute before this instruction executes
pipeline = []

# Before the cycle starts, the new instruction is added
# to the pipeline
def before_cycle(ins = None):
    global pipeline, cycle, total_signal_strength, x_reg

    # Cannot add NULL instructions
    if ins is None:
        return
    
    # noop takes 1 cycle
    if ins == "noop":
        pipeline.append(["noop", 0, 1])

    # addx takes 2 cycles
    else:
        addx_value = ins.split(" ")[1]
        pipeline.append(["addx", int(addx_value), 2])

# During the cycle, we check the CRT position against the value of the X register
def during_cycle():
    global cycle, x_reg

    # Get the CRT position
    crt_position = (cycle - 1) % 40

    # If the X register is within 1 pixel of the CRT position, then light the pixel up
    if abs(crt_position - x_reg) <= 1:
        pixels.append("#")
    else:
        pixels.append(".")

# After the cycle, the oldest instruction in the pipeline is
# decremented. If the count is 0, it is executed and popped from
# the pipeline.
def after_cycle():
    global pipeline, x_reg

    # Only check instructions in the pipeline if the pipeline is not
    # empty, which could happen if we get several NOOPs in succession.
    if len(pipeline) == 0:
        return

    # Decrement the count of the oldest instruction
    pipeline[0][2] -= 1

    # If the count is 0, add the instruction value to the X register.
    # NOOPs have a value of 0, so they have no effect.
    if pipeline[0][2] == 0:
        x_reg += pipeline[0][1]
        pipeline.pop(0)

# Iterate as long as there are instructions left to load and
# the pipeline is not empty
while cycle - 1 < len(input) or len(pipeline) > 0:

    # Update the cycle.
    cycle += 1
    index = cycle - 1
    ins = None
    
    # Load the next instruction if possible
    if index < len(input):
        ins = input[index]
        
    # Run the CPU
    before_cycle(ins)
    during_cycle()
    after_cycle()

# Display the screen
for i in range(len(pixels)):
    print(pixels[i], end = "")
    if (i + 1) % 40 == 0:
        print("")