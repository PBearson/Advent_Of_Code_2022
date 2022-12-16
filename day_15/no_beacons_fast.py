# Count the number of positions that cannot contain a beacon on row 2000000.

# This is the fast way. For each sensor, it logs the positions that its signal would overlap on the target row.

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

# Given a source position, a target row, and a distance, return a list of the destination
# points on that row that are reachable.
def get_reachable_positions(src_x, src_y, dst_y, distance):
    reachable = []

    # First check the position on the same column - if this is not reachable, nothing else will be.
    if get_distance(src_x, src_y, src_x, dst_y) > distance:
        return []
    reachable.append((src_x, dst_y))

    # First walk left until we are out of bounds
    dst_x = src_x - 1
    while get_distance(src_x, src_y, dst_x, dst_y) <= distance:
        reachable.append((dst_x, dst_y))
        dst_x -= 1
    
    # Now walk right until we are out of bounds
    dst_x = src_x + 1
    while get_distance(src_x, src_y, dst_x, dst_y) <= distance:
        reachable.append((dst_x, dst_y))
        dst_x += 1

    # Return list of reachable positions
    return reachable

# Count the number of excluded beacons on a row by calculating E - B:
#   - E is the number of positions on that row that are too close to a sensor
#   - B is the number of beacons already occupying the target row
def count_excluded_beacons(readings, row):
    excluded_log = set()
    occupied_beacons = set()

    # First log the positions that cannot be occupied due to sensor interference
    for sensor in readings:
        distance = get_distance(sensor[0], sensor[1], sensor[2], sensor[3])
        reachable = get_reachable_positions(sensor[0], sensor[1], row, distance)
        for r in reachable:
            excluded_log.add(r)

    # Count the positions that cannot be occupied due to beacon occupation
    beacons = [r for r in readings if r[3] == row]
    for b in beacons:
        occupied_beacons.add(b[2:])
    
    return len(excluded_log) - len(occupied_beacons)
    
readings = parse_input(input)
exclusion_count = count_excluded_beacons(readings, 2000000)
print("Number of positions which cannot have a beacon: %d" % exclusion_count)