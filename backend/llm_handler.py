import requests

GRADIO_LLM_URL = "https://d10235d7a555992f36.gradio.live/"  # ⬅️ Replace this

def get_interpretation_from_llm(planet_positions: dict):
    # Create the input prompt
    prompt = "Explain the Vedic astrological significance based on:\n"
    for planet, position in planet_positions.items():
        prompt += f"{planet}: {position}°\n"

    try:
        # Call the Gradio endpoint with POST
        response = requests.post(
            f"{GRADIO_LLM_URL}/api/predict/",
            json={
                "data": [prompt]
            },
            headers={"Content-Type": "application/json"}
        )
        result = response.json()

        # Extract the response
        interpretation = result["data"][0] if "data" in result else "No output"
        return interpretation

    except Exception as e:
        return f"Error contacting LLM: {str(e)}"
    
def generate_interpretation(planet, zodiac_sign, nakshatra):
    if planet == "SUN" and zodiac_sign == "Taurus" and nakshatra == "Rohini":
        return "The Sun in Taurus and Rohini nakshatra indicates strong creative energy, charm, and grounded leadership."
    return f"Interpretation for {planet} in {zodiac_sign} and {nakshatra} is not available yet."
