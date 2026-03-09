from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Persistent storage for the session (clears on restart)
# { "BAP-1234": {"path": [...], "turns": [...]} }
storage = {}

@app.post("/save-route")
async def save_route(data: dict):
    # Create a simple 4-digit ID for easier typing
    short_id = str(uuid.uuid4().hex[:4]).upper()
    address_id = f"BAP-{short_id}"
    storage[address_id] = {
        "path": data.get("path"),
        "turns": data.get("turns")
    }
    return {"address_id": address_id}

@app.get("/get-route/{address_id}")
async def get_route(address_id: str):
    route = storage.get(address_id.upper())
    if not route:
        raise HTTPException(status_code=404, detail="Address ID not found")
    return route

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)