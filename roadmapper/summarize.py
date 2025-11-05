"""Session summarization functionality."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from roadmapper.utils import read_text_file
from roadmapper.paths import get_project_root


def extract_session_summary(session_file: Path) -> Dict[str, any]:
    """
    Extract summary information from a session file.
    
    Args:
        session_file: Path to session file
    
    Returns:
        Dictionary with summary, accomplishments, decisions, discoveries
    """
    if not session_file.exists():
        return {
            "summary": "",
            "accomplishments": [],
            "decisions": [],
            "discoveries": [],
            "tasks": [],
        }
    
    content = read_text_file(session_file)
    
    # Extract accomplishments from "Session Accomplishments" section
    accomplishments = _extract_accomplishments(content)
    
    # Extract decisions using reasoning markers
    decisions = _extract_decisions(content)
    
    # Extract discoveries
    discoveries = _extract_discoveries(content)
    
    # Extract structured tasks
    tasks = _extract_tasks(content)
    
    # Generate summary from accomplishments
    summary = _generate_summary(accomplishments, decisions, discoveries)
    
    return {
        "summary": summary,
        "accomplishments": accomplishments,
        "decisions": decisions,
        "discoveries": discoveries,
        "tasks": tasks,
    }


def _extract_accomplishments(content: str) -> List[str]:
    """Extract accomplishments from session file."""
    accomplishments = []
    
    # Look for "## ✅ Session Accomplishments" section
    pattern = r'##\s*✅\s*Session Accomplishments(.*?)(?=\n##|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if match:
        section = match.group(1)
        
        # Look for "Completed:" subsection
        completed_pattern = r'Completed:.*?(?=In Progress:|Deferred:|Discoveries:|\Z)'
        completed_match = re.search(completed_pattern, section, re.DOTALL | re.IGNORECASE)
        
        if completed_match:
            completed_section = completed_match.group(0)
            # Extract list items starting with - or * and containing ✅
            items = re.findall(r'[-*]\s*✅\s*(.+?)(?=\n[-*]|\n##|\Z)', completed_section, re.MULTILINE)
            for item in items:
                item = item.strip()
                # Remove markdown formatting
                item = re.sub(r'\*\*([^*]+)\*\*', r'\1', item)  # Remove bold
                item = re.sub(r'`([^`]+)`', r'\1', item)  # Remove code
                # Clean up nested bullets
                item = re.sub(r'\n\s*[-*]\s*', ' ', item)
                if item and len(item) > 10:  # Filter out very short items
                    accomplishments.append(item)
    
    return accomplishments


def _extract_decisions(content: str) -> List[str]:
    """Extract decisions using reasoning markers."""
    decisions = []
    
    # Look for 🧭 DECISION: markers
    pattern = r'🧭\s*DECISION:\s*(.+?)(?=\n|🧭|🤔|✅|⚠️|💡|\Z)'
    matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
    
    for match in matches:
        decision = match.strip()
        if decision:
            decisions.append(decision)
    
    return decisions


def _extract_discoveries(content: str) -> List[str]:
    """Extract discoveries from session file."""
    discoveries = []
    
    # Look for "Discoveries:" section
    pattern = r'Discoveries:.*?(?=\n---|\n##|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if match:
        section = match.group(0)
        # Extract list items with bold text (discoveries are usually bold)
        items = re.findall(r'[-*]\s*\*\*(.+?)\*\*\s*[-–—]\s*(.+?)(?=\n[-*]|\n##|\Z)', section)
        for bold_part, rest in items:
            discovery = f"{bold_part.strip()} - {rest.strip()}"
            discoveries.append(discovery)
        
        # Also catch standalone bold items
        if not discoveries:
            items = re.findall(r'[-*]\s*\*\*(.+?)\*\*', section)
            for item in items:
                item = item.strip()
                if item and len(item) > 10:
                    discoveries.append(item)
    
    return discoveries


def _extract_tasks(content: str) -> List[Dict[str, str]]:
    """Extract structured tasks from session file."""
    tasks = []
    
    # Look for [TASK] blocks
    pattern = r'\[TASK\]\s*(.+?)(?=\n\[TASK\]|\n\[STATUS\]|\Z)'
    task_matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
    
    for task_desc in task_matches:
        task_desc = task_desc.strip()
        
        # Find corresponding [STATUS] and [NOTES]
        task_start = content.find(f"[TASK] {task_desc}")
        if task_start != -1:
            task_section = content[task_start:task_start + 500]  # Look ahead 500 chars
            
            status_match = re.search(r'\[STATUS\]\s*(.+?)(?=\n\[|\Z)', task_section, re.MULTILINE | re.IGNORECASE)
            notes_match = re.search(r'\[NOTES\]\s*(.+?)(?=\n\[|\Z)', task_section, re.MULTILINE | re.IGNORECASE)
            
            tasks.append({
                "task": task_desc,
                "status": status_match.group(1).strip() if status_match else "unknown",
                "notes": notes_match.group(1).strip() if notes_match else "",
            })
    
    return tasks


def _generate_summary(
    accomplishments: List[str],
    decisions: List[str],
    discoveries: List[str],
) -> str:
    """
    Generate a condensed summary from extracted information.
    
    Args:
        accomplishments: List of accomplishments
        decisions: List of decisions
        discoveries: List of discoveries
    
    Returns:
        Condensed summary string
    """
    parts = []
    
    if accomplishments:
        # Take first 3 accomplishments for summary
        key_accomplishments = accomplishments[:3]
        parts.append("Completed: " + ", ".join(key_accomplishments))
    
    if decisions:
        # Include key decisions
        key_decisions = decisions[:2]
        parts.append("Key decisions: " + "; ".join(key_decisions))
    
    if discoveries:
        # Include important discoveries
        key_discoveries = discoveries[:2]
        parts.append("Discoveries: " + "; ".join(key_discoveries))
    
    if not parts:
        return "Session work completed."
    
    return ". ".join(parts) + "."


def generate_roadmap_summary(session_file: Path) -> str:
    """
    Generate a summary suitable for adding to PROJECT_ROADMAP.md.
    
    Args:
        session_file: Path to session file
    
    Returns:
        Formatted summary string for roadmap
    """
    data = extract_session_summary(session_file)
    session_id = session_file.stem
    
    # Format as roadmap entry
    lines = [f"**Session {session_id}:** ✅ Complete"]
    
    if data["accomplishments"]:
        for acc in data["accomplishments"][:5]:  # Limit to 5
            lines.append(f"- {acc}")
    
    if data["decisions"]:
        lines.append("")
        lines.append("**Key decisions:**")
        for decision in data["decisions"][:3]:  # Limit to 3
            lines.append(f"- {decision}")
    
    return "\n".join(lines)


def summarize_session(
    session_file: Optional[Path] = None,
    project_root: Optional[Path] = None,
) -> Dict[str, any]:
    """
    Summarize a session file (current session if not specified).
    
    Args:
        session_file: Path to session file (defaults to current session)
        project_root: Project root directory
    
    Returns:
        Dictionary with summary data
    """
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        project_root = Path.cwd()
    
    if session_file is None:
        # Find current session file
        session_files = sorted(project_root.glob("SESSION_*.md"))
        if not session_files:
            raise ValueError("No session file found in project root")
        session_file = session_files[-1]  # Most recent
    
    return extract_session_summary(session_file)

