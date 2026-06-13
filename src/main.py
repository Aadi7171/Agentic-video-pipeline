from config import VIDEO_DB_API_KEY, GEMINI_API_KEY
from agents.script_agent import generate_script
from agents.voice_agent import generate_voiceover
from agents.asset_agent import fetch_assets
from agents.editor_agent import render_video


def main(prompt: str):
    print(f"\n🎬 Starting Agentic Video Pipeline: '{prompt}'")

    # 1. Scriptwriter Agent (Gemini, structured output)
    print("\n🖋️ [Agent 1] Scriptwriter Agent analyzing prompt...")
    script_json = generate_script(prompt)
    if not script_json:
        print("❌ Error generating script. Aborting.")
        return
    print(f"✅ Generated {len(script_json)} scenes.")

    # 2. Voice Agent (gTTS -> VideoDB). Returns (voice_id, transcript).
    print("\n🎙️ [Agent 2] Voice Agent synthesizing audio...")
    voice_id, transcript = generate_voiceover(script_json)
    if not voice_id:
        print("⚠️ Voiceover generation failed. Continuing without audio.")

    # 3. Asset Agent (Pexels -> VideoDB). Returns updated scenes.
    print("\n🎞️ [Agent 3] Asset Agent fetching scene media...")
    script_json = fetch_assets(script_json)

    # 4. Editor Agent (VideoDB Timeline). Needs scenes AND the voice_id.
    print("\n✂️ [Agent 4] Editor Agent cutting the timeline...")
    final_video_url = render_video(script_json, voice_id)

    if final_video_url and final_video_url != "ERROR_GENERATING_URL":
        print("\n--- 🍿 PRODUCTION COMPLETE ---")
        print(f"📺 Watch your video here: {final_video_url}")
    else:
        print("\n--- ❌ PRODUCTION FAILED ---")
        print("No video could be rendered. Check the agent logs above.")


if __name__ == "__main__":
    # config.py already ran load_dotenv(); validate keys before doing any work
    if not VIDEO_DB_API_KEY or not GEMINI_API_KEY:
        print("⚠️ Missing API keys. Copy .env.example to .env and fill in the values.")
    else:
        topic = input("Enter a topic for your video: ")
        main(topic)
