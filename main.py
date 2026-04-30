import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("No api_key found")

import argparse
from google import genai
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`
from google.genai import types
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
client = genai.Client(api_key=api_key)
response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
prompt_token_count = response.usage_metadata.prompt_token_count
candidates_token_count = response.usage_metadata.candidates_token_count

def main():
    if response.usage_metadata != "None":
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_token_count}\nResponse tokens: {candidates_token_count}")
    else:
        raise RuntimeError("Failed API request, no usage_metadata")
    print(response.text)

if __name__ == "__main__":
    main()
