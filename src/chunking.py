from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import torch
import pickle

# Load cleaned data
df = pd.read_parquet('data/processed/filtered_complaints.parquet')

# Initialize text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 50,
    separators = ['\n\n', '\n', '.', ' ']
)

# Apply chunking
documents = []
for idx, row in df.iterrows():
    chunks = splitter.split_text(row['cleaned_narrative'])
    for chunk in chunks:
        documents.append({
            'text': chunk,
            'product': row['Product'],
            'complaint_id': row.get('Complaint ID', idx)
        })

print(f"✅ Total chunks created: {len(documents)}")

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2', device="cuda")

# Embed chunks
texts = [doc['text'] for doc in documents]
embeddings = model.encode(texts, show_progress_bar=True, batch_size=32, convert_to_tensor=True)

# Attach embeddings to documents
for i, emb in enumerate(embeddings):
    documents[i]['embedding'] = emb.tolist()

# Save to disk
with open('vector_store/chunks_with_embeddings.pkl', 'wb') as f:
    pickle.dump(documents, f)