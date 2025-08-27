import os
from google import genai
from google.genai import types
import sys
from dotenv import load_dotenv


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
        
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_input)])
    ]
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages
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
