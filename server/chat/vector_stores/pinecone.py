import os
import pinecone
from langchain.vectorstores import Pinecone
from server.chat.embeddings.openai import embeddings

pinecone.init(
    api_key=os.getenv("PINECONE_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT"),
    )   # Initialize Pinecone


pinecone_vector_store = Pinecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"), embeddings
)

def build_retriever(chat_args, k):
    # "filter": { "pdf_id": chat_args.pdf_id },
    search_kwargs = {
        "k": k
    }
    return pinecone_vector_store.as_retriever(
        search_kwargs=search_kwargs
    )
    
