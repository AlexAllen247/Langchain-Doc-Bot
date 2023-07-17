from codeinterpreterapi import CodeInterpreterSession
import openai
from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

async def main():
    # create a session
    session = CodeInterpreterSession()
    await session.astart()

    # generate a response based on user input
    output = await session.generate_response(
        "Plot the bitcoin chart of 2023 YTD"
    )

    # ouput the response (text + image)
    print("AI: ", response.content)
    for file in response.files:
        file.show_image()

    # terminate the session
    await session.astop()
    

if __name__ == "__main__":
    import asyncio
    # run the async function
    asyncio.run(main())
