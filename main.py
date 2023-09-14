import os
import argparse
import tarfile
import zipfile

# Function to extract the file system image
def extract_fs(archive_file, extract_dir):
    if archive_file.endswith(".tar"):
        with tarfile.open(archive_file, 'r') as tar:
            tar.extractall(path=extract_dir)
    elif archive_file.endswith(".zip"):
        with zipfile.ZipFile(archive_file, 'r') as zipf:
            zipf.extractall(path=extract_dir)
    else:
        raise ValueError("Unsupported archive format")

# Function to execute the 'pwd' command
def do_pwd(current_dir):
    print(current_dir)

# Function to execute the 'ls' command
def do_ls(current_dir):
    files = os.listdir(current_dir)
    for file in files:
        print(file)

# Function to execute the 'cd' command
def do_cd(current_dir, args):
    if len(args) == 0:
        os.chdir(os.path.expanduser("~"))
    else:
        new_dir = os.path.abspath(os.path.join(current_dir, args[0]))
        if os.path.exists(new_dir) and os.path.isdir(new_dir):
            os.chdir(new_dir)
        else:
            print("Directory not found")

# Function to execute the 'cat' command
def do_cat(args):
    if len(args) == 0:
        print("Usage: cat <file>")
    else:
        file_path = args[0]
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                print(file.read())
        else:
            print("File not found")

# Function to execute a list of commands from a script file
def execute_script(script_file):
    with open(script_file, 'r') as file:
        commands = file.read().splitlines()
        for command in commands:
            execute_command(command)

# Function to execute a single command
def execute_command(command):
    parts = command.split()
    if not parts:
        return
    cmd = parts[0]
    args = parts[1:]

    if cmd == 'pwd':
        do_pwd(os.getcwd())
    elif cmd == 'ls':
        do_ls(os.getcwd())
    elif cmd == 'cd':
        do_cd(os.getcwd(), args)
    elif cmd == 'cat':
        do_cat(args)
    else:
        print("Unknown command:", cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="vshell - Virtual Shell")
    parser.add_argument("archive_file", help="File containing the file system image (tar or zip)")
    parser.add_argument("--script", help="File containing a list of commands to execute")
    args = parser.parse_args()

    extract_fs(args.archive_file, "vshell_fs")
    os.chdir("vshell_fs")

    if args.script:
        execute_script(args.script)
    else:
        while True:
            command = input("gugu trap dude$ ")
            if command == "exit" or command == "e":
                break
            execute_command(command)

    os.chdir("..")
    print("Exiting vshell.")
