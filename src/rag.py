import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

from transformers import pipeline
from prompt_template import build_prompt
from retriever import retrieve_top_k_chunks

# Load index and metadata
index = faiss.read_index('vector_store/faiss_index.index')
with open('vector_store/chunks_with_embeddings.pkl') as f:
    documents = pickle.load(f)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_top_k_chunks(query, k=5):
    query_vec = model.encode([query]).astype('float32')
    distance, indices = index.search(query_vec, k)
    return [documents[i] for i in indices[0]]

def build_prompt(context_chunks, question):
    context = "\n\n".join([f"- {chunk['text']}" for chunk in context_chunks])
    return f"""You are a financial analyst assistant for CrediTrust. Your task is to answer questions about customer complaints.

            Use the following retrieved complaint excerpts to formulate your answer. If the context doesn't contain the answer, say so.

            Context:
            {context}

            Question: {question}
            Answer:"""

generator = pipeline('text-generation', model='tiiuae/falcon-7b-instruct', max_new_tokens=200)

def answer_question(question):
    chunks = retrieve_top_k_chunks(question)
    prompt = build_prompt(chunks, question)
    response = generator(prompt, return_full_text=False)[0]['generated_text']
    return response.strip(), chunks

