from transformers import pipeline
from src.prompt_template import build_prompt
from src.retriever import retrieve_top_k_chunks

generator = pipeline('text-generation', model='google/flan-t5-base', max_new_tokens=200)

def answer_question(question):
    """
    Answers a given question by retrieving relevant text chunks, building a prompt, and generating a response.
    Args:
        question (str): The question to be answered.
    Returns:
        tuple: A tuple containing:
            - response (str): The generated answer to the question.
            - chunks (list): The list of retrieved text chunks used to build the prompt.
    """

    chunks = retrieve_top_k_chunks(question)
    prompt = build_prompt(chunks, question)
    response = generator(prompt, return_full_text=False)[0]['generated_text']
    return response.strip(), chunks
