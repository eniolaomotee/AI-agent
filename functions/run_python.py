import os
import subprocess
from google.genai import types

def run_python(working_directory, file_path, args=[]):
    base_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(base_dir, file_path))
    
    # Check if the target path is within the base directory
    if not target_path.startswith(base_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside'
    
    if os.path.isdir(target_path):
        return f'Error: File "{file_path}" not found'
    
    if not os.path.isfile(target_path):
        return f'Error: File "{file_path}" not found'

    if not target_path.endswith('.py'):
        return f'Error: File "{file_path}" is not a Python file'
    
    try:
        completed_process = subprocess.run(["python", target_path, *args], capture_output=True, text=True, timeout=30, cwd=working_directory)
        output = []
        
        if completed_process.stdout.strip():
            output.append(f"STDOUT:\n{completed_process.stdout.strip()}")
        if completed_process.stderr.strip():
            output.append(f"STDERR:\n{completed_process.stderr.strip()}")
        
        if completed_process.returncode != 0:
            output.append(f'Process exited with code {completed_process.returncode}')
        
        if not output:
            return "No output"
        
        return "\n".join(output)
    
    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds"
    
    except Exception as e:
        return f'Error: running file: {e}'
        
    
# Standard schema for the function
schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file with optional arguments, constrained to the working directory.",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The path to the Python file to execute, relative to the working directory."
            ),
            "args": types.Schema(
                type = types.Type.ARRAY,
                items = types.Schema(
                    type = types.Type.STRING
                ),
                description = "Optional list of arguments to pass to the Python script."
            )
        },
        required=["file_path"]
    )
)