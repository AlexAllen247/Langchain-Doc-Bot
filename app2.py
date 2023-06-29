from dotenv import load_dotenv
import os
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
embeddings = OpenAIEmbeddings(
    disallowed_special=(), openai_api_key=openai_api_key, model="text-embedding-ada-002"
)

root_dir = "/home/alex/repos/langchain"
docs = []

for dirpath, dirnames, filenames in os.walk(root_dir):
    for file in filenames:
        try:
            loader = TextLoader(os.path.join(dirpath, file), encoding="utf-8")
            docs.extend(loader.load_and_split())
        except Exception as e:
            pass

print (f"You have {len(docs)} documents\n")
print ("------ Start Document ------")
print (docs[0].page_content[:200])

docsearch = FAISS.from_documents(docs, embeddings)

retrievalQA = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())

query = "What can you tell me about this git repository?"
output = retrievalQA.run(query)
print (output)