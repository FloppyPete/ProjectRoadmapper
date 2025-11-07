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
        List of consistency issues found with fix suggestions
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
                    "fix": {
                        "action": "update_status",
                        "target_file": "README.md",
                        "old_status": readme_phase_4_status,
                        "new_status": phase_4_status,
                    },
                })
    
    # Check feature list consistency
    if readme_path.exists():
        roadmap_features = _extract_feature_list(roadmap_content)
        readme_features = _extract_feature_list(read_text_file(readme_path))
        
        if roadmap_features and readme_features:
            missing_in_readme = roadmap_features - readme_features
            if missing_in_readme:
                issues.append({
                    "type": "feature_mismatch",
                    "file": "README.md",
                    "message": f"Features in roadmap but not in README: {', '.join(list(missing_in_readme)[:3])}",
                    "priority": "low",
                    "fix": {
                        "action": "add_features",
                        "target_file": "README.md",
                        "features": list(missing_in_readme),
                    },
                })
    
    return issues


def fix_doc_consistency(
    issue: Dict[str, str],
    project_root: Optional[Path] = None,
    dry_run: bool = False,
) -> bool:
    """
    Auto-fix a documentation consistency issue.
    
    Args:
        issue: Consistency issue dictionary with fix information
        project_root: Project root directory
        dry_run: If True, only show what would be fixed
    
    Returns:
        True if fix was applied (or would be applied in dry_run)
    """
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        project_root = Path.cwd()
    
    if "fix" not in issue:
        return False
    
    fix_info = issue["fix"]
    target_file = project_root / fix_info["target_file"]
    
    if not target_file.exists():
        return False
    
    content = read_text_file(target_file)
    original_content = content
    
    if fix_info["action"] == "update_status":
        # Update phase status in file
        old_status = fix_info["old_status"]
        new_status = fix_info["new_status"]
        
        # Find and replace status
        patterns = [
            (rf"Phase 4.*?{re.escape(old_status)}", f"Phase 4: {new_status}"),
            (rf"🔵 Phase 4.*?{re.escape(old_status)}", f"🔵 Phase 4: {new_status}"),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.DOTALL)
    
    elif fix_info["action"] == "add_features":
        # Add missing features to README
        features = fix_info["features"]
        # This is more complex - would need to find the right place in README
        # For now, just log it
        if dry_run:
            return True
        # Implementation would need to parse README structure
    
    if dry_run:
        return content != original_content
    
    if content != original_content:
        from roadmapper.utils import write_text_file
        write_text_file(target_file, content)
        return True
    
    return False


def _extract_feature_list(content: str) -> Set[str]:
    """Extract feature list from content (simple heuristic)."""
    features = set()
    
    # Look for feature-like patterns
    # This is a simple implementation - could be enhanced
    feature_patterns = [
        r'roadmapper (\w+)',
        r'`roadmapper (\w+)`',
        r'roadmapper\.(\w+)',
    ]
    
    for pattern in feature_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        features.update(matches)
    
    return features


def _extract_phase_status(content: str, phase_name: str) -> Optional[str]:
    """Extract phase status from content."""
    # Look for phase status patterns
    patterns = [
        rf"{phase_name}.*?✅.*?Complete",
        rf"{phase_name}.*?🔵.*?In Progress",
        rf"{phase_name}.*?🟡.*?Planning",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            if "Complete" in match.group(0):
                return "Complete"
            elif "In Progress" in match.group(0):
                return "In Progress"
            elif "Planning" in match.group(0):
                return "Planning"
    
    return None


def suggest_next_steps(
    project_root: Optional[Path] = None,
) -> List[Dict[str, str]]:
    """
    Proactively suggest next steps based on roadmap progress.
    
    Args:
        project_root: Project root directory
    
    Returns:
        List of suggestions with type, priority, and message
    """
    suggestions = []
    
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        project_root = Path.cwd()
    
    roadmap_path = project_root / "PROJECT_ROADMAP.md"
    if not roadmap_path.exists():
        return suggestions
    
    roadmap_content = read_text_file(roadmap_path)
    
    # Find current phase
    current_phase = _find_current_phase(roadmap_content)
    if not current_phase:
        return suggestions
    
    # Check phase progress
    phase_status = _extract_phase_status(roadmap_content, current_phase)
    
    # Get recent session accomplishments
    session_files = sorted(project_root.glob("SESSION_*.md"))
    recent_accomplishments = []
    if session_files:
        latest_session = session_files[-1]
        session_content = read_text_file(latest_session)
        
        # Extract accomplishments
        if "## ✅ Session Accomplishments" in session_content:
            acc_section = session_content.split("## ✅ Session Accomplishments")[1].split("##")[0]
            accomplishments = re.findall(r'[-*]\s*✅\s*(.+?)(?=\n[-*]|\n##|\Z)', acc_section, re.MULTILINE)
            recent_accomplishments = [acc.strip() for acc in accomplishments[:5]]
    
    # Suggest based on phase
    if "Phase 4.2" in current_phase:
        # Check which 4.2 features are complete
        completed_features = []
        for feature_num in ["4.2.1", "4.2.2", "4.2.3", "4.2.4", "4.2.5", "4.2.6"]:
            if f"Phase {feature_num}" in roadmap_content or f"4.2.{feature_num[-1]}" in roadmap_content:
                # Check if marked complete
                feature_section = re.search(rf"Phase {feature_num}.*?(?=Phase |\Z)", roadmap_content, re.DOTALL | re.IGNORECASE)
                if feature_section and "✅" in feature_section.group(0):
                    completed_features.append(feature_num)
        
        # Suggest next incomplete feature
        all_features = ["4.2.1", "4.2.2", "4.2.3", "4.2.4", "4.2.5", "4.2.6"]
        for feature in all_features:
            if feature not in completed_features:
                feature_names = {
                    "4.2.1": "Auto-Generate Session Summaries",
                    "4.2.2": "Auto-Generate Commit Messages",
                    "4.2.3": "Smart Session Closing",
                    "4.2.4": "Incremental Documentation",
                    "4.2.5": "Documentation Consistency Checks",
                    "4.2.6": "Proactive Suggestions",
                }
                suggestions.append({
                    "type": "next_feature",
                    "priority": "high",
                    "message": f"Continue with Phase {feature}: {feature_names.get(feature, feature)}",
                    "action": f"Implement Phase {feature}",
                })
                break
    
    # Check if session needs closing
    if session_files:
        latest_session = session_files[-1]
        session_content = read_text_file(latest_session)
        
        # Check if session has accomplishments but not closed
        if "## ✅ Session Accomplishments" in session_content:
            if "roadmap" not in session_content.lower() or "archive" not in session_content.lower():
                suggestions.append({
                    "type": "session_close",
                    "priority": "medium",
                    "message": "Current session has accomplishments. Consider closing with 'roadmapper close'",
                    "action": "roadmapper close",
                })
    
    # Check if roadmap needs updating
    if recent_accomplishments:
        roadmap_content_lower = roadmap_content.lower()
        latest_session_id = session_files[-1].stem if session_files else None
        if latest_session_id and latest_session_id not in roadmap_content_lower:
            suggestions.append({
                "type": "roadmap_update",
                "priority": "high",
                "message": f"Session {latest_session_id} accomplishments not in roadmap. Update with 'roadmapper summarize --roadmap'",
                "action": "roadmapper summarize --roadmap",
            })
    
    return suggestions


def _find_current_phase(content: str) -> Optional[str]:
    """Find the current active phase from roadmap."""
    # Look for phase progress section
    phase_pattern = r'Phase Progress:.*?🔵 Phase (\d+[\.\d]*):\s*([^\n]+)'
    match = re.search(phase_pattern, content, re.DOTALL)
    if match:
        return f"Phase {match.group(1)}"
    
    # Fallback: look for first incomplete phase
    phase_pattern = r'🔵 Phase (\d+[\.\d]*):\s*([^\n]+)'
    match = re.search(phase_pattern, content)
    if match:
        return f"Phase {match.group(1)}"
    
    return None


# Import re for regex
import re

