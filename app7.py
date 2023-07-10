from langchain.chains.api.prompt import API_RESPONSE_PROMPT
from langchain.chains import APIChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.llms import OpenAI
from langchain.chains import SequentialChain, LLMChain

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

api_docs = """
Public APIs

Base URL: https://api.publicapis.org/

The Public APIs provides access to various public APIs data and information.

API Endpoints:

1. GET /entries
    List all entries currently cataloged in the project

    Query Parameters:
    - title (string): name of entry (matches via substring - i.e. "at" would return "cat" and "atlas")
    - description (string): description of entry (matches via substring)
    - auth (string): auth type of entry (can only be values matching in project or null)
    - https (bool): return entries that support HTTPS or not
    - cors (string): CORS support for entry ("yes", "no", or "unknown")
    - category (string): return entries of a specific category. For categories like "Science & Math" which have a space and an ampersand, the query is simply the first word. Using "Science & Math" as an example, the correct query would be category=science

2. GET /random
    List a single entry selected at random

    Query Parameters:
    - title (string): name of entry (matches via substring - i.e. "at" would return "cat" and "atlas")
    - description (string): description of entry (matches via substring)
    - auth (string): auth type of entry (can only be values matching in project or null)
    - https (bool): return entries that support HTTPS or not
    - cors (string): CORS support for entry ("yes", "no", or "unknown")
    - category (string): return entries of a specific category

3. GET /categories
    List all categories

4. GET /health
    Check health of the running service
"""

chain_new = APIChain.from_llm_and_api_docs(llm, api_docs, verbose=True)

answer = chain_new.run("Can you give me a list of Public APIs realted to health I can use?")

print(answer)

