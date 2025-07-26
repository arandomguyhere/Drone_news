#!/usr/bin/env python3
"""
Drone Intelligence Collection System
GitHub Pages & Actions Compatible Version
"""

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup as Soup
import pandas as pd
import os
import time
from datetime import datetime, timedelta
import json
import random
import logging

# Setup logging for GitHub Actions
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create directories
os.makedirs("data", exist_ok=True)
os.makedirs("docs", exist_ok=True)

def parse_date(date_string):
    """Parse relative date strings to datetime objects"""
    if not date_string:
        return datetime.now()
    
    try:
        if ' ago' in date_string.lower():
            parts = date_string.split()
            if len(parts) >= 3:
                quantity = int(parts[0])
                if 'minute' in date_string.lower():
                    return datetime.now() - timedelta(minutes=quantity)
                elif 'hour' in date_string.lower():
                    return datetime.now() - timedelta(hours=quantity)
                elif 'day' in date_string.lower():
                    return datetime.now() - timedelta(days=quantity)
        elif 'yesterday' in date_string.lower():
            return datetime.now() - timedelta(days=1)
    except:
        pass
    
    return datetime.now()

def process_image_url(img_src):
    """Process and normalize image URLs"""
    if not img_src or img_src.startswith('data:'):
        return None
    
    if img_src.startswith('//'):
        return 'https:' + img_src
    elif img_src.startswith('/'):
        return 'https://news.google.com' + img_src
    elif img_src.startswith('http'):
        return img_src
    else:
        return 'https://news.google.com/' + img_src.lstrip('/')

