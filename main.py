import os
from google import genai
from google.genai import types
import sys
from dotenv import load_dotenv
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_files_content import schema_get_file_contents, get_file_contents
from functions.write_files import schema_write_file, write_file
from functions.run_python import schema_run_python, run_python

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    print("Hello from AI-agent!")
    
    
    # check if user provided a prompt and if verbose flag is set
    if len(sys.argv) < 2:
        print("Please provide a prompt as a command-line argument.")
        sys.exit(1)
    
    user_input = sys.argv[1]
    verbose = "--verbose" in sys.argv
    
    # If user input is empty
    if user_input == "":
        print("Input cannot be empty")
        sys.exit(1)
        
    # Available functions to the model
    available_functions = types.Tool(
        function_declarations= [
            schema_get_files_info,
            schema_get_file_contents,
            schema_write_file,
            schema_run_python
        ]
    )
        
    # Users input message
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_input)])
    ]
    
    max_iterations = 20
    for i in range(max_iterations):
        # Generate a response from the model
        response = client.models.generate_content(
            model = "gemini-2.0-flash-001",
            contents = messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools= [available_functions],
                
            )
        )
        
        # Token Usage
        prompt_token_count = response.usage_metadata.prompt_token_count
        response_token_count = response.usage_metadata.candidates_token_count
        
        
        
        if verbose:
            print(f"User prompt: {user_input}")
            print(f"Prompt tokens: {prompt_token_count}")
            print(f"Response tokens: {response_token_count}")
        
        # If no candidates, stop
        if not response.candidates:
            print("No candidates, stopping")
            break  
        
        candidate = response.candidates[0]
        
        # Add model response to messages, keeps conversation updated 
        messages.append(candidate.content)
        
        # if it has normal text response, print and stop -> we're done here
        if candidate.content.parts and candidate.content.parts[0].text:
            print("Final answer:", candidate.content.parts[0].text)
            break
            
        # Otherwise it's a tool call, so we need to handle it(handle tool calls)
        if response.function_calls:
            for function_call_part in response.function_calls:
                function_response = call_function(function_call_part,verbose)
                
                
                if (not function_response.parts or not hasattr(function_response.parts[0], 'function_response')
                    or not hasattr(function_response.parts[0].function_response, 'response')
                    ) :
                    print(f"Fatal: function {function_call_part.name} returned no valid response")
                    break
                
                if verbose:
                    print(f"Function response: {function_response.parts[0].function_response.response}")
                    
                    
                # Append function response as user message
                messages.append(function_response)
                
        
        if response.text:
            print("Model text:", response.text)
            break
        
 
# Call the appropriate function based on the function call part
def call_function(function_call_part,verbose=False):
    func_name = function_call_part.name
    func_args = function_call_part.args

    func_args["working_directory"] = "./calculator"
    
    if verbose:
        print(f"Calling function: {func_name}({func_args})")
    else:
        print(f"Calling function: {func_name}")
    
    # Find the function by name and call it with the provided arguments
    if func_name == "get_files_info":
        function_result = get_files_info(**func_args)
    elif func_name == "get_file_contents":
        function_result = get_file_contents(**func_args)
    elif func_name == "write_file":
        function_result = write_file(**func_args)
    elif func_name == "run_python_file":
        function_result = run_python(**func_args)
    else:
        #  detailed error message for unknown function
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unkown function {func_name}"}
                )
            ]
        )
    
    # detailed function result
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={'result':function_result}
            )
        ]
    )

if __name__ == "__main__":
    main()
    




