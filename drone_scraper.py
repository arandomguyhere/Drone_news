import urllib.request
import urllib.parse
from bs4 import BeautifulSoup as Soup
import pandas as pd
import os
import time
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlunparse
import json
import random
import re

# Create necessary directories
os.makedirs("data", exist_ok=True)
os.makedirs("docs", exist_ok=True)

# ---------------------------------------------------------
# SEARCH QUERIES - Comprehensive source list
# ---------------------------------------------------------
SEARCH_QUERIES = [
    # MAINSTREAM MEDIA
    ("site:wsj.com cyber", "WSJ Cyber"),
    ("site:ft.com cyber", "FT Cyber"),
    ("site:reuters.com cyber", "Reuters Cyber"),
    ("site:nytimes.com cyber", "NYT Cyber"),
    ("site:france24.com cyber", "France24 Cyber"),
    ("site:independent.co.uk cyber", "Independent Cyber"),
    ("site:smh.com.au cyber", "SMH Cyber"),
    ("site:chosun.com cyber", "Chosun Cyber"),
    ("site:msn.com cyber", "MSN Cyber"),
    ("site:bloomberg.com cybersecurity", "Bloomberg Cyber"),
    ("site:techcrunch.com security", "TechCrunch Security"),
    ("site:wired.com cyber", "Wired Cyber"),
    ("site:forbes.com cybersecurity", "Forbes Cyber"),

    # TECH/SECURITY PUBLICATIONS
    ("site:therecord.media", "The Record"),
    ("site:theregister.com security", "The Register"),
    ("site:bleepingcomputer.com", "Bleeping Computer"),
    ("site:thehackernews.com", "The Hacker News"),
    ("site:gbhackers.com", "GBHackers"),
    ("site:securityweek.com", "SecurityWeek"),
    ("site:cybernews.com", "CyberNews"),
    ("site:cyberscoop.com", "CyberScoop"),
    ("site:cybersecuritydive.com", "Cybersecurity Dive"),
    ("site:darkreading.com", "Dark Reading"),
    ("site:scworld.com", "SC World"),
    ("site:csoonline.com", "CSO Online"),
    ("site:cpomagazine.com", "CPO Magazine"),
    ("site:bankinfosecurity.com", "Bank Info Security"),
    ("site:computerweekly.com cyber", "Computer Weekly"),
    ("site:itpro.com security", "ITPro"),
    ("site:redhotcyber.com", "Red Hot Cyber"),
    ("site:krebsonsecurity.com", "Krebs on Security"),
    ("site:schneier.com", "Schneier on Security"),

    # VENDOR RESEARCH / THREAT INTEL
    ("site:trendmicro.com research", "Trend Micro"),
    ("site:elastic.co security-labs", "Elastic Security Labs"),
    ("site:kaspersky.com securelist", "Kaspersky"),
    ("site:mandiant.com blog", "Mandiant"),
    ("site:wiz.io blog", "Wiz"),
    ("site:huntress.com blog", "Huntress"),
    ("site:trailofbits.com", "Trail of Bits"),
    ("site:unit42.paloaltonetworks.com", "Unit 42"),
    ("site:crowdstrike.com blog", "CrowdStrike"),
    ("site:sentinelone.com blog", "SentinelOne"),

    # CHINESE SECURITY SITES
    ("site:freebuf.com", "Freebuf"),

    # REGIONAL / INTERNATIONAL
    ("site:scmp.com cyber", "SCMP"),
    ("site:koreatimes.co.kr cyber", "Korea Times"),
    ("site:kyivindependent.com cyber", "Kyiv Independent"),
    ("site:united24media.com", "United 24"),
    ("site:unn.ua cyber", "UNN"),
    ("site:nst.com.my cyber", "New Straits Times"),
    ("site:wionews.com cyber", "WION News"),
    ("site:ibtimes.com cyber", "IBT"),
    ("site:intelligenceonline.com", "Intelligence Online"),

    # GOVERNMENT / THINK TANKS / POLICY
    ("site:fdd.org cyber", "FDD"),
    ("site:justsecurity.org cyber", "Just Security"),
    ("site:smallwarsjournal.com cyber", "Small Wars Journal"),
    ("site:kharon.com", "Kharon"),
    ("site:thedefensepost.com cyber", "Defense Post"),
    ("site:nationalinterest.org cyber", "National Interest"),
    ("site:realcleardefense.com cyber", "Real Clear Defense"),
    ("site:aspi.org.au cyber", "ASPI"),

    # LEGAL / REGULATORY
    ("site:iclg.com cyber", "ICLG"),

    # SUBSTACKS
    ("site:aisafetychina.substack.com", "AI Safety China"),
    ("site:chinapolicy.substack.com", "China Policy"),
    ("site:chinai.substack.com", "ChinAI"),
    ("site:phillipspobrien.substack.com", "Phillips O'Brien"),
    ("site:cisotradecraft.substack.com", "CISO Tradecraft"),
    ("site:cybermaterial.substack.com", "Cybermaterial"),

    # PODCASTS / MEDIA
    ("site:risky.biz", "Risky Business"),
    ("site:lawfaremedia.org", "Lawfare"),

    # ---------------------------------------------------------
    # TOPIC-BASED SEARCHES - Nation State Actors
    # ---------------------------------------------------------
    ("China cyber attack", "China Cyber"),
    ("Russia cyber attack", "Russia Cyber"),
    ("DPRK cyber", "DPRK Cyber"),
    ("North Korea hackers", "North Korea Cyber"),
    ("Iran cyber", "Iran Cyber"),
    ("state-sponsored hackers", "State-Sponsored Cyber"),

    # ---------------------------------------------------------
    # TOPIC-BASED SEARCHES - Threat Types
    # ---------------------------------------------------------
    ("ransomware attack", "Ransomware"),
    ("zero day exploit", "Zero Days"),
    ("CVE vulnerability", "Vulnerabilities"),
    ("APT threat actor", "APT Groups"),
    ("Advanced Persistent Threat", "Advanced Threats"),
    ("Salt Typhoon", "Salt Typhoon"),
    ("Volt Typhoon", "Volt Typhoon"),
    ("phishing attack", "Phishing"),
    ("malware campaign", "Malware"),
    ("data breach", "Data Breach"),

    # ---------------------------------------------------------
    # TOPIC-BASED SEARCHES - Infrastructure & Supply Chain
    # ---------------------------------------------------------
    ("critical infrastructure cyber", "Critical Infrastructure"),
    ("supply chain attack", "Supply Chain"),
    ("power grid cyber", "Energy Security"),

    # ---------------------------------------------------------
    # TOPIC-BASED SEARCHES - General Cyber
    # ---------------------------------------------------------
    ("cybersecurity news", "Cybersecurity"),
    ("hackers breach", "Hackers"),
    ("cyber attack today", "Cyber Attacks"),

    # ---------------------------------------------------------
    # TOPIC-BASED SEARCHES - Emerging Tech
    # ---------------------------------------------------------
    ("AI security threat", "AI Security"),
    ("quantum computing cyber", "Quantum Threats"),

    # ---------------------------------------------------------
    # TOPIC-BASED SEARCHES - Geopolitical
    # ---------------------------------------------------------
    ("Taiwan cyber attack", "Taiwan Security"),
    ("Ukraine cyber war", "Ukraine Conflict"),
    ("Israel cyber attack", "Middle East Cyber"),

    # ---------------------------------------------------------
    # TOPIC-BASED SEARCHES - Industry Sectors
    # ---------------------------------------------------------
    ("healthcare cyber attack", "Healthcare Security"),
    ("bank cyber attack", "Financial Security"),
    ("telecom cyber attack", "Telecom Security"),

    # ---------------------------------------------------------
    # TOPIC-BASED SEARCHES - Technology Targets
    # ---------------------------------------------------------
    ("Ivanti vulnerability", "VPN Security"),
    ("Fortinet vulnerability", "Firewall Security"),
    ("Cisco vulnerability", "Network Security"),
]

