"""Incremental documentation monitoring and suggestions."""

import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime

from roadmapper.paths import get_project_root
from roadmapper.utils import read_text_file


def get_recent_changes(
    project_root: Optional[Path] = None,
    since: Optional[str] = None,
) -> Dict[str, List[str]]:
    """
    Get recent git changes that might need documentation updates.
    
    Args:
        project_root: Project root directory
        since: Git ref or date (e.g., "HEAD~1", "2024-01-01")
    
    Returns:
        Dictionary with modified, added, deleted files
    """
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        project_root = Path.cwd()
    
    changes = {
        "modified": [],
        "added": [],
        "deleted": [],
        "code_files": [],
        "doc_files": [],
    }
    
    try:
        # Get git diff
        if since:
            cmd = ["git", "diff", "--name-status", since, "HEAD"]
        else:
            cmd = ["git", "diff", "--name-status", "HEAD"]
        
        result = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        
        if result.returncode != 0:
            # Try unstaged changes
            result = subprocess.run(
                ["git", "diff", "--name-status"],
                cwd=project_root,
                capture_output=True,
                text=True,
                check=False,
            )
        
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            
            # Parse git status line (format: XY filename)
            status_code = line[0]
            filename = line[1:].strip().split('\t')[-1] if '\t' in line else line[2:].strip()
            file_path = project_root / filename
            
            if status_code == 'M':
                changes["modified"].append(filename)
            elif status_code == 'A':
                changes["added"].append(filename)
            elif status_code == 'D':
                changes["deleted"].append(filename)
            
            # Categorize files
            if _is_code_file(file_path):
                changes["code_files"].append(filename)
            elif _is_doc_file(file_path):
                changes["doc_files"].append(filename)
    
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return changes


def _is_code_file(file_path: Path) -> bool:
    """Check if file is a code file."""
    code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.rs', '.go', '.rb', '.php'}
    return file_path.suffix.lower() in code_extensions


def _is_doc_file(file_path: Path) -> bool:
    """Check if file is a documentation file."""
    doc_extensions = {'.md', '.txt', '.rst', '.adoc'}
    doc_names = {'readme', 'changelog', 'license', 'contributing', 'roadmap'}
    return (
        file_path.suffix.lower() in doc_extensions
        or file_path.stem.lower() in doc_names
    )


def suggest_doc_updates(
    project_root: Optional[Path] = None,
    since: Optional[str] = None,
) -> List[Dict[str, str]]:
    """
    Suggest documentation updates based on code changes.
    
    Args:
        project_root: Project root directory
        since: Git ref or date to check changes since
    
    Returns:
        List of suggestions with type, file, and message
    """
    suggestions = []
    
    changes = get_recent_changes(project_root, since)
    
    # Check if new features were added
    new_code_files = [f for f in changes["added"] if f in changes["code_files"]]
    if new_code_files:
        suggestions.append({
            "type": "new_feature",
            "file": "PROJECT_ROADMAP.md",
            "message": f"New code files added: {', '.join(new_code_files[:3])}. Consider updating roadmap with new features.",
            "priority": "medium",
        })
    
    # Check if major modules were modified
    modified_modules = [f for f in changes["modified"] if f in changes["code_files"]]
    significant_modules = [f for f in modified_modules if _is_significant_module(f)]
    if significant_modules:
        suggestions.append({
            "type": "module_update",
            "file": "PROJECT_ROADMAP.md",
            "message": f"Significant modules modified: {', '.join(significant_modules[:3])}. Consider updating roadmap status.",
            "priority": "low",
        })
    
    # Check if README needs updates
    if changes["added"] or significant_modules:
        suggestions.append({
            "type": "readme_update",
            "file": "README.md",
            "message": "New features or significant changes detected. Consider updating README features list.",
            "priority": "low",
        })
    
    # Check if session file has accomplishments but roadmap not updated
    roadmap_path = project_root / "PROJECT_ROADMAP.md" if project_root else Path.cwd() / "PROJECT_ROADMAP.md"
    if roadmap_path.exists():
        session_files = sorted((project_root or Path.cwd()).glob("SESSION_*.md"))
        if session_files:
            latest_session = session_files[-1]
            session_content = read_text_file(latest_session)
            
            # Check if session has accomplishments
            if "## ✅ Session Accomplishments" in session_content or "**Completed:**" in session_content:
                # Check if roadmap was recently updated
                roadmap_content = read_text_file(roadmap_path)
                session_id = latest_session.stem
                
                if session_id not in roadmap_content:
                    suggestions.append({
                        "type": "roadmap_update",
                        "file": "PROJECT_ROADMAP.md",
                        "message": f"Session {session_id} has accomplishments but roadmap not updated. Use 'roadmapper summarize --roadmap' to generate summary.",
                        "priority": "high",
                    })
    
    return suggestions


def _is_significant_module(filename: str) -> bool:
    """Check if a module is significant (main modules, not tests)."""
    significant_patterns = [
        'cli.py',
        'init.py',
        'session.py',
        'dashboard.py',
        'projects.py',
        'search.py',
        'knowledge.py',
    ]
    return any(pattern in filename for pattern in significant_patterns)


def check_doc_consistency(
    project_root: Optional[Path] = None,
) -> List[Dict[str, str]]:
    """
    Check documentation consistency across files.
    
    Args:
        project_root: Project root directory
    
    Returns:
        List of consistency issues found
    """
    issues = []
    
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        project_root = Path.cwd()
    
    roadmap_path = project_root / "PROJECT_ROADMAP.md"
    readme_path = project_root / "README.md"
    
    if not roadmap_path.exists():
        return issues
    
    roadmap_content = read_text_file(roadmap_path)
    
    # Check phase status consistency
    if "Phase 4" in roadmap_content:
        # Look for phase status indicators
        phase_4_status = _extract_phase_status(roadmap_content, "Phase 4")
        
        if readme_path.exists():
            readme_content = read_text_file(readme_path)
            readme_phase_4_status = _extract_phase_status(readme_content, "Phase 4")
            
            if phase_4_status != readme_phase_4_status and readme_phase_4_status:
                issues.append({
                    "type": "status_mismatch",
                    "file": "README.md",
                    "message": f"Phase 4 status mismatch: Roadmap shows '{phase_4_status}', README shows '{readme_phase_4_status}'",
                    "priority": "medium",
                })
    
    return issues


def _extract_phase_status(content: str, phase_name: str) -> Optional[str]:
    """Extract phase status from content."""
    # Look for phase status patterns
    patterns = [
        rf"{phase_name}.*?✅.*?Complete",
        rf"{phase_name}.*?🔵.*?In Progress",
        rf"{phase_name}.*?🟡.*?Planning",
    ]
    
    for pattern in patterns:
        match = __import__('re').search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            if "Complete" in match.group(0):
                return "Complete"
            elif "In Progress" in match.group(0):
                return "In Progress"
            elif "Planning" in match.group(0):
                return "Planning"
    
    return None


# Import re for regex
import re

