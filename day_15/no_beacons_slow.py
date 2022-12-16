# Count the number of positions that cannot contain a beacon on row 2000000.

# This is the slow way. For each position in the target row, we compare the distance between that position and the distances of every other sensor.
# If the distance is too short, i.e., if this position is too close to a sensor, then a beacon cannot go in that position.

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

# Create a dictionary of sensor locations and the distance between each sensor and its nearest beacon
def create_distances_map(readings):
    distances = {}

    for reading in readings:
        sensor = (reading[0], reading[1])
        dist = get_distance(reading[0], reading[1], reading[2], reading[3])
        distances[sensor] = dist
    return distances

# Count the number of positions in the given row that cannot have a beacon.
# A position cannot have a beacon if it is already occupied by a sensor.
# It also cannot have a beacon if the distance between it and the closest sensor is
# less than or equal to that sensor's distance to its own closest beacon.
def count_excluded_beacons(row, readings, distances, min_column, max_column):
    count = 0
    for col in range(min_column, max_column + 1):
        # Check if already occupied by a beacon -- skip this position
        beacon = [r for r in readings if r[2] == col and r[3] == row]
        if len(beacon) > 0:
            continue

        # Check if occupied by a sensor -- beacon cannot go here
        sensor = [r for r in readings if r[0] == col and r[1] == row]
        if len(sensor) > 0 or len(beacon) > 0:
            count += 1
            continue

        # Check if it is too close to any sensor
        for sensor in distances.keys():
            dist = get_distance(col, row, sensor[0], sensor[1])
            if dist <= distances[sensor]:
                count += 1
                break

    return count

# Get the smallest and largest feasible column we will have to check. The smallest
# can be found by finding the smallest (sensor X - distance). The largest can be 
# found by finding the largest (sensor X + distance).
def get_column_bounds(distances):
    min_column = 2 ** 32
    max_column = 0
    for sensor in distances.keys():
        left_column = sensor[0] - distances[sensor]
        min_column = min(left_column, min_column)
        right_column = sensor[0] + distances[sensor]
        max_column = max(right_column, max_column)
    return min_column, max_column

readings = parse_input(input)
distances = create_distances_map(readings)
min_column, max_column = get_column_bounds(distances)

exclusion_count = count_excluded_beacons(2000000, readings, distances, min_column, max_column)
print("Number of positions which cannot have a beacon: %d" exclusion_count)