# ---------------------------------------------------------
# JUNK FILTERS - Patterns to exclude
# ---------------------------------------------------------
JUNK_TITLE_PATTERNS = [
    "news showcase", "popular stories", "latest news", "breaking news",
    "top stories", "all news", "latest articles", "news & updates",
    "today's top", "today's breaking", "| page", "page 2", "page 3",
    "archives", "- latest news", "latest cyber security", "latest security news",
    "news, analysis", "news and analysis", "news, videos, reports",
    "news & world", "cybersecurity, technology news", "breaking stock market",
    "deals market headlines", "| #1 trusted source", "national security, foreign policy",
    "author at", "contact us", "about us", "content by", "webinar |",
    "resources", "free templates", "coupons in", "cyber monday", "black friday",
    "boxing day", "holiday gift", "deals under", "best deals", "sale!",
    "china news |", "india news |", "energy news |", "topic |",
    "network security", "fraud management", "artificial intelligence & machine",
    "it management", "business news, analysis", "military spouses",
    "- breaking news, us news", "the new york times canada",
    "new straits times (nst online)", "bleepingcomputer |",
    "schneier on security -", "welcome to the new", "global banking and finance awards",
]

JUNK_EXACT_MATCHES = [
    "news showcase", "threats", "policy", "resources", "contact us",
    "about us", "cybercrime", "op-eds", "analysis", "china",
    "russia archives", "china archives",
]

