#!/usr/bin/env python3
"""
Drone Intelligence System - Master Controller
GitHub Pages & Actions Compatible Version
"""

import sys
import time
import subprocess
import json
from datetime import datetime
from pathlib import Path

def run_command(command, description):
    """Run a system command with GitHub Actions compatible output"""
    print(f"🔄 {description}...")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                # Format output for GitHub Actions
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        print(f"   {line}")
            return True
        else:
            print(f"❌ {description} failed (exit code: {result.returncode})")
            if result.stderr.strip():
                print(f"Error output:")
                for line in result.stderr.strip().split('\n'):
                    print(f"   {line}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def check_github_environment():
    """Check if running in GitHub Actions environment"""
    github_actions = os.environ.get('GITHUB_ACTIONS') == 'true'
    if github_actions:
        print("🤖 Running in GitHub Actions environment")
        print(f"   Repository: {os.environ.get('GITHUB_REPOSITORY', 'Unknown')}")
        print(f"   Workflow: {os.environ.get('GITHUB_WORKFLOW', 'Unknown')}")
        print(f"   Run ID: {os.environ.get('GITHUB_RUN_ID', 'Unknown')}")
    else:
        print("💻 Running in local environment")
    
    return github_actions

def check_dependencies():
    """Check if required files exist for GitHub deployment"""
    required_files = [
        "drone_scraper.py",
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
        print(f"❌ Missing REQUIRED files: {', '.join(missing_required)}")
        return False
    
    if missing_optional:
        print(f"⚠️ Missing optional files: {', '.join(missing_optional)}")
    
    print("✅ All required files present for GitHub deployment")
    return True

def show_github_status():
    """Show system status optimized for GitHub environment"""
    print("🚁 DRONE INTELLIGENCE SYSTEM STATUS")
    print("🌐 GitHub Pages & Actions Compatible")
    print("=" * 60)
    
    # Check GitHub environment
    is_github = check_github_environment()
    
    # Check repository structure
    print(f"\n📁 Repository Structure:")
    key_paths = {
        "Intelligence Data": "data/latest_news.json",
        "GitHub Pages Site": "docs/index.html",
        "Configuration": "config.json",
        "GitHub Workflow": ".github/workflows/intelligence.yml",
        "Requirements": "requirements.txt"
    }
    
    for name, path in key_paths.items():
        if Path(path).exists():
            size = Path(path).stat().st_size
            modified = datetime.fromtimestamp(Path(path).stat().st_mtime)
            print(f"  ✅ {name}: {size:,} bytes (modified {modified.strftime('%Y-%m-%d %H:%M')})")
        else:
            print(f"  ❌ {name}: Not found ({path})")
    
    # Check intelligence data
    print(f"\n📊 Intelligence Data Status:")
    try:
        if Path("data/latest_news.json").exists():
            with open("data/latest_news.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if data:
                print(f"  📈 Total Articles: {len(data):,}")
                
                # Category analysis
                categories = {}
                sources = {}
                for article in data:
                    cat = article.get('Category', 'Unknown')
                    src = article.get('Source', 'Unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    sources[src] = sources.get(src, 0) + 1
                
                print(f"  📂 Categories: {len(categories)}")
                print(f"  📰 Sources: {len(sources)}")
                
                print(f"  🏆 Top Categories:")
                for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"    • {cat}: {count}")
                
                print(f"  📺 Top Sources:")
                for src, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"    • {src}: {count}")
            else:
                print(f"  ⚠️ Intelligence file exists but is empty")
        else:
            print(f"  ❌ No intelligence data file found")
    except Exception as e:
        print(f"  ❌ Error reading intelligence data: {e}")
    
    # GitHub specific information
    if is_github:
        print(f"\n🤖 GitHub Actions Environment:")
        github_vars = {
            "Repository": "GITHUB_REPOSITORY",
            "Workflow": "GITHUB_WORKFLOW", 
            "Run ID": "GITHUB_RUN_ID",
            "Actor": "GITHUB_ACTOR",
            "Event": "GITHUB_EVENT_NAME"
        }
        
        for name, var in github_vars.items():
            value = os.environ.get(var, 'Not set')
            print(f"  {name}: {value}")
    else:
        print(f"\n🌐 GitHub Pages URLs (when deployed):")
        print(f"  📖 Repository: https://github.com/yourusername/drone-intelligence-system")
        print(f"  🌐 Live Brief: https://yourusername.github.io/drone-intelligence-system/")
        print(f"  📊 Actions: https://github.com/yourusername/drone-intelligence-system/actions")
    
    print("=" * 60)

def run_full_intelligence_cycle(priority_mode=False):
    """Run complete intelligence collection cycle for GitHub"""
    
    cycle_start = time.time()
    start_time = datetime.now()
    
    print(f"\n🎯 DRONE INTELLIGENCE COLLECTION CYCLE")
    print(f"🌐 Optimized for GitHub Pages & Actions")
    print(f"Mode: {'PRIORITY' if priority_mode else 'COMPREHENSIVE'}")
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("-" * 70)
    
    success_count = 0
    total_phases = 2
    
    # Phase 1: Intelligence Collection
    print("📡 PHASE 1: Drone Intelligence Collection")
    cmd = "python drone_scraper.py"
    if priority_mode:
        cmd += " --priority"
    
    if run_command(cmd, "Intelligence collection"):
        success_count += 1
    
    # Phase 2: GitHub Pages Newsletter Generation
    print("\n📰 PHASE 2: GitHub Pages Newsletter Generation")
    if run_command("python generate_newsletter.py", "Newsletter generation"):
        success_count += 1
    
    # Cycle Summary
    cycle_time = time.time() - cycle_start
    success_rate = (success_count / total_phases) * 100
    
    print(f"\n🎉 INTELLIGENCE CYCLE COMPLETE")
    print(f"⏱️  Total time: {cycle_time:.1f} seconds")
    print(f"✅ Success rate: {success_rate:.0f}% ({success_count}/{total_phases} phases)")
    
    # Show collection results
    try:
        if Path("data/latest_news.json").exists():
            with open("data/latest_news.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"📊 Articles collected: {len(data):,}")
            
            if data:
                categories = len(set(article.get('Category', '') for article in data))
                sources = len(set(article.get('Source', '') for article in data))
                print(f"📂 Categories: {categories}")
                print(f"📰 Sources: {sources}")
        else:
            print(f"📊 Articles collected: Unable to determine")
    except Exception as e:
        print(f"📊 Articles collected: Error reading data ({e})")
    
    # GitHub-specific next steps
    github_actions = os.environ.get('GITHUB_ACTIONS') == 'true'
    if not github_actions:
        print(f"\n🌐 GitHub Deployment:")
        print(f"  1. Commit changes: git add . && git commit -m 'Update intelligence'")
        print(f"  2. Push to GitHub: git push origin main")
        print(f"  3. Check Actions: https://github.com/yourusername/drone-intelligence-system/actions")
        print(f"  4. View Live Brief: https://yourusername.github.io/drone-intelligence-system/")
    
    return success_count == total_phases

def show_help():
    """Show help information for GitHub deployment"""
    print("🚁 DRONE INTELLIGENCE SYSTEM")
    print("🌐 GitHub Pages & Actions Compatible")
    print("=" * 60)
    print("COMMANDS:")
    print("  run              Run full intelligence cycle")
    print("  priority         Run priority intelligence collection")
    print("  collect          Run collection only")
    print("  newsletter       Generate GitHub Pages newsletter only")
    print("  status           Show system status")
    print("  github-setup     Show GitHub deployment instructions")
    print("  help             Show this help")
    print()
    print("EXAMPLES:")
    print("  python intelligence_system.py run")
    print("  python intelligence_system.py priority")
    print("  python intelligence_system.py status")
    print()
    print("GITHUB DEPLOYMENT:")
    print("  1. Push to GitHub repository")
    print("  2. Enable GitHub Actions")
    print("  3. Enable GitHub Pages (Settings → Pages → GitHub Actions)")
    print("  4. System runs automatically every 6 hours")
    print()
    print("LIVE BRIEF: https://yourusername.github.io/drone-intelligence-system/")
    print("=" * 60)

def show_github_setup():
    """Show GitHub deployment setup instructions"""
    print("🚁 GITHUB DEPLOYMENT SETUP GUIDE")
    print("=" * 60)
    print()
    print("STEP 1: Repository Setup")
    print("  1. Create new GitHub repository: 'drone-intelligence-system'")
    print("  2. Clone locally: git clone https://github.com/yourusername/drone-intelligence-system.git")
    print("  3. Copy all system files to the repository")
    print("  4. Commit and push: git add . && git commit -m 'Initial setup' && git push")
    print()
    print("STEP 2: Enable GitHub Features")
    print("  1. Go to repository Settings")
    print("  2. Enable GitHub Actions (if prompted)")
    print("  3. Go to Settings → Pages")
    print("  4. Source: 'GitHub Actions'")
    print("  5. Save settings")
    print()
    print("STEP 3: First Deployment")
    print("  1. Go to Actions tab")
    print("  2. Select 'Drone Intelligence Collection'")
    print("  3. Click 'Run workflow'")
    print("  4. Wait for completion (~5-10 minutes)")
    print()
    print("STEP 4: Verify Deployment")
    print("  1. Check Actions for green checkmark")
    print("  2. Visit: https://yourusername.github.io/drone-intelligence-system/")
    print("  3. Verify intelligence brief loads correctly")
    print()
    print("AUTOMATION:")
    print("  • System runs every 6 hours automatically")
    print("  • Collects latest drone intelligence")
    print("  • Generates professional briefing")
    print("  • Deploys to GitHub Pages")
    print("  • Commits data to repository")
    print()
    print("CUSTOMIZATION:")
    print("  • Edit drone_scraper.py for search terms")
    print("  • Modify generate_newsletter.py for layout")
    print("  • Update .github/workflows/intelligence.yml for schedule")
    print("=" * 60)

def main():
    """Main entry point for GitHub-compatible system"""
    
    # Import here to avoid issues if not available
    import os
    
    # Check dependencies first
    if not check_dependencies():
        print("\n💡 GitHub Setup Instructions:")
        print("1. Ensure all required files are in the repository")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Run setup: python intelligence_system.py github-setup")
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
            
        elif command == "collect-only":
            success = run_command("python drone_scraper.py", "Intelligence collection")
            sys.exit(0 if success else 1)
            
        elif command == "newsletter":
            success = run_command("python generate_newsletter.py", "GitHub Pages newsletter generation")
            sys.exit(0 if success else 1)
            
        elif command == "status":
            show_github_status()
            
        elif command == "github-setup":
            show_github_setup()
            
        elif command == "help":
            show_help()
            
        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'python intelligence_system.py help' for usage information")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n⚠️ Intelligence cycle interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
