import os
from langchain.tools import tool

    
@tool   
def get_current_directory_files() -> list[str]:
    """
    Return a list of all files in the current directory and its subdirectories.
    """
    files = []

    for root, dirs, filenames in os.walk("."):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    return files


@tool
def get_file_content( filename: str) -> str:
    """
    Read and return the contents of a file.
    """
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
    
    
@tool
def override_file( filename: str, content: str) -> str:
    """
    Overwrite an existing file with new content.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"{filename} overwritten successfully."


@tool
def create_file( filepath: str, content: str = "") -> str:
    """
    Create the directory if it doesn't exist
    Create a new file with optional content.
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return f"{filepath} created successfully."


@tool 
def delete_file(filepath: str) -> str:
    """
    Delete a file.
    """
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Deleted file: {filepath}")
        return f"{filepath} deleted successfully."
    else:
        print(f"File not found: {filepath}")
        return f"{filepath} does not exist."