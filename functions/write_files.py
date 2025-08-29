import os
from google.genai import types

def write_file(working_directory, file_path, content):
    base_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(base_dir, file_path))
    
    # Check if the target path is within the base directory
    if not target_path.startswith(base_dir):
        return f"Error: Cannot write to {file_path} as it is outside the permitted working directory."
    
    if os.path.isdir(target_path):
        return f'Error: "{file_path}" is a directory, cannot write content to a directory.'
    
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # writes the content
        with open(target_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: writing to file: {e}"
    
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory.",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The path to the file to write to, relative to the working directory."
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "The content to write to the file."
            )
        },
        required=["file_path", "content"]
    )
)