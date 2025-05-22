from fastapi import FastAPI, Depends, Request
import swisseph as swe
from fastapi.middleware.cors import CORSMiddleware
from models import init_db, SessionLocal, AstrologyRecord
from sqlalchemy.orm import Session
from swiss_ephemeris.swiss_ephemeris import get_planet_position_on_date
from datetime import datetime, date
from llm_handler import generate_interpretation

# Initialize the database
init_db()

app = FastAPI()


# Allow CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow your frontend to access backend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Vedic Astrology API"}

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoint to get planet position and save to DB
@app.get("/planet_position/{planet}/{year}/{month}/{day}")
def get_planet_position_api(
    planet: str,
    year: int,
    month: int,
    day: int,
    db: Session = Depends(get_db)
):
    # Get planet position from the Swiss Ephemeris
    position = get_planet_position_on_date(planet, year, month, day)

    # Convert birth_date to a proper Python date object
    birth_date = date(year, month, day)

# Saving the record to the DB
    record = AstrologyRecord(
    name="Anonymous",
    birth_date=birth_date,
    planet=planet,
    position=position)


    db.add(record)
    db.commit()

    return {"planet": planet.upper(), "position": position}
@app.get("/records")
def get_records(db: Session = Depends(get_db)):
    records = db.query(AstrologyRecord).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "birth_date": r.birth_date,
            "planet": r.planet,
            "position": r.position
        }
        for r in records
    ]
    
@app.get("/records/search")
def search_records(
    planet: str,
    birth_date: str,
    db: Session = Depends(get_db)
):
    record = db.query(AstrologyRecord).filter_by(
        planet=planet.upper(), birth_date=birth_date
    ).first()
    if record:
        return {
            "planet": record.planet,
            "birth_date": record.birth_date,
            "position": record.position
        }
    return {"message": "No record found"}


from swiss_ephemeris.swiss_ephemeris import get_all_planets_positions_on_datetime

@app.get("/planet-positions")
def get_planet_positions(
    date: str,
    time: str,
    location: str  # currently unused, but keep for future RAG/localization
):
    try:
        # Combine date and time to a single datetime object
        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        # Get all planet positions (you must define this in swiss_ephemeris)
        positions = get_all_planets_positions_on_datetime(dt)

        return {
            "date": date,
            "time": time,
            "location": location,
            "positions": positions
        }
    except Exception as e:
        return {"error": str(e)}



@app.post("/interpret")
async def get_interpretation(request: Request):
    data = await request.json()
    planet = data.get("planet")
    zodiac_sign = data.get("zodiac_sign")
    nakshatra = data.get("nakshatra")

    interpretation = generate_interpretation(planet, zodiac_sign, nakshatra)
    return {"interpretation": interpretation}