import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

#load dot api key
groq_api_key=os.environ['GROQ_API_KEY']
if "vector" not in st.session_state:
    st.session_state.embeddings=OllamaEmbeddings()
    st.session_state.loader=WebBaseLoader("www.google.com")
    st.session_state.docs=st.session_state.loader.load()
    st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=200)
    st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs,st.session_state.embeddings)
    st.session_state.vector=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)
st.title("ChatGroq")
llm=ChatGroq(groq_api_key=groq_api_key,
             model_name="Gemma-7b-It")
prompt=ChatPromptTemplate.from_template(
    """
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}<context> Questions:{input}"""
)
document_chain=create_stuff_documents_chain(llm,prompt)
retriever=st.seesion_state.vector.as_retriever()
retrieval_chain=create_retrieval_chain(retriever,document_chain)
