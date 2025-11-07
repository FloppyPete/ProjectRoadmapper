"""Smart session closing functionality."""

from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from roadmapper.paths import get_project_root
from roadmapper.utils import read_text_file, write_text_file
from roadmapper.summarize import extract_session_summary, generate_roadmap_summary
from roadmapper.context import add_session_summary


def close_session(
    session_file: Optional[Path] = None,
    project_root: Optional[Path] = None,
    archive: bool = True,
    update_roadmap: bool = True,
    update_context: bool = True,
) -> Dict[str, any]:
    """
    Smart session closing: summarize, suggest next steps, generate handoff.
    
    Args:
        session_file: Path to session file (defaults to current session)
        project_root: Project root directory
        archive: Whether to archive the session file
        update_roadmap: Whether to update PROJECT_ROADMAP.md
        update_context: Whether to update context compression
    
    Returns:
        Dictionary with summary, next_goals, handoff_prompt, and actions taken
    """
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        project_root = Path.cwd()
    
    # Find session file if not provided
    if session_file is None:
        session_files = sorted(project_root.glob("SESSION_*.md"))
        if not session_files:
            raise ValueError("No session file found in project root")
        session_file = session_files[-1]
    
    # Extract session summary
    session_data = extract_session_summary(session_file)
    session_id = session_file.stem
    
    # Read session file for metadata
    session_content = read_text_file(session_file)
    
    # Extract YAML frontmatter if present
    metadata = _extract_yaml_frontmatter(session_content)
    project_name = metadata.get("project", "Unknown Project")
    phase = metadata.get("phase", "Unknown Phase")
    
    # Generate next session goals based on roadmap
    next_goals = _suggest_next_goals(project_root, session_data, phase)
    
    # Generate handoff prompt for AI continuation
    handoff_prompt = _generate_handoff_prompt(
        session_id,
        session_data,
        next_goals,
        project_name,
        phase,
    )
    
    # Actions taken
    actions = {
        "archived": False,
        "roadmap_updated": False,
        "context_updated": False,
    }
    
    # Update context compression
    if update_context:
        try:
            accomplishments = session_data.get("accomplishments", [])
            decisions = session_data.get("decisions", [])
            insights = session_data.get("discoveries", [])
            
            summary_text = _generate_summary_text(session_data)
            
            add_session_summary(
                session_file=session_file,
                session_id=session_id,
                project_name=project_name,
                phase=phase,
                summary=summary_text,
                accomplishments=accomplishments,
                decisions=decisions,
                insights=insights,
                project_root=project_root,
            )
            actions["context_updated"] = True
        except Exception as e:
            # Don't fail if context update fails
            pass
    
    # Update roadmap
    if update_roadmap:
        try:
            roadmap_summary = generate_roadmap_summary(session_file)
            _update_roadmap(project_root, session_id, roadmap_summary)
            actions["roadmap_updated"] = True
        except Exception as e:
            # Don't fail if roadmap update fails
            pass
    
    # Archive session file
    if archive:
        try:
            archive_path = _archive_session(session_file, project_root)
            actions["archived"] = True
            actions["archive_path"] = str(archive_path)
        except Exception as e:
            # Don't fail if archiving fails
            pass
    
    return {
        "session_id": session_id,
        "summary": session_data,
        "next_goals": next_goals,
        "handoff_prompt": handoff_prompt,
        "actions": actions,
    }


def _extract_yaml_frontmatter(content: str) -> Dict[str, str]:
    """Extract YAML frontmatter from session file."""
    metadata = {}
    
    if content.startswith("---"):
        # Extract YAML frontmatter
        parts = content.split("---", 2)
        if len(parts) >= 3:
            yaml_content = parts[1].strip()
            for line in yaml_content.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    metadata[key] = value
    
    return metadata


