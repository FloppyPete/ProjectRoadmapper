"""Main CLI interface for roadmapper."""

import click
from datetime import datetime
from pathlib import Path
import sys

from roadmapper import __version__
from roadmapper.init import init_project
from roadmapper.session import create_session
from roadmapper.status import show_status
from roadmapper.utils import ensure_utf8_console
from roadmapper.config import (
    load_config,
    get_config_value,
    set_config_value,
    reset_config_value,
)
from roadmapper.paths import get_project_root
from roadmapper.history import read_history, get_session_stats
from roadmapper.projects import (
    get_all_projects,
    register_project,
    unregister_project,
    update_project_registry,
    discover_projects,
)


@click.group()
@click.version_option(version=__version__, prog_name="roadmapper")
def main():
    """
    ProjectRoadmapper - Multi-session development workflow tool.
    
    Helps maintain context and momentum across multiple development sessions,
    especially when working with AI assistants.
    """
    # Ensure UTF-8 encoding for console output (especially Windows)
    ensure_utf8_console()


@main.command()
@click.option(
    "--template",
    type=click.Choice(["default", "minimal", "detailed"], case_sensitive=False),
    default="default",
    help="Template to use for project initialization",
)
@click.option(
    "--no-git",
    is_flag=True,
    help="Skip git initialization if repository doesn't exist",
)
def init(template, no_git):
    """
    Initialize a new project with roadmapper workflow.
    
    Creates the directory structure, templates, and initial roadmap file.
    """
    try:
        init_project(template=template, init_git=not no_git)
        click.echo("✅ Project initialized successfully!")
    except Exception as e:
        click.echo(f"❌ Error initializing project: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--name",
    help="Custom session name (optional, defaults to date-based)",
)
def session(name):
    """
    Create a new session file.
    
    Creates a new session file with proper naming (SESSION_YYYY_MM_DD_X.md).
    Auto-increments session letters if multiple sessions exist for the same date.
    """
    try:
        session_path = create_session(name=name)
        click.echo(f"✅ Created session file: {session_path}")
    except Exception as e:
        click.echo(f"❌ Error creating session: {e}", err=True)
        sys.exit(1)


@main.command()
def status():
    """
    Show current project status.
    
    Displays current session, recent sessions, and git status summary.
    """
    try:
        show_status()
    except Exception as e:
        click.echo(f"❌ Error getting status: {e}", err=True)
        sys.exit(1)


@main.group()
def config():
    """Manage roadmapper configuration."""
    pass


@config.command("set")
@click.argument("key")
@click.argument("value")
@click.option(
    "--scope",
    type=click.Choice(["global", "project"], case_sensitive=False),
    default="project",
    help="Set in global or project config (default: project)",
)
def config_set(key, value, scope):
    """Set a configuration value."""
    try:
        project_root = get_project_root() if scope == "project" else None
        set_config_value(key, value, scope=scope, project_root=project_root)
        click.echo(f"✅ Set {key} = {value} ({scope})")
    except Exception as e:
        click.echo(f"❌ Error setting config: {e}", err=True)
        sys.exit(1)


@config.command("get")
@click.argument("key")
def config_get(key):
    """Get a configuration value."""
    try:
        project_root = get_project_root()
        value = get_config_value(key, project_root=project_root)
        if value is None:
            click.echo(f"⚠️  Key '{key}' not found")
            sys.exit(1)
        click.echo(value)
    except Exception as e:
        click.echo(f"❌ Error getting config: {e}", err=True)
        sys.exit(1)


@config.command("list")
@click.option(
    "--scope",
    type=click.Choice(["global", "project", "merged"], case_sensitive=False),
    default="merged",
    help="Show global, project, or merged config (default: merged)",
)
def config_list(scope):
    """List configuration values."""
    try:
        project_root = get_project_root() if scope != "global" else None
        
        if scope == "merged":
            config = load_config(project_root=project_root)
            click.echo("📋 Merged Configuration (project overrides global):\n")
        elif scope == "global":
            from roadmapper.config import _load_toml
            from roadmapper.paths import get_global_config_file
            config_file = get_global_config_file()
            config = _load_toml(config_file)
            click.echo("📋 Global Configuration:\n")
        else:  # project
            from roadmapper.config import _load_toml
            from roadmapper.paths import get_project_config_file
            if project_root is None:
                click.echo("⚠️  Not in a roadmapper project", err=True)
                sys.exit(1)
            config_file = get_project_config_file(project_root)
            config = _load_toml(config_file) if config_file and config_file.exists() else {}
            click.echo("📋 Project Configuration:\n")
        
        _print_config(config)
    except Exception as e:
        click.echo(f"❌ Error listing config: {e}", err=True)
        sys.exit(1)


def _print_config(config: dict, prefix: str = "") -> None:
    """Recursively print configuration."""
    for key, value in sorted(config.items()):
        if isinstance(value, dict):
            section_name = f"{prefix}.{key}" if prefix else key
            click.echo(f"[{section_name}]")
            # Recursively print nested config with updated prefix
            new_prefix = f"{prefix}.{key}" if prefix else key
            _print_config(value, new_prefix)
        else:
            key_name = f"{prefix}.{key}" if prefix else key
            if isinstance(value, str):
                click.echo(f"{key_name} = \"{value}\"")
            else:
                click.echo(f"{key_name} = {value}")


@config.command("reset")
@click.argument("key")
@click.option(
    "--scope",
    type=click.Choice(["global", "project"], case_sensitive=False),
    default="project",
    help="Reset in global or project config (default: project)",
)
def config_reset(key, scope):
    """Reset a configuration value (remove from config)."""
    try:
        project_root = get_project_root() if scope == "project" else None
        reset_config_value(key, scope=scope, project_root=project_root)
        click.echo(f"✅ Reset {key} ({scope})")
    except Exception as e:
        click.echo(f"❌ Error resetting config: {e}", err=True)
        sys.exit(1)


