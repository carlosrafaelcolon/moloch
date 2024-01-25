from flask import Blueprint, jsonify, g, request
from server.hooks import login_required, load_model
from server.models import Conversation
from server.controllers import ConversationController

bp = Blueprint("conversation", __name__, url_prefix="/api/conversations")

@bp.route("/", methods=["GET"])
@login_required
def list_conversations():
    conversations = Conversation.where(user_id=g.user.id)
    return jsonify([conv.as_dict() for conv in conversations])
# def list_conversations(pdf):
#     return [c.as_dict() for c in pdf.conversations]



@bp.route("/", methods=["POST"])
@login_required
def create_conversation():
    return ConversationController.create_conversation(g.user.id)

@bp.route("/<string:conversation_id>/messages", methods=["POST"])
@login_required
@load_model(Conversation)
def create_message(conversation):
    
    input = request.json.get("input")
    streaming = request.args.get("stream", False)
    response, error = ConversationController.create_message(
        conversation, input, g.user.id, streaming
    )
    
    if error:
        return error

    return response