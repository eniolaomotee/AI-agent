from google.genai import types
from functions.run_python import run_python, schema_run_python
from functions.get_files_content import get_file_contents, schema_get_file_contents
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.write_files import write_file, schema_write_file
from config import WORKING_DIRECTORY

# Available functions to the model
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        schema_write_file,
        schema_run_python
    ]
)


# Call the appropriate function based on the function call part
def call_function(function_call_part,verbose=False):
    
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")
    
    
    # function mapping
    function_map = {
        "get_files_info": get_files_info,
        "get_file_contents": get_file_contents,
        "write_file": write_file,
        "run_python_file": run_python
    }
    
    function_name = function_call_part.name
    
    # If function not found, return error message
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown Function: {function_name}"}
                )
            ]
        )
    
    
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIRECTORY
    
    # Find the function by name and call it with the provided arguments

    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ]
    )

