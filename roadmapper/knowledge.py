"""Knowledge base extraction and query system."""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from roadmapper.projects import get_all_projects
from roadmapper.utils import read_text_file
from roadmapper.paths import get_global_config_dir


def get_knowledge_file() -> Path:
    """Get path to knowledge base file (~/.roadmapper/knowledge.json)."""
    return get_global_config_dir() / "knowledge.json"


def load_knowledge() -> List[Dict]:
    """
    Load knowledge base from disk.
    
    Returns:
        List of knowledge entries
    """
    knowledge_file = get_knowledge_file()
    
    if not knowledge_file.exists():
        return []
    
    try:
        content = read_text_file(knowledge_file)
        return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return []


def save_knowledge(knowledge: List[Dict]) -> None:
    """
    Save knowledge base to disk.
    
    Args:
        knowledge: List of knowledge entries
    """
    knowledge_file = get_knowledge_file()
    content = json.dumps(knowledge, indent=2, sort_keys=True)
    knowledge_file.parent.mkdir(parents=True, exist_ok=True)
    knowledge_file.write_text(content, encoding='utf-8')


def extract_knowledge_from_session(session_file: Path, project_path: Path, project_name: str) -> List[Dict]:
    """
    Extract knowledge from a session file.
    
    Args:
        session_file: Path to session file
        project_path: Path to project root
        project_name: Name of the project
    
    Returns:
        List of knowledge entries
    """
    knowledge_entries = []
    
    try:
        content = read_text_file(session_file)
        
        # Extract from "Discoveries" section
        discoveries = _extract_section(content, "Discoveries")
        if discoveries:
            for discovery in discoveries:
                knowledge_entries.append({
                    "type": "discovery",
                    "content": discovery,
                    "project": project_name,
                    "project_path": str(project_path),
                    "session_file": session_file.name,
                    "extracted_at": datetime.now().isoformat(),
                })
        
        # Extract from "Session Accomplishments" -> "Completed"
        accomplishments = _extract_accomplishments(content)
        if accomplishments:
            for accomplishment in accomplishments:
                knowledge_entries.append({
                    "type": "accomplishment",
                    "content": accomplishment,
                    "project": project_name,
                    "project_path": str(project_path),
                    "session_file": session_file.name,
                    "extracted_at": datetime.now().isoformat(),
                })
        
        # Extract from "Work Log" - look for key insights
        insights = _extract_insights(content)
        if insights:
            for insight in insights:
                knowledge_entries.append({
                    "type": "insight",
                    "content": insight,
                    "project": project_name,
                    "project_path": str(project_path),
                    "session_file": session_file.name,
                    "extracted_at": datetime.now().isoformat(),
                })
    
    except Exception:
        pass
    
    return knowledge_entries


def _extract_section(content: str, section_name: str) -> List[str]:
    """Extract items from a markdown section."""
    # Look for section header
    pattern = rf"##\s*{section_name}.*?\n(.*?)(?=\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        return []
    
    section_content = match.group(1)
    
    # Extract list items
    items = []
    for line in section_content.split("\n"):
        line = line.strip()
        # Match markdown list items: - item or * item
        if re.match(r"^[-*]\s+(.+)$", line):
            item = re.match(r"^[-*]\s+(.+)$", line).group(1).strip()
            if item and len(item) > 10:  # Filter out very short items
                items.append(item)
    
    return items


def _extract_accomplishments(content: str) -> List[str]:
    """Extract accomplishments from session file."""
    # Look for "Session Accomplishments" -> "Completed"
    pattern = r"##\s*✅\s*Session Accomplishments.*?\n\*\*Completed:\*\*\s*\n(.*?)(?=\n\*\*|\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        return []
    
    completed_section = match.group(1)
    items = []
    
    for line in completed_section.split("\n"):
        line = line.strip()
        # Match checkmark items: - [x] or - ✅
        if re.match(r"^-\s*(\[x\]|✅)\s+(.+)$", line, re.IGNORECASE):
            item = re.match(r"^-\s*(\[x\]|✅)\s+(.+)$", line, re.IGNORECASE).group(2).strip()
            if item and len(item) > 10:
                items.append(item)
    
    return items


