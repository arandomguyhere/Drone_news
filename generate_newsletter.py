#!/usr/bin/env python3
"""
Drone Intelligence Newsletter Generator
GitHub Pages & Actions Compatible Version
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_intelligence_data():
    """Load the latest intelligence data for GitHub Pages"""
    json_file = "data/latest_news.json"
    
    print(f"📁 Loading intelligence data from {json_file}")
    
    try:
        if os.path.exists(json_file):
            file_size = os.path.getsize(json_file)
            print(f"📊 File size: {file_size:,} bytes")
            
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            print(f"✅ Loaded {len(data)} intelligence reports")
            return data
        else:
            print(f"⚠️ File not found: {json_file}")
            return []
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return []

def categorize_articles(articles):
    """Group articles by intelligence category for GitHub Pages display"""
    categories = {}
    
    # Enhanced category mappings with emojis for GitHub Pages
    category_mappings = [
        # Military and Defense (highest priority)
        (['military', 'warfare', 'strike', 'combat', 'defense', 'weapon', 'armed'], '🎯 Military & Defense'),
        (['autonomous', 'ai', 'artificial intelligence', 'swarm', 'ml', 'machine learning'], '🤖 Autonomous Systems'),
        (['china', 'chinese', 'russia', 'russian', 'iran', 'iranian', 'north korea', 'dprk'], '🌍 Geopolitical Intelligence'),
        (['counter', 'anti-drone', 'defense', 'c-uas', 'jammer'], '🛡️ Counter-Drone Technology'),
        
        # Commercial and Civilian
        (['delivery', 'commercial', 'civilian', 'agriculture', 'agri', 'farm'], '📦 Commercial & Civilian'),
        (['surveillance', 'security', 'monitoring', 'reconnaissance', 'isr'], '👁️ Surveillance & Security'),
        (['regulation', 'faa', 'regulatory', 'legal', 'law', 'policy'], '📋 Regulation & Policy'),
        
        # Technical categories
        (['fpv', 'first person'], '🎮 FPV Systems'),
        (['vtol', 'vertical takeoff'], '🚁 VTOL Aircraft'),
        (['quadcopter', 'multirotor'], '🔄 Quadcopters'),
        (['stealth', 'invisible'], '👻 Stealth Technology'),
        (['electronic', 'cyber', '5g', 'communication'], '📡 Electronic Systems'),
        
        # News sources
        (['janes', 'defense news', 'warzone', 'breaking defense'], '📰 Defense Publications'),
        (['reuters', 'bloomberg', 'cnn', 'bbc', 'wsj', 'financial times'], '📺 Major News'),
        (['wired', 'techcrunch', 'ars technica'], '💻 Tech Publications'),
        
        # Geographic/Country specific
        (['israel', 'turkey', 'ukraine', 'usa', 'america'], '🌐 Regional Intelligence'),
        
        # Default categories
        (['uav', 'uas'], '🛩️ UAV/UAS Systems'),
        (['drone'], '🚁 General Drones'),
    ]
    
    for article in articles:
        title = article.get('Title', '').lower()
        category_name = article.get('Category', '').lower()
        source = article.get('Source', '').lower()
        
        # Combine all text for categorization
        combined_text = f"{title} {category_name} {source}"
        
        # Find the first matching category
        assigned_category = None
        for keywords, category in category_mappings:
            if any(keyword in combined_text for keyword in keywords):
                assigned_category = category
                break
        
        # Default category if no match
        if not assigned_category:
            assigned_category = '📄 General Intelligence'
        
        # Add to category
        if assigned_category not in categories:
            categories[assigned_category] = []
        categories[assigned_category].append(article)
    
    # Sort categories by priority and article count
    priority_order = [
        '🎯 Military & Defense',
        '🤖 Autonomous Systems', 
        '🌍 Geopolitical Intelligence',
        '🛡️ Counter-Drone Technology',
        '📦 Commercial & Civilian',
        '👁️ Surveillance & Security',
        '📋 Regulation & Policy'
    ]
    
    sorted_categories = {}
    
    # Add priority categories first
    for category in priority_order:
        if category in categories:
            sorted_categories[category] = categories[category]
    
    # Add remaining categories sorted by article count
    remaining = {k: v for k, v in categories.items() if k not in priority_order}
    for category in sorted(remaining.keys(), key=lambda x: len(remaining[x]), reverse=True):
        sorted_categories[category] = remaining[category]
    
    return sorted_categories

def generate_github_pages_newsletter():
    """Generate HTML intelligence newsletter optimized for GitHub Pages"""
    
    print("📰 GENERATING DRONE INTELLIGENCE NEWSLETTER")
    print("🌐 Optimized for GitHub Pages deployment")
    print("=" * 60)
    
    # Load data
    articles = load_intelligence_data()
    
    if not articles:
        print("⚠️ No articles found - generating empty newsletter")
    
    # Categorize articles
    categories = categorize_articles(articles)
    print(f"📂 Organized into {len(categories)} categories")
    
    # Generate newsletter
    current_date = datetime.now()
    date_formatted = current_date.strftime("%B %d, %Y")
    time_formatted = current_date.strftime("%H:%M UTC")
    
    # Calculate summary statistics
    total_articles = len(articles)
    military_articles = sum(len(arts) for cat, arts in categories.items() 
                          if any(term in cat.lower() for term in ['military', 'warfare', 'defense', 'combat']))
    commercial_articles = sum(len(arts) for cat, arts in categories.items() 
                            if any(term in cat.lower() for term in ['commercial', 'civilian', 'delivery']))
    geopolitical_articles = sum(len(arts) for cat, arts in categories.items() 
                              if any(term in cat.lower() for term in ['geopolitical', 'china', 'russia', 'iran']))
    
    # GitHub Pages compatible HTML with enhanced features
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drone Intelligence Brief - {date_formatted}</title>
    <meta name="description" content="Comprehensive drone intelligence collection and analysis from {len(articles)} sources">
    <meta name="keywords" content="drone intelligence, UAV, UAS, military drones, defense news, autonomous systems">
    
    <!-- GitHub Pages SEO -->
    <meta property="og:title" content="Drone Intelligence Brief - {date_formatted}">
    <meta property="og:description" content="Latest drone intelligence from {len(articles)} sources across military, commercial, and geopolitical domains">
    <meta property="og:type" content="website">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .github-corner {{
            position: fixed;
            top: 0;
            right: 0;
            z-index: 1000;
        }}
        
        .github-corner svg {{
            fill: #1e3c72;
            color: #fff;
            width: 80px;
            height: 80px;
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
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="drone" patternUnits="userSpaceOnUse" width="20" height="20"><circle cx="10" cy="10" r="2" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23drone)"/></svg>');
            animation: float 20s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-10px) rotate(180deg); }}
        }}
        
        .header h1 {{
            font-size: 3.5em;
            font-weight: 700;
            margin-bottom: 10px;
            position: relative;
            z-index: 2;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header .subtitle {{
            font-size: 1.3em;
            opacity: 0.9;
            position: relative;
            z-index: 2;
            font-weight: 300;
            margin-bottom: 20px;
        }}
        
        .header .date-info {{
            font-size: 1.1em;
            position: relative;
            z-index: 2;
        }}
        
        .github-badge {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            z-index: 3;
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
            transition: transform 0.3s ease;
        }}
        
        .summary-card:hover {{
            transform: translateY(-5px);
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
            position: relative;
            cursor: pointer;
            transition: background 0.3s ease;
        }}
        
        .category-header:hover {{
            background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
        }}
        
        .category-toggle {{
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1.2em;
            transition: transform 0.3s ease;
        }}
        
        .category-content {{
            max-height: 1000px;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }}
        
        .category-content.collapsed {{
            max-height: 0;
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
            height: 180px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2em;
            position: relative;
            overflow: hidden;
        }}
        
        .article-image img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
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
            transition: color 0.3s ease;
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
        
        .read-more {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            font-weight: 500;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
        }}
        
        .read-more:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
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
        
        .stats-bar {{
            background: rgba(0,0,0,0.1);
            padding: 15px 40px;
            font-size: 0.9em;
            text-align: center;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                margin: 10px;
                border-radius: 10px;
            }}
            
            .header h1 {{
                font-size: 2.5em;
            }}
            
            .summary {{
                grid-template-columns: 1fr;
                padding: 20px;
            }}
            
            .articles-grid {{
                grid-template-columns: 1fr;
                padding: 20px;
            }}
            
            .category-header {{
                padding: 15px 20px;
            }}
        }}
    </style>
</head>
<body>
    <!-- GitHub Corner -->
    <a href="https://github.com/yourusername/drone-intelligence-system" class="github-corner" aria-label="View source on GitHub">
        <svg viewBox="0 0 250 250" aria-hidden="true">
            <path d="m0,0 0,250 250,0 0,-250z" fill="currentColor"/>
            <path d="m127.5,110c-21.4,0-39,17.6-39,39 0,17.2 11.2,31.8 26.8,37 2,0.4 2.7,-0.9 2.7,-2 0,-1 0,-3.7 0,-7.3 -10.8,2.4-13.1,-5.2-13.1,-5.2 -1.8,-4.5-4.4,-5.7-4.4,-5.7 -3.6,-2.5 0.3,-2.4 0.3,-2.4 4,0.3 6.1,4.1 6.1,4.1 3.5,6 9.2,4.3 11.5,3.3 0.4,-2.6 1.4,-4.3 2.5,-5.3 -8.7,-1-17.8,-4.4-17.8,-19.4 0,-4.3 1.5,-7.8 4,-10.5 -0.4,-1 -1.7,-5 0.4,-10.5 0,0 3.3,-1.1 10.8,4 3.1,-0.9 6.5,-1.3 9.8,-1.3 3.3,0 6.7,0.4 9.8,1.3 7.5,-5.1 10.8,-4 10.8,-4 2.1,5.5 0.8,9.5 0.4,10.5 2.5,2.7 4,6.2 4,10.5 0,15 -9.1,18.4-17.8,19.4 1.4,1.2 2.7,3.6 2.7,7.3 0,5.3 0,9.5 0,10.8 0,1.1 0.7,2.4 2.7,2 15.6,-5.2 26.8,-19.8 26.8,-37 0,-21.4-17.6,-39-39,-39z" fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"/>
        </svg>
    </a>

    <div class="container">
        <div class="header">
            <div class="github-badge">🔗 GitHub Pages</div>
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
                <div class="summary-number">{military_articles}</div>
                <div class="summary-label">Military & Defense</div>
            </div>
            <div class="summary-card">
                <div class="summary-number">{geopolitical_articles}</div>
                <div class="summary-label">Geopolitical</div>
            </div>
            <div class="summary-card">
                <div class="summary-number">{len(categories)}</div>
                <div class="summary-label">Categories</div>
            </div>
        </div>"""

    # Generate category sections
    if categories:
        for category, category_articles in categories.items():
            # Get category emoji for default image
            category_emoji = category.split()[0] if any(category.startswith(prefix) for prefix in ['🎯', '🤖', '🌍', '🛡️', '📦', '👁️', '📋', '🎮', '🚁', '🔄', '📰', '📺', '💻', '🌐', '🛩️', '📄']) else '🚁'
            
            html_content += f"""
        <div class="category-section">
            <div class="category-header" onclick="toggleCategory(this)">
                {category} ({len(category_articles)} reports)
                <span class="category-toggle">▼</span>
            </div>
            <div class="category-content">
                <div class="articles-grid">"""
            
            for article in category_articles[:6]:  # Show max 6 per category for GitHub Pages performance
                title = article.get('Title', 'No Title')
                source = article.get('Source', 'Unknown Source')
                published = article.get('Published', 'Unknown Date')
                link = article.get('Link', '#')
                img_url = article.get('Image')
                
                # Ensure safe links for GitHub Pages
                if not link.startswith('http'):
                    link = '#'
                
                html_content += f"""
                    <div class="article-card">
                        <div class="article-image">
                            {f'<img src="{img_url}" alt="Article Image">' if img_url else f'<span>{category_emoji}</span>'}
                        </div>
                        <div class="article-content">
                            <div class="article-title">
                                <a href="{link}" target="_blank" rel="noopener noreferrer">{title}</a>
                            </div>
                            <div class="article-meta">
                                <span class="source-badge">{source}</span>
                                <span>{published}</span>
                            </div>
                            <a href="{link}" target="_blank" rel="noopener noreferrer" class="read-more">
                                Read Full Report →
                            </a>
                        </div>
                    </div>"""
            
            html_content += """
                </div>
            </div>
        </div>"""
    else:
        html_content += """
        <div class="no-articles">
            <h3>🔍 No Intelligence Reports Available</h3>
            <p>No drone intelligence has been collected in this session. The system will retry on the next scheduled run.</p>
            <p>Check the <a href="https://github.com/yourusername/drone-intelligence-system/actions">GitHub Actions</a> for collection status.</p>
        </div>"""
    
    html_content += f"""
        <div class="stats-bar">
            Automated collection system • 
            Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} • 
            Next update: Every 6 hours via GitHub Actions
        </div>
        
        <div class="footer">
            <p>
                <strong>🚁 Drone Intelligence Collection System</strong> • 
                <a href="https://github.com/yourusername/drone-intelligence-system">Open Source Intelligence Platform</a>
            </p>
            <p style="margin-top: 10px; opacity: 0.8;">
                {len(articles)} intelligence reports processed from {len(set(article.get('Source', '') for article in articles))} sources • 
                Deployed on GitHub Pages
            </p>
        </div>
    </div>
    
    <script>
        // GitHub Pages compatible JavaScript
        function toggleCategory(header) {{
            const content = header.nextElementSibling;
            const toggle = header.querySelector('.category-toggle');
            
            if (content.classList.contains('collapsed')) {{
                content.classList.remove('collapsed');
                toggle.textContent = '▼';
            }} else {{
                content.classList.add('collapsed');
                toggle.textContent = '▶';
            }}
        }}
        
        // Analytics for GitHub Pages
        console.log('🚁 Drone Intelligence Brief loaded');
        console.log('📊 Statistics:', {{
            total_articles: {total_articles},
            categories: {len(categories)},
            military_reports: {military_articles},
            geopolitical_reports: {geopolitical_articles},
            timestamp: '{datetime.now().isoformat()}'
        }});
        
        // Add smooth scrolling for internal links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth'
                    }});
                }}
            }});
        }});
        
        // GitHub Pages deployment info
        if (window.location.hostname.includes('github.io')) {{
            console.log('🌐 Deployed on GitHub Pages');
            console.log('🔗 Repository: https://github.com/yourusername/drone-intelligence-system');
        }}
    </script>
</body>
</html>"""
    
    # Save newsletter for GitHub Pages
    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ GitHub Pages newsletter generated!")
    print(f"📊 Processed {len(articles)} intelligence reports")
    print(f"📂 Organized into {len(categories)} categories")
    print(f"💾 Saved to: docs/index.html")
    print(f"🌐 GitHub Pages URL: https://yourusername.github.io/drone-intelligence-system/")
    
    # Generate summary for GitHub Actions
    if categories:
        print(f"\n📈 Category Summary:")
        for cat, arts in list(categories.items())[:5]:
            print(f"  • {cat}: {len(arts)} reports")
    
    return len(articles)

if __name__ == "__main__":
    generate_github_pages_newsletter()
