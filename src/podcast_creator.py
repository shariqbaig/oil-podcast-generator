# src/podcast_creator.py
import os
import tempfile
import asyncio
import random
from pydub import AudioSegment
import edge_tts
from src.music_generator import BackgroundMusicGenerator

class MultiVoicePodcastCreator:
    def __init__(self, max_retries=3, base_delay=2):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.music_generator = BackgroundMusicGenerator()
        
        # Soothing, conversational voices with more natural pace
        self.voices = {
            'host1': {
                'name': 'en-US-GuyNeural',  # Warm, friendly male voice
                'rate': '+0%',  # Natural pace (not too slow)
                'pitch': '-3Hz'  # Slightly lower pitch for warmth
            },
            'host2': {
                'name': 'en-US-AriaNeural',  # Gentle, conversational female voice
                'rate': '+2%',  # Slightly faster for energy
                'pitch': '-2Hz'  # Slightly lower for warmth
            }
        }
        
        # Emotion to prosody mapping (natural variations, not too slow)
        self.emotion_settings = {
            'neutral': {'rate': '+0%', 'pitch': '-2Hz'},
            'excited': {'rate': '+5%', 'pitch': '+2Hz'},  # Natural excitement
            'thoughtful': {'rate': '-5%', 'pitch': '-3Hz'},  # Slightly slower
            'concerned': {'rate': '-3%', 'pitch': '-4Hz'},
            'optimistic': {'rate': '+3%', 'pitch': '+1Hz'},  # Upbeat
            'amused': {'rate': '+2%', 'pitch': '+1Hz'},  # Light, playful
            'surprised': {'rate': '+4%', 'pitch': '+3Hz'},  # Natural surprise
            'skeptical': {'rate': '-4%', 'pitch': '-5Hz'}  # Slightly slower
        }
    
    async def create_podcast(self, dialogue_script, output_file):
        """Generate podcast using Edge TTS with robust retry logic"""
        
        print("Generating podcast with Edge TTS (v7.2.3)...")
        audio_segments = []
        temp_files = []
        
        try:
            for i, segment in enumerate(dialogue_script):
                emotion = segment.get('emotion', 'neutral')
                print(f"Processing segment {i+1}/{len(dialogue_script)}: {emotion} tone")
                
                # Create temp file
                tmp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
                tmp_filename = tmp_file.name
                tmp_file.close()
                temp_files.append(tmp_filename)
                
                # Generate with retry logic
                success = await self._generate_speech_with_retry(
                    segment['text'],
                    segment['speaker'],
                    emotion,
                    tmp_filename
                )
                
                if success:
                    try:
                        # Load and process audio
                        audio = AudioSegment.from_file(tmp_filename, format="mp3")
                        
                        # Add minimal pauses for fluent conversation
                        if i > 0 and dialogue_script[i-1]['speaker'] != segment['speaker']:
                            silence = AudioSegment.silent(duration=300)  # Brief pause between speakers
                            audio_segments.append(silence)
                        elif i > 0:
                            # Very short pause for same speaker
                            silence = AudioSegment.silent(duration=100)
                            audio_segments.append(silence)
                        
                        audio_segments.append(audio)
                    except Exception as e:
                        print(f"  Error loading audio for segment {i+1}: {e}")
                else:
                    print(f"  Failed to generate segment {i+1} after {self.max_retries} attempts")
            
            if not audio_segments:
                raise Exception("No audio segments were generated")
            
            # Combine all segments
            print("Combining audio segments...")
            final_audio = AudioSegment.empty()
            for segment in audio_segments:
                final_audio += segment
            
            # Add intro/outro padding
            intro_silence = AudioSegment.silent(duration=1000)
            outro_silence = AudioSegment.silent(duration=1500)
            final_with_padding = intro_silence + final_audio + outro_silence
            
            # Add background music
            print("Adding subtle background music...")
            try:
                # Generate ambient music for the full duration
                music_duration = len(final_with_padding)
                background_music = self.music_generator.create_ambient_music(music_duration)
                
                # Mix with speech
                final_with_music = self.music_generator.mix_with_speech(final_with_padding, background_music)
            except Exception as e:
                print(f"Could not add background music: {e}")
                final_with_music = final_with_padding
            
            # Normalize and export
            print(f"Exporting to {output_file}")
            final_normalized = final_with_music.normalize()
            
            # Higher quality export
            final_normalized.export(
                output_file, 
                format="mp3", 
                bitrate="192k",
                parameters=["-ar", "44100"]  # Standard podcast sample rate
            )
            
            # Get duration for logging
            duration_seconds = len(final_normalized) / 1000
            duration_min = int(duration_seconds // 60)
            duration_sec = int(duration_seconds % 60)
            
            print(f"[SUCCESS] Podcast created: {output_file} (Duration: {duration_min}:{duration_sec:02d})")
            return output_file
            
        finally:
            # Clean up temp files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
    
    async def _generate_speech_with_retry(self, text, speaker, emotion, output_file):
        """Generate speech with robust retry logic for handling 403 errors"""
        
        voice_config = self.voices.get(speaker, self.voices['host1'])
        emotion_config = self.emotion_settings.get(emotion, self.emotion_settings['neutral'])
        
        # Enhance text with SSML
        enhanced_text = self._enhance_with_ssml(text)
        
        for attempt in range(self.max_retries):
            try:
                if attempt > 0:
                    # Exponential backoff with jitter
                    delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                    print(f"  Retry {attempt + 1}/{self.max_retries} in {delay:.1f} seconds...")
                    await asyncio.sleep(delay)
                
                # Create communicate instance
                communicate = edge_tts.Communicate(
                    enhanced_text,
                    voice_config['name'],
                    rate=emotion_config['rate'],
                    pitch=emotion_config['pitch']
                )
                
                # Save with timeout
                await asyncio.wait_for(
                    communicate.save(output_file),
                    timeout=30.0  # 30 second timeout
                )
                
                print(f"  [OK] Success on attempt {attempt + 1}")
                return True
                
            except asyncio.TimeoutError:
                print(f"  Timeout on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    continue
                    
            except Exception as e:
                error_msg = str(e)
                print(f"  Attempt {attempt + 1} failed: {error_msg}")
                
                # Check for specific errors
                if "403" in error_msg or "Invalid response status" in error_msg:
                    if attempt < self.max_retries - 1:
                        # For 403 errors, use longer delay
                        await asyncio.sleep(self.base_delay * 3)
                        continue
                elif "connection" in error_msg.lower():
                    # Network issues, retry
                    if attempt < self.max_retries - 1:
                        continue
                
                # For other errors or last attempt
                if attempt == self.max_retries - 1:
                    return False
        
        return False
    
    def _enhance_with_ssml(self, text):
        """Clean and enhance text for natural speech"""
        
        # Clean up URLs before processing
        text = self._clean_urls(text)
        
        # Process laugh and reaction markers
        text = self._process_reactions(text)
        
        # Fix pronunciations for oil industry terms (without SSML tags)
        text = text.replace('WTI', 'W T I')
        text = text.replace('OPEC', 'O P E C')
        text = text.replace('bbl', 'barrels')
        text = text.replace('bbl/d', 'barrels per day')
        text = text.replace('E&P', 'E and P')
        text = text.replace('LNG', 'L N G')
        text = text.replace('API', 'A P I')
        text = text.replace('EIA', 'E I A')
        text = text.replace('CEO', 'C E O')
        text = text.replace('IPO', 'I P O')
        text = text.replace('M&A', 'M and A')
        
        # Clean up common abbreviations
        text = text.replace('vs.', 'versus')
        text = text.replace('etc.', 'etcetera')
        text = text.replace('i.e.', 'that is')
        text = text.replace('e.g.', 'for example')
        text = text.replace('Q1', 'first quarter')
        text = text.replace('Q2', 'second quarter')
        text = text.replace('Q3', 'third quarter')
        text = text.replace('Q4', 'fourth quarter')
        
        # Add natural pauses with commas instead of SSML
        text = text.replace('...', ', ')
        text = text.replace(' - ', ', ')
        text = text.replace('—', ', ')
        
        return text
    
    def _process_reactions(self, text):
        """Convert reaction markers to more subtle expressions"""
        import re
        
        # More subtle, natural reactions
        reactions = {
            '[laughs]': '',  # Remove explicit laughs, let emotion handle it
            '[chuckles]': '',  # Remove explicit chuckles
            '[sighs]': '',  # Remove sighs
            '[surprised]': '',  # Remove marker, emotion handles it
            '[upbeat]': '',  # Remove marker, emotion handles it
            '[amused]': '',  # Remove marker, emotion handles it
            'Hmm...': 'Hmm,',  # Shorter thinking sound
            'Oh wow!': 'Wow',  # More subtle
            'Actually, wait—': 'Actually,',  # Smoother
            'Oh, that reminds me—': 'That reminds me,',  # Less abrupt
            'ha ha': '',  # Remove any explicit ha ha
            'haha': '',  # Remove variations
            'Ha ha': '',  # Remove variations
        }
        
        for marker, replacement in reactions.items():
            text = text.replace(marker, replacement)
        
        # Remove any remaining brackets
        text = re.sub(r'\[.*?\]', '', text)
        
        return text
    
    def _clean_urls(self, text):
        """Remove or simplify URLs for better TTS output"""
        import re
        
        # Pattern to match URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+|www\.[^\s<>"{}|\\^`\[\]]+'
        
        # Find all URLs in the text
        urls = re.findall(url_pattern, text)
        
        for url in urls:
            # Extract domain name for speaking
            domain_match = re.search(r'(?:https?://)?(?:www\.)?([^/]+)', url)
            if domain_match:
                domain = domain_match.group(1)
                # Clean up domain for speaking
                domain = domain.replace('.com', ' dot com')
                domain = domain.replace('.org', ' dot org')
                domain = domain.replace('.net', ' dot net')
                domain = domain.replace('.gov', ' dot gov')
                domain = domain.replace('.', ' dot ')
                
                # Replace the full URL with just the domain name
                text = text.replace(url, domain)
        
        return text