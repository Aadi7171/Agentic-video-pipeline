import os
import requests
from config import get_collection


def fetch_assets(script_json: list) -> list:
    """Takes scene data, fetches B-roll URLs, uploads to VideoDB, and returns updated scenes."""
    PEXELS_KEY = os.getenv("PEXELS_API_KEY")

    # Pre-defined fallback video if Pexels API fails or key is missing
    FALLBACK_URL = "https://www.w3schools.com/html/mov_bbb.mp4"

    # Get the authenticated collection once (videodb has no module-level upload())
    collection = get_collection()

    for idx, scene in enumerate(script_json):
        keyword = scene.get("visual_keyword", "abstract nature")
        print(f" -> {idx + 1}. Fetching Asset for keyword: '{keyword}'...")

        video_url = FALLBACK_URL
        if PEXELS_KEY and PEXELS_KEY != "your_pexels_api_key_here":
            headers = {"Authorization": PEXELS_KEY}
            params = {"query": keyword, "per_page": 1, "orientation": "landscape"}

            try:
                res = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
                if res.status_code == 200:
                    data = res.json()
                    videos = data.get("videos", [])
                    if videos and videos[0].get("video_files"):
                        # Get best SD/HD link
                        video_url = videos[0]["video_files"][0].get("link", FALLBACK_URL)
            except Exception as e:
                print(f" -> Pexels Error: {e}")

        # Upload chosen URL into VideoDB server-to-server via the collection
        print(" -> Uploading Video URL to VideoDB...")
        try:
            db_video = collection.upload(url=video_url)
            scene["video_id"] = db_video.id
            print(f" -> Success! VideoDB ID: {db_video.id}")
        except Exception as e:
            print(f" -> VideoDB URL Upload failed: {e}")
            scene["video_id"] = None

    return script_json
