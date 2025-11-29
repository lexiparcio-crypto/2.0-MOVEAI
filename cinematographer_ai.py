# cinematographer_ai.py
# This file contains the logic for the Expert Cinematographer AI.
# It generates a detailed shot list for a scene, including camera angles and lighting.

from typing import Dict, Any, List

def generate_shot_list(scene_manifest: Dict[str, Any], visual_concept: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Takes a scene manifest and visual concept guide to generate a list of shots.
    """
    print(f"CINEMATOGRAPHER: Generating shot list for Scene {scene_manifest['scene_id']}")
    
    shot_list = []
    mood = scene_manifest['mood'].lower()
    # Use the guide's lighting style as a default
    base_lighting = visual_concept.get('lighting_style', 'neutral')

    for i, action in enumerate(scene_manifest['actions']):
        shot = {
            "shot_id": f"{scene_manifest['scene_id']}.{i+1}",
            "action_index": i,
            "character": action['character'],
            "shot_type": "medium close-up", # Default
            "camera_movement": "static",
            "lighting": base_lighting # Apply the guide's lighting by default
        }

        # Rule-based shot selection based on mood
        if "tense" in mood or "suspenseful" in mood:
            # Override the lighting for a specific mood
            shot["lighting"] = f"moody, specific override of '{base_lighting}'"
            if i % 2 == 0:
                shot["shot_type"] = "medium close-up"
                shot["camera_movement"] = "very slow push-in"
            else:
                shot["shot_type"] = "over-the-shoulder"
        
        elif "triumphant" in mood:
            shot["lighting"] = f"bright, celebratory version of '{base_lighting}'"
            shot["shot_type"] = "medium shot"
            shot["camera_movement"] = "slow crane up"
            
        # Add a wide establishing shot at the beginning
        if i == 0:
            establishing_shot = {
                "shot_id": f"{scene_manifest['scene_id']}.0",
                "action_index": -1,
                "character": None,
                "shot_type": "establishing wide shot",
                "camera_movement": "slow pan across location",
                "lighting": base_lighting
            }
            shot_list.append(establishing_shot)

        shot_list.append(shot)

    print(f"CINEMATOGRAPHER: Generated {len(shot_list)} shots.")
    return shot_list


if __name__ == "__main__":
    import json

    # Load the master visual guide
    try:
        with open("visual_concept_guide.json", "r") as f:
            concept_guide = json.load(f)
    except FileNotFoundError:
        print("ERROR: visual_concept_guide.json not found. Run production_designer_ai.py first.")
        exit()

    example_scene = {
        "scene_id": 1,
        "location": "Approver GOD Control Room - dimly lit",
        "mood": "Tense, suspenseful",
        "actions": [
            {"character": "Jaxon", "dialogue": "Another hypothesis..."},
            {"character": "Ava", "dialogue": "Run the validation."}
        ]
    }
    
    shots = generate_shot_list(example_scene, concept_guide)
    print("\n--- Generated Shot List ---")
    print(json.dumps(shots, indent=2))
