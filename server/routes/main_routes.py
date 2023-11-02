from server import app
import json
from flask import jsonify

@app.route('/')
def index():
    return "<h1>Home</h1>"

@app.route('/code/<string:eventid>')
def code(eventid:str):
    # load JSON data from file
    with open('server/data/events.json') as f:
        data = json.load(f)
        
    # access the data based on the eventid
    event_data = data.get(eventid)
    
    if event_data is not None:
        # If data for the eventid exists, return it as a JSON response
        return jsonify(event_data)
    else:
        # If data for the eventid does not exist, return 202001010001 as default
        default_data = data.get("202001010001")
        return jsonify(default_data)
