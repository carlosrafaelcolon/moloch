from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from server.chat.vector_stores.pinecone import vector_store

import json
from flask import jsonify


def documents_to_dict(documents):
    return [{'page_content': doc.page_content, 'metadata': doc.metadata} for doc in documents]


def create_embeddings_for_articles(eventid: str):


    # load JSON data from file
    with open('server/data/events.json') as f:
        data = json.load(f)
    
    # Access the event with the given eventid
    event = data.get(eventid)

    # Access the sources key
    sources = event['sources']
    
    # Concatenate the text from each source
    large_text = ' '.join(source['text'] for source in sources)
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=70,
    )
    # Split the large text into chunks
    docs = text_splitter.split_text(large_text)
    
     # Create a list of Document objects with the page_content attribute set to each chunk of text
    documents = [Document(page_content=doc, metadata={'eventid': eventid, 'text': doc}) for doc in docs]
    
    for doc in documents:
        doc.metadata = {
            'eventid': eventid,
            'text': doc.page_content
        }
    vector_store.add_documents(documents)    # Add the chunks to the vector store
    
    return jsonify(documents_to_dict(documents))


