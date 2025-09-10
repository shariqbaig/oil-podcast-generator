# src/rss_generator.py
from datetime import datetime
import xml.etree.ElementTree as ET
import os
import hashlib

class PodcastRSSGenerator:
    def __init__(self, base_url="https://YOUR-USERNAME.github.io/oil-podcast-generator"):
        self.base_url = base_url
        self.podcast_info = {
            'title': 'Oil Field Insights Daily',
            'description': 'Your daily automated podcast for oil and gas industry news',
            'author': 'AI Podcast Generator',
            'email': 'podcast@example.com',
            'category': 'Business',
            'language': 'en-us',
            'image': f'{base_url}/podcast-cover.jpg'
        }
    
    def generate_rss_feed(self, episodes_dir='docs/episodes'):
        """Generate RSS feed for podcast distribution"""
        
        # Create root RSS element
        rss = ET.Element('rss', {
            'version': '2.0',
            'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
            'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
        })
        
        channel = ET.SubElement(rss, 'channel')
        
        # Add channel metadata
        ET.SubElement(channel, 'title').text = self.podcast_info['title']
        ET.SubElement(channel, 'description').text = self.podcast_info['description']
        ET.SubElement(channel, 'link').text = self.base_url
        ET.SubElement(channel, 'language').text = self.podcast_info['language']
        ET.SubElement(channel, 'copyright').text = f'© {datetime.now().year}'
        ET.SubElement(channel, 'itunes:author').text = self.podcast_info['author']
        ET.SubElement(channel, 'itunes:summary').text = self.podcast_info['description']
        ET.SubElement(channel, 'itunes:owner')
        ET.SubElement(channel, 'itunes:explicit').text = 'no'
        ET.SubElement(channel, 'itunes:category', {'text': self.podcast_info['category']})
        
        # Add image
        image = ET.SubElement(channel, 'itunes:image', {'href': self.podcast_info['image']})
        
        # Add episodes
        episodes = self._get_episodes(episodes_dir)
        for episode in episodes:
            self._add_episode_to_feed(channel, episode)
        
        # Save RSS feed
        tree = ET.ElementTree(rss)
        tree.write('docs/feed.xml', encoding='utf-8', xml_declaration=True)
        
        return 'docs/feed.xml'
    
    def _get_episodes(self, episodes_dir):
        """Get all episodes from directory"""
        episodes = []
        
        if os.path.exists(episodes_dir):
            for filename in sorted(os.listdir(episodes_dir), reverse=True):
                if filename.endswith('.mp3'):
                    filepath = os.path.join(episodes_dir, filename)
                    file_stats = os.stat(filepath)
                    
                    # Parse date from filename (oil_news_YYYYMMDD.mp3)
                    date_str = filename.replace('oil_news_', '').replace('.mp3', '')
                    try:
                        date = datetime.strptime(date_str, '%Y%m%d')
                    except:
                        date = datetime.now()
                    
                    episodes.append({
                        'title': f"Oil Field Insights - {date.strftime('%B %d, %Y')}",
                        'description': f"Daily oil and gas industry news for {date.strftime('%B %d, %Y')}",
                        'file': filename,
                        'date': date,
                        'size': file_stats.st_size,
                        'duration': '10:00'  # You can calculate actual duration
                    })
        
        return episodes[:50]  # Keep last 50 episodes
    
    def _add_episode_to_feed(self, channel, episode):
        """Add episode to RSS feed"""
        item = ET.SubElement(channel, 'item')
        
        ET.SubElement(item, 'title').text = episode['title']
        ET.SubElement(item, 'description').text = episode['description']
        
        # Generate unique GUID
        guid = hashlib.md5(episode['file'].encode()).hexdigest()
        ET.SubElement(item, 'guid').text = guid
        
        # Publication date
        pub_date = episode['date'].strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(item, 'pubDate').text = pub_date
        
        # Enclosure (the actual MP3 file)
        url = f"{self.base_url}/episodes/{episode['file']}"
        ET.SubElement(item, 'enclosure', {
            'url': url,
            'type': 'audio/mpeg',
            'length': str(episode['size'])
        })
        
        # iTunes specific tags
        ET.SubElement(item, 'itunes:duration').text = episode['duration']
        ET.SubElement(item, 'itunes:explicit').text = 'no'