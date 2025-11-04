"""Platform-aware path utilities for roadmapper."""

import os
from pathlib import Path
from typing import Optional


def get_home_dir() -> Path:
    """Get user's home directory."""
    return Path.home()


def get_global_config_dir() -> Path:
    """Get global configuration directory (~/.roadmapper)."""
    home = get_home_dir()
    config_dir = home / ".roadmapper"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_global_config_file() -> Path:
    """Get global configuration file path (~/.roadmapper/config.toml)."""
    return get_global_config_dir() / "config.toml"


def get_project_root(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    Find project root by looking for .roadmapper.toml or PROJECT_ROADMAP.md.
    
    Args:
        start_path: Path to start searching from (defaults to current directory)
    
    Returns:
        Path to project root, or None if not found
    """
    if start_path is None:
        start_path = Path.cwd()
    
    current = Path(start_path).resolve()
    
    # Check up to 10 levels up
    for _ in range(10):
        if (current / ".roadmapper.toml").exists():
            return current
        if (current / "PROJECT_ROADMAP.md").exists():
            return current
        
        parent = current.parent
        if parent == current:  # Reached filesystem root
            break
        current = parent
    
    return None


def get_project_config_file(project_root: Optional[Path] = None) -> Optional[Path]:
    """
    Get project configuration file path (.roadmapper.toml).
    
    Args:
        project_root: Project root directory (searches from cwd if None)
    
    Returns:
        Path to project config file, or None if not found
    """
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        return None
    
    return project_root / ".roadmapper.toml"


def get_project_history_dir(project_root: Optional[Path] = None) -> Path:
    """
    Get project history directory (.roadmapper/).
    
    Args:
        project_root: Project root directory (searches from cwd if None)
    
    Returns:
        Path to project history directory (creates if needed)
    """
    if project_root is None:
        project_root = get_project_root()
    
    if project_root is None:
        # Fallback to current directory
        project_root = Path.cwd()
    
    history_dir = project_root / ".roadmapper"
    history_dir.mkdir(parents=True, exist_ok=True)
    return history_dir


def get_project_history_file(project_root: Optional[Path] = None) -> Path:
    """
    Get project history file path (.roadmapper/history.jsonl).
    
    Args:
        project_root: Project root directory (searches from cwd if None)
    
    Returns:
        Path to project history file
    """
    return get_project_history_dir(project_root) / "history.jsonl"

