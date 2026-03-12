from fastapi import APIRouter, HTTPException
from models.schemas import WateringSchedule, WaterLog
from database import watering_collection
from datetime import datetime, timedelta
from bson import ObjectId

router = APIRouter()


@router.post("/schedule")
async def create_schedule(schedule: WateringSchedule):
    """Create a watering schedule for a plant."""
    schedule_dict = schedule.model_dump()
    schedule_dict["last_watered"] = datetime.utcnow()
    schedule_dict["next_watering"] = datetime.utcnow() + timedelta(days=schedule.frequency_days)
    
    result = await watering_collection.insert_one(schedule_dict)
    return {
        "message": f"Watering schedule created for {schedule.plant_name}!",
        "id": str(result.inserted_id),
        "next_watering": schedule_dict["next_watering"]
    }


@router.get("/schedules")
async def get_schedules(user_id: str = "default"):
    """Get all watering schedules with status."""
    cursor = watering_collection.find({"user_id": user_id})
    schedules = await cursor.to_list(length=100)
    now = datetime.utcnow()

    result = []
    for s in schedules:
        s["_id"] = str(s["_id"])
        next_w = s.get("next_watering")
        if next_w:
            days_until = (next_w - now).days
            s["status"] = "overdue" if days_until < 0 else ("due_today" if days_until == 0 else "upcoming")
            s["days_until_watering"] = days_until
        result.append(s)

    return {"schedules": result}


@router.post("/log-watering/{schedule_id}")
async def log_watering(schedule_id: str):
    """Mark a plant as watered and update next watering date."""
    schedule = await watering_collection.find_one({"_id": ObjectId(schedule_id)})
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    next_watering = datetime.utcnow() + timedelta(days=schedule["frequency_days"])
    await watering_collection.update_one(
        {"_id": ObjectId(schedule_id)},
        {"$set": {"last_watered": datetime.utcnow(), "next_watering": next_watering}}
    )
    return {"message": f"✅ Watered! Next watering: {next_watering.strftime('%Y-%m-%d')}"}


@router.get("/due-today")
async def get_due_today(user_id: str = "default"):
    """Get plants that need watering today or are overdue."""
    now = datetime.utcnow()
    cursor = watering_collection.find({
        "user_id": user_id,
        "next_watering": {"$lte": now + timedelta(days=1)}
    })
    due = await cursor.to_list(length=100)
    for d in due:
        d["_id"] = str(d["_id"])
    return {"due_plants": due, "count": len(due)}
