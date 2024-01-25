from langchain.chains import ConversationalRetrievalChain
from server.chat.chains.streamable import StreamableChain

class StreamingConversationalRetrievalChain(
    StreamableChain, ConversationalRetrievalChain
):
    pass