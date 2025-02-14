import os
import sys

def generate_structured_output(path):
    output = ""

    def build_tree(dir_path, indent=""):
        nonlocal output
        items = os.listdir(dir_path)
        num_items = len(items)
        for i, item in enumerate(items):
            item_path = os.path.join(dir_path, item)
            is_last = i == num_items - 1
            connector = "└── " if is_last else "├── "

            output += indent + connector + item + "/" + "\n" if os.path.isdir(item_path) else indent + connector + item + "\n"

            if os.path.isdir(item_path):
                new_indent = indent + ("    " if is_last else "│   ")
                build_tree(item_path, new_indent)

    output += "Directory structure:\n"
    output += "└── " + os.path.basename(path) + "/" + "\n"
    build_tree(path, "    ")

    output += "\n\nFiles Content:\n\n"

    def read_files(dir_path):
        nonlocal output
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    output += "================================================\n"
                    output += f"File: {file_path}\n"
                    output += "================================================\n"
                    output += content + "\n\n"
                except Exception as e:
                    output += "================================================\n"
                    output += f"File: {file_path} (Error reading file: {e})\n"
                    output += "================================================\n"
                    output += "\n\n"

    read_files(path)
    return output


def main():
    if len(sys.argv) != 2:
        print("Usage: dir2llm <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)

    structured_output = generate_structured_output(directory_path)
    print(structured_output)


if __name__ == "__main__":
    main()