@main.group()
def history():
    """View session history and statistics."""
    pass


@history.command("list")
@click.option(
    "--limit",
    type=int,
    default=10,
    help="Maximum number of sessions to show (default: 10)",
)
@click.option(
    "--since",
    help="Only show sessions since this date (YYYY-MM-DD)",
)
def history_list(limit, since):
    """List recent session history."""
    try:
        project_root = get_project_root()
        if project_root is None:
            click.echo("⚠️  Not in a roadmapper project", err=True)
            sys.exit(1)
        
        since_date = None
        if since:
            try:
                since_date = datetime.strptime(since, "%Y-%m-%d")
            except ValueError:
                click.echo(f"❌ Invalid date format: {since}. Use YYYY-MM-DD", err=True)
                sys.exit(1)
        
        records = read_history(project_root=project_root, limit=limit, since=since_date)
        
        if not records:
            click.echo("📝 No session history found")
            return
        
        click.echo(f"📚 Recent Sessions (showing {len(records)}):\n")
        for record in records:
            date_str = record["date"][:10]  # YYYY-MM-DD
            file_name = record["file"]
            branch = record.get("branch", "?")
            click.echo(f"  {date_str}  {file_name}  (branch: {branch})")
    except Exception as e:
        click.echo(f"❌ Error listing history: {e}", err=True)
        sys.exit(1)


@history.command("stats")
@click.option(
    "--since",
    help="Only analyze sessions since this date (YYYY-MM-DD)",
)
def history_stats(since):
    """Show session statistics."""
    try:
        from datetime import datetime
        
        project_root = get_project_root()
        if project_root is None:
            click.echo("⚠️  Not in a roadmapper project", err=True)
            sys.exit(1)
        
        since_date = None
        if since:
            try:
                since_date = datetime.strptime(since, "%Y-%m-%d")
            except ValueError:
                click.echo(f"❌ Invalid date format: {since}. Use YYYY-MM-DD", err=True)
                sys.exit(1)
        
        stats = get_session_stats(project_root=project_root, since=since_date)
        
        click.echo("📊 Session Statistics\n")
        click.echo(f"  Total sessions: {stats['total_sessions']}")
        click.echo(f"  Last 7 days: {stats['sessions_last_7_days']}")
        click.echo(f"  Last 30 days: {stats['sessions_last_30_days']}")
        click.echo(f"  Avg per week: {stats['avg_sessions_per_week']}")
    except Exception as e:
        click.echo(f"❌ Error getting stats: {e}", err=True)
        sys.exit(1)


@main.group()
def projects():
    """Manage and query multiple projects."""
    pass


@projects.command("list")
def projects_list():
    """List all registered projects."""
    try:
        projects = get_all_projects()
        
        if not projects:
            click.echo("📁 No projects registered yet.")
            click.echo("\n💡 Tip: Run 'roadmapper projects discover' to find projects automatically.")
            return
        
        click.echo(f"📁 Registered Projects ({len(projects)}):\n")
        
        for proj in projects:
            name = proj.get("name", "Unknown")
            path = proj.get("path", "?")
            health = proj.get("health", "unknown")
            last_session = proj.get("last_session")
            
            # Health indicator
            health_icons = {
                "healthy": "✅",
                "inactive": "⚠️",
                "stale": "💤",
                "unknown": "❓",
            }
            health_icon = health_icons.get(health, "❓")
            
            click.echo(f"  {health_icon} {name}")
            click.echo(f"     Path: {path}")
            
            if last_session and last_session.get("date"):
                date_str = last_session["date"][:10]  # YYYY-MM-DD
                file_name = last_session.get("file", "?")
                click.echo(f"     Last session: {date_str} ({file_name})")
            else:
                click.echo(f"     Last session: Never")
            
            click.echo()
    except Exception as e:
        click.echo(f"❌ Error listing projects: {e}", err=True)
        sys.exit(1)


@projects.command("register")
@click.argument("path", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
@click.option("--name", help="Project name (defaults to directory name)")
def projects_register(path, name):
    """Register a project in the registry."""
    try:
        # Verify it's a roadmapper project
        if not (path / "PROJECT_ROADMAP.md").exists() and not (path / ".roadmapper.toml").exists():
            click.echo(f"⚠️  {path} doesn't appear to be a roadmapper project", err=True)
            click.echo("   (missing PROJECT_ROADMAP.md or .roadmapper.toml)")
            sys.exit(1)
        
        project_info = register_project(path, name)
        click.echo(f"✅ Registered project: {project_info['name']}")
        click.echo(f"   Path: {project_info['path']}")
    except Exception as e:
        click.echo(f"❌ Error registering project: {e}", err=True)
        sys.exit(1)


@projects.command("unregister")
@click.argument("path", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
def projects_unregister(path):
    """Unregister a project from the registry."""
    try:
        if unregister_project(path):
            click.echo(f"✅ Unregistered project: {path}")
        else:
            click.echo(f"⚠️  Project not found in registry: {path}", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error unregistering project: {e}", err=True)
        sys.exit(1)


@projects.command("discover")
def projects_discover():
    """Discover and register projects automatically."""
    try:
        click.echo("🔍 Discovering projects...")
        new_count = update_project_registry()
        
        if new_count > 0:
            click.echo(f"✅ Discovered and registered {new_count} new project(s)")
        else:
            click.echo("📁 No new projects found")
        
        projects = get_all_projects()
        click.echo(f"\n📊 Total registered projects: {len(projects)}")
    except Exception as e:
        click.echo(f"❌ Error discovering projects: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

