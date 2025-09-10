# src/podcast_creator_gtts.py - Alternative with Google TTS
import os
import tempfile
import time
from pydub import AudioSegment
from gtts import gTTS
import asyncio

class MultiVoicePodcastCreator:
    def __init__(self):
        # We'll use different accents to simulate different voices
        self.voices = {
            'host1': {'lang': 'en', 'tld': 'com', 'slow': False},  # American accent
            'host2': {'lang': 'en', 'tld': 'co.uk', 'slow': False}, # British accent
        }
    
    async def create_podcast(self, dialogue_script, output_file):
        """Generate podcast using Google TTS"""
        
        print("Generating multi-voice podcast using gTTS...")
        
        audio_segments = []
        temp_files = []
        
        try:
            for i, segment in enumerate(dialogue_script):
                print(f"Processing segment {i+1}/{len(dialogue_script)}")
                
                # Create temp file
                tmp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
                tmp_filename = tmp_file.name
                tmp_file.close()
                temp_files.append(tmp_filename)
                
                # Get voice settings
                voice_settings = self.voices.get(segment['speaker'], self.voices['host1'])
                
                # Generate speech with gTTS with retry logic
                success = False
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        print(f"  Attempt {attempt + 1} for segment {i+1}")
                        tts = gTTS(
                            text=segment['text'],
                            lang=voice_settings['lang'],
                            tld=voice_settings['tld'],
                            slow=voice_settings['slow']
                        )
                        tts.save(tmp_filename)
                        success = True
                        break  # Success, exit retry loop
                        
                    except Exception as e:
                        print(f"  Attempt {attempt + 1} failed: {e}")
                        if attempt < max_retries - 1:
                            wait_time = 2 ** attempt
                            print(f"  Waiting {wait_time} seconds before retry...")
                            time.sleep(wait_time)
                        else:
                            print(f"  All attempts failed for segment {i+1}, skipping...")
                
                if not success:
                    continue  # Skip this segment and move to next
                
                # Load audio
                try:
                    audio = AudioSegment.from_file(tmp_filename, format="mp3")
                    
                    # Adjust speed slightly for variety between voices
                    if segment['speaker'] == 'host1':
                        audio = audio.speedup(playback_speed=1.05)  # Slightly faster
                    
                    # Add pause between different speakers
                    if i > 0 and dialogue_script[i-1]['speaker'] != segment['speaker']:
                        silence = AudioSegment.silent(duration=400)
                        audio_segments.append(silence)
                    
                    audio_segments.append(audio)
                    
                except Exception as e:
                    print(f"  Error loading audio for segment {i+1}: {e}")
                    continue
            
            if not audio_segments:
                raise Exception("No audio segments were generated")
            
            # Combine all segments
            print("Combining audio segments...")
            final_audio = AudioSegment.empty()
            for segment in audio_segments:
                final_audio += segment
            
            # Add intro/outro
            intro_silence = AudioSegment.silent(duration=1000)
            outro_silence = AudioSegment.silent(duration=1500)
            final_with_padding = intro_silence + final_audio + outro_silence
            
            # Export
            print(f"Exporting to {output_file}")
            final_normalized = final_with_padding.normalize()
            final_normalized.export(output_file, format="mp3", bitrate="128k")
            
            print(f"Podcast successfully created: {output_file}")
            return output_file
            
        finally:
            # Clean up
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass