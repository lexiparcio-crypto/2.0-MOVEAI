from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import requests
import json

from .screenwriter_ai import generate_scene # Keep this for scene generation
from .character_ai import generate_character_profile, generate_costume_and_appearance
from .cinematographer_ai import generate_shot_list
from .sound_ai import generate_sound_design
from .dialogue_ai import generate_dialogue_audio
from .animation_ai import generate_lip_sync_video, animate_storyboard_shot
from .editor_ai import create_edit_decision_list, assemble_scene_from_edl
from .post_production_ai import generate_subtitles, check_visual_continuity, score_final_quality
from .music_ai import generate_music_composition
from .visuals_ai import generate_storyboard_image

app = FastAPI()

class SceneRequest(BaseModel):
    prompt: str
    context: dict

class CharacterRequest(BaseModel):
    brief: str
    film_context: dict

class StoryboardRequest(BaseModel):
    scene_text: str 
    character_id: str # The ID of the main character in the scene
    film_context: dict

class AuditoryRequest(BaseModel):
    scene_text: str
    # storyboard_data: Optional[List[Dict]] = None # Could be used for more precise timing
    film_context: dict

class DialogueRequest(BaseModel):
    character_id: str
    dialogue_text: str
    emotion: str = "neutral" # e.g., "angry", "sad", "happy"
    film_context: dict

class AnimationRequest(BaseModel):
    storyboard: List[Dict] # The full storyboard with image URLs
    dialogue_clips: List[Dict] # List of {'character_id': str, 'audio_path': str}
    film_context: dict

class AssemblyRequest(BaseModel):
    scene_text: str
    animated_shots: List[str] # List of paths to animated shot videos
    lip_sync_clips: Dict[str, str] # Maps dialogue text to lip-sync video path
    music_track_path: str = None
    film_context: dict

class EnhancementRequest(BaseModel):
    assembled_video_path: str
    source_clips: List[str] # Paths to the clips that were used
    film_context: dict

@app.post("/generate/scene")
async def create_scene(request: SceneRequest):
    """ Generates a script scene. """
    try:
        # 1. Generate the first draft
        scene = generate_scene(request.prompt, request.context)
        
        # 2. Submit for validation (fire and forget for this example)
        # In a real system, you'd wait for the result and refine.
        validation_payload = {"content_type": "script_scene", "content": scene, "context": request.context}
        requests.post("http://127.0.0.1:8000/validate", json=validation_payload)
        
        # 3. Return the generated scene
        return {"scene": scene}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/character_profile")
async def create_character_profile(request: CharacterRequest):
    """ Generates a detailed character profile. """
    try:
        character_profile = generate_character_profile(request.brief, request.film_context)
        
        # Submit for validation
        validation_payload = {
            "content_type": "character_profile",
            "content": json.dumps(character_profile), # Convert dict to string for content field
            "context": request.film_context
        }
        requests.post("http://127.0.0.1:8000/validate", json=validation_payload)
        
        return {"character_profile": character_profile}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/costume_and_appearance")
