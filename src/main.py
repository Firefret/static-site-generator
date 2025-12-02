from textnode import *
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, "../static")
DESTINATION_DIR = os.path.join(BASE_DIR, "../public")

def source_to_destination_copy(source = SOURCE_DIR, destination = DESTINATION_DIR):
    source = os.path.realpath(source)
    destination = os.path.realpath(destination)

    if not os.path.exists(source):
        raise ValueError(f"Source directory {source} does not exist")
    if os.path.exists(destination):
        print(f"Deleting existing files in {destination}")
        shutil.rmtree(destination)
    os.mkdir(destination)

    dirlist = os.listdir(source)
    for directory in dirlist:
        if os.path.isdir(os.path.join(source, directory)):
            source_to_destination_copy(os.path.join(source, directory), os.path.join(destination, directory))
            print(f"Copying files in {directory} to {destination}")
        elif os.path.isfile(os.path.join(source, directory)):
            shutil.copy(os.path.join(source, directory), destination)
            print(f"Copied {directory} to {destination}")
        else:
            print(f"Skipping {directory}")



def main():
    source_to_destination_copy()


if __name__ == "__main__":
    main()