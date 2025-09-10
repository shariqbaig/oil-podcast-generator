# src/news_collector.py
import feedparser
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
import json

class SmartNewsCollector:
    def __init__(self):
        self.feeds = [
            "https://www.rigzone.com/news/rss/rigzone_latest.aspx",
            "https://www.worldoil.com/rss",
            "https://www.oilandgas360.com/feed/",
            "https://www.upstreamonline.com/rss",
            "https://www.oilprice.com/rss/main",
            "https://www.spglobal.com/commodityinsights/en/rss-feed/oil",
            "https://www.reuters.com/markets/commodities/rss"
        ]
        
        # Weighted keywords for relevance scoring
        self.keywords = {
            'critical': {
                'words': ['drilling', 'extraction', 'production', 'discovery', 
                         'oil rig', 'fracking', 'offshore', 'onshore', 'barrel'],
                'weight': 3
            },
            'important': {
                'words': ['OPEC', 'crude', 'pipeline', 'refinery', 'exploration',
                         'reserves', 'shale', 'deepwater', 'upstream'],
                'weight': 2
            },
            'relevant': {
                'words': ['energy', 'petroleum', 'fossil', 'oil price', 'oil market',
                         'oil company', 'drilling technology', 'oil field'],
                'weight': 1
            }
        }
        
        # Exclusion keywords
        self.exclude_keywords = ['renewable', 'solar', 'wind power', 'electric vehicle']
    
    def calculate_relevance_score(self, text):
        """Smart scoring based on keyword density and importance"""
        text_lower = text.lower()
        score = 0
        
        # Check exclusions
        for exclude in self.exclude_keywords:
            if exclude in text_lower:
                return -1
        
        # Calculate weighted score
        for category, data in self.keywords.items():
            for keyword in data['words']:
                occurrences = len(re.findall(r'\b' + keyword + r'\b', text_lower))
                score += occurrences * data['weight']
        
        # Boost for recent content (within 24 hours)
        return score
    
    def fetch_and_filter_news(self):
        """Collect and intelligently filter news"""
        all_articles = []
        seen_titles = set()
        
        for feed_url in self.feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:10]:  # Get more initially for better filtering
                    # De-duplicate by title
                    title_hash = entry.title.lower().strip()
                    if title_hash in seen_titles:
                        continue
                    seen_titles.add(title_hash)
                    
                    # Combine title and summary for scoring
                    full_text = f"{entry.title} {entry.get('summary', '')}"
                    score = self.calculate_relevance_score(full_text)
                    
                    if score > 0:
                        # Try to get publication date
                        pub_date = entry.get('published_parsed', None)
                        if pub_date:
                            pub_datetime = datetime.fromtimestamp(
                                datetime(*pub_date[:6]).timestamp()
                            )
                            # Boost recent articles
                            hours_old = (datetime.now() - pub_datetime).total_seconds() / 3600
                            if hours_old < 24:
                                score += 5
                            elif hours_old < 48:
                                score += 2
                        
                        all_articles.append({
                            'title': entry.title,
                            'summary': entry.get('summary', '')[:500],
                            'link': entry.link,
                            'source': feed.feed.title if hasattr(feed, 'feed') else 'Unknown',
                            'score': score,
                            'published': pub_datetime if pub_date else datetime.now()
                        })
            except Exception as e:
                print(f"Error processing feed {feed_url}: {e}")
        
        # Sort by score and return top articles
        all_articles.sort(key=lambda x: x['score'], reverse=True)
        
        # Ensure diversity - no more than 2 from same source
        final_articles = []
        source_count = {}
        for article in all_articles:
            source = article['source']
            if source_count.get(source, 0) < 2:
                final_articles.append(article)
                source_count[source] = source_count.get(source, 0) + 1
                if len(final_articles) >= 7:
                    break
        
        return final_articles

    def get_market_data(self):
        """Fetch current oil prices (using free API)"""
        try:
            # Using a free commodity API or scraping
            # For demo, returning mock data - replace with actual API
            return {
                'wti_crude': 75.50,
                'brent_crude': 79.30,
                'change_wti': '+1.2%',
                'change_brent': '+0.8%'
            }
        except:
            return None