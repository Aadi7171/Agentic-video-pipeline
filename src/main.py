import os
import json
from .config import get_gemini
from .agents.script_agent import generate_script
from .agents.voice_agent import generate_voiceover
from .agents.asset_agent import fetch_assets
from .agents.editor_agent import render_video

def main(prompt: str):
    print(f"\n🎬 Starting Agentic Video Pipeline: '{prompt}'")
    
    # 1. Scriptwriter Agent (Gemini)
    print("\n🖋️ [Agent 1] Scriptwriter Agent analyzing prompt...")
    script_json = generate_script(prompt)
    if not script_json:
        print("❌ Error generating script.")
        return
    print(f"✅ Generated {len(script_json)} scenes.")

    # 2. Voiceover Agent (gTTS -> VideoDB)
    print("\n🎙️ [Agent 2] Voice Agent synthesizing audio track...")
    voice_url, full_transcript = generate_voiceover(script_json)
    
    # 3. Asset Agent (Pexels -> VideoDB)
    print("\n🎞️ [Agent 3] Asset Agent fetching scene media...")
    scenes_with_media = fetch_assets(script_json)

    # 4. Editor Agent (VideoDB Timeline)
    print("\n✂️ [Agent 4] Editor Agent cutting the timeline...")
    final_video_url = render_video(scenes_with_media, voice_url)

    print("\n--- 🍿 PRODUCTION COMPLETE ---")
    print(f"📺 Watch your video here: {final_video_url}")

if __name__ == "__main__":
    # Validate .env has been filled
    if not os.getenv("VIDEO_DB_API_KEY") or not os.getenv("GEMINI_API_KEY"):
        print("⚠️ Warning: Missing API Keys. Please copy .env.example to .env and fill in the values.")
    else:
        # Example prompt
        topic = input("Enter a topic for your video: ")
        main(topic)
