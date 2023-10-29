from flask import Blueprint, request
from server.chat.create_embeddings import create_embeddings_for_articles    
chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/embeddings', methods=['POST'])
def embeddings():
    #grab eventid from post request
    eventid = request.form.get('eventid')  # Use request.form instead of request.args for POST requests
    
    # call create_embeddings_for_articles(eventid) here
    create_embeddings_for_articles(eventid)
    
    return "Messages"
