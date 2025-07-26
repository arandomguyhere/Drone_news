#!/usr/bin/env python3
"""
Simplified Drone Intelligence Newsletter Generator
GitHub Actions Compatible - Error Resistant Version
"""

import json
import os
from datetime import datetime

def load_data():
    """Load intelligence data with error handling"""
    
    print("📁 Loading intelligence data...")
    
    try:
        data_file = "data/latest_news.json"
        
        if os.path.exists(data_file):
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"✅ Loaded {len(data)} intelligence reports")
            return data
        else:
            print("⚠️ No data file found, using empty dataset")
            return []
            
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return []

def categorize_articles(articles):
    """Simple categorization of articles"""
    
    categories = {}
    
    for article in articles:
        # Get category from article or determine from content
        category = article.get('Category', '📄 General Intelligence')
        
        # Clean up category name
        if not category.startswith(('🚁', '🎯', '🤖', '🌍', '🛡️', '📦', '👁️', '📋', '🎮', '🔄', '📰', '📺', '💻', '🌐', '🛩️', '📄')):
            category = f"📄 {category}"
        
        if category not in categories:
            categories[category] = []
        categories[category].append(article)
    
    print(f"📂 Organized into {len(categories)} categories")
    return categories

def generate_html(articles, categories):
    """Generate HTML newsletter"""
    
    current_date = datetime.now()
    date_formatted = current_date.strftime("%B %d, %Y")
    time_formatted = current_date.strftime("%H:%M UTC")
    
    # Calculate statistics
    total_articles = len(articles)
    military_count = sum(len(arts) for cat, arts in categories.items() 
                        if any(term in cat.lower() for term in ['military', 'combat', 'warfare']))
    commercial_count = sum(len(arts) for cat, arts in categories.items() 
                          if any(term in cat.lower() for term in ['commercial', 'delivery', 'civilian']))
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drone Intelligence Brief - {date_formatted}</title>
    <meta name="description" content="Comprehensive drone intelligence collection from {len(articles)} sources">
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
            font-weight: 300;
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
        
        .summary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            text-align: center;
        }}
        
        .summary-card {{
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        .summary-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }}
        
        .summary-label {{
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
        
        .article-image {{
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
            align-items: center;
            color: #6c757d;
            font-size: 0.9em;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .source-badge {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 500;
        }}
        
        .no-articles {{
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
            .container {{ margin: 10px; border-radius: 10px; }}
            .header h1 {{ font-size: 2.5em; }}
            .summary {{ grid-template-columns: 1fr; padding: 20px; }}
            .articles-grid {{ grid-template-columns: 1fr; padding: 20px; }}
            .category-header {{ padding: 15px 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="https://github.com/arandomguyhere/drone-intelligence-system" class="github-link">
                🔗 GitHub Repository
            </a>
            <h1>🚁 Drone Intelligence Brief</h1>
            <div class="subtitle">Comprehensive UAV/UAS Intelligence Collection & Analysis</div>
            <div class="date-info">
                <strong>{date_formatted}</strong> • Generated at {time_formatted}
            </div>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <div class="summary-number">{total_articles}</div>
                <div class="summary-label">Intelligence Reports</div>
            </div>
            <div class="summary-card">
                <div class="summary-number">{military_count}</div>
                <div class="summary-label">Military & Defense</div>
            </div>
            <div class="summary-card">
                <div class="summary-number">{commercial_count}</div>
                <div class="summary-label">Commercial & Civilian</div>
            </div>
            <div class="summary-card">
                <div class="summary-number">{len(categories)}</div>
                <div class="summary-label">Categories</div>
            </div>
        </div>
"""

    # Add categories and articles
    if categories:
        for category, category_articles in categories.items():
            # Get emoji for category
            emoji = category.split()[0] if category.split() else '🚁'
            
            html += f"""
        <div class="category-section">
            <div class="category-header">
                {category} ({len(category_articles)} reports)
            </div>
            <div class="articles-grid">"""
            
            # Show up to 6 articles per category
            for article in category_articles[:6]:
                title = article.get('Title', 'No Title')
                source = article.get('Source', 'Unknown Source')
                published = article.get('Published', 'Unknown Date')
                link = article.get('Link', '#')
                
                # Ensure safe links
                if not link.startswith('http'):
                    link = '#'
                
                html += f"""
                <div class="article-card">
                    <div class="article-image">
                        <span>{emoji}</span>
                    </div>
                    <div class="article-content">
                        <div class="article-title">
                            <a href="{link}" target="_blank" rel="noopener noreferrer">{title}</a>
                        </div>
                        <div class="article-meta">
                            <span class="source-badge">{source}</span>
                            <span>{published}</span>
                        </div>
                    </div>
                </div>"""
            
            html += """
            </div>
        </div>"""
    else:
        html += """
        <div class="no-articles">
            <h3>🔍 No Intelligence Reports Available</h3>
            <p>Intelligence collection is in progress. The system will update automatically every 6 hours.</p>
            <p>Check the <a href="https://github.com/arandomguyhere/drone-intelligence-system/actions">GitHub Actions</a> for collection status.</p>
        </div>"""
    
    # Footer
    html += f"""
        <div class="footer">
            <p>
                <strong>🚁 Drone Intelligence Collection System</strong> • 
                <a href="https://github.com/arandomguyhere/drone-intelligence-system">Open Source Intelligence Platform</a>
            </p>
            <p style="margin-top: 10px; opacity: 0.8;">
                Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} • 
                {len(articles)} intelligence reports processed • 
                Automated collection every 6 hours
            </p>
        </div>
    </div>
    
    <script>
        console.log('🚁 Drone Intelligence Brief loaded');
        console.log('📊 Statistics:', {{
            total_articles: {total_articles},
            categories: {len(categories)},
            timestamp: '{datetime.now().isoformat()}'
        }});
    </script>
</body>
</html>"""
    
    return html

def save_newsletter(html):
    """Save HTML newsletter"""
    
    try:
        os.makedirs("docs", exist_ok=True)
        
        with open("docs/index.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        print("✅ Newsletter saved to docs/index.html")
        return True
        
    except Exception as e:
        print(f"❌ Error saving newsletter: {e}")
        return False

def main():
    """Main function"""
    
    print("📰 DRONE INTELLIGENCE NEWSLETTER GENERATOR")
    print("🌐 GitHub Pages Compatible")
    print("=" * 60)
    
    try:
        # Load data
        articles = load_data()
        
        # Categorize
        categories = categorize_articles(articles)
        
        # Generate HTML
        html = generate_html(articles, categories)
        
        # Save newsletter
        if save_newsletter(html):
            print(f"🎉 Newsletter generated successfully!")
            print(f"📊 Processed {len(articles)} intelligence reports")
            print(f"📂 Organized into {len(categories)} categories")
            print(f"🌐 Ready for GitHub Pages deployment")
            
            if categories:
                print(f"\n📈 Category Summary:")
                for cat, arts in list(categories.items())[:5]:
                    print(f"  • {cat}: {len(arts)} reports")
        else:
            print("❌ Newsletter generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        # Create minimal newsletter as fallback
        try:
            minimal_html = f"""<!DOCTYPE html>
<html><head><title>Drone Intelligence Brief</title></head>
<body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
<h1>🚁 Drone Intelligence Brief</h1>
<p>Intelligence collection system is initializing. Please check back later.</p>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</p>
<p><a href="https://github.com/arandomguyhere/drone-intelligence-system">View Repository</a></p>
</body></html>"""
            
            os.makedirs("docs", exist_ok=True)
            with open("docs/index.html", "w", encoding="utf-8") as f:
                f.write(minimal_html)
            print("📄 Created minimal newsletter as fallback")
        except:
            pass
        
        return False

if __name__ == "__main__":
    main()
