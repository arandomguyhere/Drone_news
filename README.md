# Cybersecurity News Aggregator

Scrapes cybersecurity news from 100+ sources and generates a daily briefing. Runs automatically via GitHub Actions every 6 hours.

**[View the live briefing](https://arandomguyhere.github.io/Drone_news/)**

## What it does

- Pulls articles from security publications (Krebs, Bleeping Computer, The Record, etc.)
- Covers threat intel blogs (Mandiant, CrowdStrike, Unit 42, etc.)
- Tracks geopolitical cyber activity (state-sponsored attacks, APT groups)
- Monitors mainstream tech/security coverage (WSJ, Reuters, Wired)
- Generates an HTML briefing deployed to GitHub Pages

## Setup

```bash
pip install -r requirements.txt
```

### Running locally

```bash
# Full collection
python intelligence_system.py run

# Quick run (fewer sources)
python intelligence_system.py priority

# Just regenerate the newsletter from existing data
python intelligence_system.py newsletter

# Check status
python intelligence_system.py status
```

### GitHub Actions

The workflow in `.github/workflows/intelligence.yml` runs every 6 hours and:
1. Scrapes all configured sources
2. Dedupes and categorizes articles
3. Generates the HTML briefing
4. Commits data and deploys to GitHub Pages

To run manually: Actions tab > "Drone Intelligence Collection" > Run workflow

## Files

```
drone_scraper.py          # Main scraper, search queries defined here
generate_newsletter.py    # Builds the HTML briefing
intelligence_system.py    # CLI wrapper
config.json               # Settings
data/                     # Scraped articles (JSON/CSV)
docs/index.html           # Generated briefing (served by GitHub Pages)
```

## Adding sources

Edit the `SEARCH_QUERIES` list in `drone_scraper.py`:

```python
("site:example.com security", "Example Security"),
```

## Changing the schedule

Edit `.github/workflows/intelligence.yml`:

```yaml
schedule:
  - cron: '0 */3 * * *'  # Every 3 hours instead of 6
```

## Notes

- Uses Google News as the aggregation backend
- Rate-limited to avoid getting blocked
- Only collects publicly available articles
- The repo name says "Drone" but that's legacy - it's all cybersecurity now

## License

MIT
