# FastAPI entrypoint (Zhuoyang, most likely going to need to do work here for the streamlit stuff)

# For Fish, can look into importing your functions from retriever/ into this py file!

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

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
    return {"response": f"You just said, '{user_input}'"} # Repeat user's message
