# 🌿 GardenMind — Smart Garden Planner

An AI-powered full-stack garden planning app built with **FastAPI**, **MongoDB**, and **OpenAI**.

## ✨ Features
- 🌱 **AI Plant Suggestions** — Get personalized plant recommendations based on location, climate, and space
- 💧 **Watering Schedules** — Track watering frequency with overdue alerts
- 🤖 **AI Chat Assistant** — Ask gardening questions to GardenBot
- 🔬 **Plant Health Analyzer** — Upload a photo or describe symptoms for AI diagnosis

---

## 🗂️ Project Structure
```
smart-garden/
├── backend/
│   ├── main.py               # FastAPI app entry point
│   ├── database.py           # MongoDB connection
│   ├── requirements.txt
│   ├── .env.example
│   ├── models/
│   │   └── schemas.py        # Pydantic models
│   ├── routers/
│   │   ├── plants.py         # Plant suggestion & garden CRUD
│   │   ├── watering.py       # Watering schedules
│   │   ├── chat.py           # AI chat endpoints
│   │   └── health_tracker.py # Plant health analysis
│   └── services/
│       └── ai_service.py     # OpenAI integration
└── frontend/
    └── index.html            # Full web app (single file)
```

---

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.10+
- MongoDB running locally (`mongod`) or MongoDB Atlas URI
- OpenAI API key → https://platform.openai.com/api-keys

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and MONGO_URL

# Run the server
uvicorn main:app --reload --port 8000
```

### 3. Frontend
Just open `frontend/index.html` in your browser. No build step needed!

Or serve it with Python:
```bash
cd frontend
python -m http.server 5500
# Open http://localhost:5500
```

---

## 🌐 API Endpoints

| Method | Endpoint                        | Description                      |
|--------|---------------------------------|----------------------------------|
| POST   | `/api/plants/suggest`           | Get AI plant suggestions         |
| POST   | `/api/plants/save`              | Save plant to garden             |
| GET    | `/api/plants/my-garden`         | Get all saved plants             |
| DELETE | `/api/plants/{name}`            | Remove plant from garden         |
| POST   | `/api/watering/schedule`        | Create watering schedule         |
| GET    | `/api/watering/schedules`       | Get all schedules with status    |
| POST   | `/api/watering/log-watering/{id}` | Log a watering event           |
| GET    | `/api/watering/due-today`       | Plants due for watering          |
| POST   | `/api/chat/message`             | Chat with AI assistant           |
| GET    | `/api/chat/history`             | Get chat history                 |
| POST   | `/api/health/analyze`           | Analyze plant health (+ photo)   |
| GET    | `/api/health/logs`              | Get health check history         |

API docs available at: **http://localhost:8000/docs**

---

## 🛠️ Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | FastAPI, Python                   |
| Database  | MongoDB (via Motor async driver)  |
| AI        | OpenAI GPT-4o-mini / GPT-4o       |
| Frontend  | Vanilla HTML/CSS/JS               |
| Dev Tools | Uvicorn, python-dotenv            |

---

