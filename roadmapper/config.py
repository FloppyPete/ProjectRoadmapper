"""Configuration management for roadmapper."""

from pathlib import Path
from typing import Any, Dict, Optional
import os

try:
    import tomli
except ImportError:
    try:
        import tomllib as tomli  # Python 3.11+
    except ImportError:
        tomli = None

from roadmapper.paths import (
    get_global_config_file,
    get_project_config_file,
    get_project_root,
)
from roadmapper.utils import read_text_file, write_text_file


# Default configuration
DEFAULT_CONFIG: Dict[str, Any] = {
    "preferences": {
        "template_variant": "default",
        "editor": os.getenv("EDITOR", "code"),
        "ai_assistant": "cursor",
    },
    "git": {
        "commit_template": "feat: {summary}",
    },
}


def _load_toml(file_path: Path) -> Dict[str, Any]:
    """
    Load TOML file.
    
    Args:
        file_path: Path to TOML file
    
    Returns:
        Parsed TOML as dictionary, or empty dict if file doesn't exist or can't be parsed
    """
    if not file_path.exists():
        return {}
    
    if tomli is None:
        raise ImportError(
            "TOML support requires 'tomli' package. Install with: pip install tomli"
        )
    
    try:
        content = read_text_file(file_path)
        return tomli.loads(content)
    except Exception as e:
        # Return empty dict on parse errors
        return {}


def _save_toml(file_path: Path, config: Dict[str, Any]) -> None:
    """
    Save configuration to TOML file.
    
    Args:
        file_path: Path to save to
        config: Configuration dictionary
    """
    if tomli is None:
        raise ImportError(
            "TOML support requires 'tomli' package. Install with: pip install tomli"
        )
    
    # Use tomli-w for writing (or fallback to manual TOML generation)
    try:
        import tomli_w
        content = tomli_w.dumps(config)
    except ImportError:
        # Fallback: basic TOML generation
        content = _dict_to_toml(config)
    
    write_text_file(file_path, content)


def _dict_to_toml(data: Dict[str, Any], indent: int = 0) -> str:
    """Convert dictionary to TOML string (basic implementation)."""
    lines = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"[{key}]")
            for subkey, subvalue in value.items():
                if isinstance(subvalue, str):
                    lines.append(f'{subkey} = "{subvalue}"')
                elif isinstance(subvalue, bool):
                    lines.append(f"{subkey} = {str(subvalue).lower()}")
                else:
                    lines.append(f"{subkey} = {subvalue}")
            lines.append("")
        elif isinstance(value, str):
            lines.append(f'{key} = "{value}"')
        elif isinstance(value, bool):
            lines.append(f"{key} = {str(value).lower()}")
        else:
            lines.append(f"{key} = {value}")
    return "\n".join(lines)


def load_config(project_root: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load merged configuration (project overrides global overrides defaults).
    
    Args:
        project_root: Project root directory (searches from cwd if None)
    
    Returns:
        Merged configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()
    
    # Load global config
    global_config_file = get_global_config_file()
    if global_config_file.exists():
        global_config = _load_toml(global_config_file)
        _deep_merge(config, global_config)
    
    # Load project config (overrides global)
    if project_root is None:
        project_root = get_project_root()
    
    if project_root:
        project_config_file = get_project_config_file(project_root)
        if project_config_file and project_config_file.exists():
            project_config = _load_toml(project_config_file)
            _deep_merge(config, project_config)
    
    return config


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> None:
    """Recursively merge override into base."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


def get_config_value(key: str, project_root: Optional[Path] = None) -> Optional[Any]:
    """
    Get a configuration value using dot notation (e.g., 'preferences.editor').
    
    Args:
        key: Configuration key in dot notation
        project_root: Project root directory (searches from cwd if None)
    
    Returns:
        Configuration value, or None if not found
    """
    config = load_config(project_root)
    keys = key.split(".")
    value = config
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return None
    return value


def set_config_value(
    key: str,
    value: Any,
    scope: str = "project",
    project_root: Optional[Path] = None,
) -> None:
    """
    Set a configuration value.
    
    Args:
        key: Configuration key in dot notation (e.g., 'preferences.editor')
        value: Value to set
        scope: 'global' or 'project' (default: 'project')
        project_root: Project root directory (searches from cwd if None)
    """
    if scope == "global":
        config_file = get_global_config_file()
        config = _load_toml(config_file)
    else:
        if project_root is None:
            project_root = get_project_root()
            if project_root is None:
                raise ValueError("Not in a roadmapper project. Run 'roadmapper init' first.")
        
        config_file = get_project_config_file(project_root)
        if config_file is None:
            config_file = project_root / ".roadmapper.toml"
        config = _load_toml(config_file) if config_file.exists() else {}
    
    # Set nested value
    keys = key.split(".")
    current = config
    for k in keys[:-1]:
        if k not in current:
            current[k] = {}
        current = current[k]
    current[keys[-1]] = value
    
    # Save
    _save_toml(config_file, config)


def reset_config_value(
    key: str,
    scope: str = "project",
    project_root: Optional[Path] = None,
) -> None:
    """
    Reset a configuration value (remove from config file).
    
    Args:
        key: Configuration key in dot notation
        scope: 'global' or 'project' (default: 'project')
        project_root: Project root directory (searches from cwd if None)
    """
    if scope == "global":
        config_file = get_global_config_file()
        config = _load_toml(config_file)
    else:
        if project_root is None:
            project_root = get_project_root()
            if project_root is None:
                raise ValueError("Not in a roadmapper project. Run 'roadmapper init' first.")
        
        config_file = get_project_config_file(project_root)
        if config_file is None or not config_file.exists():
            return  # Nothing to reset
        config = _load_toml(config_file)
    
    # Remove nested value
    keys = key.split(".")
    current = config
    for k in keys[:-1]:
        if k not in current:
            return  # Key doesn't exist
        current = current[k]
    
    if keys[-1] in current:
        del current[keys[-1]]
        
        # Clean up empty sections
        _clean_empty_sections(config, keys[:-1])
        
        # Save
        _save_toml(config_file, config)


def _clean_empty_sections(config: Dict[str, Any], section_path: list) -> None:
    """Remove empty sections after deleting a value."""
    if not section_path:
        return
    
    current = config
    for k in section_path[:-1]:
        if k not in current:
            return
        current = current[k]
    
    last_key = section_path[-1]
    if last_key in current and isinstance(current[last_key], dict) and not current[last_key]:
        del current[last_key]

