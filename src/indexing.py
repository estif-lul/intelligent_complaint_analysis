import faiss
import numpy as np
import pickle

# Load embedded documents
with open('vector_store/chunks_with_embeddings.pkl', 'rb') as f:
    documents = pickle.load(f)

# Prepare index
dimension = len(documents[0]['embedding'])
index = faiss.IndexFlatL2(dimension)

# Add vectors
vectors = np.array([doc['embedding'] for doc in documents]).astype('float32')
index.add(vectors)

# Save index
faiss.write_index(index, 'vector_store/faiss_index.index')

print('Vector store idexed and saved')