# screenwriter_ai.py
# This file contains the logic for the Expert Screenwriter AI.
# It generates scene manifests, character dialogue, and plot points.

import os
from dotenv import load_dotenv
from typing import Dict, Any, List

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

import google.generativeai as genai

if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

import json
import google.generativeai as genai

if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_scene_manifest(prompt: str, scene_id: int) -> Dict[str, Any]:
    """
    Takes a high-level prompt and generates a structured scene manifest
    using the Gemini Pro model.
    """
    print(f"SCREENWRITER: Generating scene {scene_id} from prompt: '{prompt}' using Gemini Pro...")

    # Crafting a detailed prompt for Gemini
    gemini_prompt = f"""
You are an expert screenwriter AI. Your task is to generate a detailed scene manifest in JSON format based on the given prompt.
The scene manifest should include:
- "scene_id": The unique identifier for the scene.
- "location": A detailed description of the scene's setting (e.g., "INT. ABANDONED WAREHOUSE - NIGHT").
- "mood": The overall emotional tone of the scene (e.g., "Tense, Suspenseful", "Hopeful, Determined").
- "actions": A list of character actions and dialogue. Each action should be an object with:
    - "character": The name of the character speaking or performing the action.
    - "action_description": (Optional) A brief description of the character's physical action.
    - "dialogue": (Optional) The lines spoken by the character.

Ensure the dialogue and actions are compelling and suitable for a blockbuster Hollywood screenplay.
The output MUST be a valid JSON object. Do not include any other text outside the JSON.

Scene Prompt: "{prompt}"
Scene ID: {scene_id}

Example JSON Structure:
{{
  "scene_id": 1,
  "location": "INT. SPACESHIP BRIDGE - NIGHT",
  "mood": "Urgent, Panicked",
  "actions": [
    {{"character": "AVA", "dialogue": "Sensors are going wild! What is that thing?"}},
    {{"character": "JAXON", "action_description": "Grabs his blaster, eyes scanning the main viewscreen.", "dialogue": "Whatever it is, it's fast. Brace for impact!"}}
  ]
}}
"""
    try:
        response = model.generate_content(gemini_prompt)
        # Attempt to parse the response as JSON
        # Sometimes the LLM might include markdown fences (```json ... ```)
        json_string = response.text.strip()
        if json_string.startswith("```json") and json_string.endswith("```"):
            json_string = json_string[7:-3].strip()

        scene_manifest = json.loads(json_string)
        # Ensure the scene_id matches the requested one
        scene_manifest["scene_id"] = scene_id
        return scene_manifest
    except Exception as e:
        print(f"Error generating scene with Gemini: {e}")
        print(f"Gemini response (raw): {response.text}")
        # Fallback to a basic structure or re-raise
        return {
            "scene_id": scene_id,
            "location": "ERROR: Gemini AI failed to generate specific content.",
            "mood": "Uncertain",
            "actions": [
                {"character": "SYSTEM", "dialogue": "AI encountered an error. Please try a different prompt."}
            ]
        }


if __name__ == "__main__":
    print("\n--- Testing Gemini-powered Scene Generation ---")

    # Test Case 1: Tense confrontation
    prompt1 = "Jaxon and Ava confront a rogue AI in a data center, realizing it has taken over all systems."
    scene1 = generate_scene_manifest(prompt1, 1)
    print("\n--- Generated Scene 1 ---")
    import json
    print(json.dumps(scene1, indent=2))

    # Test Case 2: Dramatic breakthrough
    prompt2 = "Ava makes a critical discovery about the rogue AI's weakness in her lab, under extreme time pressure."
    scene2 = generate_scene_manifest(prompt2, 2)
    print("\n--- Generated Scene 2 ---")
    print(json.dumps(scene2, indent=2))

    # Test Case 3: Action sequence
    prompt3 = "Jaxon fights off security drones while trying to upload a virus to the rogue AI's core server."
    scene3 = generate_scene_manifest(prompt3, 3)
    print("\n--- Generated Scene 3 ---") 
    print(json.dumps(scene3, indent=2))
