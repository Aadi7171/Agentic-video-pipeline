import os
from gtts import gTTS
from config import get_collection


def generate_voiceover(script_json: list):
    """Generates an MP3 from script text, uploads to VideoDB, and returns (audio_id, transcript)."""
    print(" -> Generating full transcript...")
    full_transcript = " ".join([scene.get("narrator", "") for scene in script_json])

    if not full_transcript.strip():
        print(" -> No dialogue found.")
        return None, ""

    print(" -> Passing to gTTS engine...")
    tts = gTTS(text=full_transcript, lang='en', slow=False)
    audio_path = "temp_voiceover.mp3"
    tts.save(audio_path)

    print(" -> Uploading Audio to VideoDB...")
    try:
        # Upload through the authenticated collection (videodb has no module-level upload())
        collection = get_collection()
        audio = collection.upload(file_path=audio_path)
        print(f" -> Success! VideoDB Audio ID: {audio.id}")
        return audio.id, full_transcript
    except Exception as e:
        print(f" -> VideoDB Upload Error: {e}")
        return None, ""
    finally:
        # Always clean up the temp file, even on failure
        if os.path.exists(audio_path):
            os.remove(audio_path)
