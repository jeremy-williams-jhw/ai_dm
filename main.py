from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import create_character, update_character, add_chat_message
from models import CharacterCreate, ChatMessageRead, ChatRequest
from chat import chat_with_gpt
import json

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/characters/")
def create_character_endpoint(character: CharacterCreate, db: Session = Depends(get_db)):
    return create_character(db, character.name, character.role, character.stats)

@app.put("/characters/{character_id}")
def edit_character_endpoint(character_id: int, updates: dict, db: Session = Depends(get_db)):
    return update_character(db, character_id, updates)

@app.post("/chats/")
def add_chat_message_endpoint(chat_message: ChatMessageRead, db: Session = Depends(get_db)):
    return add_chat_message(db, chat_message.message_from, chat_message.message_to, chat_message.content)

@app.post("/chat/gpt/")
async def chat_gpt(request: ChatRequest):
    """
    Endpoint to send messages to OpenAI's GPT model.
    """
    try:
        response = chat_with_gpt(
            messages=[{"role": m.role, "content": m.content} for m in request.messages],
            model=request.model
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))