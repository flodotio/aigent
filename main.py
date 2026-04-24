import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import available_functions, call_function
from agent import call_agent



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
parser = argparse.ArgumentParser(description="Chatbot")
client = genai.Client(api_key=api_key)


def main():
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    call_agent(client, args)


if __name__ == "__main__":
    main()
