from langchain.chains.api.prompt import API_RESPONSE_PROMPT
from langchain.chains import APIChain
from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

api_key = os.getenv("USDA_API_KEY")

llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

api_docs = """
BASE URL: https://api.nal.usda.gov/fdc/v1/

API Documentation:

The API endpoint /food/{fdcId}?api_key={api_key} is used to fetch details for one food item. All URL parameters are listed below:
    - fdcId: ID of the food item. Ex: 123456, 789012
    - api_key: Your API key obtained from data.gov.
    
The API endpoint /foods?api_key={api_key} is used to fetch details for multiple food items. This endpoint can handle both GET and POST requests. In case of a POST request, a list of FDC IDs needs to be provided in the request body.

The API endpoint /foods/list?api_key={api_key} is used to return a paged list of foods in the 'abridged' format. This endpoint can also handle both GET and POST requests. In case of a POST request, additional parameters like 'pageSize' can be provided in the request body.

The API endpoint /foods/search?api_key={api_key} is used to return a list of foods that match search (query) keywords. This endpoint also accepts both GET and POST requests. For GET requests, the search query is passed as a URL parameter 'query'. For POST requests, the search query and other optional parameters can be provided in the request body.

For all the above endpoints, an API key obtained from data.gov is required.
"""

chain_new = APIChain.from_llm_and_api_docs(llm, api_docs, verbose=True)

answer = chain_new.run("Can you give me all the nutritional details for kidney beans?")

print(answer)
