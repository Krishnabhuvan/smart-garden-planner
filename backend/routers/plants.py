from fastapi import APIRouter, HTTPException
from models.schemas import PlantSuggestionRequest, Plant
from services.ai_service import get_plant_suggestions
from database import plants_collection
import json

router = APIRouter()

@router.post("/suggest")
async def suggest_plants(request: PlantSuggestionRequest):
    try:
        ai_response = await get_plant_suggestions(
            request.location,
            request.climate,
            request.available_space,
            request.experience_level
        )
        # Clean up markdown code blocks if present
        clean = ai_response.strip()
        if "```json" in clean:
            clean = clean.split("```json")[1].split("```")[0].strip()
        elif "```" in clean:
            clean = clean.split("```")[1].split("```")[0].strip()

        data = json.loads(clean)
        plants = data.get("plants", data) if isinstance(data, dict) else data
        return {"suggestions": plants, "location": request.location}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save")
async def save_plant(plant: Plant):
    """Save a plant to user's garden."""
    plant_dict = plant.model_dump()
    result = await plants_collection.insert_one(plant_dict)
    return {"message": "Plant saved!", "id": str(result.inserted_id)}


@router.get("/my-garden")
async def get_my_garden(user_id: str = "default"):
    """Get all plants in user's garden."""
    cursor = plants_collection.find({"user_id": user_id}, {"_id": 0})
    plants = await cursor.to_list(length=100)
    return {"plants": plants, "count": len(plants)}


@router.delete("/{plant_name}")
async def remove_plant(plant_name: str, user_id: str = "default"):
    """Remove a plant from the garden."""
    result = await plants_collection.delete_one({"name": plant_name, "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plant not found")
    return {"message": f"{plant_name} removed from your garden"}
