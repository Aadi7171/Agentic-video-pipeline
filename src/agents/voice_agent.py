import os
from gtts import gTTS
import videodb

def generate_voiceover(script_json: list):
    """Generates an MP3 from script text, uploads to VideoDB, and returns the audio ID."""
    print("      -> Generating full transcript...")
    full_transcript = " ".join([scene.get("narrator", "") for scene in script_json])
    
    if not full_transcript.strip():
        print("      -> No dialogue found.")
        return None, ""
        
    print("      -> Passing to gTTS engine...")
    tts = gTTS(text=full_transcript, lang='en', slow=False)
    audio_path = "temp_voiceover.mp3"
    tts.save(audio_path)
    
    print("      -> Uploading Audio to VideoDB...")
    try:
        # Uploading to VideoDB directly
        audio = videodb.upload(file_path=audio_path)
        print(f"      -> Success! VideoDB Audio ID: {audio.id}")
        
        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        return audio.id, full_transcript
    except Exception as e:
        print(f"      -> VideoDB Upload Error: {e}")
        return None, ""
