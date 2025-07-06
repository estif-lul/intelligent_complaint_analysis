from transformers import pipeline
from prompt_template import build_prompt
from retriever import retrieve_top_k_chunks

generator = pipeline('text-generation', model='tiiuae/falcon-7b-instruct', max_new_tokens=200)

def answer_question(question):
    chunks = retrieve_top_k_chunks(question)
    prompt = build_prompt(chunks, question)
    response = generator(prompt, return_full_text=False)[0]['generated_text']
    return response.strip(), chunks
