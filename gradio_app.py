import gradio as gr
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)



API_URL = "http://127.0.0.1:8000/api/uploadfile"

stored_text = ""


def upload_doc(file):

    global stored_text

    if file is None:
        raise gr.Error("Please upload a document.")

    with open(file.name, "rb") as f:

        response = requests.post(
            API_URL,
            files={"file": f}
        )

    result = response.json()

    stored_text = result.get("extracted_text", "")

    structured_data = result.get("structured_data", {})

    status = """
✅ Document Processed Successfully

• OCR Extraction Completed
• Structured Data Generated
• Embeddings Created
• Ready for RAG Chat
"""

    return (
        stored_text,
        structured_data,
        status
    )


def chat_with_doc(message, history):

    global stored_text

    if not stored_text:
        return "Please upload a document first."

    prompt = f"""
You are a helpful AI document assistant.

Answer ONLY from the uploaded document.

DOCUMENT:
{stored_text}

QUESTION:
{message}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You answer questions using uploaded documents."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="slate",
    neutral_hue="gray"
)


with gr.Blocks(
    title="DocuParse Engine",
    theme=theme
) as demo:

    gr.Markdown(
        """
# 📄 DocuParse Engine

### AI-Powered Document Extraction + RAG System

FastAPI • OCR • GPT-4 • ChromaDB • PostgreSQL
"""
    )

    with gr.Row():

        with gr.Column(scale=1):

            gr.Markdown("## 📤 Upload Document")

            file_input = gr.File(
                label="Upload PDF / Image",
                file_types=[".pdf", ".png", ".jpg", ".jpeg"]
            )

            upload_btn = gr.Button(
                "⚡ Process Document",
                variant="primary"
            )

            status_box = gr.Textbox(
                label="Processing Status",
                lines=8,
                interactive=False
            )

            gr.Markdown("## ⚙️ AI Pipeline")

            gr.HTML(
                """
<div style="
padding:15px;
border-radius:12px;
background:#111827;
color:white;
line-height:2;
font-size:16px;
">

📥 Upload Document <br>
⚙️ OCR + Text Extraction <br>
🧠 LLM Structured Extraction <br>
🔍 Embedding Generation <br>
💬 RAG Question Answering

</div>
"""
            )

        with gr.Column(scale=2):

            with gr.Tab("📄 Extracted Text"):

                extracted_text = gr.Textbox(
                    label="Extracted Text",
                    lines=20
                )

            with gr.Tab("🧾 Structured JSON"):

                structured_json = gr.JSON(
                    label="Structured Output"
                )

            with gr.Tab("💬 Chat With Document"):

                chatbot = gr.ChatInterface(
                    fn=chat_with_doc,
                    chatbot=gr.Chatbot(
                        height=500
                    ),
                    textbox=gr.Textbox(
                        placeholder="Ask questions about the uploaded document...",
                        container=False
                    )
                )

    upload_btn.click(
        fn=upload_doc,
        inputs=file_input,
        outputs=[
            extracted_text,
            structured_json,
            status_box
        ]
    )

demo.launch(
    inbrowser=True
)