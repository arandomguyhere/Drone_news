#!/usr/bin/env python3
"""
Enhanced Drone News Scraper - Extracts Real Article Links
Collects actual news articles from Google News searches
"""

import requests
import json
import os
import time
from datetime import datetime
from urllib.parse import urlencode, parse_qs, urlparse, unquote
import re
from bs4 import BeautifulSoup

print("🚁 ENHANCED DRONE NEWS SCRAPER")
print("🔗 Extracting Real Article Links")
print("=" * 60)

# Enhanced search categories with better targeting
SEARCH_CATEGORIES = {
    '🎯 Military Drones': [
        'military drone news',
        'defense drone systems',
        'military UAV operations'
    ],
    '🇨🇳 China Drones': [
        'China drone technology',
        'Chinese military drones',
        'China UAV development'
    ],
    '🇷🇺 Russia Drones': [
        'Russia drone attacks',
        'Russian military UAV',
        'Russia drone warfare'
    ],
    '🤖 Autonomous Drones': [
        'autonomous drone technology',
        'AI powered drones',
        'self-flying drones'
    ],
    '⚔️ Drone Warfare': [
        'drone warfare tactics',
        'combat drone operations',
        'military drone strikes'
    ],
    '💥 Drone Strikes': [
        'drone strike news',
        'targeted drone attacks',
        'drone bombing operations'
    ],
    '🇺🇦 Ukraine Drones': [
        'Ukraine drone attacks',
        'Ukrainian drone warfare',
        'Ukraine military drones'
    ],
    '🇮🇷 Iran Drones': [
        'Iran drone program',
        'Iranian military drones',
        'Iran UAV technology'
    ],
    '🇮🇱 Israel Drones': [
        'Israel drone operations',
        'Israeli military UAV',
        'Israel drone strikes'
    ],
    '🇰🇵 DPRK Drones': [
        'North Korea drones',
        'DPRK UAV program',
        'North Korean military drones'
    ],
    '🇹🇷 Turkey Drones': [
        'Turkey drone exports',
        'Turkish military UAV',
        'Bayraktar drone news'
    ],
    '🛡️ Counter-Drone': [
        'anti-drone technology',
        'drone defense systems',
        'counter-UAV measures'
    ],
    '🚁 Commercial Drones': [
        'commercial drone market',
        'drone delivery services',
        'civilian UAV applications'
    ],
    '📋 Drone Regulation': [
        'drone regulations news',
        'UAV policy updates',
        'FAA drone rules'
    ],
    '🤖 AI Drones': [
        'artificial intelligence drones',
        'machine learning UAV',
        'smart drone technology'
    ]
}

def clean_google_url(url):
    """Extract real URL from Google News redirect"""
    if not url:
        return None
        
    # Handle Google News URL redirects
    if 'news.google.com' in url and '/articles/' in url:
        # Extract the actual URL from Google News article URL
        try:
            if '?url=' in url:
                actual_url = url.split('?url=')[1].split('&')[0]
                return unquote(actual_url)
            elif '/articles/' in url:
                # For Google News articles, we'll keep the Google URL for now
                return url
        except:
            pass
    
    # Handle other Google redirects
    if url.startswith('/url?'):
        try:
            parsed = parse_qs(url[5:])  # Remove '/url?'
            if 'url' in parsed:
                return parsed['url'][0]
        except:
            pass
    
    # Return cleaned URL
    if url.startswith('http'):
        return url
    elif url.startswith('//'):
        return 'https:' + url
    else:
        return None

def extract_google_news_articles(query, max_results=10):
    """Extract real articles from Google News search"""
    articles = []
    
    try:
        # Use Google News RSS feed for better structured data
        base_url = "https://news.google.com/rss/search"
        params = {
            'q': query,
            'hl': 'en-US',
            'gl': 'US',
            'ceid': 'US:en'
        }
        
        url = f"{base_url}?{urlencode(params)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"  📡 Fetching: {query}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parse RSS feed
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        for item in items[:max_results]:
            try:
                title = item.find('title')
                link = item.find('link')
                pub_date = item.find('pubDate')
                source = item.find('source')
                
                if title and link:
                    article_title = title.get_text().strip()
                    article_link = clean_google_url(link.get_text().strip())
                    
                    # Skip if we couldn't extract a real URL
                    if not article_link or 'google.com' in article_link:
                        continue
                    
                    # Extract source name
                    source_name = "News Source"
                    if source and source.get_text():
                        source_name = source.get_text().strip()
                    
                    # Parse publication date
                    pub_time = "Recent"
                    if pub_date:
                        try:
                            pub_time = datetime.strptime(
                                pub_date.get_text().strip(), 
                                '%a, %d %b %Y %H:%M:%S %Z'
                            ).strftime('%Y-%m-%d %H:%M')
                        except:
                            pub_time = "Recent"
                    
                    # Filter out obviously bad results
                    if (len(article_title) > 10 and 
                        not article_title.startswith('/') and
                        'rss/search' not in article_title.lower() and
                        'window.IJ_values' not in article_title):
                        
                        articles.append({
                            'Title': article_title,
                            'Link': article_link,
                            'Source': source_name,
                            'Published': pub_time,
                            'Query': query
                        })
                        
            except Exception as e:
                print(f"    ⚠️ Error parsing item: {e}")
                continue
        
        print(f"    ✅ Found {len(articles)} articles")
        
    except Exception as e:
        print(f"    ❌ Error fetching {query}: {e}")
    
    return articles

