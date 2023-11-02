from flask import Blueprint, request, jsonify
from server.chat.create_embeddings import create_embeddings_for_articles
from server.chat.chat import main
from server.chat.sim_search import fixed_search_results

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/embeddings', methods=['POST'])
def embeddings():
    #grab eventid from post request
    eventid = request.form.get('eventid')  
    
    # call create_embeddings_for_articles(eventid) here
    results = create_embeddings_for_articles(eventid)
    return results
 


@chat_bp.route('/run_chat')
def run_chat():
    result = main()
    return jsonify({'result': result})  

# for demonstration purposes - change to POST and exec search_results(query, eventid, top_k=5 ) in final version
# http://127.0.0.1:5000/chat/run_search
@chat_bp.route('/run_search')
def run_search():
    results = fixed_search_results()
    return jsonify(results)  
