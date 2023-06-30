from langchain.chains.api.prompt import API_RESPONSE_PROMPT
from langchain.chains import APIChain
from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains.api import open_meteo_docs
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

chain_new = APIChain.from_llm_and_api_docs(
    llm, open_meteo_docs.OPEN_METEO_DOCS, verbose=True
)

answer = chain_new.run(
    "Can you give me the current weather in Marbella, Spain?"
)

print(answer)