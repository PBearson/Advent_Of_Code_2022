# Find the most pressure that can be released in 30 minutes

with open("day_16/sample_input.txt", "r") as f:
    input = f.read().splitlines()

# Parse input into a dictionary, where keys are valve IDs, and values
# are tuples (FR, [id1, id2, ...]). FR is the flow rate of this valve,
# and id1, id2, etc., are IDs of connected valves
def parse_input(input):

    tunnels = {}

    for line in input:
        line = line.split(" ")
        tunnel = line[1]
        flow = line[4].split("=")[1][:-1]
        flow = int(flow)

        connected_valves = line[9:-1]
        connected_valves = [c[:-1] for c in connected_valves]
        connected_valves += line[-1:]

        tunnels[tunnel] = (flow, connected_valves)

    return tunnels

# This finds the pressure by treating the problem as a graph search problem. Given a current valve, it finds the 
# maximum pressure by recursively exploring every connected valve, both with and without opening the current valve.
# Its time complexity is exponential, and it will take several days to run, so I do not recommend using it.
# Note: Please read the previous statement again.
def find_maximum_pressure_graph_approach(tunnels, current_valve, current_time, current_pressure, opened_valves = []):

    # Out of time
    if current_time <= 0:
        return current_pressure

    # Options are 1) open the valve and go down a new tunnel, or 2) skip
    # the valve and go down a new tunnel
    
    flow = tunnels[current_valve][0]
    connected_valves = tunnels[current_valve][1]

    flow_pressure = 0
    pressure_with_open = 0
    pressure_without_open = 0

    # If the flow of this valve is non-zero and we haven't opened it, then get 
    # the pressure for opening it
    if flow > 0 and current_valve not in opened_valves:
        flow_pressure = flow * current_time

        # Traverse other tunnels after opening current valve
        pressure_with_open = max([find_maximum_pressure_graph_approach(tunnels, v, current_time - 2, current_pressure + flow_pressure, opened_valves + [current_valve]) for v in connected_valves])

    # Traverse other tunnels without opening current valve
    pressure_without_open = max([find_maximum_pressure_graph_approach(tunnels, v, current_time - 1, current_pressure, opened_valves) for v in connected_valves])

    # Return the higher pressure
    return max(pressure_with_open, pressure_without_open)

tunnels = parse_input(input)