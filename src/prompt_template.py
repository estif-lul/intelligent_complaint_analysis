def build_prompt(context_chunks, question):
    context = "\n\n".join([f"- {chunk['text']}" for chunk in context_chunks])
    return f"""You are a financial analyst assistant for CrediTrust. Your task is to answer questions about customer complaints.

            Use the following retrieved complaint excerpts to formulate your answer. If the context doesn't contain the answer, say so.

            Context:
            {context}

            Question: {question}
            Answer:"""