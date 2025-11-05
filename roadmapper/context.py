"""Context compression and storage functionality."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib

from roadmapper.paths import get_project_root
from roadmapper.utils import read_text_file, write_text_file


def get_context_file(project_root: Optional[Path] = None) -> Path:
    """
    Get path to context compression file (.roadmapper/context.json).
    
    Args:
        project_root: Project root directory (searches from cwd if None)
    
    Returns:
        Path to context.json file
    """
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        # Fallback to current directory
        project_root = Path.cwd()
    
    context_dir = project_root / ".roadmapper"
    context_dir.mkdir(parents=True, exist_ok=True)
    return context_dir / "context.json"


def load_context(project_root: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load context compression data from .roadmapper/context.json.
    
    Args:
        project_root: Project root directory
    
    Returns:
        Dictionary with context data, or empty dict if file doesn't exist
    """
    context_file = get_context_file(project_root)
    
    if not context_file.exists():
        return {
            "version": "1.0",
            "project": None,
            "sessions": [],
            "summaries": {},
            "key_decisions": [],
            "embeddings": {},  # Reserved for future embedding storage
        }
    
    try:
        content = read_text_file(context_file)
        return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return {
            "version": "1.0",
            "project": None,
            "sessions": [],
            "summaries": {},
            "key_decisions": [],
            "embeddings": {},
        }


def save_context(context_data: Dict[str, Any], project_root: Optional[Path] = None) -> None:
    """
    Save context compression data to .roadmapper/context.json.
    
    Args:
        context_data: Context data dictionary to save
        project_root: Project root directory
    """
    context_file = get_context_file(project_root)
    
    # Ensure version is set
    if "version" not in context_data:
        context_data["version"] = "1.0"
    
    # Write with pretty formatting
    content = json.dumps(context_data, indent=2, ensure_ascii=False)
    write_text_file(context_file, content)


def add_session_summary(
    session_file: Path,
    summary: str,
    accomplishments: List[str],
    decisions: List[str],
    project_root: Optional[Path] = None,
) -> None:
    """
    Add a session summary to context compression storage.
    
    Args:
        session_file: Path to session file
        summary: Condensed summary of the session
        accomplishments: List of key accomplishments
        decisions: List of key decisions made
        project_root: Project root directory
    """
    context_data = load_context(project_root)
    
    # Extract session identifier from filename
    session_id = session_file.stem  # e.g., "SESSION_2025_11_04_I"
    
    # Create session entry
    session_entry = {
        "id": session_id,
        "file": str(session_file.relative_to(project_root or Path.cwd())),
        "summary": summary,
        "accomplishments": accomplishments,
        "decisions": decisions,
        "archived_at": datetime.now().isoformat(),
    }
    
    # Add to sessions list
    if "sessions" not in context_data:
        context_data["sessions"] = []
    
    # Remove existing entry if present (update scenario)
    context_data["sessions"] = [
        s for s in context_data["sessions"] if s["id"] != session_id
    ]
    
    # Add new entry
    context_data["sessions"].append(session_entry)
    
    # Store summary by session ID for quick lookup
    if "summaries" not in context_data:
        context_data["summaries"] = {}
    context_data["summaries"][session_id] = summary
    
    # Add decisions to key_decisions list
    if "key_decisions" not in context_data:
        context_data["key_decisions"] = []
    
    for decision in decisions:
        decision_entry = {
            "session_id": session_id,
            "decision": decision,
            "timestamp": datetime.now().isoformat(),
        }
        # Avoid duplicates
        if decision_entry not in context_data["key_decisions"]:
            context_data["key_decisions"].append(decision_entry)
    
    # Set project name if not set
    if context_data.get("project") is None and project_root:
        roadmap_path = project_root / "PROJECT_ROADMAP.md"
        if roadmap_path.exists():
            content = read_text_file(roadmap_path)
            # Try to extract project name
            import re
            project_match = re.search(r'^# ([A-Za-z0-9_\- ]+)$', content, re.MULTILINE)
            if project_match:
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('# ') and 'Quick Start' not in line and 'Project' in line:
                        context_data["project"] = line.replace('# ', '').strip()
                        break
    
    save_context(context_data, project_root)


def get_session_summary(session_id: str, project_root: Optional[Path] = None) -> Optional[str]:
    """
    Get summary for a specific session.
    
    Args:
        session_id: Session identifier (e.g., "SESSION_2025_11_04_I")
        project_root: Project root directory
    
    Returns:
        Session summary, or None if not found
    """
    context_data = load_context(project_root)
    return context_data.get("summaries", {}).get(session_id)


def get_recent_decisions(limit: int = 10, project_root: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Get recent key decisions from context.
    
    Args:
        limit: Maximum number of decisions to return
        project_root: Project root directory
    
    Returns:
        List of decision dictionaries
    """
    context_data = load_context(project_root)
    decisions = context_data.get("key_decisions", [])
    # Return most recent first
    return decisions[-limit:][::-1]


def get_session_pointers(
    query: Optional[str] = None,
    project_root: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    """
    Get pointers to key sessions and decisions for context retrieval.
    
    Args:
        query: Optional query string to filter sessions
        project_root: Project root directory
    
    Returns:
        List of session pointers with summaries
    """
    context_data = load_context(project_root)
    sessions = context_data.get("sessions", [])
    
    if query:
        # Simple text matching (can be enhanced with embeddings later)
        query_lower = query.lower()
        filtered = []
        for session in sessions:
            if (query_lower in session.get("summary", "").lower() or
                any(query_lower in acc.lower() for acc in session.get("accomplishments", []))):
                filtered.append(session)
        return filtered
    
    return sessions


def clear_context(project_root: Optional[Path] = None) -> None:
    """
    Clear all context compression data (useful for testing or reset).
    
    Args:
        project_root: Project root directory
    """
    context_file = get_context_file(project_root)
    if context_file.exists():
        context_file.unlink()

