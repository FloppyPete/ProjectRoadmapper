"""Status display functionality."""

import subprocess
from pathlib import Path
from datetime import datetime
import re

from roadmapper.utils import ensure_utf8_console
from roadmapper.history import get_session_stats
from roadmapper.paths import get_project_root


def show_status() -> None:
    """Show current project status."""
    # Ensure UTF-8 encoding for console output (especially Windows)
    ensure_utf8_console()
    
    cwd = Path.cwd()
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
        
        # Show session stats if available
        project_root = get_project_root()
        if project_root:
            try:
                stats = get_session_stats(project_root=project_root)
                if stats["total_sessions"] > 0:
                    print(f"\n📈 Activity: {stats['sessions_last_7_days']} sessions in last 7 days")
            except Exception:
                pass  # Silently fail if stats unavailable
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

