from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai import get_reply
from db import save_message, get_session, set_active_device
import os

app = FastAPI(title="Flash Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str
    device_id: str  # "pc" or "android"
    message: str


class HandoffRequest(BaseModel):
    session_id: str
    device_id: str  # device taking over


@app.get("/")
async def root():
    return {"status": "Flash Backend is live 🚀"}


@app.post("/chat")
async def chat(req: ChatRequest, x_device_token: str = Header(...)):
    if x_device_token != os.getenv("DEVICE_TOKEN"):
        raise HTTPException(403, "Unauthorized")
    reply = await get_reply(req.session_id, req.message)
    save_message(req.session_id, req.device_id, req.message, reply)
    return {"reply": reply, "session_id": req.session_id}


@app.post("/handoff")
async def handoff(req: HandoffRequest):
    set_active_device(req.session_id, req.device_id)
    history = get_session(req.session_id)
    return {"active_device": req.device_id, "history": history}


@app.get("/session/{session_id}")
async def session(session_id: str):
    return get_session(session_id)
