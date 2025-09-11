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
            # Verified working sources
            "https://www.rigzone.com/news/rss/rigzone_latest.aspx",  # Rigzone - WORKING
            "https://www.oilprice.com/rss/main",  # Oil Price - WORKING
            "https://www.worldoil.com/rss",  # World Oil
            "https://www.oilandgas360.com/feed/",  # Oil and Gas 360
            
            # Major financial/energy sources
            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=XOM,CVX,COP,EOG,SLB&region=US&lang=en-US",  # Yahoo Finance Energy
            "https://feeds.bloomberg.com/energy.rss",  # Bloomberg Energy
            "https://www.marketwatch.com/rss/energy",  # MarketWatch Energy
            
            # Government and industry sources
            "https://www.eia.gov/rss/press_releases.xml",  # US Energy Information Admin
            "https://www.api.org/news-policy-and-issues/news/feed.xml",  # American Petroleum Institute
            
            # Alternative verified energy sources
            "https://oilchange.org/feed/",  # Oil Change International
            "https://energynow.com/feed/",  # Energy Now
            "https://www.naturalgasintel.com/feed/",  # Natural Gas Intelligence
            "https://www.energypost.eu/feed/",  # Energy Post
            "https://www.jwnenergy.com/feed/",  # JWN Energy
            
            # Regional energy sources
            "https://www.spglobal.com/platts/en/rss-feed/oil",  # S&P Global Platts
            "https://www.argusmedia.com/en/news/energy-feed",  # Argus Media
            
            # Backup sources (may not all work, but worth trying)
            "https://feeds.reuters.com/reuters/businessNews",  # Reuters Business
            "https://www.cnbc.com/id/10000698/device/rss/rss.html",  # CNBC Oil
            "https://rss.cnn.com/rss/money_news_energy.rss",  # CNN Energy
        ]
        
        # Weighted keywords for relevance scoring
        self.keywords = {
            'critical': {
                'words': ['drilling', 'extraction', 'production', 'discovery', 'oil rig', 
                         'fracking', 'offshore', 'onshore', 'barrel', 'completion', 
                         'horizontal drilling', 'subsea', 'unconventional', 'tight oil'],
                'weight': 3
            },
            'important': {
                'words': ['OPEC', 'crude', 'pipeline', 'refinery', 'exploration', 'reserves', 
                         'shale', 'deepwater', 'upstream', 'downstream', 'midstream', 'LNG',
                         'natural gas', 'gas processing', 'Permian', 'Bakken', 'Eagle Ford',
                         'wellhead', 'flowback', 'hydraulic fracturing'],
                'weight': 2
            },
            'relevant': {
                'words': ['energy', 'petroleum', 'fossil', 'oil price', 'oil market', 
                         'oil company', 'drilling technology', 'oil field', 'E&P', 
                         'exploration production', 'oilfield services', 'rig count',
                         'drilling permits', 'oil inventory', 'crude stocks', 'API',
                         'WTI', 'Brent', 'energy sector', 'petrochemical'],
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
    
    def format_time_ago(self, hours):
        """Format hours into human-readable time ago string"""
        if hours < 1:
            return "Just now"
        elif hours < 2:
            return "1 hour ago"
        elif hours < 24:
            return f"{int(hours)} hours ago"
        elif hours < 48:
            return "Yesterday"
        else:
            days = int(hours / 24)
            return f"{days} days ago"
    
    def fetch_and_filter_news(self):
        """Collect and intelligently filter news"""
        all_articles = []
        seen_titles = set()
        
        for feed_url in self.feeds:
            try:
                # Add timeout and user agent to avoid being blocked
                import socket
                socket.setdefaulttimeout(10)  # 10 second timeout
                
                # Set user agent to avoid blocking
                feedparser.USER_AGENT = "Oil Podcast Generator/1.0 (+https://github.com/shariqbaig/oil-podcast-generator)"
                
                print(f"Fetching from: {feed_url}")
                feed = feedparser.parse(feed_url)
                
                if not feed.entries:
                    print(f"  No entries found")
                    continue
                    
                print(f"  Found {len(feed.entries)} entries")
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
                        pub_datetime = None
                        
                        if pub_date:
                            try:
                                pub_datetime = datetime.fromtimestamp(
                                    datetime(*pub_date[:6]).timestamp()
                                )
                            except:
                                pub_datetime = None
                        
                        # If no parsed date, try to parse from published string
                        if not pub_datetime and hasattr(entry, 'published'):
                            try:
                                from dateutil import parser
                                pub_datetime = parser.parse(entry.published)
                            except:
                                pub_datetime = None
                        
                        # Calculate article age
                        if pub_datetime:
                            hours_old = (datetime.now() - pub_datetime).total_seconds() / 3600
                            
                            # ONLY include articles from last 48 hours (2 days)
                            if hours_old > 48:
                                continue  # Skip old articles
                            
                            # Boost recent articles
                            if hours_old < 6:  # Less than 6 hours old
                                score += 10
                            elif hours_old < 12:  # Less than 12 hours old
                                score += 7
                            elif hours_old < 24:  # Less than 24 hours old
                                score += 5
                            elif hours_old < 48:  # Less than 48 hours old
                                score += 2
                            
                            time_ago = self.format_time_ago(hours_old)
                        else:
                            time_ago = "Recently"
                        
                        all_articles.append({
                            'title': entry.title,
                            'summary': entry.get('summary', '')[:500],
                            'link': entry.link,
                            'source': feed.feed.title if hasattr(feed, 'feed') else 'Unknown',
                            'score': score,
                            'published': pub_datetime if pub_datetime else datetime.now(),
                            'time_ago': time_ago if pub_datetime else "Recently"
                        })
            except Exception as e:
                print(f"Error processing feed {feed_url}: {e}")
        
        # Sort by score and return top articles
        all_articles.sort(key=lambda x: x['score'], reverse=True)
        
        # Ensure diversity - no more than 2 from same source, get more articles
        final_articles = []
        source_count = {}
        for article in all_articles:
            source = article['source']
            if source_count.get(source, 0) < 2:
                final_articles.append(article)
                source_count[source] = source_count.get(source, 0) + 1
                if len(final_articles) >= 10:  # Increased from 7 to 10 for more content
                    break
        
        return final_articles

    def get_market_data(self):
        """Fetch current oil prices from Alpha Vantage"""
        import os
        import requests
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        
        if not api_key:
            print("[WARNING] ALPHA_VANTAGE_API_KEY not found in environment")
            return None
        
        try:
            # Fetch WTI Crude (CL=F) and Brent Crude (BZ=F) data
            # Alpha Vantage uses WTI and BRENT as commodity symbols
            wti_url = f"https://www.alphavantage.co/query?function=WTI&interval=daily&apikey={api_key}"
            brent_url = f"https://www.alphavantage.co/query?function=BRENT&interval=daily&apikey={api_key}"
            
            print("[INFO] Fetching WTI Crude data from Alpha Vantage...")
            wti_response = requests.get(wti_url, timeout=10)
            wti_data = wti_response.json()
            
            print("[INFO] Fetching Brent Crude data from Alpha Vantage...")
            brent_response = requests.get(brent_url, timeout=10)
            brent_data = brent_response.json()
            
            # Debug: Print raw response
            print(f"[DEBUG] WTI Response: {wti_data}")
            print(f"[DEBUG] Brent Response: {brent_data}")
            
            # Check for API errors
            if 'Error Message' in wti_data or 'Error Message' in brent_data:
                print("[ERROR] Alpha Vantage API error - check your API key")
                return None
            
            if 'Note' in wti_data or 'Note' in brent_data:
                print("[WARNING] Alpha Vantage API rate limit reached (5 calls/minute for free tier)")
                return None
            
            # Extract latest prices
            if 'data' in wti_data and len(wti_data['data']) > 0:
                wti_latest = float(wti_data['data'][0]['value'])
                wti_previous = float(wti_data['data'][1]['value']) if len(wti_data['data']) > 1 else wti_latest
                wti_change = ((wti_latest - wti_previous) / wti_previous) * 100
                wti_change_str = f"{'+' if wti_change >= 0 else ''}{wti_change:.2f}%"
            else:
                print("[WARNING] No WTI data available")
                return None
            
            if 'data' in brent_data and len(brent_data['data']) > 0:
                brent_latest = float(brent_data['data'][0]['value'])
                brent_previous = float(brent_data['data'][1]['value']) if len(brent_data['data']) > 1 else brent_latest
                brent_change = ((brent_latest - brent_previous) / brent_previous) * 100
                brent_change_str = f"{'+' if brent_change >= 0 else ''}{brent_change:.2f}%"
            else:
                print("[WARNING] No Brent data available")
                return None
            
            market_data = {
                'wti_crude': wti_latest,
                'brent_crude': brent_latest,
                'change_wti': wti_change_str,
                'change_brent': brent_change_str
            }
            
            print(f"[SUCCESS] Market Data Retrieved:")
            print(f"  WTI Crude: ${wti_latest:.2f} ({wti_change_str})")
            print(f"  Brent Crude: ${brent_latest:.2f} ({brent_change_str})")
            
            return market_data
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to fetch market data: {e}")
            return None
        except (KeyError, ValueError, IndexError) as e:
            print(f"[ERROR] Failed to parse market data: {e}")
            return None
        except Exception as e:
            print(f"[ERROR] Unexpected error fetching market data: {e}")
            return None