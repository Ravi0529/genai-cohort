#### ERROR #### Code not working due to Gemini key limitations
#### ERROR #### Code not working due to Gemini key limitations
#### ERROR #### Code not working due to Gemini key limitations
#### ERROR #### Code not working due to Gemini key limitations
#### ERROR #### Code not working due to Gemini key limitations

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
from langchain_qdrant import QdrantVectorStore
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

texts = [doc.page_content.strip() for doc in split_docs if doc.page_content.strip()]
texts = texts[:1]

embedder = client.models.embed_content(
    model="gemini-embedding-exp-03-07", contents=texts
)
# print(embedder.embeddings)

embeddings = embedder.embeddings

vector_store = QdrantVectorStore.from_documents(
    documents=[],
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embeddings,
)
vector_store.add_documents(documents=texts)
print("Injection Done")
