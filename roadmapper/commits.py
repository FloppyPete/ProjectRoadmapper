"""Auto-generate commit messages from session logs and git diffs."""

import subprocess
from pathlib import Path
from typing import Optional, List, Dict

from roadmapper.paths import get_project_root
from roadmapper.summarize import extract_session_summary


def get_git_diff(project_root: Optional[Path] = None) -> str:
    """
    Get git diff of staged and unstaged changes.
    
    Args:
        project_root: Project root directory
    
    Returns:
        Git diff output as string
    """
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        project_root = Path.cwd()
    
    try:
        # Get staged changes
        result = subprocess.run(
            ["git", "diff", "--cached"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        staged_diff = result.stdout
        
        # Get unstaged changes
        result = subprocess.run(
            ["git", "diff"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        unstaged_diff = result.stdout
        
        return staged_diff + unstaged_diff
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def get_git_status(project_root: Optional[Path] = None) -> Dict[str, List[str]]:
    """
    Get git status information.
    
    Args:
        project_root: Project root directory
    
    Returns:
        Dictionary with modified, added, deleted files
    """
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        project_root = Path.cwd()
    
    status = {
        "modified": [],
        "added": [],
        "deleted": [],
        "renamed": [],
    }
    
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            
            # Parse git status line (format: XY filename)
            status_code = line[:2]
            filename = line[3:].strip()
            
            if status_code[0] == 'M' or status_code[1] == 'M':
                status["modified"].append(filename)
            elif status_code[0] == 'A' or status_code[1] == 'A':
                status["added"].append(filename)
            elif status_code[0] == 'D' or status_code[1] == 'D':
                status["deleted"].append(filename)
            elif status_code[0] == 'R':
                status["renamed"].append(filename)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return status


def generate_commit_message(
    session_file: Optional[Path] = None,
    project_root: Optional[Path] = None,
) -> str:
    """
    Generate a structured commit message from session and git changes.
    
    Args:
        session_file: Path to session file (defaults to current session)
        project_root: Project root directory
    
    Returns:
        Generated commit message
    """
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        project_root = Path.cwd()
    
    # Get session summary
    if session_file is None:
        session_files = sorted(project_root.glob("SESSION_*.md"))
        if session_files:
            session_file = session_files[-1]
    
    session_data = {}
    if session_file and session_file.exists():
        session_data = extract_session_summary(session_file)
        session_id = session_file.stem
    else:
        session_id = "current"
    
    # Get git status
    git_status = get_git_status(project_root)
    
    # Determine commit type from changes
    commit_type = _determine_commit_type(git_status, session_data)
    
    # Build commit message
    message_parts = []
    
    # Header: type(scope): subject
    subject = _generate_subject(session_data, git_status)
    header = f"{commit_type}: {subject}"
    message_parts.append(header)
    message_parts.append("")
    
    # Body: details from session
    if session_data.get("accomplishments"):
        message_parts.append("**Changes:**")
        for acc in session_data["accomplishments"][:5]:  # Limit to 5
            # Clean up accomplishment text
            acc_clean = acc.replace("✅", "").strip()
            if acc_clean:
                message_parts.append(f"- {acc_clean}")
        message_parts.append("")
    
    # Footer: session reference
    if session_file:
        message_parts.append(f"Session: {session_id}")
    
    return "\n".join(message_parts)


def _determine_commit_type(
    git_status: Dict[str, List[str]],
    session_data: Dict,
) -> str:
    """
    Determine commit type based on changes.
    
    Returns:
        Commit type: feat, fix, docs, refactor, etc.
    """
    # Check session data for clues
    accomplishments = session_data.get("accomplishments", [])
    accomplishments_text = " ".join(accomplishments).lower()
    
    # Check file types
    modified_files = git_status.get("modified", [])
    added_files = git_status.get("added", [])
    
    # Determine type
    if any("doc" in f.lower() or "readme" in f.lower() or "guide" in f.lower() for f in modified_files + added_files):
        return "docs"
    elif any("test" in f.lower() for f in modified_files + added_files):
        return "test"
    elif "fix" in accomplishments_text or "bug" in accomplishments_text or "error" in accomplishments_text:
        return "fix"
    elif "refactor" in accomplishments_text:
        return "refactor"
    elif any(f.endswith(".md") for f in added_files + modified_files) and "template" in accomplishments_text:
        return "docs"
    elif any("feature" in accomplishments_text or "add" in accomplishments_text or "implement" in accomplishments_text):
        return "feat"
    else:
        return "feat"  # Default


def _generate_subject(
    session_data: Dict,
    git_status: Dict[str, List[str]],
) -> str:
    """
    Generate commit subject line.
    
    Args:
        session_data: Session summary data
        git_status: Git status information
    
    Returns:
        Subject line for commit message
    """
    # Try to extract from first accomplishment
    accomplishments = session_data.get("accomplishments", [])
    if accomplishments:
        # Take first accomplishment and create subject
        first_acc = accomplishments[0]
        # Remove prefixes and clean up
        subject = first_acc.replace("✅", "").replace("Phase", "").strip()
        # Remove common prefixes
        subject = re.sub(r'^(Completed|Added|Created|Implemented|Fixed):?\s*', '', subject, flags=re.IGNORECASE)
        # Limit length
        if len(subject) > 72:
            subject = subject[:69] + "..."
        return subject
    
    # Fallback: generate from file changes
    added = git_status.get("added", [])
    modified = git_status.get("modified", [])
    
    if added:
        # Use first added file
        filename = Path(added[0]).stem
        return f"Add {filename}"
    elif modified:
        # Use first modified file
        filename = Path(modified[0]).stem
        return f"Update {filename}"
    else:
        return "Update project"


# Import re for regex in _generate_subject
import re

