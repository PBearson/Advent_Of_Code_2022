# Find the correct order of the packets, including 2 new divider packets: [[2]] and [[6]]. Multiply the indices of the divider packets together.

with open("day_13/input.txt", "r") as f:
    input = f.read().splitlines()

# Given a packet, return a list of numbers and lists
def transform_packet(packet):
    integers = "0123456789"
    newlist = []

    # Presumably, the first element is an opening bracket, which we don't care about
    i = 1

    # Go until we reach the end of the packet
    while i < len(packet):

        # If this is an integer, then append it to the list. Integers may be multiple digits in length.
        if packet[i] in integers:
            j = i
            while packet[j] in integers:
                j += 1
            newlist.append(int(packet[i:j]))
            i = j

        # If this is an opening bracket, then it is the start of a a list, in which case
        # we need to find the closing bracket. Since lists can be nested, we can keep a tally
        # of opening and closing brackets; when the number of opening brackets equals the number
        # of closing brackets, we are at the end of list. 
        elif packet[i] == "[":
            layers = 0
            j = 0
            for j in range(i, len(packet)):
                if packet[j] == "[":
                    layers += 1
                elif packet[j] == "]":
                    layers -= 1

                # At this point, we have the indices of the sublist: i and j. We use recursion 
                # to transform the sublist and append it to the root list.
                if layers == 0:
                    sublist = transform_packet(packet[i:j+1])
                    newlist.append(sublist)
                    i += j - 1
                    break

        # Other elements, e.g., commas, are ignored
        else:
            i += 1

    return newlist

# Insert divicer packets [[2]] and [[6]] into the packets
def insert_divider_packets(packets):
    divider1 = [[2]]
    divider2 = [[6]]
    packets.append(divider1)
    packets.append(divider2)

# Transform the input into a list of packets.
# The packets themselves have correct typing (e.g., consisting of ints and lists).
def transform_input(input):
    packets = []

    for i in range(0, len(input), 3):
        packet1 = transform_packet(input[i])
        packet2 = transform_packet(input[i+1])
        packets.append(packet1)
        packets.append(packet2)

    return packets

# Given 2 integers, return whether they are in the right order:
#   - If n1 is less than n2, return 1
#   - If n1 is greater than n1, return -1
#   - If equal, return 0
def compare_ints(n1, n2):
    if n1 < n2:
        return 1
    if n1 > n2:
        return -1
    return 0

# Compare the first value in both lists, then the second value,
# and so on. Call recursively as needed.
#   - If list1 runs out of items first, return 1
#   - If list2 runs out of items first, return -1
#   - Otherwise, return 0
def compare_lists(list1, list2):
    listlen = max(len(list1), len(list2))

    for index in range(listlen):

        # If left side runs out of items, return 1. If right side runs out of items, return -1.
        if index >= len(list1):
            return 1
        if index >= len(list2):
            return -1
        
        # Compare element types
        element1 = list1[index]
        element2 = list2[index]

        # Call the appropriate function based on the element types
        ret = 0
        if type(element1) == int and type(element2) == int:
            ret = compare_ints(element1, element2)
                
        elif type(element1) == list and type(element2) == list:
            ret = compare_lists(element1, element2)

        elif type(element1) == list and type(element2) == int:
            ret = compare_list_and_int(element1, element2, True)

        elif type(element1) == int and type(element2) == list:
            ret = compare_list_and_int(element2, element1, False)

        # Keep going if the return code is 0, otherwise stop
        if ret != 0:
            return ret

    # If we reach the end of the list, simply return 0
    return 0

# Compare a list and an integer by first converting the integer to a list,
# then calling compare_lists.
def compare_list_and_int(list1:list, n2:int, list_is_left:bool):
    list2 = [n2]
    
    # Call compare_lists, depending on which element was the original list.
    if list_is_left:
        return compare_lists(list1, list2)
    return compare_lists(list2, list1)

# Sort the packets in-place and get the key. Algorithm: bubble sort (sorry).
def sort_and_get_key(packets):
    
    # Update divider indices over time. At the end we will use them to calculate the divider key.
    divider1 = [[2]]
    divider2 = [[6]]
    divider1_index = 0
    divider2_index = 0

    # Bubble sort
    while True:
        swap = False
        for i in range(len(packets) - 1):

            # If an adjacent pair is out-of-order, swap them.
            if compare_lists(packets[i], packets[i + 1]) == -1:
                packets[i], packets[i + 1] = packets[i + 1], packets[i]
                swap = True

            # Does this pair have the first divider?
            if packets[i] == divider1:
                divider1_index = i + 1
            elif packets[i + 1] == divider1:
                divider1_index = i + 2

            # Does this pair have the second divider?
            if packets[i] == divider2:
                divider2_index = i + 1
            elif packets[i + 1] == divider2:
                divider2_index = i + 2

        # Bubble sort is done if the whole list is ordered
        if swap == False:
            break
    
    # Get the key
    return divider1_index * divider2_index

packets = transform_input(input)
insert_divider_packets(packets)
key = sort_and_get_key(packets)
print("Decoder key: %d" % key)