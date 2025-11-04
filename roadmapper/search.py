"""Cross-project search functionality."""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from roadmapper.projects import get_all_projects
from roadmapper.utils import read_text_file
from roadmapper.history import read_history


class SearchResult:
    """Represents a single search result."""
    
    def __init__(
        self,
        project_name: str,
        project_path: Path,
        file_path: Path,
        file_type: str,
        matches: List[Tuple[int, str]],  # List of (line_number, line_content)
        context_lines: int = 2,
    ):
        self.project_name = project_name
        self.project_path = project_path
        self.file_path = file_path
        self.file_type = file_type  # "session", "roadmap", "history"
        self.matches = matches
        self.context_lines = context_lines
    
    def get_context(self) -> List[str]:
        """Get context lines around matches."""
        if not self.matches:
            return []
        
        try:
            content = read_text_file(self.file_path)
            lines = content.split("\n")
            
            context = []
            line_nums_covered = set()
            
            for line_num, _ in self.matches:
                # Add context before
                start = max(0, line_num - self.context_lines)
                end = min(len(lines), line_num + self.context_lines + 1)
                
                for i in range(start, end):
                    if i not in line_nums_covered:
                        context.append(f"{i+1:4d}| {lines[i]}")
                        line_nums_covered.add(i)
            
            return context
        except Exception:
            return []


def search_projects(
    query: str,
    project_paths: Optional[List[Path]] = None,
    file_types: Optional[List[str]] = None,
    case_sensitive: bool = False,
    max_results: int = 50,
) -> List[SearchResult]:
    """
    Search across multiple projects.
    
    Args:
        query: Search query (text to find)
        project_paths: Optional list of project paths to search (defaults to all registered)
        file_types: Optional list of file types to search ("session", "roadmap", "history")
        case_sensitive: Whether search should be case-sensitive
        max_results: Maximum number of results to return
    
    Returns:
        List of SearchResult objects
    """
    if file_types is None:
        file_types = ["session", "roadmap", "history"]
    
    # Get projects to search
    if project_paths is None:
        projects = get_all_projects()
        project_paths = [Path(p["path"]) for p in projects]
        project_names = {str(Path(p["path"])): p.get("name", Path(p["path"]).name) for p in projects}
    else:
        project_paths = [Path(p).resolve() for p in project_paths]
        project_names = {str(p): p.name for p in project_paths}
    
    # Prepare search pattern
    if case_sensitive:
        pattern = re.compile(re.escape(query))
    else:
        pattern = re.compile(re.escape(query), re.IGNORECASE)
    
    results = []
    
    for project_path in project_paths:
        if not project_path.exists():
            continue
        
        project_name = project_names.get(str(project_path), project_path.name)
        
        # Search session files
        if "session" in file_types:
            session_results = _search_sessions(project_path, project_name, pattern)
            results.extend(session_results)
        
        # Search roadmap
        if "roadmap" in file_types:
            roadmap_results = _search_roadmap(project_path, project_name, pattern)
            results.extend(roadmap_results)
        
        # Search history
        if "history" in file_types:
            history_results = _search_history(project_path, project_name, pattern)
            results.extend(history_results)
    
    # Limit results
    if len(results) > max_results:
        results = results[:max_results]
    
    return results


def _search_sessions(
    project_path: Path,
    project_name: str,
    pattern: re.Pattern,
) -> List[SearchResult]:
    """Search session files in a project."""
    results = []
    
    # Search current session files
    for session_file in project_path.glob("SESSION_*.md"):
        try:
            content = read_text_file(session_file)
            matches = _find_matches(content, pattern)
            if matches:
                results.append(SearchResult(
                    project_name=project_name,
                    project_path=project_path,
                    file_path=session_file,
                    file_type="session",
                    matches=matches,
                ))
        except Exception:
            continue
    
    # Search archived sessions
    archive_dir = project_path / "docs" / "archive" / "sessions"
    if archive_dir.exists():
        for session_file in archive_dir.glob("SESSION_*.md"):
            try:
                content = read_text_file(session_file)
                matches = _find_matches(content, pattern)
                if matches:
                    results.append(SearchResult(
                        project_name=project_name,
                        project_path=project_path,
                        file_path=session_file,
                        file_type="session",
                        matches=matches,
                    ))
            except Exception:
                continue
    
    return results


def _search_roadmap(
    project_path: Path,
    project_name: str,
    pattern: re.Pattern,
) -> List[SearchResult]:
    """Search roadmap file in a project."""
    results = []
    
    roadmap_file = project_path / "PROJECT_ROADMAP.md"
    if roadmap_file.exists():
        try:
            content = read_text_file(roadmap_file)
            matches = _find_matches(content, pattern)
            if matches:
                results.append(SearchResult(
                    project_name=project_name,
                    project_path=project_path,
                    file_path=roadmap_file,
                    file_type="roadmap",
                    matches=matches,
                ))
        except Exception:
            pass
    
    return results


def _search_history(
    project_path: Path,
    project_name: str,
    pattern: re.Pattern,
) -> List[SearchResult]:
    """Search history file in a project."""
    results = []
    
    try:
        history_records = read_history(project_path)
        if not history_records:
            return results
        
        # Convert history records to text for searching
        history_text = "\n".join([
            json.dumps(record, indent=2) for record in history_records
        ])
        
        matches = _find_matches(history_text, pattern)
        if matches:
            history_file = project_path / ".roadmapper" / "history.jsonl"
            results.append(SearchResult(
                project_name=project_name,
                project_path=project_path,
                file_path=history_file,
                file_type="history",
                matches=matches,
            ))
    except Exception:
        pass
    
    return results


def _find_matches(content: str, pattern: re.Pattern) -> List[Tuple[int, str]]:
    """
    Find all matches of pattern in content.
    
    Returns:
        List of (line_number, line_content) tuples
    """
    matches = []
    lines = content.split("\n")
    
    for line_num, line in enumerate(lines):
        if pattern.search(line):
            matches.append((line_num, line))
    
    return matches

