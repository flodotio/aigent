import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
parser = argparse.ArgumentParser(description="Chatbot")
client = genai.Client(api_key=api_key)

def main():
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(model="gemini-3-flash-preview", contents=messages)

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

        if response.usage_metadata != None:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
        else:
            raise RuntimeError("Cannot retrieve response meta data") 
    

    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
