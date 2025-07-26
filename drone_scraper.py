#!/usr/bin/env python3
"""
Simplified Drone Intelligence Scraper
GitHub Actions Compatible - Error Resistant Version
"""

import urllib.request
import urllib.parse
import json
import os
import time
import random
from datetime import datetime
import sys

def create_directories():
    """Ensure required directories exist"""
    os.makedirs("data", exist_ok=True)
    os.makedirs("docs", exist_ok=True)
    print("✅ Directories created")

def get_search_queries(priority_mode=False):
    """Get search queries for drone intelligence"""
    
    if priority_mode or '--priority' in sys.argv:
        print("🚀 Using PRIORITY mode (15 searches)")
        return [
            ("drone when:24h", "🚁 Drones"),
            ("UAV when:24h", "🛩️ UAV"),
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
            ("site:reuters.com drone when:24h", "📺 Reuters"),
            ("site:defensenews.com drone when:24h", "📰 Defense News"),
            ("site:janes.com drone when:24h", "📰 Jane's Defence")
        ]
    
    print("🔍 Using COMPREHENSIVE mode (25 searches)")
    return [
        # Core searches
        ("drone when:24h", "🚁 Drones"),
        ("UAV when:24h", "🛩️ UAV"),
        ("UAS when:24h", "🛩️ UAS"),
        ("quadcopter when:24h", "🚁 Quadcopters"),
        
        # Military
        ("military drone when:24h", "🎯 Military Drones"),
        ("drone warfare when:24h", "⚔️ Drone Warfare"),
        ("drone strike when:24h", "💥 Drone Strikes"),
        ("combat drone when:24h", "⚔️ Combat Systems"),
        ("tactical UAV when:24h", "🎯 Tactical UAV"),
        
        # Geopolitical
        ("China drone when:24h", "🇨🇳 China Drones"),
        ("Russia drone when:24h", "🇷🇺 Russia Drones"),
        ("Iran drone when:24h", "🇮🇷 Iran Drones"),
        ("North Korea drone when:24h", "🇰🇵 DPRK Drones"),
        ("Ukraine drone when:24h", "🇺🇦 Ukraine Drones"),
        
        # Technology
        ("autonomous drone when:24h", "🤖 Autonomous Drones"),
        ("drone swarm when:24h", "🐝 Drone Swarms"),
        ("anti-drone when:24h", "🛡️ Counter-Drone"),
        ("FPV drone when:24h", "🎮 FPV Systems"),
        
        # Commercial
        ("commercial drone when:24h", "📦 Commercial Drones"),
        ("drone delivery when:24h", "📦 Delivery Services"),
        
        # Sources
        ("site:reuters.com drone when:24h", "📺 Reuters"),
        ("site:defensenews.com drone when:24h", "📰 Defense News"),
        ("site:janes.com drone when:24h", "📰 Jane's Defence"),
        ("site:cnn.com drone when:24h", "📺 CNN"),
        ("site:bbc.com drone when:24h", "📺 BBC")
    ]

def simple_search(query, category, max_articles=5):
    """Simplified search function with better error handling"""
    
    print(f"  🔍 Searching: {category}")
    
    try:
        # Build URL
        encoded_query = urllib.parse.quote(query.encode('utf-8'))
        url = f'https://news.google.com/search?q={encoded_query}&hl=en'
        
        # Add delay
        time.sleep(random.uniform(1, 3))
        
        # Make request with timeout
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8', errors='ignore')
        
        # Simple title extraction (looking for common patterns)
        articles = []
        
        # Very basic extraction - look for article-like patterns
        import re
        
        # Find potential article titles (between quotes or in title-like tags)
        patterns = [
            r'"([^"]{20,150})"',  # Text in quotes (likely titles)
            r'<h\d[^>]*>([^<]{20,150})</h\d>',  # Header tags
            r'aria-label="([^"]{20,150})"'  # Aria labels
        ]
        
        found_titles = set()
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                clean_title = match.strip()
                if (len(clean_title) > 20 and 
                    len(clean_title) < 150 and
                    clean_title not in found_titles and
                    any(word in clean_title.lower() for word in ['drone', 'uav', 'uas', 'aircraft'])):
                    
                    found_titles.add(clean_title)
                    articles.append({
                        'Title': clean_title,
                        'Link': f"https://news.google.com/search?q={encoded_query}",
                        'Source': f"{category} Source",
                        'Published': 'Recent',
                        'Category': category,
                        'Image': None,
                        'Scraped_At': datetime.now().isoformat()
                    })
                    
                    if len(articles) >= max_articles:
                        break
            
            if len(articles) >= max_articles:
                break
        
        print(f"    ✅ Found {len(articles)} articles")
        return articles
        
    except Exception as e:
        print(f"    ❌ Error: {str(e)[:100]}")
        return []

def collect_intelligence():
    """Main collection function"""
    
    print("🚁 DRONE INTELLIGENCE COLLECTION")
    print("=" * 50)
    
    # Determine mode
    priority_mode = '--priority' in sys.argv or '--fast' in sys.argv
    queries = get_search_queries(priority_mode)
    
    print(f"📊 Executing {len(queries)} searches...")
    
    all_articles = []
    
    for i, (query, category) in enumerate(queries):
        try:
            articles = simple_search(query, category)
            all_articles.extend(articles)
            
            # Progress update
            if (i + 1) % 5 == 0:
                print(f"📈 Progress: {i+1}/{len(queries)} searches completed")
                
        except Exception as e:
            print(f"❌ Error in search {i+1}: {e}")
            continue
    
    # Simple deduplication
    unique_articles = []
    seen_titles = set()
    
    for article in all_articles:
        title_lower = article['Title'].lower()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            unique_articles.append(article)
    
    print(f"✅ Collection complete!")
    print(f"📊 Raw articles: {len(all_articles)}")
    print(f"📊 Unique articles: {len(unique_articles)}")
    
    return unique_articles

def save_data(articles):
    """Save articles to JSON and CSV"""
    
    try:
        # Save JSON
        with open("data/latest_news.json", "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(articles)} articles to data/latest_news.json")
        
        # Try to save CSV if pandas is available
        try:
            import pandas as pd
            df = pd.DataFrame(articles)
            df.to_csv("data/latest_news.csv", index=False)
            print(f"✅ Saved CSV to data/latest_news.csv")
        except ImportError:
            print("⚠️ Pandas not available, skipping CSV export")
        
        return True
        
    except Exception as e:
        print(f"❌ Save error: {e}")
        return False

def main():
    """Main function"""
    
    try:
        # Create directories
        create_directories()
        
        # Collect intelligence
        articles = collect_intelligence()
        
        # Always save something, even if empty
        if not articles:
            print("⚠️ No articles collected, creating empty dataset")
            articles = []
        
        # Save data
        if save_data(articles):
            print(f"🎉 Success! Collected {len(articles)} intelligence reports")
            
            # Show summary
            if articles:
                categories = {}
                for article in articles:
                    cat = article.get('Category', 'Unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                
                print(f"\n📊 Summary by Category:")
                for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
                    print(f"  • {cat}: {count}")
        else:
            print("❌ Failed to save data")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()
        
        # Create empty file so workflow doesn't fail
        try:
            with open("data/latest_news.json", "w") as f:
                json.dump([], f)
            print("📁 Created empty data file")
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()
