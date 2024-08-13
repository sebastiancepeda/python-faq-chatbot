from loguru import logger

from lib.faiss_index import CorpusIndex
from lib.generators import LLaMATextGenerator

class RAGSystem:
    def __init__(self, corpus_index, text_generator):
        self.corpus_index = corpus_index
        self.text_generator = text_generator

    def rag(self, query, top_k=3):
        query_embedding = self.corpus_index.retriever.encode(query, convert_to_tensor=True).unsqueeze(0)
        retrieved_docs = self.corpus_index.search(query_embedding, top_k)
        retrieved_text = " ".join(retrieved_docs)
        input_text = f"""
        The following is the context, use the information from there, even if it contradicts your knowledge:
        {retrieved_text}.
        
        Answer the following query shortly, using the context and your knowledge (just answer, don't give explanations):
        query: {query}
        """
        response = self.text_generator.generate_text(input_text)
        return response

class ConversationalRAGSystem(RAGSystem):
    def __init__(self, corpus_index, text_generator):
        super().__init__(corpus_index, text_generator)
        self.conversation_history = []

    def rag(self, query, top_k=3):
        self.conversation_history.append(query)
        
        conversation_history_str = " ".join(self.conversation_history)
        
        query_embedding = self.corpus_index.retriever.encode(query, convert_to_tensor=True).unsqueeze(0)
        retrieved_docs = self.corpus_index.search(query_embedding, top_k)
        retrieved_text = " ".join(retrieved_docs)
        # logger.info(retrieved_text)
        input_text = f"""
        This is the info of the past conversation:
        {conversation_history_str}
        
        The following is the context (queried from the corpus index), use the information from there, even if it contradicts your knowledge:
        {retrieved_text}
        
        Answer the following query shortly, using the context and your knowledge (just answer, don't give explanations):
        query: {query}
        """
        response = self.text_generator.generate_text(input_text)
        self.conversation_history.append(response)
        return response
