import re
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from pathlib import Path

def create_edit_decision_list(scene_text: str, animated_shots: list, lip_sync_clips: dict) -> list:
    """
    Parses a script and maps dialogue and action lines to video clips to create an EDL.
    """
    print("Creating Edit Decision List (EDL)...")
    edl = []
    
    # Simple script parser: find dialogue lines (CHARACTER in caps followed by text)
    dialogue_pattern = re.compile(r"^\s*([A-Z\s]+)\n(.*?)\n", re.MULTILINE)
    
    last_index = 0
    shot_index = 0

    for match in dialogue_pattern.finditer(scene_text):
        # 1. Handle action lines before the dialogue
        action_block = scene_text[last_index:match.start()].strip()
        if action_block and shot_index < len(animated_shots):
            print(f"Action block found: '{action_block[:30]}...'. Assigning animated shot.")
            edl.append({"type": "action", "path": animated_shots[shot_index]})
            shot_index += 1
        
        # 2. Handle the dialogue line
        character_name = match.group(1).strip()
        dialogue_text = match.group(2).strip().replace('\n', ' ')
        
        # Find the corresponding lip-sync video
        if dialogue_text in lip_sync_clips:
            print(f"Dialogue found for {character_name}: '{dialogue_text[:30]}...'. Assigning lip-sync clip.")
            edl.append({"type": "dialogue", "path": lip_sync_clips[dialogue_text]})
        else:
            print(f"Warning: No lip-sync clip found for dialogue: {dialogue_text}")

        last_index = match.end()

    # 3. Handle any remaining action lines at the end of the script
    remaining_action = scene_text[last_index:].strip()
    if remaining_action and shot_index < len(animated_shots):
        print("Trailing action block found. Assigning animated shot.")
        edl.append({"type": "action", "path": animated_shots[shot_index]})

    print("EDL created successfully.")
    return edl

def assemble_scene_from_edl(edl: list, music_track_path: str = None) -> str:
    """
    Assembles a final video from an Edit Decision List using moviepy.
    """
    print("Assembling final scene from EDL...")
    if not edl:
        raise ValueError("Edit Decision List is empty.")

    video_clips = [VideoFileClip(item['path']) for item in edl]
    
    final_video = concatenate_videoclips(video_clips, method="compose")

    # Add background music if provided
    if music_track_path:
        print(f"Adding music track: {music_track_path}")
        music = AudioFileClip(music_track_path).volumex(0.1) # Lower volume for background
        # If music is longer than video, trim it
        if music.duration > final_video.duration:
            music = music.subclip(0, final_video.duration)
        final_video = CompositeVideoClip([final_video]).set_audio(music)

    output_dir = Path("generated_scenes")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "final_scene_assembly.mp4"

    final_video.write_videofile(str(output_path), codec="libx264", fps=24)
    print(f"Final scene assembled successfully: {output_path}")
    return str(output_path)