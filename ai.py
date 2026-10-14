import google.generativeai as genai
from db import get_history
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are Flash, a smart personal AI assistant.
You are helpful, concise, and speak naturally like a real assistant.
Keep responses short (1-3 sentences) since they will be spoken aloud.
You remember everything in this conversation."""


async def get_reply(session_id: str, user_message: str) -> str:
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
    history = get_history(session_id)  # list of dicts
    chat = model.start_chat(history=history)
    response = chat.send_message(user_message)
    return response.text
