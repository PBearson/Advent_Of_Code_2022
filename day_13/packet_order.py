# Find the pairs of packets that are in the right order, then find the sum of their indices.

with open("day_13/sample_input.txt", "r") as f:
    input = f.read().splitlines()

# Given a packet, return a list of numbers and lists
def transform_packet(packet):
    integers = "0123456789"
    newlist = []

    # Presumably, the first element is an opening bracket, which we don't care about
    i = 1

    # Go until we reach the end of the packet
    while i < len(packet):

        # If this is an integer, append it to the list
        if packet[i] in integers:
            newlist.append(int(packet[i]))
            i += 1

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

                # At this point, we have the indices of the sublist: i and j + 1. We use recursion 
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

# Transform the input into a list, where each entry is a pair of packets.
# The packets themselves have correct typing (e.g., consisting of ints and lists).
def transform_input(input):
    packets = []

    for i in range(0, len(input), 3):
        pair1 = transform_packet(input[i])
        pair2 = transform_packet(input[i+1])
        packets.append([pair1, pair2])

    return packets

packets = transform_input(input)