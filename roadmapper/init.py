"""Project initialization functionality."""

import os
import subprocess
from pathlib import Path
from typing import Optional

from roadmapper.templates import get_template
from roadmapper.utils import write_text_file
from roadmapper.projects import register_project


def init_project(template: str = "default", init_git: bool = True) -> None:
    """
    Initialize a new project with roadmapper workflow.
    
    Args:
        template: Template to use ("default", "minimal", "detailed")
        init_git: Whether to initialize git if repository doesn't exist
    """
    cwd = Path.cwd()
    
    # Create directory structure
    dirs_to_create = [
        "docs/reference",
        "docs/archive/sessions",
    ]
    
    for dir_path in dirs_to_create:
        full_path = cwd / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
    
    # Create PROJECT_ROADMAP.md from template
    roadmap_template = get_template("PROJECT_ROADMAP.md", template)
    roadmap_path = cwd / "PROJECT_ROADMAP.md"
    
    if not roadmap_path.exists():
        write_text_file(roadmap_path, roadmap_template)
    else:
        print(f"⚠️  PROJECT_ROADMAP.md already exists, skipping...")
    
    # Create SESSION_WORKING_TEMPLATE.md
    session_template = get_template("SESSION_WORKING_TEMPLATE.md", template)
    session_template_path = cwd / "docs" / "reference" / "SESSION_WORKING_TEMPLATE.md"
    
    if not session_template_path.exists():
        write_text_file(session_template_path, session_template)
    else:
        print(f"⚠️  SESSION_WORKING_TEMPLATE.md already exists, skipping...")
    
    # Initialize git if requested and not already a git repo
    if init_git:
        try:
            result = subprocess.run(
                ["git", "status"],
                capture_output=True,
                text=True,
                cwd=cwd,
            )
            if result.returncode != 0:
                # Not a git repo, initialize it
                subprocess.run(["git", "init"], cwd=cwd, check=True)
                print("✅ Git repository initialized")
        except FileNotFoundError:
            print("⚠️  Git not found, skipping git initialization")
        except subprocess.CalledProcessError:
            print("⚠️  Error checking git status, skipping git initialization")
    
    # Automatically register this project in the registry
    try:
        register_project(cwd)
        print("✅ Project registered in dashboard")
    except Exception as e:
        # Don't fail initialization if registration fails
        print(f"⚠️  Could not register project: {e}")

