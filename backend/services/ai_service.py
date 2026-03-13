import os
import httpx
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


GARDEN_SYSTEM_PROMPT = """You are GardenBot 🌱, an expert gardening AI assistant.
Help with plant care, diseases, watering advice, and gardening tips.
Always be friendly, concise, and practical."""


async def call_groq(prompt: str, system: str = None) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system or GARDEN_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1500,
        "temperature": 0.7
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(GROQ_URL, headers=headers, json=payload)
        data = response.json()
        print("Groq response status:", response.status_code)
        if "choices" not in data:
            raise Exception(f"Groq API error: {data}")
        return data["choices"][0]["message"]["content"]


async def get_plant_suggestions(location: str, climate: str, space: str, experience: str) -> str:
    prompt = f"""Suggest 5 plants suitable for:
- Location: {location}
- Climate: {climate}
- Space: {space}
- Experience: {experience}

Return ONLY valid JSON, no markdown, no extra text:
{{
  "plants": [
    {{
      "name": "Plant Name",
      "scientific_name": "Scientific Name",
      "description": "One sentence.",
      "sunlight": "Full sun",
      "water_frequency": "Every 2 days",
      "difficulty": "Easy",
      "best_season": "Summer"
    }}
  ]
}}"""

    text = await call_groq(prompt, system="You are a gardening expert. Always respond with valid JSON only, no markdown, no explanation.")
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return text


async def chat_with_garden_ai(message: str, history: list) -> str:
    history_text = ""
    for h in history[-6:]:
        history_text += f"User: {h['user']}\nAssistant: {h['bot']}\n"

    prompt = f"""Previous conversation:
{history_text}
User: {message}
Assistant:"""
    return await call_groq(prompt)


async def analyze_plant_health(plant_name: str, symptoms: str, image_base64: str = None) -> str:
    symptom_text = symptoms if symptoms else "No symptoms described."
    
    if image_base64:
        # Use vision model when image is provided
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",  # Groq vision model
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": f"""You are a plant health expert. Analyze this plant image.

Plant name: {plant_name}
Symptoms described: {symptom_text}

Provide:
1. 🔍 Diagnosis (what's wrong based on the image)
2. 🌿 Possible causes
3. 💊 Treatment steps
4. 🛡️ Prevention tips

Be concise and practical."""
                        }
                    ]
                }
            ],
            "max_tokens": 700
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(GROQ_URL, headers=headers, json=payload)
            data = response.json()
            print("Groq vision response status:", response.status_code)
            if "choices" not in data:
                raise Exception(f"Groq vision error: {data}")
            return data["choices"][0]["message"]["content"]
    else:
        # Text only — no image
        prompt = f"""You are a plant health expert. Analyze this plant:

Plant: {plant_name}
Symptoms: {symptom_text}

Provide:
1. 🔍 Diagnosis
2. 🌿 Possible causes
3. 💊 Treatment steps
4. 🛡️ Prevention tips

Be concise and practical."""
        return await call_groq(prompt)