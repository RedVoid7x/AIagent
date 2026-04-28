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
args = parser.parse_args()
# Now we can access `args.user_prompt`
client = genai.Client(api_key=api_key)
response = client.models.generate_content(model="gemini-2.5-flash", contents=args.user_prompt)
prompt_token_count = response.usage_metadata.prompt_token_count
candidates_token_count = response.usage_metadata.candidates_token_count
if response.usage_metadata != "None":
    print(f"Prompt tokens: {prompt_token_count}\nResponse tokens: {candidates_token_count}")
else:
    raise RuntimeError("Failed API request, no usage_metadata")
print(response.text)



def main():
    print("Hello from aiagent!")


if __name__ == "__main__":
    main()
