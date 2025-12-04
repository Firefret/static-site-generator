import os
import shutil
import sys
from parsing_block import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "../static")
PUBLIC_DIR = os.path.join(BASE_DIR, "../docs")
TEMPLATE_PATH = os.path.join(BASE_DIR, "../template.html")
MARKDOWN_PATH = os.path.join(BASE_DIR, "../content")

website_path = sys.argv[1] if len(sys.argv ) > 1 else "/"

def source_to_destination_copy(source = STATIC_DIR, destination = PUBLIC_DIR):
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
            print(f"Copying files in {directory} to {destination}")
            source_to_destination_copy(os.path.join(source, directory), os.path.join(destination, directory))
        elif os.path.isfile(os.path.join(source, directory)):
            shutil.copy(os.path.join(source, directory), destination)
            print(f"Copied {directory} to {destination}")
        else:
            print(f"Skipping {directory}")

def extract_title(markdown:str):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")

def generate_page(from_path: os.PathLike = MARKDOWN_PATH, template_path: os.PathLike = TEMPLATE_PATH, dest_path: os.PathLike = PUBLIC_DIR):
    from_path = os.path.realpath(from_path)
    template_path = os.path.realpath(template_path)
    dest_path = os.path.realpath(dest_path)
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}...")

    markdown_object = open(from_path, "r")
    markdown = markdown_object.read()
    file_name = markdown_object.name.split("/")[-1].split(".")
    if file_name[-1] != "md":
        raise ValueError("Provided file is not a markdown file (.md extension expected)")
    file_name = "".join(file_name[:-1])
    print(f"File name: {file_name}.md")
    template = open(template_path, "r").read()

    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    output = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    output = output.replace("href=\"/", f"href=\"{website_path}")
    output = output.replace("src=\"/", f"src=\"{website_path}")

    if not os.path.exists(dest_path):
        print(f"Destination directory not found, creating {dest_path}...")
        os.makedirs(dest_path)
    print(f"Destination directory {dest_path} found")
    html_file_path = os.path.join(dest_path, f"{file_name}.html")
    if os.path.exists(html_file_path):
        print(f"Removing existing file {file_name}.html...")
        os.remove(html_file_path)

    html_file = open(html_file_path, "x")
    html_file.write(output)
    print(f"Page {html_file_path} generated successfully!")
    markdown_object.close()
    html_file.close()

def generate_page_recursive(dir_path_content: os.PathLike, template_dir_path: os.PathLike, dest_dir_path: os.PathLike):
    current_folder = os.path.abspath(dir_path_content)
    template_folder = os.path.abspath(template_dir_path)
    dest_folder = os.path.abspath(dest_dir_path)
    for file in os.listdir(current_folder):
        print(f"Processing {file}...")
        file_path = os.path.abspath(os.path.join(current_folder, file))
        dest_file_path = os.path.abspath(os.path.join(dest_folder, file))
        if os.path.isdir(file_path):
            generate_page_recursive(file_path, template_folder, dest_file_path)
        elif file_path.endswith(".md"):
            generate_page(file_path, template_folder, dest_folder)



def main():
    source_to_destination_copy()
    generate_page_recursive(MARKDOWN_PATH, TEMPLATE_PATH, PUBLIC_DIR)


if __name__ == "__main__":
    main()