MIN_TITLE_LENGTH = 25


def parse_relative_time(time_str):
    """Parse relative time string and return datetime object"""
    if not time_str:
        return None
    
    time_str = time_str.lower().strip()
    now = datetime.now()
    
    try:
        # Extract number from string
        numbers = re.findall(r'\d+', time_str)
        if not numbers:
            if 'yesterday' in time_str:
                return now - timedelta(days=1)
            return None
        
        num = int(numbers[0])
        
        if 'minute' in time_str or 'min' in time_str:
            return now - timedelta(minutes=num)
        elif 'hour' in time_str:
            return now - timedelta(hours=num)
        elif 'day' in time_str:
            return now - timedelta(days=num)
        elif 'week' in time_str:
            return now - timedelta(weeks=num)
        elif 'month' in time_str:
            return now - timedelta(days=num * 30)
        elif 'year' in time_str:
            return now - timedelta(days=num * 365)
        
    except:
        pass
    
    return None


def is_within_timeframe(dt, hours=48):
    """Check if datetime is within the specified hours"""
    if not dt:
        return False
    try:
        cutoff = datetime.now() - timedelta(hours=hours)
        return dt >= cutoff
    except:
        return False


def format_relative_time(dt):
    """Format datetime as relative time string"""
    if not dt:
        return "Recent"
    
    try:
        delta = datetime.now() - dt
        seconds = delta.total_seconds()
        
        if seconds < 3600:
            mins = int(seconds // 60)
            return f"{mins} minute{'s' if mins != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = int(seconds // 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
    except:
        return "Recent"


def clean_img_url(src):
    """Process and validate image URL from Google News"""
    if not src:
        return None
    if src.startswith("//"):
        return "https:" + src
    if src.startswith("/"):
        return "https://news.google.com" + src
    if src.startswith("data:"):
        return None
    return src


def normalize_url(url):
    """Normalize URL by removing amp and standardizing format"""
    try:
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path.replace("/amp", ""), "", "", ""))
    except:
        return url


def is_junk_title(title):
    """Check if a title matches known junk patterns"""
    if not title:
        return True
    
    title_lower = title.lower().strip()
    
    if len(title_lower) < MIN_TITLE_LENGTH:
        return True
    
    if title_lower in JUNK_EXACT_MATCHES:
        return True
    
    for pattern in JUNK_TITLE_PATTERNS:
        if pattern in title_lower:
            return True
    
    return False


