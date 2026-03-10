# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import uuid

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# storage = {}

# @app.post("/save-route")
# async def save_route(data: dict):
#     short_id = uuid.uuid4().hex[:4].upper()
#     address_id = f"BAP-{short_id}"
#     storage[address_id] = {
#         "landmark": data.get("landmark", "Landmark"),
#         "path": data.get("path"),
#         "turns": data.get("turns"),
#         "turn_labels": data.get("turn_labels"),
#         "rating": None
#     }
#     return {"address_id": address_id}

# @app.get("/get-route/{address_id}")
# async def get_route(address_id: str):
#     route = storage.get(address_id.upper())
#     if not route:
#         raise HTTPException(status_code=404, detail="Address ID not found")
#     return route

# @app.post("/rate-route/{address_id}")
# async def rate_route(address_id: str, data: dict):
#     if address_id in storage:
#         storage[address_id]["rating"] = data.get("rating")
#         return {"status": "success"}
#     raise HTTPException(status_code=404, detail="Route not found")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)




from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import uuid

# ── Supabase config ──────────────────────────────────────────
SUPABASE_URL = "https://fsrthjexwbobjyfabyfr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZzcnRoamV4d2JvYmp5ZmFieWZyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMxNTQ5NzEsImV4cCI6MjA4ODczMDk3MX0.UF8Ubzno6RD0zyK6PG9tGKt954EVf8SUzHC244-4lsM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── App ──────────────────────────────────────────────────────
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ───────────────────────────────────────────────────

@app.post("/save-route")
async def save_route(data: dict):
    short_id = uuid.uuid4().hex[:4].upper()
    address_id = f"BAP-{short_id}"

    row = {
        "id":           address_id,
        "landmark":     data.get("landmark", "Landmark"),
        "path":         data.get("path"),
        "turns":        data.get("turns"),
        "turn_labels":  data.get("turn_labels"),
        "rating":       None,
    }

    result = supabase.table("routes").insert(row).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to save route")

    return {"address_id": address_id}


@app.get("/get-route/{address_id}")
async def get_route(address_id: str):
    result = (
        supabase.table("routes")
        .select("*")
        .eq("id", address_id.upper())
        .single()
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Address ID not found")

    row = result.data
    return {
        "landmark":    row["landmark"],
        "path":        row["path"],
        "turns":       row["turns"],
        "turnLabels":  row["turn_labels"],
        "rating":      row["rating"],
    }


@app.post("/rate-route/{address_id}")
async def rate_route(address_id: str, data: dict):
    result = (
        supabase.table("routes")
        .update({"rating": data.get("rating")})
        .eq("id", address_id.upper())
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Route not found")

    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)