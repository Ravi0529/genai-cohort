from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai

# from langchain_openai import OpenAIEmbeddings
# from langchain_qdrant import QdrantVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

pdf_path = Path(__file__).parent / "nodejs.pdf"
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()
# print("Docs: ", docs)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
split_docs = text_splitter.split_documents(documents=docs)
# print("Split texts: ", text_splitter)
# Split texts:  <langchain_text_splitters.character.RecursiveCharacterTextSplitter object at 0x000002707F075730>

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

embedder = client.models.embed_content(
    model="gemini-embedding-exp-03-07"
)

# print(embedder.embeddings)
# print("Injection Done")
