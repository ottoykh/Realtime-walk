from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gps_data = []
users = set()

class Location(BaseModel):
    username: str
    latitude: float
    longitude: float

class User(BaseModel):
    username: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the GPS Marker API"}

@app.post("/create_user")
def create_user(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users.add(user.username)
    return {"status": "success", "message": "User created successfully"}

@app.post("/save_location")
def save_location(location: Location):
    if location.username not in users:
        raise HTTPException(status_code=400, detail="Invalid username")
    location_data = location.dict()
    location_data['timestamp'] = datetime.now().isoformat()
    gps_data.append(location_data)
    return {"status": "success"}

@app.get("/get_locations/{username}", response_model=List[Location])
def get_locations(username: str):
    if username not in users:
        raise HTTPException(status_code=400, detail="Invalid username")
    user_locations = [loc for loc in gps_data if loc['username'] == username]
    return user_locations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
