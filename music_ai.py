# music_ai.py
# This file contains the logic for the Expert Music Director AI.
# It generates a detailed music plan based on a scene's mood and actions.

from typing import Dict, Any, List

def generate_music_plan(scene_manifest: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes a scene manifest and generates a detailed plan for the music.

    A real system would use a generative model trained on music theory
    and film scores to create a nuanced plan. This prototype uses a
    rule-based system based on the scene's mood.
    """
    print(f"MUSIC DIRECTOR: Generating music plan for mood: '{scene_manifest['mood']}'")
    mood = scene_manifest['mood'].lower()

    if "tense" in mood or "suspenseful" in mood:
        return {
            "style": "Orchestral, Suspense",
            "tempo": "60-80 BPM",
            "instruments": ["Low strings (cello, double bass)", "Timpani", "Distant brass swells"],
            "dynamics": "Starts quiet (pianissimo), builds with each line of dialogue.",
            "key": "C minor"
        }
    elif "excited" in mood or "triumphant" in mood:
        return {
            "style": "Orchestral, Fanfare",
            "tempo": "120-140 BPM",
            "instruments": ["Full brass section (trumpets, horns)", "Soaring strings", "Cymbals"],
            "dynamics": "Loud and celebratory (fortissimo).",
            "key": "D major"
        }
    else:
        # Default fallback plan
        return {
            "style": "Ambient, Minimalist",
            "tempo": "70 BPM",
            "instruments": ["Synthesizer pads", "Light piano melody"],
            "dynamics": "Consistent and unobtrusive (mezzo-piano).",
            "key": "A minor"
        }

if __name__ == "__main__":
    example_scene_tense = {
        "scene_id": 1,
        "mood": "Tense, suspenseful",
    }
    plan1 = generate_music_plan(example_scene_tense)
    import json
    print("\n--- Music Plan for Tense Scene ---")
    print(json.dumps(plan1, indent=2))

    example_scene_triumphant = {
        "scene_id": 2,
        "mood": "Excited, triumphant",
    }
    plan2 = generate_music_plan(example_scene_triumphant)
    print("\n--- Music Plan for Triumphant Scene ---")
    print(json.dumps(plan2, indent=2))
