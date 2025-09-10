# main.py
import asyncio
import os
from datetime import datetime
from src.news_collector import SmartNewsCollector
from src.script_generator import DialogueScriptGenerator
from src.podcast_creator import MultiVoicePodcastCreator
from src.rss_generator import PodcastRSSGenerator

async def generate_daily_podcast():
    """Main function to generate daily podcast"""
    
    print("=" * 60)
    print("Oil Field Insights - AI Podcast Generator")
    print("=" * 60)
    
    # Check for AI capabilities
    if os.getenv('GEMINI_API_KEY'):
        print("[OK] Gemini AI enabled for enhanced script generation")
    else:
        print("[INFO] Using template-based script generation (set GEMINI_API_KEY for AI)")
    
    # 1. Collect and filter news
    print("\n[STEP 1] Collecting news...")
    collector = SmartNewsCollector()
    articles = collector.fetch_and_filter_news()
    market_data = collector.get_market_data()
    
    if not articles:
        print("[ERROR] No relevant news found today")
        return
    
    print(f"[OK] Found {len(articles)} relevant articles")
    for i, article in enumerate(articles[:5], 1):
        print(f"   {i}. {article['title'][:60]}...")
    
    # 2. Generate dialogue script
    print("\n[STEP 2] Generating script...")
    generator = DialogueScriptGenerator()
    dialogue_script = generator.generate_dialogue_script(articles, market_data)
    print(f"[OK] Generated {len(dialogue_script)} dialogue segments")
    
    # 3. Create multi-voice podcast
    print("\n[STEP 3] Creating podcast with Edge TTS...")
    creator = MultiVoicePodcastCreator()
    
    # Ensure directories exist
    os.makedirs('docs/episodes', exist_ok=True)
    
    date_str = datetime.now().strftime('%Y%m%d')
    output_file = f'docs/episodes/oil_news_{date_str}.mp3'
    
    await creator.create_podcast(dialogue_script, output_file)
    
    # 4. Update RSS feed
    print("\n[STEP 4] Updating RSS feed...")
    rss_gen = PodcastRSSGenerator()
    rss_gen.generate_rss_feed()
    print("[OK] RSS feed updated")
    
    # 5. Generate HTML index
    print("\n[STEP 5] Updating HTML index...")
    generate_html_index()
    print("[OK] HTML index updated")
    
    print("\n" + "=" * 60)
    print(f"[SUCCESS] PODCAST GENERATED SUCCESSFULLY!")
    print(f"[FILE] {output_file}")
    print("=" * 60)

def generate_html_index():
    """Generate simple HTML page for GitHub Pages"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Oil Field Insights Daily Podcast</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .subscribe-section { background: #f0f0f0; padding: 20px; border-radius: 10px; margin: 20px 0; }
            .episode { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            .ai-badge { background: #4CAF50; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px; }
        </style>
    </head>
    <body>
        <h1>🛢️ Oil Field Insights Daily</h1>
        <p>Your AI-generated daily podcast covering the latest in oil and gas industry news. 
        <span class="ai-badge">AI Powered</span></p>
        
        <div class="subscribe-section">
            <h2>Subscribe to Podcast</h2>
            <p>Copy the RSS feed URL (feed.xml) to your podcast app to subscribe.</p>
            <p>This podcast is available as an RSS feed that can be added to any podcast player.</p>
        </div>
        
        <h2>Recent Episodes</h2>
        <div id="episodes">
            <!-- Episodes will be listed here -->
        </div>
        
        <script>
            // Load recent episodes
            fetch('feed.xml')
                .then(response => response.text())
                .then(data => {
                    const parser = new DOMParser();
                    const xml = parser.parseFromString(data, 'text/xml');
                    const items = xml.querySelectorAll('item');
                    const episodesDiv = document.getElementById('episodes');
                    
                    items.forEach((item, index) => {
                        if (index < 10) {
                            const title = item.querySelector('title').textContent;
                            const url = item.querySelector('enclosure').getAttribute('url');
                            const date = item.querySelector('pubDate').textContent;
                            
                            episodesDiv.innerHTML += `
                                <div class="episode">
                                    <h3>${title}</h3>
                                    <p>${new Date(date).toLocaleDateString()}</p>
                                    <audio controls>
                                        <source src="${url}" type="audio/mpeg">
                                    </audio>
                                </div>
                            `;
                        }
                    });
                });
        </script>
    </body>
    </html>
    """
    
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    asyncio.run(generate_daily_podcast())