class DroneIntelligenceScraper:
    """GitHub Actions compatible drone intelligence scraper"""
    
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.results = []
    
    def get_search_queries(self, priority_mode=False):
        """Get search queries optimized for GitHub Actions"""
        
        if priority_mode:
            return [
                ("drone when:24h", "🚁 Drones"),
                ("UAV when:24h", "🛩️ UAV"),
                ("military drone when:24h", "🎯 Military Drones"),
                ("China drone when:24h", "🇨🇳 China Drones"),
                ("Russia drone when:24h", "🇷🇺 Russia Drones"),
                ("autonomous drone when:24h", "🤖 Autonomous Drones"),
                ("drone warfare when:24h", "⚔️ Drone Warfare"),
                ("site:janes.com drone when:24h", "📰 Jane's Defence"),
                ("site:defensenews.com drone when:24h", "📰 Defense News"),
                ("site:reuters.com drone when:24h", "📺 Reuters"),
                ("Iran drone when:24h", "🇮🇷 Iran Drones"),
                ("drone strike when:24h", "💥 Drone Strikes"),
                ("anti-drone when:24h", "🛡️ Counter-Drone"),
                ("drone swarm when:24h", "🐝 Drone Swarms"),
                ("combat drone when:24h", "⚔️ Combat Systems")
            ]
        
        # Comprehensive search queries for GitHub Actions
        return [
            # Core drone searches
            ("drone when:24h", "🚁 Drones"),
            ("UAV when:24h", "🛩️ UAV"),
            ("UAS when:24h", "🛩️ UAS"),
            ("quadcopter when:24h", "🚁 Quadcopters"),
            ("unmanned aircraft when:24h", "🛩️ Unmanned Aircraft"),
            
            # Military and defense intelligence
            ("military drone when:24h", "🎯 Military Drones"),
            ("drone warfare when:24h", "⚔️ Drone Warfare"),
            ("drone strike when:24h", "💥 Drone Strikes"),
            ("combat drone when:24h", "⚔️ Combat Systems"),
            ("tactical UAV when:24h", "🎯 Tactical UAV"),
            ("reconnaissance drone when:24h", "👁️ ISR Drones"),
            ("armed drone when:24h", "🔫 Armed Systems"),
            ("loitering munition when:24h", "💣 Loitering Munitions"),
            ("kamikaze drone when:24h", "💥 Kamikaze Drones"),
            ("suicide drone when:24h", "💥 Suicide Drones"),
            
            # Autonomous and AI systems
            ("autonomous drone when:24h", "🤖 Autonomous Drones"),
            ("AI drone when:24h", "🧠 AI-Controlled"),
            ("drone swarm when:24h", "🐝 Drone Swarms"),
            ("swarming drone when:24h", "🐝 Swarm Technology"),
            ("machine learning drone when:24h", "🧠 ML Drones"),
            
            # Geopolitical intelligence (high priority)
            ("China drone when:24h", "🇨🇳 China Drones"),
            ("Chinese UAV when:24h", "🇨🇳 Chinese Systems"),
            ("Russia drone when:24h", "🇷🇺 Russia Drones"),
            ("Russian UAV when:24h", "🇷🇺 Russian Systems"),
            ("Iran drone when:24h", "🇮🇷 Iran Drones"),
            ("Iranian UAV when:24h", "🇮🇷 Iranian Systems"),
            ("North Korea drone when:24h", "🇰🇵 DPRK Drones"),
            ("DPRK UAV when:24h", "🇰🇵 DPRK Systems"),
            ("Israel drone when:24h", "🇮🇱 Israel Drones"),
            ("Turkey drone when:24h", "🇹🇷 Turkey Drones"),
            ("Ukraine drone when:24h", "🇺🇦 Ukraine Drones"),
            ("USA drone when:24h", "🇺🇸 US Drones"),
            
            # Counter-drone and defense
            ("anti-drone when:24h", "🛡️ Counter-Drone"),
            ("counter-UAS when:24h", "🛡️ Counter-UAS"),
            ("drone defense when:24h", "🛡️ Drone Defense"),
            ("C-UAS when:24h", "🛡️ C-UAS Systems"),
            ("drone jammer when:24h", "📡 Electronic Warfare"),
            
            # Technical categories
            ("FPV drone when:24h", "🎮 FPV Systems"),
            ("VTOL UAV when:24h", "🚁 VTOL Systems"),
            ("fixed wing drone when:24h", "✈️ Fixed Wing"),
            ("solar drone when:24h", "☀️ Solar UAV"),
            ("stealth drone when:24h", "👻 Stealth Technology"),
            
            # Commercial and civilian
            ("commercial drone when:24h", "📦 Commercial Drones"),
            ("drone delivery when:24h", "📦 Delivery Services"),
            ("agricultural drone when:24h", "🚜 Agricultural"),
            ("inspection drone when:24h", "🔍 Inspection"),
            ("rescue drone when:24h", "🚑 Search & Rescue"),
            
            # Regulatory and policy
            ("FAA drone when:24h", "📋 FAA Regulation"),
            ("drone regulation when:24h", "📋 Drone Policy"),
            ("drone law when:24h", "⚖️ Drone Law"),
            ("airspace drone when:24h", "🛩️ Airspace Management"),
            
            # Technology and innovation
            ("drone cybersecurity when:24h", "🔒 Cybersecurity"),
            ("5G drone when:24h", "📡 5G Connectivity"),
            ("drone battery when:24h", "🔋 Power Systems"),
            ("satellite drone when:24h", "🛰️ Satellite Comms"),
            
            # Defense sources (high reliability)
            ("site:janes.com drone when:24h", "📰 Jane's Defence"),
            ("site:defensenews.com drone when:24h", "📰 Defense News"),
            ("site:thedrive.com drone when:24h", "📰 The Drive"),
            ("site:breakingdefense.com drone when:24h", "📰 Breaking Defense"),
            ("site:c4isrnet.com drone when:24h", "📰 C4ISRNET"),
            
            # Major news sources
            ("site:reuters.com drone when:24h", "📺 Reuters"),
            ("site:bloomberg.com drone when:24h", "📺 Bloomberg"),
            ("site:wsj.com drone when:24h", "📺 Wall Street Journal"),
            ("site:ft.com drone when:24h", "📺 Financial Times"),
            ("site:cnn.com drone when:24h", "📺 CNN"),
            ("site:bbc.com drone when:24h", "📺 BBC"),
            ("site:npr.org drone when:24h", "📺 NPR"),
            
            # Technology sources
            ("site:wired.com drone when:24h", "💻 Wired"),
            ("site:arstechnica.com drone when:24h", "💻 Ars Technica"),
            ("site:techcrunch.com drone when:24h", "💻 TechCrunch"),
            ("site:ieee.org drone when:24h", "🔬 IEEE"),
            ("site:aviationweek.com drone when:24h", "✈️ Aviation Week")
        ]
    
    def search_single_query(self, query, category, max_articles=8):
        """Search Google News for a single query - GitHub Actions optimized"""
        
        logger.info(f"Searching: {category}")
        
        encoded_query = urllib.parse.quote(query.encode('utf-8'))
        url = f'https://news.google.com/search?q={encoded_query}&hl=en'
        
        try:
            # GitHub Actions friendly delay
            time.sleep(random.uniform(2, 4))
            
            req = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(req, timeout=30)
            page = response.read()
            soup = Soup(page, "html.parser")
            
            articles = soup.select('article')
            valid_articles = []
            
            for article in articles[:max_articles * 2]:
                if len(valid_articles) >= max_articles:
                    break
                
                try:
                    # Extract title
                    title = None
                    links = article.find_all('a')
                    if links:
                        title = links[0].get_text(strip=True)
                    
                    if not title or len(title) < 15:
                        continue
                    
                    # Skip navigation items
                    nav_terms = ['home', 'for you', 'following', 'world', 'local', 'business', 'technology', 'entertainment', 'sports', 'science', 'health']
                    if title.lower().strip() in nav_terms:
                        continue
                    
                    # Extract link
                    link = url  # fallback
                    try:
                        link_elem = article.find('div').find("a")
                        if link_elem and link_elem.get("href"):
                            href = link_elem.get("href")
                            if href.startswith('./'):
                                link = 'https://news.google.com' + href[1:]
                            elif href.startswith('/'):
                                link = 'https://news.google.com' + href
                            else:
                                link = href
                    except:
                        pass
                    
                    # Extract date
                    date = "Recent"
                    try:
                        time_elem = article.find("time")
                        if time_elem:
                            date = time_elem.get_text(strip=True)
                    except:
                        pass
                    
                    # Extract source
                    source = category.split(' ', 1)[-1]  # Use category as fallback
                    try:
                        source_elem = article.find("time")
                        if source_elem and source_elem.parent:
                            source_link = source_elem.parent.find("a")
                            if source_link:
                                source_text = source_link.get_text(strip=True)
                                if source_text and len(source_text) <= 50:
                                    source = source_text
                    except:
                        pass
                    
                    # Extract image
                    img = None
                    try:
                        img_tag = article.find("img")
                        if img_tag and img_tag.get("src"):
                            img = process_image_url(img_tag.get("src"))
                    except:
                        pass
                    
                    valid_articles.append({
                        'title': title,
                        'link': link,
                        'source': source,
                        'published': date,
                        'category': category,
                        'image': img,
                        'scraped_at': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    logger.debug(f"Error processing article: {e}")
                    continue
            
            response.close()
            logger.info(f"✓ {category}: {len(valid_articles)} articles")
            return valid_articles
            
        except Exception as e:
            logger.error(f"✗ {category}: {e}")
            return []
    
    def collect_intelligence(self, priority_mode=False):
        """Main intelligence collection optimized for GitHub Actions"""
        
        print(f"🚁 DRONE INTELLIGENCE COLLECTION")
        print(f"Mode: {'PRIORITY' if priority_mode else 'COMPREHENSIVE'}")
        print(f"Optimized for: GitHub Actions & Pages")
        print("=" * 60)
        
        queries = self.get_search_queries(priority_mode)
        all_articles = []
        
        print(f"🔍 Executing {len(queries)} intelligence searches...")
        
        for i, (query, category) in enumerate(queries):
            articles = self.search_single_query(query, category)
            all_articles.extend(articles)
            
            # Progress update for GitHub Actions logs
            if (i + 1) % 10 == 0:
                print(f"📊 Progress: {i+1}/{len(queries)} searches completed ({len(all_articles)} articles collected)")
            
            # Respectful delay between searches
            if i < len(queries) - 1:
                time.sleep(random.uniform(1, 2))
        
        # Remove duplicates
        unique_articles = self.remove_duplicates(all_articles)
        
        print(f"✅ Intelligence collection complete!")
        print(f"📊 Raw articles: {len(all_articles)}")
        print(f"📊 Unique articles: {len(unique_articles)}")
        
        return unique_articles
    
    def remove_duplicates(self, articles):
        """Remove duplicate articles with GitHub Actions logging"""
        if not articles:
            return []
        
        unique_articles = []
        seen_titles = set()
        
        for article in articles:
            title = article['title'].lower().strip()
            
            # Advanced similarity check
            title_words = set(title.split())
            is_duplicate = False
            
            for seen_title in seen_titles:
                seen_words = set(seen_title.split())
                if len(title_words) > 0 and len(seen_words) > 0:
                    # Jaccard similarity
                    intersection = len(title_words.intersection(seen_words))
                    union = len(title_words.union(seen_words))
                    similarity = intersection / union if union > 0 else 0
                    
                    if similarity > 0.7:  # 70% similarity threshold
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                seen_titles.add(title)
                unique_articles.append(article)
        
        duplicates_removed = len(articles) - len(unique_articles)
        if duplicates_removed > 0:
            print(f"🔄 Removed {duplicates_removed} duplicate articles")
        
        return unique_articles

def save_intelligence_data(articles):
    """Save intelligence data with GitHub Pages compatibility"""
    if not articles:
        print("⚠️ No intelligence data to save")
        # Create empty files for GitHub Actions
        with open("data/latest_news.json", "w") as f:
            json.dump([], f)
        return None
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Format for GitHub Pages
    formatted_articles = []
    for article in articles:
        formatted_articles.append({
            "Title": article['title'],
            "Link": article['link'],
            "Source": article['source'],
            "Published": article['published'],
            "Category": article['category'],
            "Image": article['image'],
            "Scraped_At": article['scraped_at']
        })
    
    try:
        # Create DataFrame
        df = pd.DataFrame(formatted_articles)
        
        # Save timestamped backup
        backup_file = f"data/drone_intelligence_{timestamp}.csv"
        df.to_csv(backup_file, index=False)
        
        # Save latest files for GitHub Pages
        df.to_csv("data/latest_news.csv", index=False)
        
        # Save JSON for web consumption
        with open("data/latest_news.json", "w", encoding="utf-8") as f:
            json.dump(formatted_articles, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Intelligence data saved!")
        print(f"📁 Backup: {backup_file}")
        print(f"📁 Latest: data/latest_news.json")
        
        return backup_file
        
    except Exception as e:
        print(f"❌ Save failed: {e}")
        return None

def main():
    """Main function optimized for GitHub Actions"""
    import sys
    
    priority_mode = '--priority' in sys.argv or '--fast' in sys.argv
    
    print("🚁 DRONE INTELLIGENCE SYSTEM")
    print("🔗 GitHub Repository: https://github.com/yourusername/drone-intelligence-system")
    print("🌐 Live Brief: https://yourusername.github.io/drone-intelligence-system/")
    print("=" * 80)
    
    try:
        scraper = DroneIntelligenceScraper()
        start_time = time.time()
        
        articles = scraper.collect_intelligence(priority_mode)
        
        collection_time = time.time() - start_time
        
        if articles:
            save_intelligence_data(articles)
            
            # GitHub Actions summary
            print(f"\n📊 COLLECTION SUMMARY")
            print(f"⏱️  Collection time: {collection_time:.1f} seconds")
            print(f"📈 Articles per minute: {len(articles) / (collection_time / 60):.1f}")
            
            # Category breakdown for GitHub Actions logs
            categories = {}
            sources = {}
            for article in articles:
                cat = article['category']
                src = article['source']
                categories[cat] = categories.get(cat, 0) + 1
                sources[src] = sources.get(src, 0) + 1
            
            print(f"📂 Categories: {len(categories)}")
            print(f"📰 Sources: {len(sources)}")
            
            print(f"\n🏆 Top Categories:")
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  • {cat}: {count}")
            
            print(f"\n📺 Top Sources:")
            for src, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:8]:
                print(f"  • {src}: {count}")
                
            print(f"\n🎉 Intelligence collection successful!")
            print(f"🔗 Next: Generate newsletter with 'python generate_newsletter.py'")
            
        else:
            print("❌ No intelligence collected")
            print("🔍 Check network connectivity and search parameters")
    
    except Exception as e:
        print(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
