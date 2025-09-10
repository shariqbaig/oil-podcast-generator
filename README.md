# Oil Field Insights Podcast Generator

An automated system that generates daily podcasts about the oil and gas industry by collecting news, creating dialogue scripts, and producing audio content with multiple voices.

## Features

- **News Collection**: Automatically fetches latest oil and gas industry news from RSS feeds
- **AI Script Generation**: Creates engaging podcast dialogue between multiple hosts
- **Multi-Voice TTS**: Supports multiple text-to-speech engines:
  - Google TTS (gTTS) with different accents for voice variety
  - Windows SAPI (pyttsx3) as local fallback
  - Edge TTS (when available)
- **Audio Processing**: Combines segments with proper pacing and silence between speakers
- **Automated Pipeline**: Complete end-to-end podcast generation

## Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the podcast generator:
```bash
python main.py
```

This will:
1. Collect recent oil & gas news articles
2. Generate a dialogue script between hosts
3. Create audio using TTS with multiple voices
4. Export the final podcast as MP3

## Configuration

- Edit `config.yaml` to customize news sources and AI settings
- Modify voice settings in the podcast creator for different accents/speeds
- Adjust dialogue templates and host personalities as needed

## Output

Generated podcasts are saved as MP3 files with timestamps in the filename.