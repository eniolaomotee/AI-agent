import os
from google import genai
from google.genai import types
import sys
from config import MAX_ITERATION
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import call_function, available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # Check for verbose flag and collect other args
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    
    if not args:
        print("Hello from AI-agent!")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)
        
    user_input = " ".join(args)
    
     # If user input is empty
    if user_input == "":
        print("Input cannot be empty")
        sys.exit(1)
        
    
    if verbose:
        print(f" User Prompt: {user_input} \n")
    
   
    # Users input message
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_input)])
    ]
    
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERATION:
            print(f"Reached max iterations ({MAX_ITERATION}), stopping.")
            sys.exit(1)
            
        try:
            final_response = generate_response(client, messages,verbose)
            if final_response:
                print("Final response")
                print(final_response)
                break
        except Exception as e:
            print("Error in generating response:", e)
            
    
def generate_response(client, messages, verbose):
    response = client.models.generate_content(
            model = "gemini-2.0-flash-001",
            contents = messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools= [available_functions],
            )
        )
    
    if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)
            
    if not response.function_calls:
        return response.text
    
    
    function_responses = []
    for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part,verbose)
                
                
                if (not function_call_result.parts or not hasattr(function_call_result.parts[0], 'function_response')
                    or not hasattr(function_call_result.parts[0].function_response, 'response')
                    ) :
                    raise Exception("empty function call result")
                
                if verbose:
                    print(f"Function response: {function_call_result.parts[0].function_response.response}")
                    
                function_responses.append(function_call_result)

    if not function_responses:
        raise Exception("no function generated, exiting")
    
    for tool_msg in function_responses:
        messages.append(tool_msg)
        
        


if __name__ == "__main__":
    main()
    




