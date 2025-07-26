#!/usr/bin/env python3
"""
Comprehensive Drone News Scraper - Adapted from Working Cyber Scraper
Uses proven scraping methodology with drone-focused search terms
"""

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup as Soup
import pandas as pd
import os
import time
from datetime import datetime, timedelta
import json
import re
import random

# Create necessary directories
os.makedirs("data", exist_ok=True)
os.makedirs("docs", exist_ok=True)

def define_date(date):
    """Convert relative date strings to datetime objects"""
    if not date:
        return None
    
    try:
        if ' ago' in date.lower():
            parts = date.split()
            if len(parts) >= 3:
                q = int(parts[0])
                if 'minute' in date.lower():
                    return datetime.now() - timedelta(minutes=q)
                elif 'hour' in date.lower():
                    return datetime.now() - timedelta(hours=q)
                elif 'day' in date.lower():
                    return datetime.now() - timedelta(days=q)
                elif 'week' in date.lower():
                    return datetime.now() - timedelta(days=7*q)
        elif 'yesterday' in date.lower():
            return datetime.now() - timedelta(days=1)
        else:
            return datetime.now()
    except:
        return datetime.now()

def process_image_url(img_src):
    """Process and validate image URL from Google News"""
    if not img_src:
        return None
    
    # Handle different URL formats from Google News
    if img_src.startswith('//'):
        return 'https:' + img_src
    elif img_src.startswith('/'):
        return 'https://news.google.com' + img_src
    elif img_src.startswith('data:'):
        # Skip data URLs as they're usually tiny placeholders
        return None
    elif img_src.startswith('http'):
        # Already a full URL
        return img_src
    else:
        # Relative URL, make it absolute
        return 'https://news.google.com/' + img_src.lstrip('/')

