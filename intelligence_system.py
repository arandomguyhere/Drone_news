#!/usr/bin/env python3
"""
Cybersecurity News System - CLI Controller
"""

import sys
import time
import subprocess
import json
from datetime import datetime
from pathlib import Path

def run_command(command, description):
    """Run a system command"""
    print(f"Running: {description}...")

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Done: {description}")
            if result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        print(f"   {line}")
            return True
        else:
            print(f"Failed: {description} (exit code: {result.returncode})")
            if result.stderr.strip():
                print(f"Error output:")
                for line in result.stderr.strip().split('\n'):
                    print(f"   {line}")
            return False
    except Exception as e:
        print(f"Failed: {description} - {e}")
        return False

def check_github_environment():
    """Check if running in GitHub Actions environment"""
    github_actions = os.environ.get('GITHUB_ACTIONS') == 'true'
    if github_actions:
        print("Running in GitHub Actions")
        print(f"   Repository: {os.environ.get('GITHUB_REPOSITORY', 'Unknown')}")
    else:
        print("Running locally")

    return github_actions

def check_dependencies():
    """Check if required files exist for GitHub deployment"""
    required_files = [
        "scraper.py",
        "generate_newsletter.py",
        "requirements.txt",
        "config.json"
    ]
    
    optional_files = [
        ".github/workflows/intelligence.yml",
        "README.md"
    ]
    
    missing_required = []
    missing_optional = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_required.append(file)
    
    for file in optional_files:
        if not Path(file).exists():
            missing_optional.append(file)
    
    if missing_required:
        print(f"Missing required files: {', '.join(missing_required)}")
        return False

    if missing_optional:
        print(f"Missing optional files: {', '.join(missing_optional)}")

    print("All required files present")
    return True

def show_github_status():
    """Show system status"""
    print("CYBER NEWS SYSTEM STATUS")
    print("=" * 60)

    # Check GitHub environment
    is_github = check_github_environment()

    # Check repository structure
    print(f"\nFiles:")
    key_paths = {
        "Data": "data/latest_news.json",
        "Site": "docs/index.html",
        "Config": "config.json",
        "Workflow": ".github/workflows/intelligence.yml",
        "Requirements": "requirements.txt"
    }

    for name, path in key_paths.items():
        if Path(path).exists():
            size = Path(path).stat().st_size
            modified = datetime.fromtimestamp(Path(path).stat().st_mtime)
            print(f"  [ok] {name}: {size:,} bytes ({modified.strftime('%Y-%m-%d %H:%M')})")
        else:
            print(f"  [missing] {name}: {path}")
    
    # Check data
    print(f"\nData:")
    try:
        if Path("data/latest_news.json").exists():
            with open("data/latest_news.json", 'r', encoding='utf-8') as f:
                data = json.load(f)

            if data:
                print(f"  Total Articles: {len(data):,}")

                # Category analysis
                categories = {}
                sources = {}
                for article in data:
                    cat = article.get('Category', 'Unknown')
                    src = article.get('Source', 'Unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    sources[src] = sources.get(src, 0) + 1

                print(f"  Categories: {len(categories)}")
                print(f"  Sources: {len(sources)}")

                print(f"  Top Categories:")
                for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"    {cat}: {count}")

                print(f"  Top Sources:")
                for src, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"    {src}: {count}")
            else:
                print(f"  Data file is empty")
        else:
            print(f"  No data file found")
    except Exception as e:
        print(f"  Error reading data: {e}")
    
    print("=" * 60)

def run_full_intelligence_cycle(priority_mode=False):
    """Run complete collection cycle"""

    cycle_start = time.time()
    start_time = datetime.now()

    print(f"\nCYBER NEWS COLLECTION")
    print(f"Mode: {'priority' if priority_mode else 'full'}")
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    success_count = 0
    total_phases = 2

    # Phase 1: Collection
    print("\n[1/2] Scraping news...")
    cmd = "python scraper.py"
    if priority_mode:
        cmd += " --priority"

    if run_command(cmd, "News collection"):
        success_count += 1

    # Phase 2: Generate briefing
    print("\n[2/2] Generating briefing...")
    if run_command("python generate_newsletter.py", "Briefing generation"):
        success_count += 1

    # Summary
    cycle_time = time.time() - cycle_start

    print(f"\nComplete: {cycle_time:.1f}s, {success_count}/{total_phases} phases succeeded")
    
    # Show collection results
    try:
        if Path("data/latest_news.json").exists():
            with open("data/latest_news.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Articles: {len(data):,}")

            if data:
                categories = len(set(article.get('Category', '') for article in data))
                sources = len(set(article.get('Source', '') for article in data))
                print(f"Categories: {categories}, Sources: {sources}")
    except Exception as e:
        print(f"Could not read results: {e}")

    return success_count == total_phases

def show_help():
    """Show help"""
    print("Cyber News Aggregator")
    print("=" * 40)
    print("Commands:")
    print("  run        Full collection cycle")
    print("  priority   Quick collection (fewer sources)")
    print("  newsletter Generate briefing only")
    print("  status     Show system status")
    print("  help       Show this help")
    print()
    print("Examples:")
    print("  python intelligence_system.py run")
    print("  python intelligence_system.py status")

def main():
    """Main entry point"""

    # Import here to avoid issues if not available
    import os

    # Check dependencies first
    if not check_dependencies():
        print("\nMissing files. Install deps: pip install -r requirements.txt")
        sys.exit(1)

    # Parse command
    if len(sys.argv) < 2:
        command = "help"
    else:
        command = sys.argv[1].lower()

    # Execute command
    try:
        if command in ["run", "collect"]:
            success = run_full_intelligence_cycle()
            sys.exit(0 if success else 1)

        elif command in ["priority", "fast"]:
            success = run_full_intelligence_cycle(priority_mode=True)
            sys.exit(0 if success else 1)

        elif command == "newsletter":
            success = run_command("python generate_newsletter.py", "Briefing generation")
            sys.exit(0 if success else 1)

        elif command == "status":
            show_github_status()

        elif command == "help":
            show_help()

        else:
            print(f"Unknown command: {command}")
            print("Use 'python intelligence_system.py help' for usage")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"\nInterrupted")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
