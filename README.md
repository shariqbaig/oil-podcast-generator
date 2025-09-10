# Oil Field Insights Podcast Generator

An automated system that generates daily podcasts about the oil and gas industry by collecting news, creating dialogue scripts, and producing audio content with multiple voices.

## 🎧 Sample Output

**Latest Episode**: [Oil News - September 10, 2025](docs/episodes/oil_news_20250910.mp3) (4.1MB)

Listen to a fully automated podcast featuring two AI hosts discussing the latest oil and gas industry news with natural conversation flow and different voice accents.

## ✨ Features

- **🔍 News Collection**: Automatically fetches latest oil and gas industry news from RSS feeds
- **🤖 AI Script Generation**: Creates engaging podcast dialogue between multiple hosts using OpenAI
- **🎙️ Multi-Voice TTS**: Robust text-to-speech with fallback systems:
  - Google TTS (gTTS) with American/British accents for voice variety
  - Windows SAPI (pyttsx3) as local fallback
  - Edge TTS support (when available)
- **🎵 Audio Processing**: Combines segments with proper pacing, silence between speakers, and speed variations
- **📡 RSS Distribution**: Generates podcast RSS feed and HTML index for easy distribution
- **🔄 Automated Pipeline**: Complete end-to-end podcast generation with error handling and retry logic

## 🚀 Quick Start

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up API key** (optional - uses free services by default):
```bash
# For enhanced AI script generation
export OPENAI_API_KEY="your-key-here"
```

3. **Generate podcast**:
```bash
python main.py
```

## 📁 Project Structure

```
oil-podcast-generator/
├── main.py              # Main execution script
├── requirements.txt     # Python dependencies
├── src/
│   ├── news_collector.py    # RSS news fetching
│   ├── script_generator.py  # AI dialogue creation
│   ├── podcast_creator.py   # Multi-voice TTS and audio processing
│   └── rss_generator.py     # RSS feed generation
├── docs/
│   ├── episodes/        # Generated MP3 files
│   ├── feed.xml        # RSS feed for podcast distribution
│   └── index.html      # Web interface
└── .github/workflows/   # Automated generation (optional)
```

## ⚙️ Configuration

The system works out-of-the-box but can be customized:

- **News Sources**: Modify RSS feeds in `src/news_collector.py`
- **Voice Settings**: Adjust accents, speed, and pauses in `src/podcast_creator.py`
- **AI Prompts**: Customize host personalities and dialogue style in `src/script_generator.py`
- **Output Format**: Change audio quality, format, and file naming in `main.py`

## 📊 Technical Details

- **Language**: Python 3.8+
- **Audio Format**: MP3 (128kbps)
- **TTS Engines**: gTTS (primary), pyttsx3 (fallback)
- **Error Handling**: Retry logic with exponential backoff
- **Dependencies**: See `requirements.txt` for full list

## 🔧 Troubleshooting

- **TTS Timeouts**: The system automatically retries failed segments with different engines
- **Network Issues**: Built-in fallback from Google TTS to local Windows SAPI
- **Unicode Errors**: Fixed with UTF-8 encoding for cross-platform compatibility

## 📈 Output

Generated content includes:
- **MP3 Episodes**: `docs/episodes/oil_news_YYYYMMDD.mp3`
- **RSS Feed**: `docs/feed.xml` for podcast aggregators
- **Web Interface**: `docs/index.html` for browser listening

Perfect for automated podcast generation, content creation, or learning about AI-powered media workflows!