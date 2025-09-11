# src/music_generator.py
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import tempfile
import os

class BackgroundMusicGenerator:
    def __init__(self):
        """Initialize the background music generator"""
        self.sample_rate = 44100
        self.bit_depth = 16
        
    def create_ambient_music(self, duration_ms):
        """
        Create subtle ambient background music suitable for podcasts
        Uses low-frequency drones and gentle harmonics
        """
        
        # Create a subtle drone sound with multiple harmonics
        # Base frequency (low E - gives a professional, serious tone)
        base_freq = 82.41  # E2
        
        # Create multiple sine waves for richness
        harmonics = [
            (base_freq, 0.3),       # Fundamental
            (base_freq * 2, 0.15),  # Octave
            (base_freq * 3, 0.08),  # Fifth
            (base_freq * 1.5, 0.1), # Perfect fifth
        ]
        
        # Generate the combined sound
        combined = None
        
        for freq, amplitude in harmonics:
            # Create sine wave
            tone = Sine(freq)
            
            # Generate for the specified duration
            sound = tone.to_audio_segment(duration=duration_ms)
            
            # Apply fade in and fade out for smoothness
            sound = sound.fade_in(2000).fade_out(2000)
            
            # Adjust volume
            sound = sound - (20 - int(20 * amplitude))  # Convert amplitude to dB reduction
            
            if combined is None:
                combined = sound
            else:
                combined = combined.overlay(sound)
        
        # Apply gentle LFO (Low Frequency Oscillation) for movement
        # This creates a subtle "breathing" effect
        combined = self._apply_gentle_lfo(combined)
        
        # Make it very quiet (background level)
        combined = combined - 25  # Reduce by 25 dB for subtle background
        
        return combined
    
    def _apply_gentle_lfo(self, audio_segment):
        """Apply a gentle volume oscillation to create movement"""
        samples = np.array(audio_segment.get_array_of_samples())
        
        # Create a very slow sine wave for volume modulation
        duration_seconds = len(samples) / audio_segment.frame_rate
        lfo_frequency = 0.1  # Very slow, 10 second cycle
        
        time_array = np.linspace(0, duration_seconds, len(samples))
        lfo = 0.9 + 0.1 * np.sin(2 * np.pi * lfo_frequency * time_array)
        
        # Apply the LFO to the samples
        modulated_samples = samples * lfo
        modulated_samples = np.clip(modulated_samples, -32768, 32767).astype(np.int16)
        
        # Create new audio segment with modulated samples
        modulated_audio = audio_segment._spawn(
            modulated_samples.tobytes(),
            overrides={
                "frame_rate": audio_segment.frame_rate,
                "channels": audio_segment.channels,
                "sample_width": audio_segment.sample_width,
            }
        )
        
        return modulated_audio
    
    def mix_with_speech(self, speech_audio, music_audio):
        """
        Mix background music with speech, ensuring speech remains clear
        """
        # Ensure both tracks are the same length
        if len(music_audio) < len(speech_audio):
            # Loop the music if it's shorter
            loops_needed = (len(speech_audio) // len(music_audio)) + 1
            music_audio = music_audio * loops_needed
        
        # Trim music to match speech length
        music_audio = music_audio[:len(speech_audio)]
        
        # Duck the music slightly when speech is present (simple ducking)
        # This ensures speech remains clear
        music_ducked = music_audio - 5  # Additional reduction during speech
        
        # Mix the audio
        mixed = speech_audio.overlay(music_ducked)
        
        return mixed


def add_background_music(audio_file_path):
    """
    Add background music to an existing audio file
    
    Args:
        audio_file_path: Path to the input audio file
        
    Returns:
        Path to the output audio file with music
    """
    from pydub import AudioSegment
    import os
    
    # Load the existing audio
    audio = AudioSegment.from_mp3(audio_file_path)
    
    # Create music generator
    generator = BackgroundMusicGenerator()
    
    # Generate ambient music for the audio duration
    music = generator.create_ambient_music(len(audio))
    
    # Apply volume reduction to music
    music = music - 25  # Reduce by 25dB to keep it subtle
    
    # Duck the music slightly more
    music_ducked = music - 5  # Additional reduction during speech
    
    # Mix the audio with music
    mixed = audio.overlay(music_ducked)
    
    # Save to a temporary file first
    base_name = os.path.splitext(audio_file_path)[0]
    output_path = f"{base_name}_with_music.mp3"
    
    # Export with good quality
    mixed.export(output_path, format="mp3", bitrate="192k")
    
    return output_path


def add_background_music_to_file(audio_file_path):
    """
    Add background music to an audio file in place
    
    Args:
        audio_file_path: Path to the audio file to modify
    """
    from pydub import AudioSegment
    import tempfile
    import os
    import shutil
    
    print(f"Loading audio from: {audio_file_path}")
    
    # Load the existing audio
    audio = AudioSegment.from_mp3(audio_file_path)
    
    print(f"Audio duration: {len(audio)/1000:.1f} seconds")
    
    # Create music generator
    generator = BackgroundMusicGenerator()
    
    # Generate ambient music for the audio duration
    print("Generating ambient background music...")
    music = generator.create_ambient_music(len(audio))
    
    # Apply volume reduction to music (make it very subtle)
    music = music - 30  # Reduce by 30dB to keep it very subtle
    
    # Mix the audio with music
    print("Mixing audio with background music...")
    mixed = audio.overlay(music)
    
    # Save to a temporary file first
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
        temp_path = tmp_file.name
    
    # Export with good quality
    mixed.export(temp_path, format="mp3", bitrate="192k")
    
    # Replace the original file
    shutil.move(temp_path, audio_file_path)
    
    print(f"Background music added successfully")