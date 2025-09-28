import os
import tempfile
import streamlit as st
from embedchain import App
# from embedchain import App
import base64
from streamlit_chat import message

# Configure embedchain App- we are using ollama specifically llama3.2
def embedchain_bot(db_path):
    return App.from_config(
        config = {
            "llm": {"provider":"ollama", "config": {"model":"llama3.2:latest", "max_tokens":250,
                                                    "temperature": 0.5, "stream": True, "base_url": 'http://localhost:11434'}},
            "vectordb": {"provider": "chroma", "config": {"dir":db_path}},
            "embedder": {"provider": "ollama", "config": {"model": "llama3.2:latest", "base_url": 'http://localhost:11434'}},
        }
    )

#Add function to display PDF's in the streamlit app
def display_pdf(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64, {base64_pdf}" width="100%" height="400" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

#streamlit title and prep
st.title("Chat with your PDF's using LLM's")
st.caption("This App lets you chat with your model")

db_path = tempfile.mkdtemp() #db to store  pdf temporarily

if 'app' not in st.session_state:
    st.session_state.app = embedchain_bot(db_path)
if 'message' not in st.session_state:
    st.session_state.messages = []

#sidebar for pdf upload
with st.sidebar:
    st.header("PDF Upload")
    pdf_file = st.file_upload("Upload a PDF File", type="pdf")

    if pdf_file:
        st.subheader("PDF Preview")
        display_pdf(pdf_file)

#add pdf to knowledge base
if st.button("Submit PDF"):
    with st.spinner("Adding PDF to knowledge base..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(pdf_file.getvalue())
            st.session_state.app.add(f.name, data_type="pdf_file")
        os.remove(f.name)
    st.success(f"Added {pdf_file.name} to knowledge base!")

#Set up chat interface
for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=msg["role"] == "user", key=str[i])

if prompt:= st.chat_input("Ask a question about the PDF"):
    st.session_state.messages.append({"role":"user", "content":prompt})
    message(prompt, is_user=True)

#User query and display responses
with st.spinner("Thinking..."):
    response = st.session_state.app.chat(prompt)
    st.session_state.messagers.append({"role":"assistant","content": response})
    message(response)

if st.button("Clear Chat"):
    st.session_state.messages = []