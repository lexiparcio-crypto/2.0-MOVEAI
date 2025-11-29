# costume_designer_ai.py
# This file contains the logic for the Expert Costume Designer AI.
# It selects outfits for characters based on the scene context and their wardrobe.

from typing import Dict, Any, List

def assign_outfits_for_scene(scene_manifest: Dict[str, Any], character_profiles: List[Dict[str, Any]], visual_concept: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Takes a scene manifest, character profiles, and a visual concept guide, 
    and assigns an outfit to each character.
    """
    print("COSTUME DESIGNER: Assigning outfits based on the visual concept guide.")
    
    actions = scene_manifest['actions']
    location = scene_manifest['location'].lower()
    aesthetic = visual_concept.get('overall_aesthetic', '').lower()

    for action in actions:
        character_name = action['character']
        character = next((c for c in character_profiles if c['name'] == character_name), None)

        if not character:
            continue

        # Start with the default outfit
        chosen_outfit = character['outfits'].get('default', 'no outfit specified')

        # Use the guide and location to select an outfit
        if "cyberpunk" in aesthetic and "control room" in location:
            # In a gritty setting, people might not have formal uniforms
            chosen_outfit = character['outfits'].get('default', chosen_outfit)
        elif "utopian" in aesthetic and "control room" in location:
            # In a utopian setting, uniforms might be more common
            chosen_outfit = character['outfits'].get('uniform', chosen_outfit)
        elif "off duty" in location:
            chosen_outfit = character['outfits'].get('off_duty', chosen_outfit)
        
        action['outfit'] = chosen_outfit
        print(f"COSTUME DESIGNER: Assigned outfit '{chosen_outfit}' to {character_name} for '{aesthetic}' aesthetic.")

    return actions

if __name__ == "__main__":
    import json

    # Load the character profiles and visual guide
    try:
        # This is a simplified example; in practice, you'd load from the JSON file
        from character_ai import characters 
        with open("visual_concept_guide.json", "r") as f:
            concept_guide = json.load(f)
    except (ImportError, FileNotFoundError) as e:
        print(f"ERROR: Could not load necessary files. {e}")
        exit()

    example_scene = {
        "scene_id": 1,
        "location": "Approver GOD Control Room - dimly lit",
        "mood": "Tense, suspenseful",
        "actions": [
            {"character": "Jaxon", "dialogue": "..."},
            {"character": "Ava", "dialogue": "..."}
        ]
    }
    
    updated_actions = assign_outfits_for_scene(example_scene, characters, concept_guide)
    print("\n--- Actions with Outfits ---")
    print(json.dumps(updated_actions, indent=2))
