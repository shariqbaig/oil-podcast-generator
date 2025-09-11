# tests/test_podcastfy.py
from podcastfy.client import generate_podcast
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Quick test with minimal content
test_config = {
    "word_count": 200,
    "conversation_style": ["casual", "friendly"],
    "podcast_name": "Test Podcast",
    "text_to_speech": {
        "model": "edge",
        "edge": {
            "default_voices": {
                "question": "en-US-AriaNeural",
                "answer": "en-US-GuyNeural"
            }
        }
    }
}

# Option 1: Using text parameter (if supported)
try:
    audio = generate_podcast(
        text="Oil prices rose 5% today on OPEC news. Drilling increased in Texas.",  # Changed from raw_text to text
        conversation_config=test_config,
        tts_model="edge",
        llm_model_name="gemini-1.5-flash",
        api_key_label="GEMINI_API_KEY"
    )
    print(f"Test successful! Generated: {audio}")
except Exception as e:
    print(f"Error with text parameter: {e}")
    
    # Option 2: Save text to file and use as URL
    print("\nTrying file-based approach...")
    
    # Create a temporary text file
    with open("temp_content.txt", "w") as f:
        f.write("Oil prices rose 5% today on OPEC news. Drilling increased in Texas.")
    
    # Use file path as URL
    audio = generate_podcast(
        urls=["temp_content.txt"],  # Podcastfy can read local files
        conversation_config=test_config,
        tts_model="edge",
        llm_model_name="gemini-1.5-flash",
        api_key_label="GEMINI_API_KEY"
    )
    
    print(f"Test successful with file! Generated: {audio}")
    
    # Clean up
    import os
    if os.path.exists("temp_content.txt"):
        os.remove("temp_content.txt")