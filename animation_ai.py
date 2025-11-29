import requests
from pathlib import Path
import time
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from .config import DID_API_KEY

DID_API_URL = "https://api.d-id.com/talks"

def generate_lip_sync_video(character_key_visual_url: str, dialogue_audio_path: str) -> str:
    """
    Simulates generating a lip-synced video of a character.
    In a real-world scenario, this would call an API like D-ID or a similar service.
    For this project, we will create a static image video with the dialogue audio.
    """
    print(f"Generating real lip-sync video for audio: {dialogue_audio_path}")
    output_dir = Path("generated_video_clips")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"lip_sync_{Path(dialogue_audio_path).stem}.mp4"

    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json",
    }

    # 1. Create the talk
    with open(dialogue_audio_path, 'rb') as audio_file:
        payload = {
            "source_url": character_key_visual_url,
            "driver_url": "bank://lively", # Use a pre-recorded driver
            "script": {
                "type": "audio",
                "audio_url": "s3://...", # This needs to be a public URL
            }
        }
        # D-ID requires the audio to be at a public URL. This is a major limitation for local files.
        # For a real implementation, you'd upload the local audio to a temporary public host (like S3).
        # For now, we will have to stop here as we cannot complete this without an upload step.
        print("D-ID INTEGRATION NOTE: The D-ID API requires the dialogue audio to be at a public URL.")
        print("To complete this, you would need to add a service to upload the local audio file to a public host (e.g., AWS S3) and then pass that URL to the API.")
        print("Falling back to simulation for this example.")

        # --- Fallback Simulation Logic ---
        audio_clip = AudioFileClip(dialogue_audio_path)
        try:
            response = requests.get(character_key_visual_url, stream=True)
            response.raise_for_status()
            image_path = output_dir / f"temp_image_{Path(dialogue_audio_path).stem}.jpg"
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            image_clip = ImageClip(str(image_path), duration=audio_clip.duration)
            final_clip = image_clip.set_audio(audio_clip)
            final_clip.write_videofile(str(output_path), codec="libx264", fps=24)
            image_path.unlink()
            return str(output_path)
        except Exception as e:
            return f"Error during fallback simulation: {e}"

def animate_storyboard_shot(storyboard_image_url: str, shot_info: dict, duration: float = 3.0) -> str:
    """
    Applies simple camera movement (zoom) to a static storyboard image.
    """
    print(f"Animating shot {shot_info.get('shot_number', 'N/A')}")
    output_dir = Path("generated_video_clips")
    output_dir.mkdir(exist_ok=True)

    # Download the image
    try:
        response = requests.get(storyboard_image_url, stream=True)
        response.raise_for_status()
        image_path = output_dir / f"temp_image_shot_{shot_info.get('shot_number', 'N/A')}.jpg"
        with open(image_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception as e:
        return f"Error: Could not download image from {storyboard_image_url}"

    # Create a simple zoom-in effect
    clip = ImageClip(str(image_path), duration=duration)
    zoomed_clip = clip.resize(lambda t: 1 + 0.1 * (t / duration)) # Zoom in by 10% over the duration
    final_clip = CompositeVideoClip([zoomed_clip.set_position("center")], size=clip.size)

    output_path = output_dir / f"animated_shot_{shot_info.get('shot_number', 'N/A')}.mp4"
    final_clip.write_videofile(str(output_path), codec="libx264", fps=24)

    image_path.unlink()
    return str(output_path)