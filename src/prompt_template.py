def build_prompt(context_chunks, question):
    """
    Builds a prompt for a financial analyst assistant to answer questions about customer complaints using provided context excerpts.
    Args:
        context_chunks (list of dict): A list of dictionaries, each containing a 'text' key with a complaint excerpt as its value.
        question (str): The question to be answered based on the provided context.
    Returns:
        str: A formatted prompt string instructing the assistant to answer the question using the given context, or indicate if the answer is not present.
    """

    context = "\n\n".join([f"- {chunk['text']}" for chunk in context_chunks])
    return f"""You are a financial analyst assistant for CrediTrust. Your task is to answer questions about customer complaints.

            Use the following retrieved complaint excerpts to formulate your answer. If the context doesn't contain the answer, say so.

            Context:
            {context}

            Question: {question}
            Answer:"""