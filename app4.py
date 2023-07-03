from langchain.chains.api.prompt import API_RESPONSE_PROMPT
from langchain.chains import APIChain
from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

api_docs = """
Open Library Works API

Base URL: https://openlibrary.org/works/

The Open Library Works API provides information about specific works.
Each work in Open Library begins with the URL prefix "/works".

API Endpoints:
1. Work Details
    - Endpoint: '/{work_id}.json'
    - Method: GET
    - Description: Fetches detailed information about a specific work in JSON format.
    - Example: https://openlibrary.org/works/OL45804W.json

2. Work's Editions
    - Endpoint: '/{work_id}/editions.json'
    - Method: GET
    - Description: Fetches all editions of a specific work in JSON format.
    - Example: https://openlibrary.org/works/OL45804W/editions.json

3. Work's Bookshelves
    - Endpoint: '/{work_id}/bookshelves.json'
    - Method: GET
    - Description: Fetches information about the bookshelves a work is placed in.
    - Example: https://openlibrary.org/works/OL18020194W/bookshelves.json

4. Work's Ratings
    - Endpoint: '/{work_id}/ratings.json'
    - Method: GET
    - Description: Fetches rating information of a specific work.
    - Example: https://openlibrary.org/works/OL18020194W/ratings.json

Note:
Replace '{work_id}' with the specific ID of the work.
"""

chain_new = APIChain.from_llm_and_api_docs(llm, api_docs, verbose=True)

answer = chain_new.run("Can you give me all the details of the book Fantastic Mr Fox?")

print(answer)
