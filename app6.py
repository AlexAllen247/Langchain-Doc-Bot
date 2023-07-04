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
Bitfinex Public API

Base URL: https://api-pub.bitfinex.com/v2/

The Bitfinex Public API provides access to various trading data and information.

API Endpoints:

1. Platform Status
    - Endpoint: '/platform/status'
    - Method: GET
    - Description: Fetches the current status of the Bitfinex platform.
    
2. Tickers
    - Endpoint: '/tickers?symbols={symbols}'
    - Method: GET
    - Description: Fetches tickers for given symbols.
    - Parameters:
        - symbols: Comma separated list of symbols (e.g. "fUSD,tBTCUSD")
    
3. Ticker
    - Endpoint: '/ticker/{symbol}'
    - Method: GET
    - Description: Fetches a single ticker for a given symbol.
    - Parameters:
        - symbol: The symbol to fetch the ticker for (e.g. "tBTCUSD")

... (Other endpoints would be documented in similar fashion)

Calculation Endpoints:

1. Market Average Price
    - Endpoint: '/calc/market_average_price'
    - Method: POST
    - Description: Calculates the market average price based on the parameters provided.

... (Other calculation endpoints would be documented in similar fashion)

Notes:
Replace '{symbols}' and '{symbol}' with the relevant symbols.
"""


chain_new = APIChain.from_llm_and_api_docs(llm, api_docs, verbose=True)

answer_one = chain_new.run("Can you give me all the information about Ethereum?")

answer_two = chain_new.run("Can you give me all the information on Bitcoin?")

prompt = PromptTemplate(
    input_variables=["answer_one", "answer_two"],
    template="Analyze the following two answers: {answer_one} and {answer_two}. What is a combined answer?"
)

# Create the LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

# The result is the combined answer
print(chain)

