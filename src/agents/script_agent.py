import json
from jsonschema import validate, ValidationError
from config import get_gemini

# Formal contract every scene from the Scriptwriter Agent must satisfy.
# Validating against this catches malformed model output at the source,
# before it can corrupt the Voice, Asset, or Editor stages downstream.
SCRIPT_SCHEMA = {
    "type": "array",
    "minItems": 1,
    "items": {
        "type": "object",
        "required": ["id", "narrator", "visual_keyword", "estimated_duration"],
        "properties": {
            "id": {"type": "integer"},
            "narrator": {"type": "string", "minLength": 1},
            "visual_keyword": {"type": "string", "minLength": 1},
            # Gemini returns this as a string (e.g. "4"); keep it permissive
            # but require a value the Editor can cast to a number.
            "estimated_duration": {"type": ["string", "number"]},
        },
        "additionalProperties": True,
    },
}


def generate_script(prompt: str) -> list:
    """Uses Gemini to generate a structured script, validated against SCRIPT_SCHEMA.

    Returns a list of validated scene dicts, or [] if generation, parsing,
    or schema validation fails.
    """
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

    # 1. Parse — strip any accidental markdown fences first
    try:
        text = response.text.replace('```json', '').replace('```', '').strip()
        script_data = json.loads(text)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"   -> Failed to parse Gemini response as JSON: {e}")
        return []

    # 2. Validate against the schema — fail fast with a clear message
    try:
        validate(instance=script_data, schema=SCRIPT_SCHEMA)
    except ValidationError as e:
        # e.message is human-readable; e.json_path shows exactly where it broke
        print(f"   -> Script failed schema validation at {e.json_path}: {e.message}")
        return []

    print(f"   -> Script validated against schema ({len(script_data)} scenes).")
    return script_data
