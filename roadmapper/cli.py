"""Main CLI interface for roadmapper."""

import click
from pathlib import Path
import sys

from roadmapper import __version__
from roadmapper.init import init_project
from roadmapper.session import create_session
from roadmapper.status import show_status


@click.group()
@click.version_option(version=__version__, prog_name="roadmapper")
def main():
    """
    ProjectRoadmapper - Multi-session development workflow tool.
    
    Helps maintain context and momentum across multiple development sessions,
    especially when working with AI assistants.
    """
    pass


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


if __name__ == "__main__":
    main()

