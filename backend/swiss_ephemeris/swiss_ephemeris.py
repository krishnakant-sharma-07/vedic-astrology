import swisseph as swe

PLANET_MAP = {
    "SUN": swe.SUN,
    "MOON": swe.MOON,
    "MERCURY": swe.MERCURY,
    "VENUS": swe.VENUS,
    "MARS": swe.MARS,
    "JUPITER": swe.JUPITER,
    "SATURN": swe.SATURN,
    "URANUS": swe.URANUS,
    "NEPTUNE": swe.NEPTUNE,
    "PLUTO": swe.PLUTO,
    
}

# Add Zodiac and Nakshatra Data
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

def get_planet_position_on_date(planet_name, year, month, day):
    planet_name = planet_name.upper()
    if planet_name not in PLANET_MAP:
        raise ValueError(f"Unsupported planet name: {planet_name}")
    
    swe.set_ephe_path('.')  # Or wherever your .se1 files are
    jd = swe.julday(year, month, day)
    planet = PLANET_MAP[planet_name]
    result, retflag = swe.calc_ut(jd, planet)
    lon, lat, dist = result[:3]  # Only take the first three values

    # Zodiac sign calculation
    zodiac_index = int(lon // 30)
    zodiac_sign = ZODIAC_SIGNS[zodiac_index]

    # Nakshatra calculation
    nakshatra_index = int((lon % 360) // (360 / 27))
    nakshatra = NAKSHATRAS[nakshatra_index]

    return {
        "planet": planet_name,
        "longitude": lon,
        "latitude": lat,
        "distance": dist,
        "julian_day": jd,
        "zodiac_sign": zodiac_sign,
        "nakshatra": nakshatra
    }
# import swisseph as swe

def get_all_planets_positions_on_datetime(dt):
    swe.set_ephe_path('.')  # Set the path to Swiss Ephemeris files
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)
    
    planets = {
        "SUN": swe.SUN,
        "MOON": swe.MOON,
        "MERCURY": swe.MERCURY,
        "VENUS": swe.VENUS,
        "MARS": swe.MARS,
        "JUPITER": swe.JUPITER,
        "SATURN": swe.SATURN,
        "URANUS": swe.URANUS,
        "NEPTUNE": swe.NEPTUNE,
        "PLUTO": swe.PLUTO
    }

    positions = {}

    for name, planet_id in planets.items():
        pos, _ = swe.calc_ut(jd, planet_id)
        lon, lat, dist = pos[:3]

        # Zodiac sign
        zodiac_index = int(lon // 30)
        zodiac_sign = ZODIAC_SIGNS[zodiac_index]

        # Nakshatra
        nakshatra_index = int((lon % 360) // (360 / 27))
        nakshatra = NAKSHATRAS[nakshatra_index]

        positions[name] = {
            "longitude": lon,
            "latitude": lat,
            "distance": dist,
            "zodiac_sign": zodiac_sign,
            "nakshatra": nakshatra
        }

    return positions

