#!/usr/bin/env python3
"""
Drone News Newsletter Generator - GitHub-Only Version
Creates professional GitHub Pages intelligence briefing
"""

import json
import os
from datetime import datetime

print("📰 DRONE NEWS NEWSLETTER GENERATOR")
print("🌐 GitHub Pages Compatible")
print("=" * 60)

def load_intelligence_data():
    """Load intelligence data from JSON file"""
    
    try:
        if os.path.exists("data/latest_news.json"):
            with open("data/latest_news.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"✅ Loaded {len(data)} intelligence reports")
            return data
        else:
            print("⚠️ No intelligence data file found")
            return []
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return []

def organize_by_categories(articles):
    """Organize articles into categories"""
    
    categories = {}
    
    for article in articles:
        category = article.get('Category', '📄 General Intelligence')
        
        if category not in categories:
            categories[category] = []
        categories[category].append(article)
    
    # Sort categories by importance and article count
    priority_categories = [
        '🎯 Military Drones',
        '🇨🇳 China Drones', 
        '🇷🇺 Russia Drones',
        '🤖 Autonomous Drones',
        '⚔️ Drone Warfare',
        '💥 Drone Strikes'
    ]
    
    sorted_categories = {}
    
    # Add priority categories first
    for cat in priority_categories:
        if cat in categories:
            sorted_categories[cat] = categories[cat]
    
    # Add remaining categories by article count
    remaining = {k: v for k, v in categories.items() if k not in priority_categories}
    for cat in sorted(remaining.keys(), key=lambda x: len(remaining[x]), reverse=True):
        sorted_categories[cat] = remaining[cat]
    
    print(f"📂 Organized into {len(sorted_categories)} categories")
    return sorted_categories

def generate_html_newsletter(articles, categories):
    """Generate HTML newsletter for GitHub Pages"""
    
    # Get repository name from environment or use default
    repo_name = os.environ.get('GITHUB_REPOSITORY', 'user/Drone_news')
    
    # Current date and stats
    current_date = datetime.now()
    date_str = current_date.strftime("%B %d, %Y")
    time_str = current_date.strftime("%H:%M UTC")
    
    total_articles = len(articles)
    military_articles = sum(len(arts) for cat, arts in categories.items() 
                           if any(term in cat.lower() for term in ['military', 'combat', 'warfare', 'strike']))
    geopolitical_articles = sum(len(arts) for cat, arts in categories.items() 
                               if any(term in cat.lower() for term in ['china', 'russia', 'iran', 'dprk', 'ukraine']))
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drone News Brief - {date_str}</title>
    <meta name="description" content="Latest drone intelligence from {total_articles} sources">
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
            margin-top: 20px;
            margin-bottom: 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
            position: relative;
        }}
        
        .header h1 {{
            font-size: 3.5em;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header .subtitle {{
            font-size: 1.3em;
            opacity: 0.9;
            margin-bottom: 20px;
        }}
        
        .github-link {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 15px;
            border-radius: 20px;
            text-decoration: none;
            color: white;
            font-size: 0.9em;
        }}
        
        .stats {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            text-align: center;
        }}
        
        .stat-card {{
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            opacity: 0.9;
        }}
        
        .category-section {{
            margin: 0;
        }}
        
        .category-header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 20px 40px;
            font-size: 1.4em;
            font-weight: 600;
            border-left: 5px solid #ffd700;
        }}
        
        .articles-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            padding: 30px 40px;
            background: #f8f9fa;
        }}
        
        .article-card {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 1px solid #e9ecef;
        }}
        
        .article-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }}
        
        .article-header {{
            width: 100%;
            height: 120px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2em;
        }}
        
        .article-content {{
            padding: 25px;
        }}
        
        .article-title {{
            font-size: 1.2em;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 15px;
            line-height: 1.4;
        }}
        
        .article-title a {{
            color: inherit;
            text-decoration: none;
        }}
        
        .article-title a:hover {{
            color: #1e3c72;
        }}
        
        .article-meta {{
            display: flex;
            justify-content: space-between;
            color: #6c757d;
            font-size: 0.9em;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .source-tag {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
        }}
        
        .no-data {{
            text-align: center;
            padding: 60px 40px;
            color: #6c757d;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 30px;
            font-size: 0.9em;
        }}
        
        .footer a {{
            color: #ffd700;
            text-decoration: none;
        }}
        
        @media (max-width: 768px) {{
            .container {{ margin: 10px; }}
            .header h1 {{ font-size: 2.5em; }}
            .stats {{ grid-template-columns: 1fr; }}
            .articles-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="https://github.com/{repo_name}" class="github-link">
                📊 GitHub Repository
            </a>
            <h1>🚁 Drone News Brief</h1>
            <div class="subtitle">Comprehensive Drone Intelligence Collection</div>
            <div>
                <strong>{date_str}</strong> • Generated at {time_str}
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{total_articles}</div>
                <div class="stat-label">News Reports</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{military_articles}</div>
                <div class="stat-label">Military & Defense</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{geopolitical_articles}</div>
                <div class="stat-label">Geopolitical</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(categories)}</div>
                <div class="stat-label">Categories</div>
            </div>
        </div>
'''

    # Add categories and articles
    if categories:
        for category, category_articles in categories.items():
            # Get emoji for visual representation
            emoji = category.split()[0] if category.split() else '🚁'
            
            html += f'''
        <div class="category-section">
            <div class="category-header">
                {category} ({len(category_articles)} reports)
            </div>
            <div class="articles-grid">'''
            
            # Show up to 6 articles per category
            for article in category_articles[:6]:
                title = article.get('Title', 'News Report')
                source = article.get('Source', 'News Source')
                published = article.get('Published', 'Recent')
                link = article.get('Link', '#')
                
                html += f'''
                <div class="article-card">
                    <div class="article-header">
                        <span>{emoji}</span>
                    </div>
                    <div class="article-content">
                        <div class="article-title">
                            <a href="{link}" target="_blank">{title}</a>
                        </div>
                        <div class="article-meta">
                            <span class="source-tag">{source}</span>
                            <span>{published}</span>
                        </div>
                    </div>
                </div>'''
            
            html += '''
            </div>
        </div>'''
    else:
        html += '''
        <div class="no-data">
            <h3>🔄 News Collection in Progress</h3>
            <p>The system is currently collecting drone news data.</p>
            <p>Check back in a few minutes for the latest reports.</p>
        </div>'''
    
    # Add footer
    html += f'''
        <div class="footer">
            <p>
                <strong>🚁 Drone News Collection System</strong> • 
                <a href="https://github.com/{repo_name}">Open Source Project</a>
            </p>
            <p style="margin-top: 10px; opacity: 0.8;">
                Automated collection every 6 hours • 
                {len(articles)} reports processed • 
                Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
            </p>
        </div>
    </div>
    
    <script>
        console.log('🚁 Drone News Brief loaded');
        console.log('📊 Stats: {{total: {total_articles}, categories: {len(categories)}}}');
    </script>
</body>
</html>'''
    
    return html

def save_newsletter(html_content):
    """Save newsletter to docs folder for GitHub Pages"""
    
    try:
        os.makedirs("docs", exist_ok=True)
        
        with open("docs/index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ Newsletter saved to docs/index.html")
        return True
        
    except Exception as e:
        print(f"❌ Error saving newsletter: {e}")
        return False

def main():
    """Main newsletter generation function"""
    
    try:
        # Load intelligence data
        articles = load_intelligence_data()
        
        # Organize by categories
        categories = organize_by_categories(articles)
        
        # Generate HTML
        html = generate_html_newsletter(articles, categories)
        
        # Save newsletter
        if save_newsletter(html):
            print(f"🎉 Newsletter generated successfully!")
            print(f"📊 {len(articles)} news reports processed")
            print(f"📂 {len(categories)} categories organized")
            print(f"🌐 Ready for GitHub Pages d
