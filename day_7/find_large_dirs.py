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

    # Find the total sum of all directories whose sizes are at most 100000
    def sum_directories(self):
        dirsize = 0
        total_sum = 0
        threshold = 100000

        # Add the size of the files
        for f in self.files:
            dirsize += f.size

        # Add the size of the directories
        for d in self.dirs:
            child_dirsize, child_total_sum = d.sum_directories()
            dirsize += child_dirsize
            total_sum += child_total_sum
        
        # Check if the size is below the threshold
        if dirsize <= threshold:
            total_sum += dirsize
        
        return dirsize, total_sum


    # Print out the directory in a user-friendly format
    def print_directory(self, depth = 1, print_root_dir = True):

        # Tabs will make it prettier :)
        tabs = "\t" * depth

        # Only print the root dir if we ask for it (i.e., first time we call this function)
        if print_root_dir:
            print(f"Dir: {self.name}")

        # Print the files and get the total size of all files
        dirsize = 0
        for f in self.files:
            print(f"{tabs}File: {f.name} {f.size}")
            dirsize += f.size

        for d in self.dirs:
            print(f"{tabs}Dir: {d.name}")
            dirsize += d.print_directory(depth + 1, False)

        # Print the total directory size
        print(f"{tabs}TOTAL DIRECTORY SIZE: {dirsize}")
        return dirsize

    # Add a file to the filesystem
    def add_file(self, path, filename, filesize):
        
        # Ignore root dir
        if path[0] == "/":
            path = path[1:]
        
        # Reach the target directory
        curdir = self
        while len(path) > 0:
            curdir = [d for d in curdir.dirs if d.name == path[0]][0]
            path = path[1:]

        # Add the new file if it does not exist
        targetfile = [f for f in curdir.files if f.name == filename]
        if len(targetfile) == 0:
            newfile = File(filename, filesize)
            curdir.files.append(newfile)

    # Add a directory to the filesystem
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

# Handle ls command by adding the listed contents to the filesystem 
def handle_ls(response):
    global current_dir, root_dir
    
    for item in response:
        item = item.split(" ")
        if item[0] == "dir":
            root_dir.add_directory(current_dir + item[1:])
        else:
            root_dir.add_file(current_dir, item[1], int(item[0]))

# Handle cd command by adding the target dir to the filesystem
def handle_cd(dir):
    global current_dir, root_dir

    if dir == "..":
        current_dir.pop()
    else:
        current_dir.append(dir)
        root_dir.add_directory(current_dir)

# Parse the command: it is either cd or ls
def handle_command(command, response):
    if command[0] == "cd":
        handle_cd(command[1])
    elif command[0] == "ls":
        handle_ls(response)

# Iterate through the input to build the filesystem
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

# Print the filesystem, because why not
print("Filesystem:")
root_dir.print_directory()

# Get the sum of our directories
total_sum, target_sum = root_dir.sum_directories()
print("Sum of target directories: %d" % target_sum)