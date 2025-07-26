#!/usr/bin/env python3
"""
Drone Intelligence Scraper for Drone_news Repository
Runs entirely on GitHub Actions - No local setup required
"""

import urllib.request
import urllib.parse
import json
import os
import time
import random
import sys
from datetime import datetime

print("🚁 DRONE INTELLIGENCE COLLECTION SYSTEM")
print("📊 Repository: Drone_news")
print("🌐 Running on GitHub Actions")
print("=" * 60)

def create_directories():
    """Create required directories"""
    os.makedirs("data", exist_ok=True)
    os.makedirs("docs", exist_ok=True)
    print("✅ Directories created")

def get_search_queries():
    """Get comprehensive drone intelligence search queries"""
    
    queries = [
        ("drone when:24h", "🚁 Drones"),
        ("UAV when:24h", "🛩️ UAV"),
        ("UAS when:24h", "🛩️ UAS"),
        ("military drone when:24h", "🎯 Military Drones"),
        ("China drone when:24h", "🇨🇳 China Drones"),
        ("Russia drone when:24h", "🇷🇺 Russia Drones"),
        ("autonomous drone when:24h", "🤖 Autonomous Drones"),
        ("drone warfare when:24h", "⚔️ Drone Warfare"),
        ("Iran drone when:24h", "🇮🇷 Iran Drones"),
        ("drone strike when:24h", "💥 Drone Strikes"),
        ("anti-drone when:24h", "🛡️ Counter-Drone"),
        ("drone swarm when:24h", "🐝 Drone Swarms"),
        ("combat drone when:24h", "⚔️ Combat Systems"),
        ("quadcopter when:24h", "🚁 Quadcopters"),
        ("tactical UAV when:24h", "🎯 Tactical UAV"),
        ("North Korea drone when:24h", "🇰🇵 DPRK Drones"),
        ("Ukraine drone when:24h", "🇺🇦 Ukraine Drones"),
        ("Israel drone when:24h", "🇮🇱 Israel Drones"),
        ("Turkey drone when:24h", "🇹🇷 Turkey Drones"),
        ("FPV drone when:24h", "🎮 FPV Systems"),
        ("VTOL drone when:24h", "🚁 VTOL Systems"),
        ("commercial drone when:24h", "📦 Commercial Drones"),
        ("drone delivery when:24h", "📦 Delivery Services"),
        ("agricultural drone when:24h", "🚜 Agricultural Drones"),
        ("drone regulation when:24h", "📋 Regulation"),
        ("FAA drone when:24h", "📋 FAA Policy"),
        ("site:reuters.com drone when:24h", "📺 Reuters"),
        ("site:defensenews.com drone when:24h", "📰 Defense News"),
        ("site:janes.com drone when:24h", "📰 Jane's Defence"),
        ("site:cnn.com drone when:24h", "📺 CNN"),
        ("site:bbc.com drone when:24h", "📺 BBC"),
        ("site:bloomberg.com drone when:24h", "📺 Bloomberg"),
        ("site:wsj.com drone when:24h", "📺 Wall Street Journal"),
        ("site:thedrive.com drone when:24h", "📰 The Drive"),
        ("site:wired.com drone when:24h", "💻 Wired")
    ]
    
    # Use priority mode if specified
    if '--priority' in sys.argv:
        print("🚀 PRIORITY MODE: Using 15 high-impact searches")
        return queries[:15]
    
    print(f"🔍 COMPREHENSIVE MODE: Using {len(queries)} searches")
    return queries

def search_google_news(query, category):
    """Search Google News for drone intelligence"""
    
    print(f"  🔍 Searching: {category}")
    
    try:
        # Encode query for URL
        encoded_query = urllib.parse.quote(query.encode('utf-8'))
        url = f'https://news.google.com/search?q={encoded_query}&hl=en'
        
        # Add respectful delay
        time.sleep(random.uniform(1, 3))
        
        # Make request with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8', errors='ignore')
        
        # Extract article information using pattern matching
        articles = []
        
        # Import regex for pattern matching
        import re
        
        # Look for article-like patterns in the HTML
        patterns = [
            r'"([^"]{30,150})"',  # Quoted text (likely titles)
            r'aria-label="([^"]{30,150})"',  # Aria labels
            r'<h[1-6][^>]*>([^<]{30,150})</h[1-6]>'  # Header tags
        ]
        
        found_titles = set()
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                title = match.strip()
                
                # Filter for drone-related content
                drone_keywords = ['drone', 'uav', 'uas', 'unmanned', 'aircraft', 'quadcopter']
                if (len(title) >= 30 and len(title) <= 150 and
                    title not in found_titles and
                    any(keyword in title.lower() for keyword in drone_keywords) and
                    not any(skip in title.lower() for skip in ['cookie', 'privacy', 'terms', 'subscribe', 'newsletter', 'advertisement'])):
                    
                    found_titles.add(title)
                    articles.append({
                        'Title': title,
                        'Link': url,
                        'Source': f"{category.split()[-1]} Source",
                        'Published': 'Recent',
                        'Category': category,
                        'Image': None,
                        'Scraped_At': datetime.now().isoformat()
                    })
                    
                    if len(articles) >= 6:  # Limit per search
                        break
            
            if len(articles) >= 6:
                break
        
        print(f"    ✅ Found {len(articles)} articles")
        return articles
        
    except Exception as e:
        print(f"    ❌ Error: {str(e)[:50]}...")
        return []

