from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = "smart_garden"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

# Collections
plants_collection = db["plants"]
watering_collection = db["watering_schedules"]
chat_collection = db["chat_history"]
health_collection = db["plant_health"]
