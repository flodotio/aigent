import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import available_functions

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

system_prompt = """
You are a coding assistant. Use tools as follows:
- get_files_info: only to list or explore files
- get_file_content: only to read the contents of a file
- run_python_file: whenever the user asks to run or execute a Python file
- write_file: only to write or save content to a file

Never call get_files_info before run_python_file unless the user explicitly asks you to explore first.
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
parser = argparse.ArgumentParser(description="Chatbot")
client = genai.Client(api_key=api_key)


def main():
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=messages,
        config= types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

        if response.usage_metadata != None:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
        else:
            raise RuntimeError("Cannot retrieve response meta data") 
    

    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
