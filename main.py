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
    
    print("Starting Oil Field Insights podcast generation...")
    
    # 1. Collect and filter news
    print("Collecting news...")
    collector = SmartNewsCollector()
    articles = collector.fetch_and_filter_news()
    market_data = collector.get_market_data()
    
    if not articles:
        print("No relevant news found today")
        return
    
    print(f"Found {len(articles)} relevant articles")
    
    # 2. Generate dialogue script
    print("Generating script...")
    generator = DialogueScriptGenerator()
    dialogue_script = generator.generate_dialogue_script(articles, market_data)
    
    # 3. Create multi-voice podcast
    print("Creating podcast...")
    creator = MultiVoicePodcastCreator()
    
    # Ensure directories exist
    os.makedirs('docs/episodes', exist_ok=True)
    
    date_str = datetime.now().strftime('%Y%m%d')
    output_file = f'docs/episodes/oil_news_{date_str}.mp3'
    
    await creator.create_podcast(dialogue_script, output_file)
    
    # 4. Update RSS feed
    print("Updating RSS feed...")
    rss_gen = PodcastRSSGenerator()
    rss_gen.generate_rss_feed()
    
    # 5. Generate HTML index
    generate_html_index()
    
    print(f"Podcast generated successfully: {output_file}")

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
        </style>
    </head>
    <body>
        <h1>🛢️ Oil Field Insights Daily</h1>
        <p>Your AI-generated daily podcast covering the latest in oil and gas industry news.</p>
        
        <div class="subscribe-section">
            <h2>Subscribe to Podcast</h2>
            <p>Copy this RSS feed URL to your podcast app:</p>
            <input type="text" value="https://YOUR-USERNAME.github.io/oil-podcast-generator/feed.xml" readonly style="width: 100%; padding: 10px;">
            
            <h3>Direct Links:</h3>
            <a href="https://podcasts.apple.com/feed?url=https://YOUR-USERNAME.github.io/oil-podcast-generator/feed.xml">
                <button>Apple Podcasts</button>
            </a>
            <a href="https://www.google.com/podcasts?feed=aHR0cHM6Ly9ZT1VSLVVTRVJOQU1FLmdpdGh1Yi5pby9vaWwtcG9kY2FzdC1nZW5lcmF0b3IvZmVlZC54bWw=">
                <button>Google Podcasts</button>
            </a>
            <a href="https://open.spotify.com/show/submit?feed=https://YOUR-USERNAME.github.io/oil-podcast-generator/feed.xml">
                <button>Submit to Spotify</button>
            </a>
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
                                        <source src="${url.replace('https://YOUR-USERNAME.github.io/oil-podcast-generator/', '')}" type="audio/mpeg">
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
        f.write(html_content.replace('YOUR-USERNAME', os.environ.get('GITHUB_REPOSITORY_OWNER', 'YOUR-USERNAME')))

if __name__ == "__main__":
    asyncio.run(generate_daily_podcast())