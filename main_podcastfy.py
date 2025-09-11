# main_podcastfy.py
import os
import asyncio
from datetime import datetime
from podcastfy.client import generate_podcast
from src.news_collector import SmartNewsCollector
from src.rss_generator import PodcastRSSGenerator
import yaml
import tempfile

async def generate_daily_podcast_with_podcastfy():
    """Generate podcast using Podcastfy with your news collector"""
    
    print("=" * 60)
    print("Oil Field Insights - Podcastfy Edition")
    print("=" * 60)
    
    # 1. Use YOUR news collector
    print("\n[STEP 1] Collecting oil industry news...")
    collector = SmartNewsCollector()
    articles = collector.fetch_and_filter_news()
    market_data = collector.get_market_data()
    
    if not articles:
        print("[ERROR] No relevant news found")
        return
    
    print(f"[OK] Found {len(articles)} relevant articles")
    
    # 2. Convert articles to text content
    # Only include market data if available
    if market_data:
        market_section = f"""
    Market Update for {datetime.now().strftime('%B %d, %Y')}:
    WTI Crude: ${market_data.get('wti_crude'):.2f} ({market_data.get('change_wti')})
    Brent Crude: ${market_data.get('brent_crude'):.2f} ({market_data.get('change_brent')})
    
    """
    else:
        market_section = ""
    
    combined_content = f"""
    Oil & Gas News for {datetime.now().strftime('%B %d, %Y')}:
    {market_section}
    Today's Top Stories:
    """
    
    for i, article in enumerate(articles[:12], 1):  # Increased from 8 to 12 articles
        time_info = article.get('time_ago', 'Recently')
        combined_content += f"""
        Story {i}: {article['title']} ({time_info})
        {article['summary']}
        Source: {article['source']}
        
        """
    
    # 3. Create Podcastfy configuration
    config = {
        "word_count": 8000,  # Increased from 3000 for ~15 minute podcast
        "conversation_style": ["engaging", "analytical", "friendly"],
        "podcast_name": "Oil Field Insights Daily",
        "podcast_tagline": "Your AI-powered oil industry briefing",
        "creativity": 0.85,
        
        "roles_person1": "Alex, a petroleum engineer with 20 years experience",
        "roles_person2": "Sam, an energy markets reporter",
        
        "custom_instructions": """
        Create a natural NotebookLM-style conversation about oil industry news.
        Include genuine reactions, natural interruptions, and industry-specific insights.
        Focus on drilling, OPEC, refineries, and market movements.
        """,
        
        "text_to_speech": {
            "model": "edge",
            "edge": {
                "default_voices": {
                    "question": "en-US-AriaNeural",
                    "answer": "en-US-GuyNeural"
                }
            }
        },
        
        "output_language": "English",
        "dialogue_structure": "two_person_dialogue",
        "max_num_chunks": 10,
        "min_chunk_size": 500
    }
    
    # 4. Generate podcast with Podcastfy
    print("\n[STEP 2] Generating podcast with Podcastfy...")
    
    try:
        # Generate using Podcastfy with text parameter
        # Note: Edge TTS has issues with podcastfy 0.4.1, but transcript generation works
        audio_file = generate_podcast(
            text=combined_content,  # Use text parameter directly
            conversation_config=config,
            tts_model="edge",  # Edge TTS (may fail due to version issues)
            llm_model_name="gemini-1.5-flash",  # FREE tier
            api_key_label="GEMINI_API_KEY"
        )
        
        # Move to your standard location
        date_str = datetime.now().strftime('%Y%m%d')
        output_file = f'docs/episodes/oil_news_{date_str}.mp3'
        
        # Ensure directory exists
        os.makedirs('docs/episodes', exist_ok=True)
        
        # Move or copy the file
        import shutil
        if os.path.exists(audio_file):
            # First move the file to its destination
            shutil.move(audio_file, output_file)
            print(f"[OK] Podcast generated: {output_file}")
            
            # Then add background music to the moved file
            print("\n[STEP 2.5] Adding background music...")
            try:
                from src.music_generator import add_background_music_to_file
                
                # Add music to the podcast in place
                add_background_music_to_file(output_file)
                print(f"[OK] Background music added to podcast")
            except Exception as music_error:
                print(f"[WARNING] Could not add background music: {music_error}")
                print("Podcast generated without music")
        else:
            print(f"[ERROR] Audio file not found: {audio_file}")
            
    except Exception as e:
        print(f"[ERROR] Podcastfy generation failed: {e}")
        print("Exiting due to podcast generation failure.")
        return
    
    # 6. Update RSS feed
    print("\n[STEP 3] Updating RSS feed...")
    rss_gen = PodcastRSSGenerator()
    rss_gen.generate_rss_feed()
    
    print("\n" + "=" * 60)
    print("[SUCCESS] PODCASTFY PODCAST GENERATED!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(generate_daily_podcast_with_podcastfy())