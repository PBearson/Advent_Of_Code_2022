# Find the most pressure that can be released in 30 minutes. 

import time

with open("day_16/input.txt", "r") as f:
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

# Given source valve, find a destination valve and report the minimum number of minutes
# required to reach it
def find_valve(tunnels, src, dst, current_cost, visited):

    # Check if we have reached the destination 
    if src == dst:
        return current_cost

    # Get the connected valves we have not visited yet
    connected = tunnels[src][1]
    not_visited = [c for c in connected if c not in visited]

    # If there are no unvisited valves, then the destination is not reachable from here.
    if len(not_visited) == 0:
        return 2 ** 32

    # Travel to each unvisited valve and get the minimum number of minutes required to reach the destination
    # valve
    return min([find_valve(tunnels, nv, dst, current_cost + 1, visited + [nv]) for nv in not_visited])

# Find the number of minutes from each path to every other path. Structure:
# path_times[src] = {dst1: time1, dst2: time2, dst3: time3, ...}
def find_all_valves(tunnels):
    path_times = {}

    keys = [t for t in tunnels.keys() if tunnels[t][0] > 0 or t == 'AA']

    for src in keys:
        path_times[src] = {}

        for dst in keys:
            path_times[src][dst] = find_valve(tunnels, src, dst, 0, [])
    return path_times

# This checks every combination of valves to open and returns the maximum pressure
def release_most_pressure(tunnels, path_times, current_time, current_valve, opened_valves, total_pressure):
    if current_time <= 0:
        return total_pressure

    # Open the current valve, unless the pressure is 0
    valve_pressure = (current_time - 1) * tunnels[current_valve][0]
    if valve_pressure > 0:
        current_time -= 1
        total_pressure += valve_pressure

    # Visit the other valves -- ignore 0 flow ones
    unopened_valves = [v for v in tunnels.keys() if v not in opened_valves and v != current_valve and tunnels[v][0] > 0]
    max_pressure = 0
    for dst in unopened_valves:
        time_cost = path_times[current_valve][dst]
        pressure = release_most_pressure(tunnels, path_times, current_time - time_cost, dst, opened_valves + [current_valve], total_pressure)
        max_pressure = max(pressure, max_pressure)

    # Get the max pressure, which might be the total pressure (i.e., all valves might have been opened already)
    return max(max_pressure, total_pressure)


tunnels = parse_input(input)
path_times = find_all_valves(tunnels)
pressure = release_most_pressure(tunnels, path_times, 30, "AA", [], 0)
print("Total pressure: %d" % pressure)