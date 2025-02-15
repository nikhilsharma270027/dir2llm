import os
import sys
import argparse

def generate_structured_output(path, specific_file=None, include_extensions=None, exclude_extensions=None):
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
                # Skip if a specific file is provided and it doesn't match
                if specific_file and file != specific_file:
                    continue

                # Filter by file extensions
                file_extension = os.path.splitext(file)[1].lower()  # Get file extension (e.g., .py)
                if include_extensions and file_extension not in include_extensions:
                    continue  # Skip if the file extension is not in the include list
                if exclude_extensions and file_extension in exclude_extensions:
                    continue  # Skip if the file extension is in the exclude list

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
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="dir2llm - A CLI tool to display directory structure and file contents.",
        epilog="""
Features:
  - Display directory structure in a tree format.
  - Show contents of all files or a specific file.
  - Filter files by extensions (include or exclude).
  - Save output to a file for later use.

Examples:
  # Display directory structure and file contents
  dir2llm ./my_project

  # Display contents of a specific file
  dir2llm ./my_project --file README.md

  # Include only .py and .md files
  dir2llm ./my_project --include .py,.md

  # Exclude .pyc files
  dir2llm ./my_project --exclude .pyc

  # Save output to a file
  dir2llm ./my_project --output output.txt

For more information, visit: https://github.com/mr-chandan/dir2llm
        """,
        formatter_class=argparse.RawTextHelpFormatter  # Preserves formatting in the epilog
    )
    parser.add_argument("directory_path", help="Path to the directory to analyze")
    parser.add_argument("--output", help="Save the output to a specified file", metavar="FILE")
    parser.add_argument("--file", help="Display contents of a specific file", metavar="FILE")
    parser.add_argument("--include", help="Include files with specified extensions (comma-separated, e.g., .py,.md)")
    parser.add_argument("--exclude", help="Exclude files with specified extensions (comma-separated, e.g., .pyc)")
    args = parser.parse_args()

    directory_path = args.directory_path

    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)

    # Parse include and exclude extensions
    include_extensions = None
    exclude_extensions = None

    if args.include:
        include_extensions = [ext.strip().lower() for ext in args.include.split(",")]
    if args.exclude:
        exclude_extensions = [ext.strip().lower() for ext in args.exclude.split(",")]

    # Check if the specified file exists in the directory
    if args.file:
        specific_file_path = os.path.join(directory_path, args.file)
        if not os.path.isfile(specific_file_path):
            print(f"Error: File '{args.file}' does not exist in '{directory_path}'.")
            sys.exit(1)

    structured_output = generate_structured_output(
        directory_path,
        specific_file=args.file,
        include_extensions=include_extensions,
        exclude_extensions=exclude_extensions
    )

    # Save output to file if --output is provided, else print to console
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(structured_output)
            print(f"Output saved to {args.output}")
        except Exception as e:
            print(f"Error writing to file: {e}")
            sys.exit(1)
    else:
        print(structured_output)


if __name__ == "__main__":
    main()