def _extract_insights(content: str) -> List[str]:
    """Extract key insights from work log section."""
    # Look for work log and extract notable findings
    pattern = r"##\s*🔧\s*Work Log.*?\n(.*?)(?=\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        return []
    
    work_log = match.group(1)
    insights = []
    
    # Look for patterns that indicate insights:
    # - "Learn:", "Learned:", "Discovery:", "Found:", "Key insight:"
    insight_patterns = [
        r"(?:Learn|Learned|Discovery|Found|Key insight|Insight|Important|Note|Remember):\s*(.+?)(?:\n|$)",
        r"\*\*(.+?)\*\*:\s*(.+?)(?:\n|$)",  # Bold headers followed by content
    ]
    
    for pattern in insight_patterns:
        matches = re.finditer(pattern, work_log, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            insight = match.group(1).strip()
            if len(insight) > 20:  # Filter short items
                insights.append(insight)
    
    return insights[:5]  # Limit to top 5 insights per session


def index_all_projects() -> int:
    """
    Extract knowledge from all registered projects.
    
    Returns:
        Number of new knowledge entries added
    """
    projects = get_all_projects()
    existing_knowledge = load_knowledge()
    
    # Create set of existing entries (by content hash)
    existing_hashes = {_hash_entry(e) for e in existing_knowledge}
    
    new_entries = []
    
    for project_info in projects:
        project_path = Path(project_info["path"])
        project_name = project_info.get("name", project_path.name)
        
        # Process current session files
        for session_file in project_path.glob("SESSION_*.md"):
            entries = extract_knowledge_from_session(session_file, project_path, project_name)
            for entry in entries:
                entry_hash = _hash_entry(entry)
                if entry_hash not in existing_hashes:
                    new_entries.append(entry)
                    existing_hashes.add(entry_hash)
        
        # Process archived sessions
        archive_dir = project_path / "docs" / "archive" / "sessions"
        if archive_dir.exists():
            for session_file in archive_dir.glob("SESSION_*.md"):
                entries = extract_knowledge_from_session(session_file, project_path, project_name)
                for entry in entries:
                    entry_hash = _hash_entry(entry)
                    if entry_hash not in existing_hashes:
                        new_entries.append(entry)
                        existing_hashes.add(entry_hash)
    
    # Add new entries to knowledge base
    if new_entries:
        all_knowledge = existing_knowledge + new_entries
        save_knowledge(all_knowledge)
    
    return len(new_entries)


def _hash_entry(entry: Dict) -> str:
    """Create a hash for a knowledge entry to detect duplicates."""
    # Use content + project + session_file as unique identifier
    key = f"{entry.get('content', '')}{entry.get('project', '')}{entry.get('session_file', '')}"
    return str(hash(key))


def search_knowledge(query: str, knowledge_type: Optional[str] = None) -> List[Dict]:
    """
    Search knowledge base.
    
    Args:
        query: Search query
        knowledge_type: Optional filter by type ("discovery", "accomplishment", "insight")
    
    Returns:
        List of matching knowledge entries
    """
    knowledge = load_knowledge()
    
    if not knowledge:
        return []
    
    # Simple text search (case-insensitive)
    query_lower = query.lower()
    results = []
    
    for entry in knowledge:
        # Filter by type if specified
        if knowledge_type and entry.get("type") != knowledge_type:
            continue
        
        # Search in content
        content = entry.get("content", "").lower()
        if query_lower in content:
            results.append(entry)
    
    return results


def get_knowledge_by_topic(topic: str) -> List[Dict]:
    """
    Get knowledge entries related to a topic.
    
    Uses simple keyword matching - can be enhanced with better NLP.
    
    Args:
        topic: Topic to search for
    
    Returns:
        List of related knowledge entries
    """
    return search_knowledge(topic)


def get_related_discoveries(entry: Dict) -> List[Dict]:
    """
    Find related discoveries across projects.
    
    Args:
        entry: Knowledge entry to find related entries for
    
    Returns:
        List of related knowledge entries
    """
    knowledge = load_knowledge()
    
    if not knowledge:
        return []
    
    # Extract keywords from entry content
    content = entry.get("content", "").lower()
    # Simple keyword extraction (first few significant words)
    words = [w for w in content.split() if len(w) > 4][:5]
    
    related = []
    for other_entry in knowledge:
        # Skip same entry
        if _hash_entry(other_entry) == _hash_entry(entry):
            continue
        
        # Skip same project (we want cross-project relations)
        if other_entry.get("project") == entry.get("project"):
            continue
        
        other_content = other_entry.get("content", "").lower()
        # Check if any keywords appear in other entry
        if any(word in other_content for word in words):
            related.append(other_entry)
    
    return related[:10]  # Limit to 10 related entries