def collect_all_intelligence():
    """Main intelligence collection function"""
    
    queries = get_search_queries()
    all_articles = []
    
    print(f"📊 Starting collection from {len(queries)} sources...")
    
    for i, (query, category) in enumerate(queries):
        try:
            articles = search_google_news(query, category)
            all_articles.extend(articles)
            
            # Progress update every 5 searches
            if (i + 1) % 5 == 0:
                print(f"📈 Progress: {i+1}/{len(queries)} searches completed ({len(all_articles)} articles so far)")
                
        except Exception as e:
            print(f"❌ Error in search {i+1}: {e}")
            continue
    
    # Remove duplicates based on title similarity
    unique_articles = []
    seen_titles = set()
    
    for article in all_articles:
        title_key = article['Title'].lower().strip()
        
        # Simple word-based deduplication
        title_words = set(title_key.split())
        is_duplicate = False
        
        for seen_title in seen_titles:
            seen_words = set(seen_title.split())
            if len(title_words) > 0 and len(seen_words) > 0:
                # Check for 70%+ word overlap
                overlap = len(title_words.intersection(seen_words))
                similarity = overlap / max(len(title_words), len(seen_words))
                if similarity > 0.7:
                    is_duplicate = True
                    break
        
        if not is_duplicate:
            seen_titles.add(title_key)
            unique_articles.append(article)
    
    print(f"✅ Collection completed!")
    print(f"📊 Total articles found: {len(all_articles)}")
    print(f"📊 Unique articles: {len(unique_articles)}")
    print(f"📊 Duplicate removal: {len(all_articles) - len(unique_articles)} duplicates filtered")
    
    return unique_articles

def save_intelligence_data(articles):
    """Save intelligence data to JSON and CSV files"""
    
    try:
        # Always save JSON file (even if empty for GitHub Actions)
        with open("data/latest_news.json", "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(articles)} articles to data/latest_news.json")
        
        # Try to save CSV if pandas is available
        try:
            import pandas as pd
            if articles:
                df = pd.DataFrame(articles)
                df.to_csv("data/latest_news.csv", index=False)
                print(f"✅ Saved CSV to data/latest_news.csv")
            else:
                # Create empty CSV
                with open("data/latest_news.csv", "w") as f:
                    f.write("Title,Link,Source,Published,Category,Image,Scraped_At\n")
                print(f"✅ Created empty CSV file")
        except ImportError:
            print("⚠️ Pandas not available for CSV export")
        except Exception as e:
            print(f"⚠️ CSV export failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Save error: {e}")
        return False

def show_collection_summary(articles):
    """Display comprehensive collection summary"""
    
    print(f"\n📊 COLLECTION SUMMARY")
    print(f"=" * 50)
    
    if not articles:
        print("📊 No articles collected this session")
        print("🔄 System will retry on next scheduled run")
        return
    
    # Calculate statistics
    categories = {}
    sources = set()
    recent_articles = 0
    
    for article in articles:
        cat = article.get('Category', 'Unknown')
        src = article.get('Source', 'Unknown')
        pub = article.get('Published', '').lower()
        
        categories[cat] = categories.get(cat, 0) + 1
        sources.add(src)
        
        if any(term in pub for term in ['hour', 'minute', 'recent']):
            recent_articles += 1
    
    print(f"📈 Total Intelligence Reports: {len(articles)}")
    print(f"📂 Categories Covered: {len(categories)}")
    print(f"📰 Unique Sources: {len(sources)}")
    print(f"🕐 Recent Reports (hours): {recent_articles}")
    
    # Show top categories
    print(f"\n🏆 Top Intelligence Categories:")
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    for i, (cat, count) in enumerate(sorted_categories[:10]):
        print(f"  {i+1:2d}. {cat}: {count} reports")
    
    # Show collection rate
    print(f"\n⚡ Collection Efficiency:")
    total_searches = len(get_search_queries())
    success_rate = (len([cat for cat, count in categories.items() if count > 0]) / total_searches) * 100
    print(f"  📊 Search Success Rate: {success_rate:.1f}%")
    print(f"  📈 Articles per Search: {len(articles) / total_searches:.1f}")

def main():
    """Main execution function optimized for GitHub Actions"""
    
    try:
        # Setup environment
        create_directories()
        
        # Collect intelligence
        print(f"\n🎯 STARTING INTELLIGENCE COLLECTION")
        print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        start_time = time.time()
        articles = collect_all_intelligence()
        collection_time = time.time() - start_time
        
        # Save data (always save, even if empty)
        if save_intelligence_data(articles):
            show_collection_summary(articles)
            
            print(f"\n🎉 INTELLIGENCE COLLECTION SUCCESS!")
            print(f"⏱️  Collection Time: {collection_time:.1f} seconds")
            print(f"📁 Data saved for GitHub Pages deployment")
            print(f"🌐 Live Brief: https://{os.environ.get('GITHUB_REPOSITORY_OWNER', 'your-username')}.github.io/Drone_news/")
            
        else:
            print(f"❌ Failed to save intelligence data")
            
    except Exception as e:
        print(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()
        
        # Always create empty data file for GitHub Actions
        try:
            with open("data/latest_news.json", "w") as f:
                json.dump([], f)
            print("📁 Created empty data file for GitHub Actions continuity")
        except:
            pass

if __name__ == "__main__":
    main()
