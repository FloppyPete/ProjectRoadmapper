"""Session history tracking for roadmapper."""

import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from roadmapper.paths import get_project_history_file, get_project_root
from roadmapper.utils import read_text_file, write_text_file


def log_session(
    session_file: Path,
    project_root: Optional[Path] = None,
) -> None:
    """
    Log a session creation event to history.
    
    Args:
        session_file: Path to the session file
        project_root: Project root directory (searches from cwd if None)
    """
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        return  # Not in a project, skip logging
    
    history_file = get_project_history_file(project_root)
    
    # Get git branch if available
    branch = None
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        if result.returncode == 0:
            branch = result.stdout.strip()
    except (FileNotFoundError, Exception):
        pass
    
    # Create event record
    event = {
        "type": "session",
        "date": datetime.now().isoformat() + "Z",
        "file": session_file.name,
        "branch": branch,
    }
    
    # Append to history file (JSONL format)
    line = json.dumps(event) + "\n"
    history_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Append to file
    try:
        with history_file.open("a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        # Fail silently if we can't write history
        pass


def read_history(
    project_root: Optional[Path] = None,
    limit: Optional[int] = None,
    since: Optional[datetime] = None,
) -> List[Dict]:
    """
    Read session history.
    
    Args:
        project_root: Project root directory (searches from cwd if None)
        limit: Maximum number of records to return
        since: Only return records since this datetime
    
    Returns:
        List of history records (most recent first)
    """
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        return []
    
    history_file = get_project_history_file(project_root)
    
    if not history_file.exists():
        return []
    
    try:
        content = read_text_file(history_file)
        records = []
        for line in content.strip().split("\n"):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                # Filter by date if specified
                if since:
                    record_date_str = record["date"].replace("Z", "+00:00")
                    record_date = datetime.fromisoformat(record_date_str)
                    # Make both timezone-aware or both naive for comparison
                    if record_date.tzinfo is None and since.tzinfo is not None:
                        record_date = record_date.replace(tzinfo=since.tzinfo)
                    elif record_date.tzinfo is not None and since.tzinfo is None:
                        since = since.replace(tzinfo=record_date.tzinfo)
                    if record_date < since:
                        continue
                records.append(record)
            except (json.JSONDecodeError, KeyError):
                continue
        
        # Reverse to get most recent first
        records.reverse()
        
        if limit:
            records = records[:limit]
        
        return records
    except Exception:
        return []


def get_session_stats(
    project_root: Optional[Path] = None,
    since: Optional[datetime] = None,
) -> Dict:
    """
    Get session statistics.
    
    Args:
        project_root: Project root directory (searches from cwd if None)
        since: Only analyze records since this datetime
    
    Returns:
        Dictionary with statistics
    """
    records = read_history(project_root=project_root, since=since)
    
    if not records:
        return {
            "total_sessions": 0,
            "sessions_last_7_days": 0,
            "sessions_last_30_days": 0,
            "avg_sessions_per_week": 0.0,
        }
    
    total = len(records)
    
    # Count sessions in last 7 and 30 days
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    last_7_days = 0
    last_30_days = 0
    
    for record in records:
        try:
            record_date_str = record["date"].replace("Z", "+00:00")
            record_date = datetime.fromisoformat(record_date_str)
            # Make timezone-aware if needed for comparison
            if record_date.tzinfo is None:
                record_date = record_date.replace(tzinfo=now.tzinfo if now.tzinfo else None)
            if record_date.tzinfo and now.tzinfo is None:
                now = now.replace(tzinfo=record_date.tzinfo)
                week_ago = week_ago.replace(tzinfo=record_date.tzinfo)
                month_ago = month_ago.replace(tzinfo=record_date.tzinfo)
            if record_date >= week_ago:
                last_7_days += 1
            if record_date >= month_ago:
                last_30_days += 1
        except (ValueError, KeyError):
            continue
    
    # Calculate average sessions per week
    if records:
        first_date_str = records[-1]["date"].replace("Z", "+00:00")
        first_date = datetime.fromisoformat(first_date_str)
        # Make timezone-aware if needed
        if first_date.tzinfo is None and now.tzinfo is not None:
            first_date = first_date.replace(tzinfo=now.tzinfo)
        elif first_date.tzinfo is not None and now.tzinfo is None:
            now = now.replace(tzinfo=first_date.tzinfo)
        days_span = (now - first_date).days
        if days_span > 0:
            avg_per_week = (total / days_span) * 7
        else:
            avg_per_week = total
    else:
        avg_per_week = 0.0
    
    return {
        "total_sessions": total,
        "sessions_last_7_days": last_7_days,
        "sessions_last_30_days": last_30_days,
        "avg_sessions_per_week": round(avg_per_week, 1),
    }


def get_files_changed_for_session(
    session_file: Path,
    project_root: Optional[Path] = None,
) -> int:
    """
    Get number of files changed since session creation (using git).
    
    Args:
        session_file: Path to session file
        project_root: Project root directory (searches from cwd if None)
    
    Returns:
        Number of files changed, or 0 if git not available
    """
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        return 0
    
    try:
        # Get file creation time from git or filesystem
        result = subprocess.run(
            ["git", "log", "--follow", "--format=%H", "--", str(session_file)],
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        
        if result.returncode != 0:
            return 0
        
        commits = result.stdout.strip().split("\n")
        if not commits:
            return 0
        
        # Get files changed since first commit that added this file
        first_commit = commits[-1]
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{first_commit}^..HEAD"],
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        
        if result.returncode == 0:
            files = [f for f in result.stdout.strip().split("\n") if f]
            return len(files)
    except (FileNotFoundError, Exception):
        pass
    
    return 0

