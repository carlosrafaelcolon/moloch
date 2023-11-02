import os
import pinecone
from langchain.vectorstores import Pinecone
from server.chat.embeddings.openai import embeddings
from server.chat.models import QArgs

pinecone.init(
    api_key=os.getenv("PINECONE_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT"),
    )   # Initialize Pinecone


vector_store = Pinecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"), embeddings
)

def build_chat_retriever(chat_args):
    return vector_store.build_retriever()

def build_retriever(q_args: QArgs):
    search_kwargs = {"filter": {"eventid": q_args.eventid}}
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )

