from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from server.chat.vector_stores.pinecone import pinecone_vector_store
from server.chat.vector_stores.chroma import (
    chroma_vector_mpnet,
    chroma_vector_openai
)


        
def print_pdf_content(pdf_path):
    loader = PyPDFLoader(pdf_path)

    # Using load() to eagerly load the entire document
    documents = loader.load()

    # Iterate through each document (page) and print its content
    for i, doc in enumerate(documents):
        print(f"Page {i + 1}:")
        print(doc.page_content)  # Assuming the content is stored in 'page_content'
        print("-" * 50)



def create_embeddings_for_pdf(pdf_path: str):
    # completed version should be a func that accepts a file path and id when file is uploaded
    #filePath = "server/static/pdf/2022_Statistical_Annex_Final__508_Compliant-revised.pdf"
   
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    
    loader = PyPDFLoader(pdf_path)
    docs = loader.load_and_split(text_splitter)
    
    for doc in docs:
        doc.metadata = {
            "page": doc.metadata["page"],
            "text": doc.page_content
        }
        
        
    
    
    # pinecone_vector_store.add_documents(docs)
    # chroma_vector_mpnet.add_documents(docs)
    # chroma_vector_openai.add_documents(docs)
    total_chunks = len(docs)
    print(f"Total number of chunks: {total_chunks}")

    # Adding documents to the vector store and checking success
    added_ids_pinecone = pinecone_vector_store.add_documents(docs)
    print(f"Number of chunks added to Pinecone vector store: {len(added_ids_pinecone)}")

    added_ids_chroma_mpnet = chroma_vector_mpnet.add_documents(docs)
    print(f"Number of chunks added to Chroma MPNet vector store: {len(added_ids_chroma_mpnet)}")

    added_ids_chroma_openai = chroma_vector_openai.add_documents(docs)
    print(f"Number of chunks added to Chroma OpenAI vector store: {len(added_ids_chroma_openai)}")

    # Check if all chunks were added successfully
    all_added_pinecone = len(added_ids_pinecone) == total_chunks
    all_added_chroma_mpnet = len(added_ids_chroma_mpnet) == total_chunks
    all_added_chroma_openai = len(added_ids_chroma_openai) == total_chunks

    print(f"All chunks stored in Pinecone vector store: {all_added_pinecone}")
    print(f"All chunks stored in Chroma MPNet vector store: {all_added_chroma_mpnet}")
    print(f"All chunks stored in Chroma OpenAI vector store: {all_added_chroma_openai}")
    
    
        
    