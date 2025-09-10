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