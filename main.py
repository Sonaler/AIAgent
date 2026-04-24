import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info


def main():
    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("user_prompt", type=str, help="Prompt for AI agent")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API key for gemini was not found")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    if args.verbose:
        print("User prompt: {}", args.user_prompt)

    generate_response(client, messages, args.verbose)

def generate_response(client, content, verbose=False):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=content
    )
    if response.usage_metadata is None:
        raise RuntimeError("Failed API request")

    if verbose:
        print("Prompt tokens: {}", response.usage_metadata.prompt_token_count)
        print("Response tokens: {}", response.usage_metadata.candidates_token_count)
    print(response.text)

if __name__ == "__main__":
    main()