class MultiSearchGoogleNews:
    def __init__(self, lang="en-US", gl="US", ceid="US:en", hours=48):
        self.lang = lang
        self.gl = gl
        self.ceid = ceid
        self.hours = hours
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.all_results = []

    def parse_article(self, card, category):
        """Parse a single article card and extract all relevant data"""
        # Extract title
        title = None
        for sel in ["h3", "h4", "a[role='heading']", "a[aria-level='2']"]:
            el = card.select_one(sel)
            if el:
                title = el.get_text(strip=True)
                if title:
                    break

        if not title:
            texts = [a.get_text(strip=True) for a in card.select("a[href]") if a.get_text(strip=True)]
            if texts:
                title = max(texts, key=len)

        if is_junk_title(title):
            return None

        # Extract link
        a = card.select_one("a[href]")
        if not a:
            return None
        href = a.get("href", "")

        if href.startswith("./"):
            link = "https://news.google.com" + href[1:]
        elif href.startswith("/"):
            link = "https://news.google.com" + href
        else:
            link = href

        link = normalize_url(link)

        # Extract time - CRITICAL for filtering
        time_elem = card.select_one("time")
        date_text = None
        dt = None
        
        if time_elem:
            # Try datetime attribute first (most reliable)
            datetime_attr = time_elem.get("datetime")
            if datetime_attr:
                try:
                    # Handle various datetime formats
                    datetime_attr = datetime_attr.replace("Z", "").replace("+00:00", "")
                    if "T" in datetime_attr:
                        dt = datetime.fromisoformat(datetime_attr)
                    else:
                        dt = datetime.strptime(datetime_attr, "%Y-%m-%d")
                except:
                    pass
            
            # Fallback to text content
            if not dt:
                date_text = time_elem.get_text(strip=True)
                dt = parse_relative_time(date_text)
        
        # Skip if no valid time or outside window
        if not dt:
            return None
        
        if not is_within_timeframe(dt, self.hours):
            return None
        
        date_text = format_relative_time(dt)

        # Extract source
        source = None
        for sp in card.select("span"):
            txt = sp.get_text(strip=True)
            if txt and len(txt) < 45 and "ago" not in txt.lower() and txt != title:
                source = txt
                break

        # Extract image
        img = card.select_one("img")
        img = clean_img_url(img.get("src")) if img else None

        return {
            "title": title,
            "link": link,
            "media": source or category,
            "date": date_text,
            "datetime": dt,
            "img": img,
            "search_category": category,
        }

    def select_cards(self, soup):
        """Select article cards using multiple selectors"""
        selectors = ["article", "c-wiz[jsrenderer]", "div.Vd5Uad", "div.SoaBEf", "div.XlKvRb"]
        for sel in selectors:
            cards = soup.select(sel)
            if cards:
                return cards
        return []

    def search_single_query(self, query, category):
        """Search Google News for a single query with date filtering"""
        print(f"\n=== Searching: {category} ===")

        # Build URL with date range
        today = datetime.now()
        start_date = today - timedelta(hours=self.hours)
        
        # Use Google's date range format: after:YYYY-MM-DD
        date_filter = f" after:{start_date.strftime('%Y-%m-%d')}"
        full_query = query + date_filter
        
        encoded = urllib.parse.quote(full_query)
        url = f"https://news.google.com/search?q={encoded}&hl={self.lang}&gl={self.gl}&ceid={self.ceid}"

        try:
            req = urllib.request.Request(url, headers=self.headers)
            html = urllib.request.urlopen(req, timeout=30).read()
            soup = Soup(html, "html.parser")
            cards = self.select_cards(soup)

            out = []
            seen_titles = set()

            for c in cards[:20]:  # Check more since we filter by time
                article = self.parse_article(c, category)
                if article:
                    title_key = article['title'].lower().strip()
                    if title_key in seen_titles:
                        continue
                    seen_titles.add(title_key)
                    
                    print(f"  ✓ [{article['date']}] {article['title'][:55]}...")
                    out.append(article)
                    
                    if len(out) >= 8:
                        break

            print(f"  → {len(out)} articles within {self.hours}h")
            return out

        except Exception as e:
            print(f"  ✗ Error: {e}")
            return []

    def run_all_searches(self, queries=None):
        """Run all searches from the query list"""
        if queries is None:
            queries = SEARCH_QUERIES

        print(f"{'='*60}")
        print(f"GOOGLE NEWS SCRAPER")
        print(f"Queries: {len(queries)} | Time window: {self.hours} hours")
        print(f"{'='*60}")

        all_articles = []

        for query, search_name in queries:
            articles = self.search_single_query(query, search_name)
            all_articles.extend(articles)
            time.sleep(random.uniform(0.4, 1.0))

        unique_articles = self.remove_duplicates(all_articles)
        
        # Sort by datetime (newest first)
        unique_articles.sort(key=lambda x: x.get('datetime') or datetime.min, reverse=True)

        print(f"\n{'='*60}")
        print(f"RESULTS: {len(all_articles)} total → {len(unique_articles)} unique")
        print(f"{'='*60}")

        # Category breakdown
        categories = {}
        for article in unique_articles:
            cat = article.get('search_category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1

        print(f"\nTop categories:")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1])[:20]:
            print(f"  {cat}: {count}")
        
        # Source breakdown
        sources = {}
        for article in unique_articles:
            src = article.get('media', 'Unknown')
            sources[src] = sources.get(src, 0) + 1
        
        print(f"\nTop sources:")
        for src, count in sorted(sources.items(), key=lambda x: -x[1])[:15]:
            print(f"  {src}: {count}")

        self.all_results = unique_articles
        return unique_articles

    def remove_duplicates(self, articles):
        """Remove duplicate articles based on title similarity and URL"""
        if not articles:
            return []

        unique_articles = []
        seen_titles = set()
        seen_urls = set()

        for article in articles:
            url_key = article['link'].lower().strip() if article.get('link') else ""
            if url_key and url_key in seen_urls:
                continue
            
            title = article['title'].lower().strip()
            title_words = set(title.split())

            is_duplicate = False
            for seen_title in seen_titles:
                seen_words = set(seen_title.split())
                if len(title_words) > 0 and len(seen_words) > 0:
                    similarity = len(title_words.intersection(seen_words)) / max(len(title_words), len(seen_words))
                    if similarity > 0.7:
                        is_duplicate = True
                        break

            if not is_duplicate:
                seen_titles.add(title)
                if url_key:
                    seen_urls.add(url_key)
                unique_articles.append(article)

        return unique_articles


