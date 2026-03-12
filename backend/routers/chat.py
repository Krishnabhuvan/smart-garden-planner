from fastapi import APIRouter
from models.schemas import ChatMessage
from services.ai_service import chat_with_garden_ai
from database import chat_collection
from datetime import datetime

router = APIRouter()


@router.post("/message")
async def send_message(chat: ChatMessage):
    """Send a message to the AI gardening assistant."""
    # Fetch last 6 messages for context
    cursor = chat_collection.find(
        {"user_id": chat.user_id},
        {"_id": 0}
    ).sort("timestamp", -1).limit(6)
    history = await cursor.to_list(length=6)
    history.reverse()

    # Get AI reply
    reply = await chat_with_garden_ai(chat.message, history)

    # Save to DB
    await chat_collection.insert_one({
        "user_id": chat.user_id,
        "user": chat.message,
        "bot": reply,
        "timestamp": datetime.utcnow()
    })

    return {"reply": reply, "timestamp": datetime.utcnow()}


@router.get("/history")
async def get_chat_history(user_id: str = "default", limit: int = 20):
    """Get chat history for a user."""
    cursor = chat_collection.find(
        {"user_id": user_id},
        {"_id": 0}
    ).sort("timestamp", -1).limit(limit)
    history = await cursor.to_list(length=limit)
    history.reverse()
    return {"history": history}


@router.delete("/history")
async def clear_history(user_id: str = "default"):
    """Clear chat history."""
    await chat_collection.delete_many({"user_id": user_id})
    return {"message": "Chat history cleared"}
