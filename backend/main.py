from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import plants, watering, chat, health_tracker

app = FastAPI(title="Smart Garden Planner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plants.router, prefix="/api/plants", tags=["Plants"])
app.include_router(watering.router, prefix="/api/watering", tags=["Watering"])
app.include_router(chat.router, prefix="/api/chat", tags=["AI Chat"])
app.include_router(health_tracker.router, prefix="/api/health", tags=["Health Tracker"])

@app.get("/")
def root():
    return {"message": "Smart Garden Planner API is running 🌱"}
