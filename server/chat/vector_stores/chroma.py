from langchain.vectorstores import Chroma
from server.chat.embeddings.openai import embeddings as openai_embeddings
from server.chat.embeddings.mpnet import embeddings as mpnet_embeddings


chroma_vector_openai = Chroma("langchain_store_openai", openai_embeddings, persist_directory="server/db/emb_openai")

chroma_vector_mpnet = Chroma("langchain_store_mpnet", mpnet_embeddings, persist_directory="server/db/emb_mpnet")

chroma_vector_test= Chroma("langchain_store_mpnet_test", mpnet_embeddings, persist_directory="server/db/emb_mpnet_test")

def build_retriever(chat_args,vector_store: Chroma, k):
    search_kwargs = {
        "k": k
    }
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )
