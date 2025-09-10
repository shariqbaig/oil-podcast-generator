# 🛢️ Oil Field Insights Daily - AI Podcast Generator

An intelligent podcast generation system that creates daily, soothing conversations about the oil and gas industry using advanced AI and neural text-to-speech technology.

## 🎧 Listen Now

**Latest Episode**: [Oil News Podcast](https://shariqbaig.github.io/oil-podcast-generator/)  
**RSS Feed**: [Subscribe in your podcast app](https://shariqbaig.github.io/oil-podcast-generator/feed.xml)

Experience AI-generated discussions between two hosts with natural conversation flow, industry insights, and market analysis.

## ✨ Key Features

### 🤖 AI-Powered Intelligence
- **Google Gemini AI Integration**: Creates dynamic, NotebookLM-style dialogue scripts
- **Smart News Filtering**: Relevance scoring system prioritizes drilling, extraction, and production news
- **Market Data Integration**: Includes real-time WTI/Brent crude prices in discussions
- **Natural Conversation Flow**: Context-aware dialogue with emotional variations

### 🎙️ Advanced Audio Production
- **Microsoft Edge TTS Neural Voices**: High-quality, soothing voices optimized for relaxed listening
  - Male host: GuyNeural (warm, friendly tone)
  - Female host: AriaNeural (gentle, conversational style)
- **Smart URL Processing**: Converts URLs to speakable domain names
- **Industry Term Pronunciation**: Proper handling of oil & gas terminology (OPEC, WTI, LNG, etc.)
- **Dynamic Pacing**: Adjustable speech rates and natural pauses for comfortable listening

### 📰 Comprehensive News Coverage
- **20+ RSS Feed Sources**: Including Rigzone, OilPrice.com, Bloomberg Energy, EIA
- **Intelligent Article Ranking**: Weighted keyword system for relevance
- **Multi-Source Aggregation**: Government, industry, financial, and regional sources
- **Daily Updates**: Automated GitHub Actions workflow at 12:00 PM UTC

### 🚀 Production Pipeline
- **Fully Automated**: End-to-end generation from news collection to audio publishing
- **Robust Error Handling**: Retry logic with exponential backoff for network issues
- **Audio Optimization**: FFmpeg processing for streaming-ready MP3s (192kbps)
- **Episode Management**: Automatic cleanup keeps last 30 episodes

## 📦 Installation

### Prerequisites
- Python 3.8+
- FFmpeg (for audio processing)
- Google Gemini API key (optional, for AI script generation)

### Quick Setup

1. **Clone the repository**:
```bash
git clone https://github.com/shariqbaig/oil-podcast-generator.git
cd oil-podcast-generator
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment** (optional for AI features):
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

4. **Generate your first podcast**:
```bash
python main.py
```

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Google AI API key for enhanced script generation (get one [here](https://makersuite.google.com/app/apikey))

### Voice Customization
Edit `src/podcast_creator.py` to adjust:
- Voice selection (Edge TTS offers 100+ voices)
- Speaking rate and pitch
- Pause durations
- Emotional tone mappings

### News Sources
Modify `src/news_collector.py` to:
- Add/remove RSS feeds
- Adjust keyword weights
- Change relevance thresholds
- Focus on specific topics

### Script Style
Configure `src/script_generator.py` for:
- Host personalities
- Conversation length
- Topic emphasis
- Dialogue patterns

## 📁 Project Structure

```
oil-podcast-generator/
├── main.py                      # Main orchestration script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
├── src/
│   ├── news_collector.py       # RSS feed aggregation and filtering
│   ├── script_generator.py     # AI dialogue generation (Gemini)
│   ├── podcast_creator.py      # Edge TTS audio synthesis
│   └── rss_generator.py        # Podcast RSS feed creation
├── docs/
│   ├── episodes/               # Generated MP3 files
│   ├── feed.xml               # Podcast RSS feed
│   └── index.html             # Web player interface
├── tests/
│   └── test_tts.py            # TTS testing utilities
└── .github/
    └── workflows/
        └── generate_podcast.yml # Daily automation (GitHub Actions)
```

## 🔄 Automated Daily Generation

The podcast generates automatically via GitHub Actions:
- **Schedule**: Daily at 12:00 PM UTC
- **Process**: News collection → AI script → Audio synthesis → Publishing
- **Requirements**: Add `GEMINI_API_KEY` to GitHub Secrets

### Manual Trigger
Run the workflow manually from GitHub Actions tab or via API:
```bash
gh workflow run generate_podcast.yml
```

## 🎯 Recent Improvements

### v2.1 (Latest)
- ✅ Extended episodes to 15 minutes with deeper discussions
- ✅ Added natural laughs, reactions, and conversational elements
- ✅ Implemented 8 new emotion states (amused, surprised, skeptical)
- ✅ Enhanced Gemini prompts for more engaging dialogue
- ✅ Fixed ffmpeg workflow issues

### v2.0
- ✅ Migrated from OpenAI to Google Gemini AI
- ✅ Switched to Edge TTS for superior voice quality
- ✅ Added soothing voice profiles for relaxed listening
- ✅ Implemented smart URL cleaning (no more "HTTP slash slash")
- ✅ Enhanced industry term pronunciation
- ✅ Improved pause timing for natural conversation
- ✅ Added robust retry logic for API resilience

### v1.0
- Initial release with basic TTS
- RSS feed aggregation
- Simple script templates

## 📊 Technical Specifications

- **Audio Format**: MP3, 192kbps, 44.1kHz
- **Episode Length**: 10-15 minutes (extended conversations with laughs and reactions)
- **Voice Technology**: Microsoft Edge TTS Neural Voices
- **AI Model**: Google Gemini 1.5 Flash
- **Update Frequency**: Daily
- **Storage**: Last 30 episodes retained

## 🐛 Troubleshooting

### Common Issues

**No audio generated**:
- Check network connection
- Verify Edge TTS is installed: `pip install edge-tts==7.2.3`
- Ensure FFmpeg is available

**Script generation fails**:
- Verify GEMINI_API_KEY is set correctly
- Falls back to template mode if AI unavailable

**Poor audio quality**:
- Adjust voice settings in `podcast_creator.py`
- Check FFmpeg installation

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional news sources
- Voice variety options
- Language support
- Interactive features

## 📜 License

MIT License - See [LICENSE](LICENSE) file

## 🔗 Links

- **Live Podcast**: [https://shariqbaig.github.io/oil-podcast-generator/](https://shariqbaig.github.io/oil-podcast-generator/)
- **RSS Feed**: [Subscribe](https://shariqbaig.github.io/oil-podcast-generator/feed.xml)
- **GitHub**: [Source Code](https://github.com/shariqbaig/oil-podcast-generator)

---

*Powered by Google Gemini AI and Microsoft Edge TTS Neural Voices*