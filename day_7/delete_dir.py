# Find the smallest directory that, if deleted, would free up enough space for the update.
# The file system has a max size of 70 million. The update size is 30 million.

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

    # Find the smallest directory that is larger than the space needed
    def get_directory_to_delete(self, space_needed:int):
        dirsize = 0
        target_dirsize = 2 ** 32

        # Add the size of the files
        for f in self.files:
            dirsize += f.size

        # Add the size of the directories, and update the the target directory as we iterate
        # through each directory
        for d in self.dirs:
            child_dirsize, child_target_dirsize = d.get_directory_to_delete(space_needed)
            dirsize += child_dirsize
            if child_target_dirsize < target_dirsize and child_target_dirsize >= space_needed:
                target_dirsize = child_target_dirsize

        # Finally, compare the current directory size to the target directory size
        # and update if need be.
        if dirsize < target_dirsize and dirsize >= space_needed:
            target_dirsize = dirsize

        return dirsize, target_dirsize

    # Find the total sum of all directories
    def sum_directories(self):
        dirsize = 0

        # Add the size of the files
        for f in self.files:
            dirsize += f.size

        # Add the size of the directories
        for d in self.dirs:
            dirsize += d.sum_directories()
        
        return dirsize


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

max_dirsize = 70000000
update_size = 30000000

# Print the filesystem, because why not
print("Filesystem:")
root_dir.print_directory()

# Get the unused space
total_size = root_dir.sum_directories()
space_needed = total_size + update_size - max_dirsize
print("Space we need to free: %d" % space_needed)

# Get the delete size
dirsize, deletesize = root_dir.get_directory_to_delete(space_needed)
print("Delete size: %d" % deletesize)