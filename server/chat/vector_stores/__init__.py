from functools import partial
from .pinecone import build_retriever
from .chroma import (
    build_retriever as chroma_retriever,
    chroma_vector_mpnet,
    chroma_vector_openai
)
# from .chroma import (build_mpnet_retriever, build_openai_retriever)

retriever_map = {
    "pinecone_3": partial(build_retriever, k=3),
    "pinecone_4": partial(build_retriever, k=4),
    "mpnet_3": partial(chroma_retriever,  vector_store=chroma_vector_mpnet, k=3),
    "mpnet_4": partial(chroma_retriever,  vector_store=chroma_vector_mpnet, k=4),
    "openai_3": partial(chroma_retriever, vector_store=chroma_vector_openai, k=3),
    "openai_4": partial(chroma_retriever, vector_store=chroma_vector_openai, k=4)
}
