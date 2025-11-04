"""Status display functionality."""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import re


def show_status() -> None:
    """Show current project status."""
    cwd = Path.cwd()
    
    # Set UTF-8 encoding for Windows console
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            # Python < 3.7
            pass
    
    print("📊 ProjectRoadmapper Status\n")
    
    # Find current session (most recent session file in root)
    session_files = sorted(
        cwd.glob("SESSION_*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    
    if session_files:
        current_session = session_files[0]
        print(f"📝 Current Session: {current_session.name}")
        
        # Show recent sessions
        if len(session_files) > 1:
            print("\n📚 Recent Sessions:")
            for session_file in session_files[1:6]:  # Show up to 5 more
                print(f"   - {session_file.name}")
    else:
        print("📝 Current Session: None")
        print("   💡 Run 'roadmapper session' to create a session")
    
    # Check for PROJECT_ROADMAP.md
    roadmap_path = cwd / "PROJECT_ROADMAP.md"
    if roadmap_path.exists():
        print("\n✅ PROJECT_ROADMAP.md found")
    else:
        print("\n⚠️  PROJECT_ROADMAP.md not found")
        print("   💡 Run 'roadmapper init' to initialize project")
    
    # Git status
    print("\n🔧 Git Status:")
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        
        if result.returncode == 0:
            if result.stdout.strip():
                print("   Modified files:")
                for line in result.stdout.strip().split("\n"):
                    print(f"   {line}")
            else:
                print("   ✅ Working tree clean")
            
            # Branch info
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                cwd=cwd,
            )
            if branch_result.returncode == 0 and branch_result.stdout.strip():
                print(f"   Branch: {branch_result.stdout.strip()}")
        else:
            print("   ⚠️  Not a git repository")
    except FileNotFoundError:
        print("   ⚠️  Git not found")
    except Exception as e:
        print(f"   ⚠️  Error checking git status: {e}")

