import openai
import requests
import json
from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_crypto_price(crypto_id, currency):
    # This function represents your call to the CoinGecko API
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={currency}'
    response = requests.get(url)
    return response.json()  # Assume this returns a dictionary with price data

# Step 1: Call the OpenAI API with function and user's input
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo-0613",
  messages=[
        {"role": "user", "content": 'What is the current price of Bitcoin in USD?'}
    ],
  functions=[
        {
            "name": "get_crypto_price",
            "description": "Get the current price of a cryptocurrency in a given currency",
            "parameters": {
                "type": "object",
                "properties": {
                    "crypto_id": {"type": "string"},
                    "currency": {"type": "string"}
                },
                "required": ["crypto_id", "currency"]
            },
        }
    ],
)

# Extract the function call data
function_call_data = response['choices'][0]['message']['function_call']['arguments']  

# Extract the 'crypto_id' and 'currency' arguments from the function call
crypto_id = function_call_data['crypto_id']
currency = function_call_data['currency']

# Step 2: Call the actual CoinGecko API using the extracted 'crypto_id' and 'currency'
price_data = get_crypto_price(crypto_id, currency)

# Step 3: Send the response back to the model to summarize
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo-0613",
  messages=[
        {"role": "user", "content": 'What is the current price of Bitcoin in USD?'},
        {"role": "assistant", "content": None, "function_call": {"name": "get_crypto_price", "arguments": { "crypto_id": crypto_id, "currency": currency}}},
        {"role": "function", "name": "get_crypto_price", "content": json.dumps(price_data)}
    ],
  functions=[
        {
            "name": "get_crypto_price",
            "description": "Get the current price of a cryptocurrency in a given currency",
            "parameters": {
                "type": "object",
                "properties": {
                    "crypto_id": {"type": "string"},
                    "currency": {"type": "string"}
                },
                "required": ["crypto_id", "currency"]
            },
        }
    ],
)

# The response should now contain a human-friendly summary of the cryptocurrency's current price
print(response['choices'][0]['message']['content'])