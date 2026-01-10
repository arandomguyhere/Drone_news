#!/usr/bin/env python3
"""
Cybersecurity News Briefing Generator
"""

import json
import os
from datetime import datetime

def load_data():
    """Load news data from JSON file"""
    try:
        if os.path.exists("data/latest_news.json"):
            with open("data/latest_news.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"Loaded {len(data)} articles")
            return data
        else:
            print("No data file found")
            return []
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

def organize_by_categories(articles):
    """Organize articles into categories"""
    categories = {}

    for article in articles:
        category = article.get('Category', 'General')
        if category not in categories:
            categories[category] = []
        categories[category].append(article)

    # Sort by article count
    return dict(sorted(categories.items(), key=lambda x: len(x[1]), reverse=True))

def generate_html(articles, categories):
    """Generate HTML briefing"""

    repo_name = os.environ.get('GITHUB_REPOSITORY', 'arandomguyhere/Drone_news')
    current_date = datetime.now()
    date_str = current_date.strftime("%B %d, %Y")
    time_str = current_date.strftime("%H:%M UTC")

    total = len(articles)
    num_categories = len(categories)
    sources = len(set(a.get('Source', '') for a in articles))

    # Count threat intel articles
    threat_keywords = ['apt', 'ransomware', 'malware', 'breach', 'attack', 'hack', 'vulnerability', 'exploit']
    threat_count = sum(1 for a in articles if any(k in a.get('Title', '').lower() for k in threat_keywords))

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber News - {date_str}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            line-height: 1.5;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            border-bottom: 1px solid #222;
            padding: 30px 0;
            margin-bottom: 30px;
        }}

        header h1 {{
            font-size: 2em;
            font-weight: 600;
            color: #fff;
            margin-bottom: 8px;
        }}

        header .meta {{
            color: #888;
            font-size: 0.9em;
        }}

        header .meta a {{
            color: #4ade80;
            text-decoration: none;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 40px;
        }}

        .stat {{
            background: #111;
            border: 1px solid #222;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}

        .stat-value {{
            font-size: 2em;
            font-weight: 700;
            color: #4ade80;
        }}

        .stat-label {{
            font-size: 0.8em;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 5px;
        }}

        .category {{
            margin-bottom: 40px;
        }}

        .category-title {{
            font-size: 1.1em;
            font-weight: 600;
            color: #fff;
            padding: 12px 0;
            border-bottom: 1px solid #222;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .category-count {{
            font-size: 0.8em;
            color: #888;
            font-weight: 400;
        }}

        .articles {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 15px;
        }}

        .article {{
            background: #111;
            border: 1px solid #222;
            border-radius: 8px;
            padding: 18px;
            transition: border-color 0.2s;
        }}

        .article:hover {{
            border-color: #333;
        }}

        .article-title {{
            font-weight: 500;
            margin-bottom: 12px;
            line-height: 1.4;
        }}

        .article-title a {{
            color: #e0e0e0;
            text-decoration: none;
        }}

        .article-title a:hover {{
            color: #4ade80;
        }}

        .article-meta {{
            display: flex;
            justify-content: space-between;
            font-size: 0.8em;
            color: #666;
        }}

        .source {{
            color: #4ade80;
        }}

        footer {{
            border-top: 1px solid #222;
            padding: 30px 0;
            margin-top: 40px;
            text-align: center;
            color: #666;
            font-size: 0.85em;
        }}

        footer a {{
            color: #4ade80;
            text-decoration: none;
        }}

        .no-data {{
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }}

        @media (max-width: 600px) {{
            .articles {{
                grid-template-columns: 1fr;
            }}
            .stats {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Cyber News Brief</h1>
            <div class="meta">
                {date_str} &bull; {time_str} &bull;
                <a href="https://github.com/{repo_name}">GitHub</a>
            </div>
        </header>

        <div class="stats">
            <div class="stat">
                <div class="stat-value">{total}</div>
                <div class="stat-label">Articles</div>
            </div>
            <div class="stat">
                <div class="stat-value">{sources}</div>
                <div class="stat-label">Sources</div>
            </div>
            <div class="stat">
                <div class="stat-value">{num_categories}</div>
                <div class="stat-label">Categories</div>
            </div>
            <div class="stat">
                <div class="stat-value">{threat_count}</div>
                <div class="stat-label">Threat Intel</div>
            </div>
        </div>
'''

    if categories:
        for category, category_articles in categories.items():
            html += f'''
        <div class="category">
            <div class="category-title">
                {category}
                <span class="category-count">{len(category_articles)} articles</span>
            </div>
            <div class="articles">
'''
            for article in category_articles[:8]:
                title = article.get('Title', 'Untitled')
                source = article.get('Source', 'Unknown')
                published = article.get('Published', '')
                link = article.get('Link', '#')

                # Escape HTML in title
                title = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

                html += f'''
                <div class="article">
                    <div class="article-title">
                        <a href="{link}" target="_blank" rel="noopener">{title}</a>
                    </div>
                    <div class="article-meta">
                        <span class="source">{source}</span>
                        <span>{published}</span>
                    </div>
                </div>
'''
            html += '''
            </div>
        </div>
'''
    else:
        html += '''
        <div class="no-data">
            <p>No articles available. Check back soon.</p>
        </div>
'''

    html += f'''
        <footer>
            Updated every 6 hours &bull;
            <a href="https://github.com/{repo_name}">View on GitHub</a>
        </footer>
    </div>
</body>
</html>'''

    return html

def main():
    print("Generating briefing...")

    articles = load_data()
    categories = organize_by_categories(articles)
    html = generate_html(articles, categories)

    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Done: {len(articles)} articles, {len(categories)} categories")
    return True

if __name__ == "__main__":
    main()
