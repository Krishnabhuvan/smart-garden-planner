from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ── Plant Models ──────────────────────────────────────────────
class PlantSuggestionRequest(BaseModel):
    location: str               # e.g. "Bangalore, India"
    climate: str                # e.g. "tropical", "arid", "temperate"
    available_space: str        # e.g. "balcony", "garden", "indoor"
    experience_level: str       # e.g. "beginner", "intermediate", "expert"

class Plant(BaseModel):
    name: str
    scientific_name: Optional[str] = None
    description: str
    sunlight: str
    water_frequency: str
    difficulty: str
    best_season: str
    location: str
    user_id: Optional[str] = "default"
    added_at: datetime = Field(default_factory=datetime.utcnow)


# ── Watering Models ───────────────────────────────────────────
class WateringSchedule(BaseModel):
    plant_name: str
    frequency_days: int         # water every N days
    last_watered: Optional[datetime] = None
    next_watering: Optional[datetime] = None
    notes: Optional[str] = None
    user_id: Optional[str] = "default"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class WaterLog(BaseModel):
    schedule_id: str
    watered_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None


# ── Chat Models ───────────────────────────────────────────────
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    reply: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ── Health Tracker Models ─────────────────────────────────────
class PlantHealthLog(BaseModel):
    plant_name: str
    image_base64: Optional[str] = None   # base64 encoded image
    symptoms: Optional[str] = None       # user-described symptoms
    user_id: Optional[str] = "default"
    logged_at: datetime = Field(default_factory=datetime.utcnow)
