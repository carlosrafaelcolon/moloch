from flask import Blueprint, g, request, Response, jsonify, stream_with_context
from server.models import Conversation
from server.chat import build_chat, ChatArgs

class ConversationController:
    @staticmethod
    def create_conversation(user_id):
        conversation = Conversation.create(user_id=user_id)
        return conversation.as_dict()

    @staticmethod
    def create_message(conversation, input, user_id, streaming):
        chat_args = ChatArgs(
            conversation_id=conversation.id,
            streaming=streaming,
            metadata={
                "conversation_id": conversation.id,
                "user_id": user_id
            },
        )
  
        chat = build_chat(chat_args)

        if not chat:
            return None, "Chat not yet implemented!"

        if streaming:
            return Response(
                stream_with_context(chat.stream(input)), mimetype="text/event-stream"
            ), None
        else:
            return jsonify({"role": "assistant", "content": chat.run(input)}), None
