from fastapi import APIRouter, UploadFile, File, Form
from models.schemas import PlantHealthLog
from services.ai_service import analyze_plant_health
from database import health_collection
from datetime import datetime
import base64

router = APIRouter()


@router.post("/analyze")
async def analyze_health(
    plant_name: str = Form(...),
    symptoms: str = Form(None),
    user_id: str = Form("default"),
    image: UploadFile = File(None)
):
    """Analyze plant health with optional photo upload."""
    image_base64 = None
    if image:
        contents = await image.read()
        image_base64 = base64.b64encode(contents).decode("utf-8")

    diagnosis = await analyze_plant_health(plant_name, symptoms, image_base64)

    # Save log to DB
    log = {
        "plant_name": plant_name,
        "symptoms": symptoms,
        "diagnosis": diagnosis,
        "has_image": image is not None,
        "user_id": user_id,
        "logged_at": datetime.utcnow()
    }
    await health_collection.insert_one(log)

    return {
        "plant_name": plant_name,
        "diagnosis": diagnosis,
        "logged_at": log["logged_at"]
    }


@router.get("/logs")
async def get_health_logs(user_id: str = "default"):
    """Get all health check logs."""
    cursor = health_collection.find(
        {"user_id": user_id},
        {"_id": 0, "image_base64": 0}  # exclude heavy fields
    ).sort("logged_at", -1)
    logs = await cursor.to_list(length=50)
    return {"logs": logs, "count": len(logs)}