async def create_costume_and_appearance(request: CharacterRequest):
    """ Generates costume, hair, makeup descriptions, and image prompts. """
    try:
        # This endpoint assumes the character profile is passed within the film_context
        appearance_data = generate_costume_and_appearance(request.film_context.get("character_profile", {"name": "Unnamed Character"}), request.film_context)
        
        # Submit for validation (e.g., visual appeal potential)
        validation_payload = {"content_type": "costume_description", "content": appearance_data["image_generation_prompt"], "context": request.film_context}
        requests.post("http://127.0.0.1:8000/validate", json=validation_payload)
        
        return {"appearance_data": appearance_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/storyboard")
async def create_storyboard(request: StoryboardRequest):
    """
    Generates a full storyboard for a scene, including a shot list and images.
    """
    try:
        # 1. Fetch character data from the Character DB service
        print(f"Fetching data for character ID: {request.character_id}")
        character_db_url = f"http://127.0.0.1:8002/characters/{request.character_id}"
        response = requests.get(character_db_url)
        response.raise_for_status()  # Raise an exception for bad status codes (like 404)
        character_data = response.json()

        # Extract the necessary info
        character_appearance = character_data.get("appearance")
        character_reference_image_url = character_data.get("key_visual_url")

        # Handle cases where data is missing
        if not character_appearance:
            # A more advanced system could auto-generate this, but for now, we require it.
            raise HTTPException(
                status_code=400,
                detail=f"Character with ID {request.character_id} lacks appearance data. Please generate it first."
            )
        if not character_reference_image_url:
            print(f"Warning: Character {request.character_id} has no key visual. Consistency may be affected.")

        # 2. Generate the shot list from the script
        shot_list = generate_shot_list(request.scene_text, request.film_context)
        
        if not shot_list:
            raise HTTPException(status_code=500, detail="Cinematographer AI failed to generate a shot list.")
            
        # 3. Generate an image for each shot using the fetched character data
        storyboard = []
        for shot in shot_list:
            image_url = generate_storyboard_image(shot, character_appearance, request.film_context, character_reference_image_url)
            shot_with_image = shot.copy()
            shot_with_image["storyboard_image_url"] = image_url
            storyboard.append(shot_with_image)
            
        return {"storyboard": storyboard}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/sound_design")
async def create_sound_design(request: AuditoryRequest):
    """
    Generates sound design suggestions for a given scene.
    """
    try:
        sound_design_data = generate_sound_design(request.scene_text, request.film_context)
        
        # Submit for validation
        validation_payload = {
            "content_type": "sound_design",
            "content": json.dumps(sound_design_data),
            "context": {**request.film_context, "mood": sound_design_data.get("overall_mood_description", "")}
        }
        requests.post("http://127.0.0.1:8000/validate", json=validation_payload)
        
        return {"sound_design": sound_design_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/music_composition")
async def create_music_composition(request: AuditoryRequest):
    """
    Generates music composition suggestions for a given scene.
    """
    try:
        music_data = generate_music_composition(request.scene_text, request.film_context)
        
        # Submit for validation
        validation_payload = {
            "content_type": "music_composition",
            "content": json.dumps(music_data),
            "context": {**request.film_context, "emotional_arc": music_data.get("main_theme_suggestion", "")}
        }
        requests.post("http://127.0.0.1:8000/validate", json=validation_payload)
        
        return {"music_composition": music_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/dialogue", response_model=dict)
async def create_dialogue(request: DialogueRequest):
    """
    Generates speech for a line of dialogue using the character's assigned voice.
    """
    try:
        # 1. Fetch character data to get the assigned voice
        print(f"Fetching voice for character ID: {request.character_id}")
        character_db_url = f"http://127.0.0.1:8002/characters/{request.character_id}"
        response = requests.get(character_db_url)
        response.raise_for_status()
        character_data = response.json()

        provider = character_data.get("tts_provider", "openai")
        voice_id = character_data.get("tts_voice_id", "alloy")
        character_name = character_data.get("profile", {}).get("name", "UnknownCharacter")

        # 2. Generate the audio file
        audio_file_path = generate_dialogue_audio(request.dialogue_text, provider, voice_id, character_name, request.emotion)

        return {"message": "Dialogue generated successfully.", "audio_file_path": audio_file_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/animated_scene", response_model=dict)
async def create_animated_scene(request: AnimationRequest):
    """
    Generates a full animated scene from storyboard images and dialogue audio.
    """
    try:
        video_clips = []

        # 1. Generate lip-sync videos for all dialogue
        lip_sync_map = {} # Maps audio path to video path
        for dialogue in request.dialogue_clips:
            # Fetch character key visual
            char_id = dialogue['character_id']
            response = requests.get(f"http://127.0.0.1:8002/characters/{char_id}")
            response.raise_for_status()
            key_visual_url = response.json().get("key_visual_url")

            if not key_visual_url:
                print(f"Warning: No key visual for character {char_id}. Skipping lip-sync.")
                continue

            video_path = generate_lip_sync_video(key_visual_url, dialogue['audio_path'])
            lip_sync_map[dialogue['audio_path']] = video_path

        # 2. Animate storyboard shots
        for shot in request.storyboard:
            # This is a simplified logic. A real system would map dialogue to shots.
            # For now, we just animate the static storyboard images.
            video_path = animate_storyboard_shot(shot['storyboard_image_url'], shot)
            video_clips.append(video_path)

        # 3. Assemble the final video (simple concatenation for this example)
        # A real editor AI would use the script and shot list for timing.
        final_video_path = "generated_video_clips/final_scene.mp4"
        # final_clips = [VideoFileClip(path) for path in video_clips]
        # final_video = concatenate_videoclips(final_clips)
        # final_video.write_videofile(final_video_path, codec="libx264", fps=24)

        return {"message": "Scene animation process complete.", "output_video_path": final_video_path, "clips": video_clips}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/assemble/scene", response_model=dict)
async def assemble_scene(request: AssemblyRequest):
    """
    Assembles a final scene from video clips based on the script's timing.
    """
    try:
        # 1. Create the Edit Decision List (EDL)
        edl = create_edit_decision_list(
            request.scene_text,
            request.animated_shots,
            request.lip_sync_clips
        )

        # 2. Assemble the video from the EDL
        final_video_path = assemble_scene_from_edl(edl, request.music_track_path)

        return {"message": "Scene assembled successfully.", "final_video_path": final_video_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/enhance/scene", response_model=dict)
async def enhance_scene(request: EnhancementRequest):
    """
    Runs post-production checks and enhancements on an assembled scene.
    """
    try:
        # 1. Check for visual continuity across the source clips
        continuity_score, continuity_feedback = check_visual_continuity(request.source_clips)

        # 2. Generate subtitles for the final video
        subtitle_path = generate_subtitles(request.assembled_video_path)

        # 3. Score the final quality of the video
        quality_score, quality_feedback = score_final_quality(request.assembled_video_path)

        return {
            "message": "Post-production enhancements complete.",
            "results": {
                "continuity_check": {"score": continuity_score, "feedback": continuity_feedback},
                "subtitle_file": subtitle_path,
                "quality_assessment": {"score": quality_score, "feedback": quality_feedback}
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
