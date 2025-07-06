import gradio as gr
from src.generator import answer_question
import datetime

chat_history = []

def chat_fn(message, history, product_filter):
    full_query = f"{message} [Product: {product_filter}]" if product_filter else message
    answer, sources = answer_question(full_query)
    
    # Format sources
    source_texts = "\n\n".join([f"• {chunk['text'][:300]}..." for chunk in sources[:2]])
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    # Append to history
    history.append((message, f"{answer}\n\n**Sources:**\n{source_texts}\n\n_{timestamp}_"))
    return "", history

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 💬 CrediTrust Complaint Assistant")
    gr.Markdown("Ask questions about customer complaints. The assistant will respond with grounded answers and source excerpts.")

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="Conversation", height=400)
            msg = gr.Textbox(label="Your Question", placeholder="e.g., Why are users unhappy with BNPL?")
            submit = gr.Button("Ask")
            clear = gr.Button("Reset Chat")

        with gr.Column(scale=1):
            product_filter = gr.Dropdown(
                choices=["", "Credit card", "Personal loan", "Buy Now, Pay Later (BNPL)", "Savings account", "Money transfers"],
                label="Filter by Product",
                value=""
            )
            gr.Markdown("🔍 Use the dropdown to narrow your query to a specific product.")

    submit.click(chat_fn, inputs=[msg, chatbot, product_filter], outputs=[msg, chatbot])
    clear.click(lambda: ("", []), inputs=[], outputs=[msg, chatbot])

demo.launch()