from flask import Flask
from server.config import Config
app = Flask(__name__)
app.config.from_object(Config)  # Config is a class in config.py
from server.routes import main_routes
from server.routes.chat_routes import chat_bp
app.register_blueprint(chat_bp)
# if __name__ == '__main__':
#     app.run()