class MultiSearchDroneNews:
    def __init__(self, lang="en"):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        self.lang = lang
        self.headers = {'User-Agent': self.user_agent}
        self.all_results = []

    def search_single_query(self, query, search_name):
        """Search Google News for a single query"""
        print(f"\n{'='*50}")
        print(f"Searching: {search_name}")
        print(f"Query: {query}")
        print(f"{'='*50}")
        
        # Build Google News search URL
        encoded_query = urllib.parse.quote(query.encode('utf-8'))
        url = f'https://news.google.com/search?q={encoded_query}&hl={self.lang}'
        
        print(f"URL: {url}")
        
        try:
            # Add random delay to be respectful
            time.sleep(random.uniform(2, 4))
            
            # Make request
            req = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(req, timeout=30)
            page = response.read()
            content = Soup(page, "html.parser")
            
            # Save debug HTML for first search
            if search_name == "Military Drones":
                with open("debug_drone_search.html", "w", encoding="utf-8") as f:
                    f.write(str(content))
                print("Saved debug HTML file")
            
            # Find articles
            articles = content.select('article')
            print(f"Found {len(articles)} article elements")
            
            valid_articles = []
            
            for i, article in enumerate(articles):
                if len(valid_articles) >= 10:  # Limit per search
                    break
                    
                try:
                    # Extract title using multiple methods
                    title = None
                    try:
                        # Method 1: article.findAll('div')[2].findAll('a')[0].text
                        divs = article.find_all('div')
                        if len(divs) > 2:
                            links = divs[2].find_all('a')
                            if links:
                                title = links[0].get_text(strip=True)
                    except:
                        try:
                            # Method 2: article.findAll('a')[1].text
                            links = article.find_all('a')
                            if len(links) > 1:
                                title = links[1].get_text(strip=True)
                        except:
                            # Method 3: any h3 or h4 in article
                            try:
                                h_tag = article.find(['h3', 'h4'])
                                if h_tag:
                                    title = h_tag.get_text(strip=True)
                            except:
                                title = None
                    
                    if not title or len(title) < 15:
                        continue
                    
                    # Skip navigation items
                    title_lower = title.lower()
                    nav_terms = ['home', 'for you', 'following', 'u.s.', 'world', 'local', 
                                'business', 'technology', 'entertainment', 'sports', 
                                'science', 'health', 'google news', 'more']
                    
                    if any(nav_term == title_lower.strip() for nav_term in nav_terms):
                        print(f"  ✗ Skipping navigation: {title}")
                        continue
                    
                    # Extract link
                    link = None
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
                        link = url  # Fallback to search URL
                    
                    # Extract date
                    date = None
                    datetime_obj = None
                    try:
                        time_elem = article.find("time")
                        if time_elem:
                            date = time_elem.get_text(strip=True)
                            datetime_obj = define_date(date)
                    except:
                        date = "Recent"
                        datetime_obj = datetime.now()
                    
                    # Extract media/source
                    media = None
                    try:
                        media = article.find("time").parent.find("a").get_text(strip=True)
                    except:
                        try:
                            # Alternative method
                            divs = article.find("div").find_all("div")
                            if len(divs) > 1:
                                nested = divs[1].find("div")
                                if nested:
                                    deeper = nested.find("div")
                                    if deeper:
                                        final = deeper.find("div")
                                        if final:
                                            media = final.get_text(strip=True)
                        except:
                            media = f"{search_name} News"
                    
                    if not media or media == title or len(media) > 50:
                        media = f"{search_name} News"
                    
                    # Extract image - try multiple methods
                    img = None
                    try:
                        # Method 1: Look for figure/img tags
                        img_elem = article.find("figure")
                        if img_elem:
                            img_tag = img_elem.find("img")
                            if img_tag and img_tag.get("src"):
                                img_src = img_tag.get("src")
                                img = process_image_url(img_src)
                        
                        # Method 2: Look for any img tag in article
                        if not img:
                            img_tag = article.find("img")
                            if img_tag and img_tag.get("src"):
                                img_src = img_tag.get("src")
                                img = process_image_url(img_src)
                        
                        # Method 3: Look for img with specific Google News classes
                        if not img:
                            img_candidates = article.find_all("img", class_=True)
                            for img_candidate in img_candidates:
                                if img_candidate.get("src"):
                                    img_src = img_candidate.get("src")
                                    img = process_image_url(img_src)
                                    if img:
                                        break
                        
                        # Method 4: Look for data-src or other lazy loading attributes
                        if not img:
                            img_tag = article.find("img", attrs={"data-src": True})
                            if img_tag and img_tag.get("data-src"):
                                img_src = img_tag.get("data-src")
                                img = process_image_url(img_src)
                        
                    except Exception as e:
                        print(f"    Error extracting image: {e}")
                        img = None
                    
                    print(f"  ✓ Found: {title[:60]}... (Source: {media}) {f'[IMG: {img[:30]}...]' if img else '[NO IMG]'}")
                    
                    valid_articles.append({
                        'title': title,
                        'desc': None,
                        'date': date,
                        'datetime': datetime_obj,
                        'link': link,
                        'img': img,
                        'media': media,
                        'site': media,
                        'reporter': None,
                        'search_category': search_name
                    })
                    
                except Exception as e:
                    print(f"  Error processing article {i+1}: {e}")
                    continue
            
            response.close()
            
            print(f"✓ {search_name}: Found {len(valid_articles)} valid articles")
            return valid_articles
            
        except Exception as e:
            print(f"✗ {search_name}: Error during search: {e}")
            return []

    def run_all_searches(self):
        """Run all the drone-focused searches"""
        print("Starting comprehensive drone news scraping...")
        print("🚁 Searches: Military Drones, Combat UAVs, Geopolitical Drone Operations")
        print("🌐 Site-specific searches from premium defense and tech sources")
        
        # Define all drone searches - comprehensive coverage
        searches = [
            # Core military drone operations
            ("military drone when:24h", "🎯 Military Drones"),
            ("combat drone when:24h", "⚔️ Combat Drones"),
            ("drone warfare when:24h", "⚔️ Drone Warfare"),
            ("drone strike when:24h", "💥 Drone Strikes"),
            ("military UAV when:24h", "🛩️ Military UAV"),
            ("tactical drone when:24h", "🎯 Tactical Drones"),
            
            # Geopolitical drone coverage
            ("Ukraine drone when:24h", "🇺🇦 Ukraine Drones"),
            ("Russia drone when:24h", "🇷🇺 Russia Drones"),
            ("China drone when:24h", "🇨🇳 China Drones"),
            ("Iran drone when:24h", "🇮🇷 Iran Drones"),
            ("Israel drone when:24h", "🇮🇱 Israel Drones"),
            ("North Korea drone when:24h", "🇰🇵 DPRK Drones"),
            ("Turkey drone when:24h", "🇹🇷 Turkey Drones"),
            
            # Advanced drone technology
            ("autonomous drone when:24h", "🤖 Autonomous Drones"),
            ("AI drone when:24h", "🤖 AI Drones"),
            ("drone swarm when:24h", "🐝 Drone Swarms"),
            ("drone technology when:24h", "🔬 Drone Technology"),
            ("unmanned aircraft when:24h", "🛩️ Unmanned Aircraft"),
            
            # Counter-drone and defense
            ("anti-drone when:24h", "🛡️ Counter-Drone"),
            ("drone defense when:24h", "🛡️ Drone Defense"),
            ("counter-UAV when:24h", "🛡️ Counter-UAV"),
            
            # Commercial and civilian drones
            ("commercial drone when:24h", "📦 Commercial Drones"),
            ("drone delivery when:24h", "📦 Drone Delivery"),
            ("agricultural drone when:24h", "🚜 Agricultural Drones"),
            ("drone regulation when:24h", "📋 Drone Regulation"),
            ("FAA drone when:24h", "📋 FAA Drone"),
            
            # Specific drone types and systems
            ("FPV drone when:24h", "🎮 FPV Drones"),
            ("quadcopter when:24h", "🚁 Quadcopters"),
            ("VTOL drone when:24h", "🚁 VTOL Drones"),
            ("surveillance drone when:24h", "👁️ Surveillance Drones"),
            
            # Major drone manufacturers and programs
            ("Bayraktar drone when:24h", "🇹🇷 Bayraktar"),
            ("Reaper drone when:24h", "🇺🇸 Reaper Drone"),
            ("DJI drone when:24h", "🇨🇳 DJI"),
            ("General Atomics drone when:24h", "🇺🇸 General Atomics"),
            
            # Site-specific searches - Defense publications
            ("site:defensenews.com drone when:24h", "📰 Defense News"),
            ("site:janes.com drone when:24h", "📰 Jane's Defence"),
            ("site:military.com drone when:24h", "📰 Military.com"),
            ("site:thedrive.com drone when:24h", "📰 The Drive"),
            
            # Site-specific searches - Major news outlets
            ("site:reuters.com drone when:24h", "📺 Reuters"),
            ("site:bbc.com drone when:24h", "📺 BBC"),
            ("site:cnn.com drone when:24h", "📺 CNN"),
            ("site:wsj.com drone when:24h", "📺 Wall Street Journal"),
            ("site:bloomberg.com drone when:24h", "📺 Bloomberg"),
            
            # Site-specific searches - Tech publications
            ("site:wired.com drone when:24h", "💻 Wired"),
            ("site:techcrunch.com drone when:24h", "💻 TechCrunch"),
            ("site:theverge.com drone when:24h", "💻 The Verge"),
            
            # Site-specific searches - Specialized drone publications
            ("site:dronexl.co when:24h", "🚁 DroneXL"),
            ("site:dronelife.com when:24h", "🚁 Drone Life"),
            ("site:suasnews.com when:24h", "🚁 sUAS News"),
            
            # Regional and conflict-specific
            ("Gaza drone when:24h", "🇵🇸 Gaza Drones"),
            ("Syria drone when:24h", "🇸🇾 Syria Drones"),
            ("Taiwan drone when:24h", "🇹🇼 Taiwan Drones"),
            ("Africa drone when:24h", "🌍 Africa Drones"),
            
            # Emerging threats and incidents
            ("drone incident when:24h", "⚠️ Drone Incidents"),
            ("airport drone when:24h", "✈️ Airport Drones"),
            ("prison drone when:24h", "🏢 Prison Drones"),
        ]
        
        all_articles = []
        
        for query, search_name in searches:
            articles = self.search_single_query(query, search_name)
            all_articles.extend(articles)
            
            # Add delay between searches
            time.sleep(random.uniform(1, 3))
        
        # Remove duplicates based on title similarity
        unique_articles = self.remove_duplicates(all_articles)
        
        print(f"\n{'='*50}")
        print(f"🚁 FINAL DRONE NEWS RESULTS")
        print(f"{'='*50}")
        print(f"Total articles found: {len(all_articles)}")
        print(f"Unique articles after deduplication: {len(unique_articles)}")
        
        # Show breakdown by category
        categories = {}
        for article in unique_articles:
            cat = article.get('search_category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"\n📊 Breakdown by category:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count} articles")
        
        self.all_results = unique_articles
        return unique_articles

    def remove_duplicates(self, articles):
        """Remove duplicate articles based on title similarity"""
        if not articles:
            return []
        
        unique_articles = []
        seen_titles = set()
        
        for article in articles:
            title = article['title'].lower().strip()
            
            # Check if title is too similar to existing ones
            is_duplicate = False
            title_words = set(title.split())
            
            for seen_title in seen_titles:
                seen_words = set(seen_title.split())
                if len(title_words) > 0 and len(seen_words) > 0:
                    # If more than 70% of words are the same, consider it a duplicate
                    similarity = len(title_words.intersection(seen_words)) / max(len(title_words), len(seen_words))
                    if similarity > 0.7:
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                seen_titles.add(title)
                unique_articles.append(article)
        
        return unique_articles

def scrape_drone_news_multi():
    """Main scraping function for multiple drone searches"""
    searcher = MultiSearchDroneNews()
    articles = searcher.run_all_searches()
    
    # Convert to expected format for newsletter generator
    formatted_articles = []
    for article in articles:
        formatted_articles.append({
            "Title": article['title'],
            "Link": article['link'] or "https://news.google.com",
            "Source": article['media'] or "Drone News",
            "Published": article['date'] or "Recent",
            "Category": article.get('search_category', 'General Drones'),
            "img": article.get('img'),  # Include image data
            "Scraped_At": datetime.now().isoformat()
        })
    
    # Sort by datetime if available
    try:
        formatted_articles.sort(key=lambda x: article.get('datetime', datetime.now()), reverse=True)
    except:
        pass
    
    return formatted_articles

def save_to_files(news):
    """Save news data to CSV and JSON files"""
    if not news:
        print("No drone news data to save.")
        with open("data/latest_news.json", "w") as f:
            json.dump([], f)
        return None
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"data/drone_news_{timestamp}.csv"
    df = pd.DataFrame(news)
    df.to_csv(filename, index=False)
    
    # Also save as latest for the website
    df.to_csv("data/latest_news.csv", index=False)
    
    # Save as JSON for web use (this is what the newsletter generator expects)
    with open("data/latest_news.json", "w", encoding="utf-8") as f:
        json.dump(news, f, indent=2, ensure_ascii=False)
    
    print(f"📁 Saved {len(news)} articles to:")
    print(f"   📄 {filename}")
    print(f"   📄 data/latest_news.csv")
    print(f"   📄 data/latest_news.json")
    
    return filename

def main():
    """Main function to run the drone news scraper"""
    print("🚁 COMPREHENSIVE DRONE NEWS SCRAPER")
    print("=" * 60)
    print("📊 Searches: 53+ categories covering:")
    print("   • Military & Combat Drones")
    print("   • Geopolitical Drone Operations (Ukraine, Russia, China, Iran, etc.)")
    print("   • Advanced Drone Technology (AI, Autonomous, Swarms)")
    print("   • Counter-Drone & Defense Systems")
    print("   • Commercial & Civilian Drones")
    print("   • Premium Defense & Tech News Sources")
    print("⏰ Timeframe: Last 24 hours for each search")
    print("🌐 Sources: Defense News, Jane's, Reuters, BBC, WSJ, Bloomberg, Wired, etc.")
    print("=" * 60)
    
    try:
        # Run the comprehensive drone news scraper
        news = scrape_drone_news_multi()
        
        if news:
            save_to_files(news)
            print(f"\n🎉 Successfully processed {len(news)} drone news articles")
            
            # Print sample articles found
            print(f"\n📰 Sample articles found:")
            for i, article in enumerate(news[:5]):
                print(f"{i+1}. {article['Title']}")
                print(f"   📺 Source: {article['Source']}")
                print(f"   📂 Category: {article['Category']}")
                print(f"   🔗 Link: {article['Link'][:60]}...")
                print()
                
            if len(news) > 5:
                print(f"... and {len(news) - 5} more articles")
                
            print(f"\n✅ Data ready for newsletter generation!")
        else:
            print("❌ No drone articles found!")
            with open("data/latest_news.json", "w") as f:
                json.dump([], f)
                
    except Exception as e:
        print(f"❌ Error in main: {e}")
        import traceback
        traceback.print_exc()
        with open("data/latest_news.json", "w") as f:
            json.dump([], f)

if __name__ == "__main__":
    main()
