import gradio as gr
import requests
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
api_key=os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

stored_text = ""

API_URL = "http://127.0.0.1:8000/api/uploadfile"


def upload_doc(file):

    global stored_text

    with open(file.name, "rb") as f:

        response = requests.post(
            API_URL,
            files={"file": f}
        )

    result = response.json()

    stored_text = result.get("extracted_text", "")

    structured_data = result.get("structured_data", {})

    return (
        stored_text,
        structured_data
    )


def chat_with_doc(message, history):

    global stored_text

    if not stored_text:
        return "Please upload a document first."

    prompt = f"""
    You are a helpful AI document assistant.

    Use ONLY the document context below to answer.

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
                "content": "You answer questions from documents."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


with gr.Blocks() as demo:

    gr.Markdown("# DocuParse Engine")

    file_input = gr.File()

    extracted_text = gr.Textbox(
        label="Extracted Text",
        lines=15
    )

    structured_json = gr.JSON(
        label="Structured Data"
    )

    upload_btn = gr.Button("Process Document")

    upload_btn.click(
        upload_doc,
        inputs=file_input,
        outputs=[extracted_text, structured_json]
    )

    chatbot = gr.ChatInterface(
        fn=chat_with_doc
    )

demo.launch(inbrowser=True)