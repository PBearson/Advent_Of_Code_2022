# Find the tuning frequency by finding the correct (X, Y) position of the distress signal, and calculating X * 4000000 + Y

with open("day_15/input.txt", "r") as f:
    input = f.read().splitlines()

# Parse the input into a list of tuples, where each tuple is of the form (sensor x, sensor y, beacon x, beacon y)
def parse_input(input):
    readings = []
    for sensor in input:
        sensor = sensor.split(" ")

        sensor_x = sensor[2].split("=")[1][:-1]
        sensor_x = int(sensor_x)

        sensor_y = sensor[3].split("=")[1][:-1]
        sensor_y = int(sensor_y)

        beacon_x = sensor[8].split("=")[1][:-1]
        beacon_x = int(beacon_x)

        beacon_y = sensor[9].split("=")[1]
        beacon_y = int(beacon_y)
        
        reading = (sensor_x, sensor_y, beacon_x, beacon_y)
        readings.append(reading)
    return readings

# Return the Manhattan distance between 2 points
def get_distance(src_x, src_y, dst_x, dst_y):
    return abs(src_x - dst_x) + abs(src_y - dst_y)

# Given a source position and a distance, return a list of destination bounds that are also reachable. Each element of the list has the following structure:
# [Y: (min X, max X)], where Y is a Y coordinate, min X is the smallest X on that
# Y position that is reachable, and max X is the largest coordinate that is reachable
def get_reachable_positions(src_x, src_y, distance):
    reachable = {}

    # Increment our Y starting from 0. The largest Y is the distance, while the X bounds depend on Y.
    for y in range(distance + 1):
        min_x = src_x - distance + y
        max_x = src_x + distance - y

        # Same X bound is used for src_y + y and src_y - y
        reachable[src_y + y] = reachable[src_y - y] = (min_x, max_x)

    return reachable

# Check if there is overlap between 2 lines by comparing their min and max values.
# Since there are only integers, overlap also happens if the lines are at most 1
# unit apart.
def check_overlap(min1, max1, min2, max2):
    return min2 - max1 <= 1 and min1 - max2 <= 1


# Given a set of bounds [(min1, max1), (min2, max2), ...], merge them into a maximumally concise set.
# Continue merging until no more merges are possible.
def merge_bounds(current_bounds):
    
    merged_bounds = []
    merged = False
    
    # Iterate through every pair of bounds
    for i in range(len(current_bounds)):
        
        # Since we will pop from current_bounds as we merge, the bounds length will change over time.
        # So we need to check the index against the length
        if i >= len(current_bounds):
            break

        # Get the first bounds
        min1 = current_bounds[i][0]
        max1 = current_bounds[i][1]
        
        # Get the second bound
        for j in range(i + 1, len(current_bounds)):
            
            # See comment in outer loop.
            if j >= len(current_bounds):
                break

            # Get the second bounds
            min2 = current_bounds[j][0]
            max2 = current_bounds[j][1]

            # Check if there is overlap between the pair of bounds
            if check_overlap(min1, max1, min2, max2):
                
                # Get the merged bounds and append it
                min3 = min(min1, min2)
                max3 = max(max1, max2)

                merged_bounds.append((min3, max3))

                # Pop the un-merged bounds
                current_bounds.pop(j)
                current_bounds.pop(i)

                merged = True

    # If we merged, then call this function again
    if merged:
        return merge_bounds(current_bounds + merged_bounds)

    # No merges occured -- we are done
    else:
        return current_bounds

# Get a dictionary of reachable X positions for every Y position. The reachable X positions are
# of the form [(min_x1, max_x1), (min_x2, max_x2)], i.e., a list of bounded X values for each Y
# position. The bound lists are merged together appropriately. 
def get_all_reachable_positions(readings):
    all_reachable = {}

    # Iterate through all sensors
    for sensor in readings:

        # Get the set of reachable positions for this sensor
        distance = get_distance(sensor[0], sensor[1], sensor[2], sensor[3])
        reachable = get_reachable_positions(sensor[0], sensor[1], distance)

        # Iterate through all reachable Y positions
        for key in reachable.keys():

            # Get the X bounds for this Y position
            val = reachable[key]


            # Case 1: Recent Y value is new. Create a new list of bounded
            # values for this Y position, and add the current entry to
            # the dictionary.
            if key not in all_reachable.keys():
                all_reachable[key] = [val]
            
            # Case 2: Recent value is not new. Add it to the list, then merge if possible.
            else:
                all_reachable[key].append((val[0], val[1]))
                all_reachable[key] = merge_bounds(all_reachable[key])

    return all_reachable

# Given the set of reachable bounds and a max X / Y bound, find the position
# that is NOT reachable. Then calculate the tuning frequency.
def get_tuning_frequency(reachable, bound):

    # Iterate through all Y positions
    for y in range(bound + 1):

        # Get the reachable X bounds on this Y position
        val = reachable[y]

        # Bounds greater than 1 have a gap -- find the value of the gap
        if len(val) > 1:
            val1, val2 = val[0], val[1]

            # Switch the order of the bounds if they are backward
            if val1[1] > val2[0]:
                val1 = val2
            
            # Get the X value of the gap
            x = val1[1] + 1

            # Make sure the X value is within our desired bounds
            if x >= 0 and x <= bound:
                
                # Calculate the tuning frequency
                freq = x * 4000000 + y
                return freq

readings = parse_input(input)
reachable = get_all_reachable_positions(readings)
freq = get_tuning_frequency(reachable, 4000000)
print("Tuning frequency: %d\n" % freq)