def scrape_google_news(hours=48):
    """Main scraping function
    
    Args:
        hours: Time window for articles (default 48 hours)
    
    Returns:
        List of formatted article dictionaries
    """
    searcher = MultiSearchGoogleNews(hours=hours)
    articles = searcher.run_all_searches()

    formatted_articles = []
    for article in articles:
        formatted_articles.append({
            "Title": article['title'],
            "Link": article['link'] or "https://news.google.com",
            "Source": article['media'] or "Google News",
            "Published": article['date'] or "Recent",
            "Datetime": article['datetime'].isoformat() if article.get('datetime') else None,
            "Category": article.get('search_category', 'General'),
            "img": article.get('img'),
            "Scraped_At": datetime.now().isoformat()
        })

    return formatted_articles


def save_to_csv(news):
    """Save news data to CSV and JSON files"""
    if not news:
        print("No news data to save.")
        with open("data/latest_news.json", "w") as f:
            json.dump([], f)
        return None

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"data/google_news_{timestamp}.csv"
    df = pd.DataFrame(news)
    df.to_csv(filename, index=False)
    df.to_csv("data/latest_news.csv", index=False)

    with open("data/latest_news.json", "w", encoding="utf-8") as f:
        json.dump(news, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(news)} articles to {filename}")
    return filename


def main(hours=48):
    """Main function to run the scraper
    
    Args:
        hours: Time window for articles (default 48 hours)
    """
    print("=" * 60)
    print("COMPREHENSIVE CYBER NEWS SCRAPER")
    print(f"Sources: {len(SEARCH_QUERIES)} queries")
    print(f"Time window: {hours} hours")
    print("=" * 60)

    try:
        news = scrape_google_news(hours=hours)

        if news:
            save_to_csv(news)
            print(f"\n✓ Successfully processed {len(news)} unique articles")

            print(f"\n{'='*60}")
            print("LATEST ARTICLES:")
            print(f"{'='*60}")
            for i, article in enumerate(news[:15]):
                print(f"\n{i+1}. {article['Title']}")
                print(f"   Source: {article['Source']} | {article['Published']}")
                print(f"   Category: {article['Category']}")

            if len(news) > 15:
                print(f"\n... and {len(news) - 15} more articles")

        else:
            print("No articles found within the time window!")
            with open("data/latest_news.json", "w") as f:
                json.dump([], f)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        with open("data/latest_news.json", "w") as f:
            json.dump([], f)


if __name__ == "__main__":
    # Run with 48-hour window (adjust as needed: 24, 48, 72)
    main(hours=48)
