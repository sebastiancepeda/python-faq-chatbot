import warnings
warnings.filterwarnings("ignore")
import streamlit as st
from loguru import logger
from lib.rag import ConversationalRAGSystem
from lib.corpus import load_corpus
from lib.faiss_index import build_faiss_index, CorpusIndex
from lib.generators import LLaMATextGenerator

def get_config():
    return {
        "data_path": "data/python_faqs.json",
        "retriever_model_name": "all-MiniLM-L6-v2",
        "base_url": "http://localhost:11434/v1/",
        "model_name": "llama3",
    }

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

def initialize_logger():
    if 'logger_initialized' not in st.session_state:
        logger.add("rag_system.log", rotation="1 MB", retention="1 week")
        st.session_state['logger_initialized'] = True
        logger.info("Logger initialized")

def initialize_session_state():
    initialize_logger()
    if 'rag_llama' not in st.session_state:
        config = get_config()
        st.session_state['rag_llama'] = create_rag_system(
            config['data_path'],
            config['retriever_model_name'],
            config['base_url'],
            config['model_name']
        )
    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = []

def get_rag_message(query):
    try:
        response = st.session_state['rag_llama'].rag(query, top_k=3)
        return response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Error during query processing: {str(e)}")

def main():
    st.set_page_config(page_title="Python FAQ Chatbot", page_icon="💬")

    initialize_session_state()

    st.title("Python FAQ Chatbot")
    st.write("Ask a question related to Python, and I will retrieve relevant information and answer.")

    # Chat history
    for exchange in st.session_state['conversation_history']:
        st.chat_message(exchange["role"]).write(exchange["content"])

    # New query
    if prompt := st.chat_input("Enter your question here:"):
        logger.info(f"{prompt}")
        st.session_state['conversation_history'].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = get_rag_message(prompt)
        logger.info(f"{response}")
        st.session_state['conversation_history'].append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

if __name__ == "__main__":
    main()
