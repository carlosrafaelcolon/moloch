import random 
from server.chat.models import ChatArgs
from server.chat.vector_stores import retriever_map
from server.chat.llms import llm_map
#from server.chat.llms.chatopenai import build_llm
from server.chat.memories import memory_map
#from server.chat.memories.sql_memory import build_memory
from server.chat.chains.retrieval import StreamingConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

from server.api import (
    set_conversation_components,
    get_conversation_components
)

def select_component(
    component_type,
    component_map,
    chat_args
):
 
    components = get_conversation_components(
        chat_args.conversation_id
    )


    previous_component = components[component_type]
   
    
    if previous_component:
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)

    else:
        # print('random choice')
        # print(random.choice(list(component_map.keys())))
        # print('builder - component_map[random_name]')
        # print(component_map[random_name])
        # print("chat_args")
        # print(chat_args)
        random_name = random.choice(list(component_map.keys()))
        builder = component_map[random_name]
        return random_name, builder(chat_args)
    
    
def build_chat(chat_args):

    retriever_name, retriever = select_component(
        "retriever",
        retriever_map,
        chat_args
    )

    
    llm_name, llm = select_component(
        "llm",
        llm_map,
        chat_args
    )
    
    
    memory_name, memory = select_component(
        "memory",
        memory_map,
        chat_args
    ) 
   
    set_conversation_components(
        chat_args.conversation_id,
        llm=llm_name,
        retriever=retriever_name,
        memory=memory_name
    )
    
    condense_question_llm = ChatOpenAI(streaming=False)
 
    
    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm,
        memory=memory,
        retriever=retriever,
        metadata=chat_args.metadata
    )
