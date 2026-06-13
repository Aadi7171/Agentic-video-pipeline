import json
from config import get_gemini


def generate_script(prompt: str) -> list:
    """Uses Gemini to generate a structured script JSON."""
    client = get_gemini()

    system_instruction = """
You are an AI Video Scriptwriter. Break the user's topic into 3-5 distinct scenes.
Return ONLY a raw JSON array. Do not include markdown or backticks.
Format:
[
  {
    "id": 1,
    "narrator": "Text to be spoken aloud.",
    "visual_keyword": "A 1-3 word keyword to search for stock video (e.g. 'galaxy', 'city at night', 'typing')",
    "estimated_duration": "4"
  }
]
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config={
            "system_instruction": system_instruction,
            "temperature": 0.5
        }
    )

    try:
        # Clean any accidental markdown fences
        text = response.text.replace('```json', '').replace('```', '').strip()
        script_data = json.loads(text)
        if not isinstance(script_data, list):
            print("Gemini did not return a JSON array.")
            return []
        return script_data
    except Exception as e:
        print(f"Failed to parse Gemini script: {e}")
        return []
