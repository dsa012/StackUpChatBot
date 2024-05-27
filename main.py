import os
import pymongo
import streamlit as st
from dotenv import load_dotenv
from llama_index.core import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from langchain_community.llms import EdenAI
from langchain_community.embeddings.edenai import EdenAiEmbeddings


# Page config
st.set_page_config(
    page_title="StackUp Helpdesk Bot 🤖",
    page_icon="🤖",
    layout="centered",
)

# Load environment variables
load_dotenv()

# Constants for database connection and API keys
ATLAS_URI = os.getenv('ATLAS_URI')
EDEN_API_KEY = os.getenv("EDEN_API_KEY")

DB_NAME = "stackup_zendesk"
COLLECTION_NAME = "data"

# MongoDB client setup
client = pymongo.MongoClient(ATLAS_URI)
collection = client[DB_NAME][COLLECTION_NAME]
VECTOR_DATABASE_FIELD_NAME = 'embedding'

# Embedding and LLM model setup
embed_model = EdenAiEmbeddings(edenai_api_key=EDEN_API_KEY, provider="openai", model="1536__text-embedding-ada-002")
llm = EdenAI(edenai_api_key=EDEN_API_KEY, provider="openai", temperature=0.9, max_tokens=1024)

# Service and storage contexts
service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)
vector_store = MongoDBAtlasVectorSearch(
    mongodb_client=client,
    db_name=DB_NAME, 
    collection_name=COLLECTION_NAME,
    index_name='idx_embeddings'
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Vector store index
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store, 
    service_context=service_context
)

st.header("StackUp Helpdesk Bot 🤖")
st.markdown("---")

# User prompt and response handling
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello fellow stackie, Have any queries ask me right away!"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Sample Question: What is the minimum amount for withdrawal?"):
    # Display user message in chat message container
    st.chat_message("stackie").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "stackie", "content": prompt})

    response = index.as_query_engine().query(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response.response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.response})
