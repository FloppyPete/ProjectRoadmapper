"""Project registry for cross-project intelligence."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import os

from roadmapper.paths import get_global_config_dir, get_project_root
from roadmapper.utils import read_text_file, write_text_file
from roadmapper.history import read_history, get_session_stats


def get_projects_registry_file() -> Path:
    """Get path to projects registry file (~/.roadmapper/projects.json)."""
    return get_global_config_dir() / "projects.json"


def load_projects_registry() -> Dict[str, Dict]:
    """
    Load projects registry from disk.
    
    Returns:
        Dictionary mapping project paths to project metadata
    """
    registry_file = get_projects_registry_file()
    
    if not registry_file.exists():
        return {}
    
    try:
        content = read_text_file(registry_file)
        return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return {}


def save_projects_registry(registry: Dict[str, Dict]) -> None:
    """
    Save projects registry to disk.
    
    Args:
        registry: Dictionary mapping project paths to project metadata
    """
    registry_file = get_projects_registry_file()
    content = json.dumps(registry, indent=2, sort_keys=True)
    write_text_file(registry_file, content)


def register_project(project_path: Path, name: Optional[str] = None) -> Dict[str, any]:
    """
    Register a project in the registry.
    
    Args:
        project_path: Path to project root
        name: Optional project name (defaults to directory name)
    
    Returns:
        Project metadata dictionary
    """
    project_path = project_path.resolve()
    project_key = str(project_path)
    
    registry = load_projects_registry()
    
    # Get project name
    if name is None:
        name = project_path.name
    
    # Get last session info
    last_session = get_last_session_info(project_path)
    
    # Get health status
    health = get_project_health(project_path)
    
    project_info = {
        "path": project_key,
        "name": name,
        "registered_at": datetime.now().isoformat(),
        "last_session": last_session,
        "health": health,
    }
    
    registry[project_key] = project_info
    save_projects_registry(registry)
    
    return project_info


def unregister_project(project_path: Path) -> bool:
    """
    Unregister a project from the registry.
    
    Args:
        project_path: Path to project root
    
    Returns:
        True if project was registered and removed, False otherwise
    """
    project_path = project_path.resolve()
    project_key = str(project_path)
    
    registry = load_projects_registry()
    
    if project_key not in registry:
        return False
    
    del registry[project_key]
    save_projects_registry(registry)
    
    return True


def get_all_projects() -> List[Dict[str, any]]:
    """
    Get all registered projects with updated metadata.
    
    Returns:
        List of project metadata dictionaries
    """
    registry = load_projects_registry()
    projects = []
    
    for project_key, project_info in registry.items():
        project_path = Path(project_key)
        
        # Skip if project no longer exists
        if not project_path.exists():
            continue
        
        # Update metadata
        project_info["last_session"] = get_last_session_info(project_path)
        project_info["health"] = get_project_health(project_path)
        
        projects.append(project_info)
    
    # Remove non-existent projects from registry
    updated_registry = {
        key: info for key, info in registry.items()
        if Path(key).exists()
    }
    if len(updated_registry) != len(registry):
        save_projects_registry(updated_registry)
    
    return projects


def get_last_session_info(project_path: Path) -> Optional[Dict[str, any]]:
    """
    Get information about the last session for a project.
    
    Args:
        project_path: Path to project root
    
    Returns:
        Dictionary with last_session_date and last_session_file, or None
    """
    try:
        history = read_history(project_path, limit=1)
        if history:
            session = history[0]
            return {
                "date": session.get("date"),  # History uses "date" not "timestamp"
                "file": session.get("file"),  # History uses "file" not "session_file"
                "branch": session.get("branch"),
            }
    except Exception:
        pass
    
    return None


def get_project_health(project_path: Path) -> str:
    """
    Assess project health based on various indicators.
    
    Args:
        project_path: Path to project root
    
    Returns:
        Health status: "healthy", "stale", or "unknown"
    """
    # Check if PROJECT_ROADMAP.md exists
    roadmap_file = project_path / "PROJECT_ROADMAP.md"
    if not roadmap_file.exists():
        return "unknown"
    
    # Check last session date
    try:
        stats = get_session_stats(project_path)
        if stats.get("total_sessions", 0) == 0:
            return "unknown"
        
        # Check if last session was within 30 days
        last_session = get_last_session_info(project_path)
        if last_session and last_session.get("date"):
            try:
                last_date = datetime.fromisoformat(last_session["date"].replace("Z", "+00:00"))
                days_ago = (datetime.now(last_date.tzinfo) - last_date).days
                
                if days_ago > 30:
                    return "stale"
                elif days_ago > 7:
                    return "inactive"
                else:
                    return "healthy"
            except Exception:
                pass
    except Exception:
        pass
    
    return "unknown"


def discover_projects(search_paths: Optional[List[Path]] = None) -> List[Path]:
    """
    Discover projects by scanning common locations.
    
    Args:
        search_paths: Optional list of paths to search (defaults to common locations)
    
    Returns:
        List of discovered project root paths
    """
    if search_paths is None:
        # Default: search in common project locations
        home = Path.home()
        search_paths = [
            home / "Projects",
            home / "projects",
            home / "Documents" / "Projects",
            home / "Development",
            home / "dev",
            Path.home() / "source",
            Path.home() / "code",
        ]
    
    discovered = []
    
    for search_path in search_paths:
        if not search_path.exists():
            continue
        
        # Recursively search for PROJECT_ROADMAP.md files
        try:
            for roadmap_file in search_path.rglob("PROJECT_ROADMAP.md"):
                project_root = roadmap_file.parent
                # Verify it's actually a roadmapper project
                if (project_root / ".roadmapper.toml").exists() or roadmap_file.exists():
                    discovered.append(project_root)
        except (PermissionError, OSError):
            # Skip directories we can't access
            continue
    
    # Remove duplicates
    return list(set(discovered))


def update_project_registry() -> int:
    """
    Update registry with newly discovered projects.
    
    Returns:
        Number of newly registered projects
    """
    registry = load_projects_registry()
    discovered = discover_projects()
    new_count = 0
    
    for project_path in discovered:
        project_key = str(project_path.resolve())
        
        if project_key not in registry:
            register_project(project_path)
            new_count += 1
    
    return new_count

