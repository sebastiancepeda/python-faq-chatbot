import faiss
from sentence_transformers import SentenceTransformer

def build_faiss_index(corpus, retriever_model_name):
    retriever = SentenceTransformer(retriever_model_name)
    corpus_embeddings = retriever.encode(corpus, convert_to_tensor=True)
    index = faiss.IndexFlatL2(corpus_embeddings.shape[1])
    index.add(corpus_embeddings.cpu().numpy())
    return retriever, index

class CorpusIndex:
    def __init__(self, corpus, index, retriever):
        self.corpus = corpus
        self.index = index
        self.retriever = retriever

    def search(self, query_embedding, top_k=2):
        D, I = self.index.search(query_embedding.cpu().numpy(), top_k)
        retrieved_docs = [self.corpus[i] for i in I[0]]
        return retrieved_docs
