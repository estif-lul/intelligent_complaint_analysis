import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

# Load index and metadata
index = faiss.read_index('vector_store/faiss_index.index')
with open('vector_store/chunks_with_embeddings.pkl', 'rb') as f:
    documents = pickle.load(f)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_top_k_chunks(query, k=5):
    """
    Retrieves the top-k most relevant document chunks for a given query.
    Args:
        query (str): The input query string to search for relevant document chunks.
        k (int, optional): The number of top relevant chunks to retrieve. Defaults to 5.
    Returns:
        list: A list of the top-k document chunks most relevant to the query.
    """
    
    query_vec = model.encode([query]).astype('float32')
    distance, indices = index.search(query_vec, k)
    return [documents[i] for i in indices[0]]




