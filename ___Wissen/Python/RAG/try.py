import os

# from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter

# load_dotenv()
# Start WSL and ollama
# ollama run DeepSeek-R1
# https://github.com/ollama/ollama

# ------------------------------- SELECT MODEL --------------------------------------------
# modelname = "llama3.2-vision"
# modelname = "DeepSeek-R1"
modelname = "phi4-mini"

# --------------------------------- SCRIPT ------------------------------------------------
def setup_qa_system(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model=modelname, base_url='http://localhost:11434')
    vector_store = FAISS.from_documents(chunks, embeddings)

    retriever = vector_store.as_retriever()
    llm = Ollama(model=modelname, base_url='http://localhost:11434')

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    return qa_chain

if __name__ == '__main__':
    qa_chain = setup_qa_system('___testdata\\diodes_low_frequency.pdf')

    while True:
        question = input('Whats your question?')
        if question.lower() == 'exit':
            break

        answer = qa_chain.invoke(question)
        print(f'Answer:\n {answer['result']}')
