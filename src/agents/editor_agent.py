import videodb
from videodb import Timeline, VideoAsset, AudioAsset

def render_video(scenes: list, voice_id: str):
    """Compiles the Timeline. Stitches B-rolls sequentially and overlays the audio track."""
    print("      -> Initializing VideoDB Timeline Engine...")
    timeline = Timeline()
    
    # 1. Add background B-roll scenes chronologically
    current_time = 0
    for scene in scenes:
        vid_id = scene.get("video_id")
        duration = int(scene.get("estimated_duration", "5"))
        if vid_id:
            try:
                # Add video asset (cut from start to the estimated duration)
                print(f"      -> Placing Asset {vid_id} on visual track for {duration}s")
                video_asset = VideoAsset(asset_id=vid_id, start=0, end=duration)
                timeline.add_inline(video_asset)
                current_time += duration
            except Exception as e:
                print(f"      -> Editor Error styling video {vid_id}: {e}")
                
    # 2. Add Voiceover layer across the timeline
    if voice_id:
        try:
            print(f"      -> Overlaying Voice Track {voice_id} over entire video length")
            voice_asset = AudioAsset(asset_id=voice_id)
            timeline.add_overlay(start=0, asset=voice_asset)
        except Exception as e:
            print(f"      -> Editor Error placing Audio {voice_id}: {e}")
            
    # 3. Render and Generate the final Video URL
    print("      -> Generating streaming manifest...")
    try:
        stream_url = timeline.generate_stream()
        return stream_url
    except Exception as e:
        print(f"      -> Stream Generation Failed: {e}")
        return "ERROR_GENERATING_URL"
