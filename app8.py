from langchain.chains.api.prompt import API_RESPONSE_PROMPT
from langchain.chains import APIChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

api_docs = """
CoinGecko API Documentation

Base URL: https://api.coingecko.com/api/v3/

Endpoints:
- GET /ping
    Check API server status

- GET /simple/price
    Get the current price of any cryptocurrencies in any supported currencies

- GET /simple/token_price/{id}
    Get current price of tokens (using contract addresses) for a given platform

- GET /simple/supported_vs_currencies
    Get list of supported_vs_currencies

- GET /coins/list
    List all supported coins id, name, and symbol

- GET /coins/markets
    List all supported coins price, market cap, volume, and market related data

- GET /coins/{id}
    Get current data (name, price, market, etc.) for a coin

- GET /coins/{id}/tickers
    Get coin tickers (paginated to 100 items)

- GET /coins/{id}/history
    Get historical data (price, market cap, 24hr volume, etc.) at a given date for a coin

- GET /coins/{id}/market_chart
    Get historical market data including price, market cap, and 24h volume (granularity auto)

- GET /coins/{id}/market_chart/range
    Get historical market data including price, market cap, and 24h volume within a range of timestamp (granularity auto)

- GET /coins/{id}/ohlc
    Get coin's OHLC (Open, High, Low, Close) data

- GET /coins/{id}/contract/{contract_address}
    Get coin info from contract address

- GET /coins/{id}/contract/{contract_address}/market_chart/
    Get historical market data including price, market cap, and 24h volume (granularity auto) from a contract address

- GET /coins/{id}/contract/{contract_address}/market_chart/range
    Get historical market data including price, market cap, and 24h volume within a range of timestamp (granularity auto) from a contract address

- GET /asset_platforms
    List all asset platforms (Blockchain networks)

- GET /coins/categories/list
    List all categories

- GET /coins/categories
    List all categories with market data

- GET /exchanges
    List all exchanges (Active with trading volumes)

- GET /exchanges/list
    List all supported markets id and name (no pagination required)

- GET /exchanges/{id}
    Get exchange volume in BTC and top 100 tickers only

- GET /exchanges/{id}/tickers
    Get exchange tickers (paginated, 100 tickers per page)

- GET /exchanges/{id}/volume_chart
    Get volume_chart data (in BTC) for a given exchange

- GET /indexes
    List all market indexes

- GET /indexes/{market_id}/{id}
    Get market index by market id and index id

- GET /indexes/list
    List market indexes id and name

- GET /derivatives
    List all derivative tickers

- GET /derivatives/exchanges
    List all derivative exchanges

- GET /derivatives/exchanges/{id}
    Show derivative exchange data

- GET /derivatives/exchanges/list
    List all derivative exchanges name and identifier

- GET /nfts/list
    List all supported NFT ids, paginated by 100 items per page

- GET /nfts/{id}
    Get current data (name, price_floor, volume_24h, etc.) for an NFT collection

- GET /nfts/{asset_platform_id}/contract/{contract_address}
    Get current data (name, price_floor, volume_24h, etc.) for an NFT collection

- GET /exchange_rates
    Get BTC-to-Currency exchange rates

- GET /search
    Search for coins, categories, and markets on CoinGecko

- GET /search/trending
    Get trending search coins (Top-7) on CoinGecko in the last 24 hours

- GET /global
    Get cryptocurrency global data

- GET /global/decentralized_finance_defi
    Get cryptocurrency global decentralized finance (defi) data

- GET /companies/public_treasury/{coin_id}
    Get public companies data
"""

chain_new = APIChain.from_llm_and_api_docs(llm, api_docs, verbose=True)

answer = chain_new.run("Can you give an analysis of the price of BTC?")

print(answer)

