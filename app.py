import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.chains import VectorDBQAWithSourcesChain
from langchain import OpenAI
import xmltodict
import requests
import pickle
from bs4 import BeautifulSoup
import argparse


def extract_text_from(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    return "\n".join(line for line in lines if line)


r = requests.get("https://python.langchain.com/sitemap.xml")
xml = r.text
raw = xmltodict.parse(xml)

pages = []
for info in raw["urlset"]["url"]:
    # info example: {'loc': 'https://www.paepper.com/...', 'lastmod': '2021-12-28'}
    url = info["loc"]
    if "https://python.langchain.com/docs" in url:
        pages.append({"text": extract_text_from(url), "source": url})

text_splitter = CharacterTextSplitter(
    separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
)
docs, metadatas = [], []
for page in pages:
    splits = text_splitter.split_text(page["text"])
    docs.extend(splits)
    metadatas.extend([{"source": page["source"]}] * len(splits))
    print(f"Split {page['source']} into {len(splits)} chunks")

store = FAISS.from_texts(docs, OpenAIEmbeddings(), metadatas=metadatas)
with open("faiss_store.pkl", "wb") as f:
    pickle.dump(store, f)

parser = argparse.ArgumentParser(description="Langchain Q&A")
parser.add_argument("question", type=str, help="Your question for the Langchain Docs")
args = parser.parse_args()

with open("faiss_store.pkl", "rb") as f:
    store = pickle.load(f)

chain = VectorDBQAWithSourcesChain.from_llm(
    llm=OpenAI(temperature=0), vectorstore=store
)
result = chain({"question": args.question})

print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
