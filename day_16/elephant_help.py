# Find the most pressure that can be released in 26 minutes. An elephant can open valves with us.

# DISCLAIMER: This solution does not yet give the right answer.

from itertools import permutations as perm

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
def get_path_lengths(tunnels):
    path_lengths = {}

    keys = [t for t in tunnels.keys() if tunnels[t][0] > 0 or t == 'AA']

    for src in keys:
        path_lengths[src] = {}

        for dst in keys:
            path_lengths[src][dst] = find_valve(tunnels, src, dst, 0, [])
    return path_lengths

def get_next_best_valve(tunnels, path_lengths, src, current_time, opened_valves, other_dst_valve):
    best_valve, best_valve_pressure = ("", 0)

    unopened_valves = [p for p in path_lengths.keys() if p not in opened_valves and p != other_dst_valve]

    if len(unopened_valves) == 0:
        return ""

    for dst in unopened_valves:
        pathlen = path_lengths[src][dst]
        valve_pressure = (current_time - pathlen - 1) * tunnels[dst][0]
        if valve_pressure > best_valve_pressure:
            best_valve = dst
            best_valve_pressure = valve_pressure

    return best_valve

def get_second_best_valve(tunnels, path_lengths, src, current_time, opened_valves, other_dst_valve):
    best_valve_pressure = 0
    second_best_valve, second_best_valve_pressure = ("", 0)

    unopened_valves = [p for p in path_lengths.keys() if p not in opened_valves and p != other_dst_valve]

    if len(unopened_valves) == 0:
        return ""

    for dst in unopened_valves:
        pathlen = path_lengths[src][dst]
        valve_pressure = (current_time - pathlen - 1) * tunnels[dst][0]
        if valve_pressure > best_valve_pressure:
            best_valve_pressure = valve_pressure
        if valve_pressure > second_best_valve_pressure and valve_pressure < best_valve_pressure:
            second_best_valve = dst
            second_best_valve_pressure = valve_pressure

    return second_best_valve


# TODO greedy approach might work now. Just move the elephant and the human to next best valve,
# based on the current time, the length from the current valve to the destination valve, and 
# that particular valve's pressure
def get_maximum_pressure(tunnels, path_lengths):

    opened_valves = []
    human_position = "AA"
    elephant_position = "AA"
    current_time = 26
    total_pressure = 0

    human_opening_valve = False
    elephant_opening_valve = False

    # Get starting destinations
    human_dst = get_next_best_valve(tunnels, path_lengths, human_position, 26, opened_valves, "")
    elephant_dst = get_next_best_valve(tunnels, path_lengths, elephant_position, 26, opened_valves, human_dst)

    # Moves left corresponds to the number of minutes it will take to reach the destination
    human_moves_left = path_lengths[human_position][human_dst]
    elephant_moves_left = path_lengths[elephant_position][elephant_dst]

    # Run the simulation until time is up
    while current_time > 0:
        current_time -= 1
        indexed_time = 26 - current_time


        # Human has reaches its destination -- add up the pressure and get the next target 
        if human_moves_left == 0:
            if not human_opening_valve:
                # print("%d: Human is about to open %s" % (indexed_time, human_dst))
                human_opening_valve = True
            else:
                human_opening_valve = False
                pressure = (current_time + 1) * tunnels[human_dst][0]
                total_pressure += pressure
                print("%d: Human opens %s and released %d (%d) pressure" % (indexed_time, human_dst, tunnels[human_dst][0], pressure))
                opened_valves.append(human_dst)
                human_position = human_dst
                
                # If the elephant is also about to open its valve, then it is possible the next best valve should be targeted by the elephant 
                # instead of the human.
                if elephant_opening_valve:

                    # Get next best valves for both elephant and human
                    human_best = get_next_best_valve(tunnels, path_lengths, human_position, current_time, opened_valves, elephant_dst)
                    elephant_best = get_next_best_valve(tunnels, path_lengths, human_position, current_time, opened_valves, elephant_dst)

                    # Get the lengths to the new valves 
                    human_length = path_lengths[human_dst][human_best]
                    elephant_length = path_lengths[elephant_dst][elephant_best]

                    # If the next valves are equal and the human is closer, then assign this valve to the human
                    if human_best == elephant_best:

                        # If the human is closer, then the human should be assigned this valve
                        if human_length < elephant_length:
                            human_dst = human_best

                        # Otherwise, the elephant will be assigned this valve, so the human should get the next-best valve
                        else:
                            human_dst = get_next_best_valve(tunnels, path_lengths, human_position, current_time, opened_valves + [human_best], elephant_dst)

                    # Not equal -- just get the next best valve, since there is no interference with the elephant
                    else:
                        human_dst = human_best
                    
                # Elephant is still traveling to its next valve, so we can just get the next valve as normal
                else:
                    human_dst = get_next_best_valve(tunnels, path_lengths, human_position, current_time, opened_valves, elephant_dst)

                # If the human destination is empty, then we'll just run out the clock
                if human_dst == "":
                    human_moves_left = 2 ** 32 

                # Otherwise, get the path length from the current position to the destination
                else:
                    human_moves_left = path_lengths[human_position][human_dst] - 1

        # Human has not reached its destination yet
        else:
            human_moves_left -= 1
            # print("%d: Human is %d moves away from opening %s" % (indexed_time, human_moves_left, human_dst))

        # Elephant has reaches its destination -- add up the pressure and get the next target 
        if elephant_moves_left == 0:
            if not elephant_opening_valve:
                # print("%d: Elephant is about to open %s" % (indexed_time, elephant_dst))
                elephant_opening_valve = True
            else:
                elephant_opening_valve = False
                pressure = (current_time + 1) * tunnels[elephant_dst][0]
                total_pressure += pressure
                print("%d: Elephant opens %s and released %d (%d) pressure" % (indexed_time, elephant_dst, tunnels[elephant_dst][0], pressure))
                opened_valves.append(elephant_dst)
                elephant_position = elephant_dst
                elephant_dst = get_next_best_valve(tunnels, path_lengths, elephant_position, current_time, opened_valves, human_dst)
                if elephant_dst == "":
                    elephant_moves_left = 2 ** 32
                else:
                    elephant_moves_left = path_lengths[elephant_position][elephant_dst] - 1
        # Elephant has not reached its destination yet
        else:
            elephant_moves_left -= 1
            # print("%d: Elephant is %d moves away from opening %s" % (indexed_time, elephant_moves_left, elephant_dst))

    return total_pressure    


tunnels = parse_input(input)
path_lengths = get_path_lengths(tunnels)
pressure = get_maximum_pressure(tunnels, path_lengths)
print("Pressure: %d" % pressure)