import os
from config import MAX_CHARACTERS
from google.genai import types

def get_file_contents(working_directory, file_path):
    base_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(base_dir, file_path))
    
    if not target_file.startswith(base_dir):
        return f"Error: Cannot access {file_path} as it is outside the permitted working directory."
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file "{file_path}"'
    
    try:
        with open(target_file,"r") as f:
            content = f.read(MAX_CHARACTERS)
            if len(content) > MAX_CHARACTERS:
                return content[:MAX_CHARACTERS] + f'[...File "{file_path}" truncated at 1000 characters]'
            return content
    
    except Exception as e:
        return f'Error: reading file "{file_path}": {e}'


# Standard schema for the function
schema_get_file_contents = types.FunctionDeclaration(
    name="get_file_contents",
    description="Reads and returns the content of a specified file, constrained to the working directory.",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The path to the file to read, relative to the working directory."
            )
        },
        required=["file_path"]
    )
)


