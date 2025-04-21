from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
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

embedder = GoogleGenerativeAIEmbeddings(
    google_api_key=os.getenv("GEMINI_API_KEY"), model="models/text-embedding-004"
)

# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     collection_name="learning_langchain",
#     embedding=embedder,
# )
# vector_store.add_documents(documents=split_docs)
# print("Injection Done")

retrival = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embedder,
)

search_results = retrival.similarity_search(
    query="What is FS Module?"
)
print("Relevant chunks: ", search_results)

# system prompt
system_prompt = f"""
    You are an helpful AI assistant that is used to answer questions.

    context: {search_results}
"""
