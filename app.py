import warnings
warnings.filterwarnings("ignore")
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import streamlit as st
from loguru import logger

from lib.rag import ConversationalRAGSystem
from lib.corpus import load_corpus
from lib.faiss_index import build_faiss_index, CorpusIndex
from lib.generators import LLaMATextGenerator

@st.cache_resource
def load_corpus_index(file_path, retriever_model_name='all-MiniLM-L6-v2'):
    corpus = load_corpus(file_path)
    retriever, index = build_faiss_index(corpus, retriever_model_name)
    return CorpusIndex(corpus, index, retriever)

@st.cache_resource
def create_rag_system(file_path, retriever_model_name='all-MiniLM-L6-v2', base_url='http://localhost:11434/v1/', model_name='llama3'):
    logger.info("Creating RAG")
    corpus_index = load_corpus_index(file_path, retriever_model_name)
    text_generator = LLaMATextGenerator(base_url=base_url, model=model_name)
    return ConversationalRAGSystem(corpus_index=corpus_index, text_generator=text_generator)

def main():
    if 'logger_initialized' not in st.session_state:
        logger.add("rag_system.log", rotation="1 MB", retention="1 week")
        st.session_state['logger_initialized'] = True
        logger.info("Reload")

    if 'rag_llama' not in st.session_state:
        st.session_state['rag_llama'] = create_rag_system("data/python_faqs.json")

    st.title("Conversational RAG Question Answering System")
    st.write("Ask a question related to Python, and the RAG system will retrieve relevant information and generate an answer. The system will remember the conversation context.")

    def submit_query():
        if st.session_state.query:
            response = st.session_state['rag_llama'].rag(st.session_state.query, top_k=3)
            if 'conversation_history' not in st.session_state:
                st.session_state['conversation_history'] = []
            st.session_state['conversation_history'].append({"user": st.session_state.query, "bot": response})

    st.text_input("Enter your question here:", on_change=submit_query, key='query')
    if st.button("Get Answer"):
        submit_query()

    if 'conversation_history' in st.session_state:
        st.subheader("Conversation History")
        for exchange in st.session_state['conversation_history']:
            st.write(f"**You:** {exchange['user']}")
            st.write(f"**Bot:** {exchange['bot']}")

if __name__ == "__main__":
    main()
