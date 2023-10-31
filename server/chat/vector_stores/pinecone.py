import os
import pinecone
from langchain.vectorstores import Pinecone
from server.chat.embeddings.openai import embeddings

pinecone.init(
    api_key=os.getenv("PINECONE_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT"),
    )   # Initialize Pinecone


vector_store = Pinecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"), embeddings
)

