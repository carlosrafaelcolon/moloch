from server import app
import json
from flask import jsonify, render_template

@app.route('/')
def index():
    return render_template('home.html')