def _suggest_next_goals(
    project_root: Path,
    session_data: Dict,
    current_phase: str,
) -> List[str]:
    """
    Suggest next session goals based on roadmap and current progress.
    
    Args:
        project_root: Project root directory
        session_data: Session summary data
        current_phase: Current phase name
    
    Returns:
        List of suggested goals
    """
    goals = []
    
    # Read roadmap to find next tasks
    roadmap_path = project_root / "PROJECT_ROADMAP.md"
    if roadmap_path.exists():
        roadmap_content = read_text_file(roadmap_path)
        
        # Look for current phase and next items
        # Simple heuristic: find current phase, suggest next items
        if "Phase 4.2" in current_phase:
            # We're in Phase 4.2, suggest remaining 4.2 features
            completed_features = []
            accomplishments_text = " ".join(session_data.get("accomplishments", [])).lower()
            
            if "4.2.1" in accomplishments_text or "summarize" in accomplishments_text:
                completed_features.append("4.2.1")
            if "4.2.2" in accomplishments_text or "commit" in accomplishments_text:
                completed_features.append("4.2.2")
            
            if "4.2.1" not in completed_features:
                goals.append("Complete Phase 4.2.1: Auto-Generate Session Summaries")
            elif "4.2.2" not in completed_features:
                goals.append("Complete Phase 4.2.2: Auto-Generate Commit Messages")
            elif "4.2.3" not in accomplishments_text.lower():
                goals.append("Complete Phase 4.2.3: Smart Session Closing")
            else:
                goals.append("Continue with Phase 4.2.4: Incremental Documentation")
        else:
            # Generic next steps
            goals.append("Continue with next phase tasks")
            goals.append("Review and test completed features")
    
    # Add generic goals if none found
    if not goals:
        goals.append("Review session accomplishments")
        goals.append("Plan next development tasks")
        goals.append("Update documentation as needed")
    
    return goals


def _generate_handoff_prompt(
    session_id: str,
    session_data: Dict,
    next_goals: List[str],
    project_name: str,
    phase: str,
) -> str:
    """
    Generate handoff prompt for AI continuation.
    
    Args:
        session_id: Session identifier
        session_data: Session summary data
        next_goals: Suggested next goals
        project_name: Project name
        phase: Current phase
    
    Returns:
        Formatted handoff prompt
    """
    lines = [
        f"# Session Handoff: {session_id}",
        "",
        f"**Project:** {project_name}",
        f"**Phase:** {phase}",
        "",
        "## Session Summary",
        "",
    ]
    
    # Add accomplishments
    accomplishments = session_data.get("accomplishments", [])
    if accomplishments:
        lines.append("**Completed:**")
        for acc in accomplishments[:5]:  # Limit to 5
            lines.append(f"- {acc}")
        lines.append("")
    
    # Add decisions
    decisions = session_data.get("decisions", [])
    if decisions:
        lines.append("**Key Decisions:**")
        for decision in decisions[:3]:  # Limit to 3
            lines.append(f"- {decision}")
        lines.append("")
    
    # Add next goals
    if next_goals:
        lines.append("## Suggested Next Goals")
        lines.append("")
        for goal in next_goals:
            lines.append(f"- {goal}")
        lines.append("")
    
    lines.append("## Instructions for Next Session")
    lines.append("")
    lines.append("1. Read PROJECT_ROADMAP.md for current phase status")
    lines.append("2. Review session accomplishments above")
    lines.append("3. Continue with suggested goals or user-specified tasks")
    lines.append("4. Use reasoning markers and structured tasks for tracking")
    lines.append("")
    
    return "\n".join(lines)


def _generate_summary_text(session_data: Dict) -> str:
    """Generate a concise summary text from session data."""
    accomplishments = session_data.get("accomplishments", [])
    if accomplishments:
        return accomplishments[0] if len(accomplishments[0]) < 200 else accomplishments[0][:197] + "..."
    return "Session work completed."


def _update_roadmap(project_root: Path, session_id: str, summary: str) -> None:
    """Update PROJECT_ROADMAP.md with session summary."""
    roadmap_path = project_root / "PROJECT_ROADMAP.md"
    if not roadmap_path.exists():
        return
    
    content = read_text_file(roadmap_path)
    
    # Find "Recent Sessions" section
    if "## 💡 Recent Sessions" in content:
        # Insert new session summary after the section header
        insertion_point = content.find("## 💡 Recent Sessions") + len("## 💡 Recent Sessions")
        new_content = (
            content[:insertion_point]
            + "\n\n"
            + summary
            + "\n\n"
            + content[insertion_point:]
        )
        write_text_file(roadmap_path, new_content)
    else:
        # Append to end before final note
        if "**Note:**" in content:
            note_pos = content.find("**Note:**")
            new_content = (
                content[:note_pos]
                + "\n\n## 💡 Recent Sessions\n\n"
                + summary
                + "\n\n"
                + content[note_pos:]
            )
            write_text_file(roadmap_path, new_content)


def _archive_session(session_file: Path, project_root: Path) -> Path:
    """Archive session file to docs/archive/sessions/."""
    archive_dir = project_root / "docs" / "archive" / "sessions"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    archive_path = archive_dir / session_file.name
    
    # Copy file to archive
    session_content = read_text_file(session_file)
    write_text_file(archive_path, session_content)
    
    # Delete original
    session_file.unlink()
    
    return archive_path

