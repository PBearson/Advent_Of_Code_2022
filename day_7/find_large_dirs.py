# Find the sum of the total sizes of all directories whose sizes are at most 100000.

with open("day_7/input.txt", "r") as f:
    input = f.readlines()
input = [i.replace("\n", "") for i in input]

class File:
    def __init__(self, name:str, size:int):
        self.name = name
        self.size = size

class Directory:
    def __init__(self, name = "", dirs = [], files = []):
        self.name = name
        self.dirs = dirs
        self.files = files

    def print_directory(self, depth = 0):
        tabs = "\t" * depth
        print(f"{tabs}{self.name}")
        for f in self.files:
            print(f"{tabs}{f.name}")
        for d in self.dirs:
            d.print_directory(depth + 1)

    def add_file(self, path, filename, filesize):
        print(path, filename, filesize)


    def add_directory(self, path):

        # Current directory has not been defined yet
        if self.name == "":
            self.name = path[0]
            return

        # Ignore root dir
        if path[0] == "/":
            path = path[1:]

        # Reach the parent directory
        curdir = self
        while len(path) > 1:
            curdir = [d for d in curdir.dirs if d.name == path[0]][0]
            path = path[1:]
        
        # Add the new directory if it does not exist
        targetdir = [d for d in curdir.dirs if d.name == path[0]]
        if len(targetdir) == 0:
            newdir = Directory(path[0], [], [])
            curdir.dirs.append(newdir)

current_dir = []
root_dir = Directory()

def handle_ls(response):
    global current_dir, root_dir
    
    for item in response:
        item = item.split(" ")
        if item[0] == "dir":
            root_dir.add_directory(current_dir + item[1:])
        else:
            root_dir.add_file(current_dir, item[1], item[0])

def handle_cd(dir):
    global current_dir, root_dir

    if dir == "..":
        current_dir.pop()
    else:
        current_dir.append(dir)
        root_dir.add_directory(current_dir)

def handle_command(command, response):
    if command[0] == "cd":
        handle_cd(command[1])
    elif command[0] == "ls":
        handle_ls(response)

for i in range(len(input)):
    if input[i][0] != "$":
        continue

    command = input[i].split(" ")[1:]
    response = []
    for j in range(i + 1, len(input)):
        if input[j][0] == "$":
            break
        response.append(input[j])
    handle_command(command, response)

# print("Filesystem:")
# root_dir.print_directory()