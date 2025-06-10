# FastAPI entrypoint (Zhuoyang, most likely going to need to do work here for the streamlit stuff)

# For Fish, can look into importing your functions from retriever/ into this py file!

#hotfix :-0
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from retriever_ant.search import query_ollama_with_context

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    response = query_ollama_with_context(user_input)
    return {"response": response}
