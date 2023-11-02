from server.chat.vector_stores.pinecone import vector_store
from server.chat.models import ChatArgs, QArgs


def search_results(query:str, eventid:str, top_k=5 ):

    q_args = QArgs(eventid=eventid)  # Initialize QArgs with the necessary arguments
    results = vector_store.similarity_search(query, k=top_k, filter={"eventid": q_args.eventid})
    content_list = [result.page_content for result in results]
    return {
        "eventid": eventid,
        "results": content_list
    }

# for demonstration purposes - delete in completed version
def fixed_search_results():
    query = "What is the method of attack and the weapons used?"
    q_args = QArgs(eventid=202001010001) 

    results = vector_store.similarity_search(query, k=5, filter={"eventid": q_args.eventid})
    print("\n")
    print("\n")
    print("START OF RESULTS")
    print("------------------------------------")
    print("\n")
    print("eventid: 202001010001")
    print("\n")
    print("Question: What is the method of attack and the weapons used?")
    print("\n")
    for i, result in enumerate(results, start=1):
        print("\n")
        print(f"Chunk {i}: {result.page_content}")
    print("\n")
    print("------------------------------------")
    print("END OF RESULTS")
    print("\n")
    print("\n")
    content_list = [result.page_content for result in results]
    return {
        "eventid": "202001010001",
        "results": content_list
    }