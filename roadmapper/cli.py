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
from roadmapper.search import search_projects
from roadmapper.knowledge import (
    index_all_projects,
    search_knowledge,
    get_knowledge_by_topic,
    get_related_discoveries,
    load_knowledge,
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


@main.command("dashboard")
@click.option(
    "--host",
    default="127.0.0.1",
    help="Host to bind to (default: 127.0.0.1)",
)
@click.option(
    "--port",
    type=int,
    default=5000,
    help="Port to bind to (default: 5000)",
)
@click.option(
    "--open",
    "open_browser",
    is_flag=True,
    help="Open browser automatically",
)
def dashboard(host, port, open_browser):
    """Start web dashboard server."""
    try:
        # Try to import Flask
        try:
            from flask import Flask, render_template_string
        except ImportError:
            click.echo("❌ Flask is required for dashboard. Install it with:", err=True)
            click.echo("   pip install flask", err=True)
            click.echo("\nOr install roadmapper with dashboard support:", err=True)
            click.echo("   pip install 'roadmapper[dashboard]'", err=True)
            sys.exit(1)
        
        from roadmapper.dashboard import get_dashboard_data, get_dashboard_template
        
        app = Flask(__name__)
        
        @app.route("/")
        def index():
            data = get_dashboard_data()
            template = get_dashboard_template()
            return render_template_string(template, **data)
        
        url = f"http://{host}:{port}"
        click.echo(f"🚀 Starting dashboard server...")
        click.echo(f"📊 Dashboard available at: {url}")
        
        if open_browser:
            import webbrowser
            webbrowser.open(url)
        
        click.echo("\n💡 Press Ctrl+C to stop the server\n")
        
        # Run Flask app
        app.run(host=host, port=port, debug=False)
        
    except KeyboardInterrupt:
        click.echo("\n\n👋 Dashboard server stopped")
    except Exception as e:
        click.echo(f"❌ Error starting dashboard: {e}", err=True)
        sys.exit(1)


@main.group()
def knowledge():
    """Query knowledge base extracted from sessions."""
    pass


@knowledge.command("index")
def knowledge_index():
    """Extract and index knowledge from all projects."""
    try:
        click.echo("🔍 Indexing knowledge from all projects...")
        new_count = index_all_projects()
        
        if new_count > 0:
            click.echo(f"✅ Indexed {new_count} new knowledge entries")
        else:
            click.echo("📚 No new knowledge found (already indexed)")
        
        total = len(load_knowledge())
        click.echo(f"\n📊 Total knowledge entries: {total}")
    except Exception as e:
        click.echo(f"❌ Error indexing knowledge: {e}", err=True)
        sys.exit(1)


@knowledge.command("search")
@click.argument("query")
@click.option(
    "--type",
    "knowledge_type",
    type=click.Choice(["discovery", "accomplishment", "insight"], case_sensitive=False),
    help="Filter by knowledge type",
)
@click.option(
    "--limit",
    type=int,
    default=20,
    help="Maximum number of results (default: 20)",
)
def knowledge_search(query, knowledge_type, limit):
    """Search knowledge base."""
    try:
        results = search_knowledge(query, knowledge_type)
        
        if not results:
            click.echo(f"❌ No knowledge found for: '{query}'")
            click.echo("\n💡 Tip: Run 'roadmapper knowledge index' to extract knowledge from projects")
            return
        
        # Limit results
        results = results[:limit]
        
        click.echo(f"📚 Found {len(results)} knowledge entries for: '{query}'\n")
        
        for i, entry in enumerate(results, 1):
            entry_type = entry.get("type", "unknown")
            content = entry.get("content", "")
            project = entry.get("project", "Unknown")
            session_file = entry.get("session_file", "?")
            
            type_icons = {
                "discovery": "💡",
                "accomplishment": "✅",
                "insight": "🔍",
            }
            icon = type_icons.get(entry_type, "📝")
            
            click.echo(f"{i}. {icon} [{entry_type}] {project}")
            click.echo(f"   {content[:100]}{'...' if len(content) > 100 else ''}")
            click.echo(f"   Session: {session_file}\n")
        
        if len(search_knowledge(query, knowledge_type)) > limit:
            click.echo(f"... and {len(search_knowledge(query, knowledge_type)) - limit} more results")
    
    except Exception as e:
        click.echo(f"❌ Error searching knowledge: {e}", err=True)
        sys.exit(1)


@knowledge.command("learn")
@click.argument("topic")
def knowledge_learn(topic):
    """Answer: 'What did I learn about X?'"""
    try:
        results = get_knowledge_by_topic(topic)
        
        if not results:
            click.echo(f"❌ No knowledge found about: '{topic}'")
            click.echo("\n💡 Tip: Run 'roadmapper knowledge index' to extract knowledge from projects")
            return
        
        click.echo(f"📚 What you learned about '{topic}':\n")
        
        # Group by project
        by_project = {}
        for entry in results:
            project = entry.get("project", "Unknown")
            if project not in by_project:
                by_project[project] = []
            by_project[project].append(entry)
        
        for project, entries in by_project.items():
            click.echo(f"📁 {project} ({len(entries)} entries):")
            for entry in entries[:5]:  # Show up to 5 per project
                content = entry.get("content", "")
                click.echo(f"  • {content[:80]}{'...' if len(content) > 80 else ''}")
            if len(entries) > 5:
                click.echo(f"  ... and {len(entries) - 5} more")
            click.echo()
    
    except Exception as e:
        click.echo(f"❌ Error querying knowledge: {e}", err=True)
        sys.exit(1)


@knowledge.command("stats")
def knowledge_stats():
    """Show knowledge base statistics."""
    try:
        knowledge = load_knowledge()
        
        if not knowledge:
            click.echo("📚 Knowledge base is empty")
            click.echo("\n💡 Tip: Run 'roadmapper knowledge index' to extract knowledge from projects")
            return
        
        # Count by type
        by_type = {}
        by_project = {}
        
        for entry in knowledge:
            entry_type = entry.get("type", "unknown")
            project = entry.get("project", "Unknown")
            
            by_type[entry_type] = by_type.get(entry_type, 0) + 1
            by_project[project] = by_project.get(project, 0) + 1
        
        click.echo("📊 Knowledge Base Statistics\n")
        click.echo(f"Total entries: {len(knowledge)}")
        click.echo(f"\nBy type:")
        for entry_type, count in sorted(by_type.items()):
            click.echo(f"  {entry_type}: {count}")
        
        click.echo(f"\nBy project (top 10):")
        for project, count in sorted(by_project.items(), key=lambda x: x[1], reverse=True)[:10]:
            click.echo(f"  {project}: {count}")
    
    except Exception as e:
        click.echo(f"❌ Error getting stats: {e}", err=True)
        sys.exit(1)


@main.command("search")
@click.argument("query")
@click.option(
    "--type",
    "file_types",
    multiple=True,
    type=click.Choice(["session", "roadmap", "history"], case_sensitive=False),
    help="File types to search (can specify multiple times)",
)
@click.option(
    "--case-sensitive",
    is_flag=True,
    help="Case-sensitive search",
)
@click.option(
    "--max-results",
    type=int,
    default=50,
    help="Maximum number of results to show (default: 50)",
)
@click.option(
    "--project",
    "project_paths",
    multiple=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Specific projects to search (can specify multiple times)",
)
def search(query, file_types, case_sensitive, max_results, project_paths):
    """Search across all registered projects."""
    try:
        # Convert project paths if provided
        project_paths_list = list(project_paths) if project_paths else None
        
        # Convert file_types tuple to list
        file_types_list = list(file_types) if file_types else None
        
        click.echo(f"🔍 Searching for: '{query}'\n")
        
        results = search_projects(
            query=query,
            project_paths=project_paths_list,
            file_types=file_types_list,
            case_sensitive=case_sensitive,
            max_results=max_results,
        )
        
        if not results:
            click.echo("❌ No matches found")
            return
        
        click.echo(f"✅ Found {len(results)} result(s)\n")
        
        # Group results by project
        projects_dict = {}
        for result in results:
            project_key = str(result.project_path)
            if project_key not in projects_dict:
                projects_dict[project_key] = {
                    "name": result.project_name,
                    "path": result.project_path,
                    "results": [],
                }
            projects_dict[project_key]["results"].append(result)
        
        # Display results
        for project_key, project_data in projects_dict.items():
            click.echo(f"📁 {project_data['name']}")
            click.echo(f"   Path: {project_data['path']}\n")
            
            for result in project_data["results"]:
                file_type_icon = {
                    "session": "📝",
                    "roadmap": "🗺️",
                    "history": "📚",
                }.get(result.file_type, "📄")
                
                relative_path = result.file_path.relative_to(result.project_path)
                click.echo(f"   {file_type_icon} {relative_path} ({len(result.matches)} match{'es' if len(result.matches) > 1 else ''})")
                
                # Show first few matches with context
                for i, (line_num, line_content) in enumerate(result.matches[:3]):
                    # Truncate long lines
                    display_line = line_content[:100] + "..." if len(line_content) > 100 else line_content
                    click.echo(f"      Line {line_num + 1}: {display_line.strip()}")
                
                if len(result.matches) > 3:
                    click.echo(f"      ... and {len(result.matches) - 3} more match(es)")
                
                click.echo()
        
        click.echo(f"\n💡 Tip: Use '--type session' to search only session files")
        click.echo(f"💡 Tip: Use '--project <path>' to search specific projects")
        
    except Exception as e:
        click.echo(f"❌ Error searching: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