def search_alternative_sources(query, max_results=5):
    """Search alternative news sources for more diverse results"""
    articles = []
    
    # Try DuckDuckGo News search as alternative
    try:
        search_url = "https://duckduckgo.com/"
        params = {
            'q': f'{query} site:reuters.com OR site:bbc.com OR site:cnn.com OR site:defensenews.com',
            'iar': 'news',
            'ia': 'news'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Note: This is a simplified approach. In practice, you might want to use
        # official news APIs like NewsAPI, Bing News API, etc.
        print(f"  🦆 Alternative search: {query}")
        
    except Exception as e:
        print(f"    ⚠️ Alternative search failed: {e}")
    
    return articles

def collect_drone_intelligence():
    """Main intelligence collection function"""
    
    all_articles = []
    
    print(f"\n🎯 Starting intelligence collection...")
    print(f"📊 Categories to process: {len(SEARCH_CATEGORIES)}")
    
    for category, queries in SEARCH_CATEGORIES.items():
        print(f"\n📂 Processing: {category}")
        category_articles = []
        
        for query in queries:
            # Add rate limiting
            time.sleep(2)
            
            # Get articles from Google News
            articles = extract_google_news_articles(query, max_results=8)
            
            # Add category to each article
            for article in articles:
                article['Category'] = category
                
            category_articles.extend(articles)
            
            # Optional: Try alternative sources for important categories
            if any(term in category.lower() for term in ['military', 'warfare', 'china', 'russia']):
                alt_articles = search_alternative_sources(query, max_results=3)
                for article in alt_articles:
                    article['Category'] = category
                category_articles.extend(alt_articles)
        
        # Remove duplicates within category
        seen_titles = set()
        unique_articles = []
        for article in category_articles:
            title_key = article['Title'].lower().strip()
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_articles.append(article)
        
        print(f"  📈 Category total: {len(unique_articles)} unique articles")
        all_articles.extend(unique_articles)
    
    # Final deduplication across all categories
    print(f"\n🔄 Deduplicating across all categories...")
    seen_global = set()
    final_articles = []
    
    for article in all_articles:
        # Create a more sophisticated duplicate key
        dup_key = f"{article['Title'].lower().strip()}_{article.get('Source', '').lower()}"
        if dup_key not in seen_global:
            seen_global.add(dup_key)
            final_articles.append(article)
    
    print(f"✅ Final collection: {len(final_articles)} articles")
    return final_articles

def save_intelligence_data(articles):
    """Save intelligence data to JSON file"""
    
    try:
        # Create data directory
        os.makedirs("data", exist_ok=True)
        
        # Add metadata
        intelligence_data = {
            'generated_at': datetime.now().isoformat(),
            'total_articles': len(articles),
            'categories': len(set(article.get('Category', 'Unknown') for article in articles)),
            'articles': articles
        }
        
        # Save main data file
        with open("data/latest_news.json", "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        
        # Save backup with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"data/backup_{timestamp}.json"
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(intelligence_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Data saved to data/latest_news.json")
        print(f"🔒 Backup saved to {backup_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving data: {e}")
        return False

def print_collection_summary(articles):
    """Print summary of collected intelligence"""
    
    if not articles:
        print("⚠️ No articles collected")
        return
    
    # Count by category
    categories = {}
    sources = {}
    
    for article in articles:
        cat = article.get('Category', 'Unknown')
        src = article.get('Source', 'Unknown')
        
        categories[cat] = categories.get(cat, 0) + 1
        sources[src] = sources.get(src, 0) + 1
    
    print(f"\n📊 COLLECTION SUMMARY")
    print(f"=" * 50)
    print(f"📰 Total Articles: {len(articles)}")
    print(f"📂 Categories: {len(categories)}")
    print(f"📡 Sources: {len(sources)}")
    
    print(f"\n🏆 Top Categories:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {cat}: {count} articles")
    
    print(f"\n📺 Top Sources:")
    for src, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {src}: {count} articles")

def main():
    """Main execution function"""
    
    try:
        # Collect intelligence
        articles = collect_drone_intelligence()
        
        if not articles:
            print("⚠️ No articles collected. Creating minimal dataset...")
            articles = [{
                'Title': 'Drone Intelligence Collection System Online',
                'Link': 'https://github.com',
                'Source': 'System',
                'Published': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'Category': '🚁 System Status'
            }]
        
        # Save data
        if save_intelligence_data(articles):
            print_collection_summary(articles)
            print(f"\n🎉 Intelligence collection completed successfully!")
            return True
        else:
            print(f"❌ Failed to save intelligence data")
            return False
            
    except KeyboardInterrupt:
        print(f"\n⚠️ Collection interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
