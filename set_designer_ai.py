# set_designer_ai.py
# This file contains the logic for the Expert Set Designer AI.
# It generates a detailed description of the set based on the scene's location and mood.

from typing import Dict, Any

def design_set(scene_manifest: Dict[str, Any], visual_concept: Dict[str, Any]) -> str:
    """
    Takes a scene manifest and a visual concept guide to generate a
    detailed description of the set.
    """
    print("SET DESIGNER: Designing the set based on the visual concept guide.")
    
    location = scene_manifest['location'].lower()
    mood = scene_manifest['mood'].lower()
    
    # Start with the high-level styles from the guide
    description = f"Visual Style: {visual_concept.get('overall_aesthetic', 'N/A')}\n"
    description += f"Architecture: {visual_concept.get('architectural_style', 'N/A')}\n"
    description += f"Base Location: {scene_manifest['location']}\n"
    
    # Use the guide to inform the description
    textures = ", ".join(visual_concept.get('material_textures', []))
    description += f"Key Textures: {textures}\n\n"
    
    # Generate specific details based on location and guide
    if "control room" in location:
        description += "A semi-circular room dominated by a large, holographic display table. "
        description += "Workstations are built from materials like brushed aluminum and smart glass, consistent with the Utopian aesthetic. "
        if "tense" in mood:
            # Override general lighting style for a specific mood
            description += "The lighting is low, with long shadows, overriding the usual soft light to create tension."
        else:
            description += f"The lighting is {visual_concept.get('lighting_style', 'neutral')}."
            
    elif "workshop" in location:
        description += "A chaotic but organized space. Workbenches are covered with tools and half-finished gadgets. "
        description += f"The materials are a mix of practical metals and {textures}. "
        if "triumphant" in mood:
            description += "A central project glows with a powerful light, casting lens flares consistent with the Utopian style."
        else:
            description += "The space is lit by the glow of a single workstation."
            
    else:
        description += "A generic, functional space, built with materials and lighting from the visual guide."

    print("SET DESIGNER: Set description generated.")
    return description

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
        "actions": []
    }
    
    set_desc = design_set(example_scene, concept_guide)
    print("\n--- Generated Set Description ---")
    print(set_desc)
