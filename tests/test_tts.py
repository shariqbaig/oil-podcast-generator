# test_tts.py - Save this in your project root
import asyncio

async def test_edge_tts():
    try:
        import edge_tts
        communicate = edge_tts.Communicate("Testing Edge TTS", "en-US-AriaNeural")
        await communicate.save("test_edge.mp3")
        print("✓ Edge TTS works!")
        return True
    except Exception as e:
        print(f"✗ Edge TTS failed: {e}")
        return False

def test_gtts():
    try:
        from gtts import gTTS
        tts = gTTS("Testing Google TTS", lang='en')
        tts.save("test_gtts.mp3")
        print("✓ gTTS works!")
        return True
    except Exception as e:
        print(f"✗ gTTS failed: {e}")
        return False

def test_pyttsx3():
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file("Testing pyttsx3", "test_pyttsx3.mp3")
        engine.runAndWait()
        print("✓ pyttsx3 works!")
        return True
    except Exception as e:
        print(f"✗ pyttsx3 failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing TTS options...\n")
    asyncio.run(test_edge_tts())
    test_gtts()
    test_pyttsx3()