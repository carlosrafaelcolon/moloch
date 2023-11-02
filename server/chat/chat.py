from server.chat.models import QArgs
from server.chat.vector_stores.pinecone import build_retriever
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

def build_q(q_args: QArgs):
    chat_model = ChatOpenAI()
    retriever = build_retriever(q_args)
    chain = RetrievalQA.from_chain_type(
        llm=chat_model,
        retriever=retriever,
        chain_type="stuff"
    )
    return chain

# for demonstration purposes - delete in completed version
def main():
    q_args = QArgs(eventid="202001010001")  # Initialize QArgs with the necessary arguments
    chain = build_q(q_args)
    result = chain.run("What is the method of attack and the weapon used?")
    print(result)
    return result

  