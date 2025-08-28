import os
from google import genai
from google.genai import types
import sys
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    print("Hello from ai-agent!")
    
    
    # check if user provided a prompt
    if len(sys.argv) < 2:
        print("Please provide a prompt as a command-line argument.")
        sys.exit(1)
    
    user_input = sys.argv[1]
    verbose = "--verbose" in sys.argv
    
    
    if user_input == "":
        print("Input cannot be empty")
        sys.exit(1)
        
    # Available functions to the model
    available_functions = types.Tool(
        function_declarations= [
            schema_get_files_info,
        ]
    )
        
    system_prompt = """ 
        You are a helpful AI coding agent.
        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
        - List files and directories
        
        All paths you provide should be relative to the working directory. You do not need to specify the working directoy in your function calls as it is automatically injecte  for security reasons.    
    """
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_input)])
    ]
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages,
        tools= [available_functions],
        system_instruction= system_prompt,
        # config = types.GenerateContentConfig(system_instruction=system_prompt)
    )
    
    
    
    prompt_token_count = response.usage_metadata.prompt_token_count
    response_token_count = response.usage_metadata.candidates_token_count
    
    if verbose:
        print(f"User prompt: {user_input}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {response_token_count}")
    
    
    print(response.text)
        
    
    
if __name__ == "__main__":
    main()
