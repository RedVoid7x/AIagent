import os
from dotenv import load_dotenv
from prompts import system_prompt
from call_functions import available_functions, call_function
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("No api_key found")
import sys
import argparse
from google import genai
# Now we can access `args.user_prompt`
from google.genai import types

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = genai.Client(api_key=api_key)
    for _ in range(20):
        response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
        prompt_token_count = response.usage_metadata.prompt_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count
        for candidate in response.candidates:
            messages.append(candidate.content)
        if response.usage_metadata != None:
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {prompt_token_count}\nResponse tokens: {candidates_token_count}")
        else:
            raise RuntimeError("Failed API request, no usage_metadata")
        if response.function_calls:
            function_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise Exception("Invalid")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Invalid")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Invalid")
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f" -> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(response.text)
            break
    else:
        print("Maximum number of model iterations reached. Exiting with a code of 1 (failure)")
        sys.exit(1)
if __name__ == "__main__":
    main()
