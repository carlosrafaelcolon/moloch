from flask import Blueprint, request, jsonify
from server.chat.create_embeddings import create_embeddings_for_articles    
chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/embeddings', methods=['POST'])
def embeddings():
    #grab eventid from post request
    eventid = request.form.get('eventid')  
    
    # call create_embeddings_for_articles(eventid) here
    results = create_embeddings_for_articles(eventid)
    return results
    # return jsonify({
    #     "eventid":eventid,
    #     "chunks":results
    #     })
