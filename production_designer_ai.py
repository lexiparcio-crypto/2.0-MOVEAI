# production_designer_ai.py
# This file contains the logic for the Expert Production Designer AI.
# It defines the overall visual style for a project.

import json
from typing import Dict, Any

def generate_visual_concept(project_prompt: str) -> Dict[str, Any]:
    """
    Takes a high-level project prompt and generates a visual concept guide.
    
    A real system would use a powerful multi-modal model to generate a rich
    visual language, including mood boards and style references. This prototype
    uses rules to establish a consistent visual theme.
    """
    print(f"PRODUCTION DESIGNER: Generating visual concept for prompt: '{project_prompt}'")
    
    prompt = project_prompt.lower()
    
    guide = {
        "project_prompt": project_prompt,
        "overall_aesthetic": "generic scifi"
    }

    if "gritty" in prompt and "cyberpunk" in prompt:
        guide.update({
            "overall_aesthetic": "Gritty Cyberpunk",
            "color_palette": {
                "primary": ["#0d0d0d", "#1a1a1a"], # Near blacks
                "secondary": ["#4a4a4a", "#6b6b6b"], # Greys
                "accent": ["#ff00ff", "#00ffff", "#ffff00"] # Neon pink, cyan, yellow
            },
            "material_textures": ["wet asphalt", "exposed wires", "chrome", "holographic ads"],
            "architectural_style": "Brutalist, layered with high-tech and decay",
            "lighting_style": "High-contrast, neon-drenched, volumetric fog"
        })
    elif "sleek" in prompt and "utopian" in prompt:
        guide.update({
            "overall_aesthetic": "Sleek Utopian",
            "color_palette": {
                "primary": ["#ffffff", "#f5f5f5"], # Whites
                "secondary": ["#a0a0a0", "#d0d0d0"], # Light Greys
                "accent": ["#3498db", "#f1c40f"] # Calming blue, gentle yellow
            },
            "material_textures": ["polished white marble", "brushed aluminum", "smart glass", "light wood"],
            "architectural_style": "Organic, minimalist, flowing curves",
            "lighting_style": "Soft, diffused, natural light, lens flare"
        })
        
    print("PRODUCTION DESIGNER: Visual concept guide generated.")
    return guide

if __name__ == '__main__':
    # This would be run once at the start of a new project.
    prompt = "A gritty, cyberpunk detective story set in a rain-soaked metropolis."
    visual_concept = generate_visual_concept(prompt)
    
    print("\n--- Generated Visual Concept Guide ---")
    print(json.dumps(visual_concept, indent=2))
    
    # Save the guide to a file so other AIs can use it
    with open("visual_concept_guide.json", "w") as f:
        json.dump(visual_concept, f, indent=2)
        
    print("\nVisual concept guide saved to 'visual_concept_guide.json'")
