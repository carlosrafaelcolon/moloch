from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
from flask import jsonify

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

    print(large_text)
