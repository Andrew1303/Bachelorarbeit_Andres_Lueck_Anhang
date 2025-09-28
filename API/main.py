from sentence_transformers import SentenceTransformer
from progresbar import progresbar
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# To run go into folder of this script
# fastapi run main.py

# model = SentenceTransformer("Alibaba-NLP/gte-Qwen2-1.5B-instruct", trust_remote_code=True)
model = SentenceTransformer("Qwen/Qwen3-Embedding-8B")

# model = SentenceTransformer("Linq-AI-Research/Linq-Embed-Mistral")
# @misc{LinqAIResearch2024,
#   title={Linq-Embed-Mistral:Elevating Text Retrieval with Improved GPT Data Through Task-Specific Control and Quality Refinement},
#   author={Junseong Kim, Seolhwa Lee, Jihoon Kwon, Sangmo Gu, Yejin Kim, Minkyung Cho, Jy-yong Sohn, Chanyeol Choi},
#   howpublished={Linq AI Research Blog},
#   year={2024},
#   url={https://getlinq.com/blog/linq-embed-mistral/}
# }

# model = SentenceTransformer("GritLM/GritLM-7B")
# @misc{muennighoff2024generative,
#       title={Generative Representational Instruction Tuning}, 
#       author={Niklas Muennighoff and Hongjin Su and Liang Wang and Nan Yang and Furu Wei and Tao Yu and Amanpreet Singh and Douwe Kiela},
#       year={2024},
#       eprint={2402.09906},
#       archivePrefix={arXiv},
#       primaryClass={cs.CL}
# }

class Chunks(BaseModel):
    chunks: str
class Embeddings(BaseModel):
    embeddings: List[List[float]]
    prompt: str
    promptembedding: List[float]

@app.get("/embeddings")
def getEmbeddings(chunk:str):
    chunk_embedding = model.encode(chunk, normalize_embeddings=True)
    embeddings = chunk_embedding.tolist()
    # Load the model
    # model = SentenceTransformer("Alibaba-NLP/gte-Qwen2-1.5B-instruct", trust_remote_code=True)
    # print("Request with", chunk)
    # embeddings = model.encode(chunk, normalize_embeddings=True)
    # ----------- NO TOKENIZING ----------------------
    # amountChunks = len(req.chunks)
    # counter = 0
    # embeddings = []
    # for chunk in req.chunks:
    #     counter += 1
    #     progresbar(counter, amountChunks)
    #     chunk_embedding = model.encode(chunk, normalize_embeddings=True)
    #     embeddings.append(chunk_embedding.tolist())
    return embeddings

@app.get("/RAG")
def getChunk(embeddings: Embeddings):
    prompt = embeddings.prompt
    # print(prompt)
    # model = SentenceTransformer("Alibaba-NLP/gte-Qwen2-1.5B-instruct", trust_remote_code=True)
    promptembedding = model.encode(prompt, normalize_embeddings=True, prompt_name="query")
    # query_embeddings = model.encode(prompt, prompt_name="query")
    promptembedding = promptembedding.tolist()
    # print(promptembedding)
    # print(len(embeddings.embeddings))
    # print(type(embeddings.embeddings))
    scores = (promptembedding @ np.array(embeddings.embeddings).T) * 100
    return scores.tolist()

@app.get("/getContextForPrompt")
def getChunk(embeddings: Embeddings):
    prompt = embeddings.prompt
    # model = SentenceTransformer("Alibaba-NLP/gte-Qwen2-1.5B-instruct", trust_remote_code=True)
    promptembedding = model.encode(prompt, normalize_embeddings=True, prompt_name="query")
    # query_embeddings = model.encode(prompt, prompt_name="query")
    promptembedding = promptembedding.tolist()
    # print(promptembedding)
    # print(len(embeddings.embeddings))
    # print(type(embeddings.embeddings))
    scores = (promptembedding @ np.array(embeddings.embeddings).T) * 100
    return scores.tolist()

@app.get("/chat")
def chatting(data: Embeddings):
    prompt = data.prompt
    promptembedding = data.promptembedding
    scores = (promptembedding @ np.array(data.embeddings).T) * 100

    # -- Internal --
    # Embedd the prompt
    # Get highest score with context embeddings
    # Use prompt with context to generate an answer
    # return answer

    # -- external --
    # Receive prompt with context
    # Use prompt with context to generate an answer
    # return answer
    return

@app.get("/ping")
def ping():
    return True

@app.get("/hello")
def message(chunk:str):
    chunk_embedding = model.encode(chunk, normalize_embeddings=True)
    embeddings = chunk_embedding.tolist()
    return embeddings

# chunks_input = Chunks(chunks=["Hallo", "Test", "LLM ist toll"])
# print(getEmbeddings(chunks_input))


# Works so far