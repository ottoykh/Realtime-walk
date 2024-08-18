from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
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
    latitude: Optional[float] = None
    longitude: Optional[float] = None


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


@app.post("/locations", response_model=List[Location])
def save_and_get_locations(location: Location):
    if location.username not in users:
        raise HTTPException(status_code=400, detail="Invalid username")

    if location.latitude is not None and location.longitude is not None:
        location_data = location.dict()
        location_data['timestamp'] = datetime.now().isoformat()
        gps_data.append(location_data)

    user_locations = [loc for loc in gps_data if loc['username'] == location.username]
    return user_locations


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
