"""Session management functionality."""

from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
import re

from roadmapper.utils import ensure_utf8_console, read_text_file, write_text_file
from roadmapper.history import log_session
from roadmapper.paths import get_project_root


def _extract_roadmap_metadata(project_root: Path) -> Dict[str, str]:
    """
    Extract project metadata from PROJECT_ROADMAP.md.
    
    Args:
        project_root: Path to project root directory
    
    Returns:
        Dictionary with project metadata (project, phase, etc.)
    """
    roadmap_path = project_root / "PROJECT_ROADMAP.md"
    if not roadmap_path.exists():
        return {
            "project": "Unknown Project",
            "phase": "Unknown Phase",
            "context_window": "medium",
            "session_type": "development",
        }
    
    content = read_text_file(roadmap_path)
    
    # Extract project name (look for "# ProjectName" after Quick Start section)
    project_name = "Unknown Project"
    project_match = re.search(r'^# ([A-Za-z0-9_\- ]+)$', content, re.MULTILINE)
    if project_match:
        # Skip "Quick Start" title, look for actual project name
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('# ') and 'Quick Start' not in line and 'Project' in line:
                # This is likely the project name line
                project_name = line.replace('# ', '').strip()
                break
    
    # Extract current phase from "Phase Progress" section
    phase = "Unknown Phase"
    phase_pattern = r'Phase Progress:.*?🔵 Phase (\d+[\.\d]*):\s*([^\n]+)'
    phase_match = re.search(phase_pattern, content, re.DOTALL)
    if phase_match:
        phase = f"Phase {phase_match.group(1)}: {phase_match.group(2).strip()}"
    else:
        # Fallback: look for "🔵 Phase" pattern
        phase_match = re.search(r'🔵 Phase (\d+[\.\d]*):\s*([^\n]+)', content)
        if phase_match:
            phase = f"Phase {phase_match.group(1)}: {phase_match.group(2).strip()}"
    
    return {
        "project": project_name,
        "phase": phase,
        "context_window": "medium",  # Default, can be customized
        "session_type": "development",  # Default, can be customized
    }


def create_session(name: Optional[str] = None) -> Path:
    """
    Create a new session file with proper naming.
    
    Args:
        name: Optional custom session name. If not provided, uses date-based naming.
            For multi-agent scenarios, include agent identifier in name (e.g., "agent1").
    
    Returns:
        Path to the created session file
    
    Note:
        Current implementation assumes single-agent mode. Multi-agent support with
        agent tracking and coordination is planned for Phase 4.
    """
    ensure_utf8_console()
    cwd = Path.cwd()
    
    if name:
        # Use custom name
        session_filename = f"SESSION_{name}.md"
        session_path = cwd / session_filename
    else:
        # Use date-based naming: SESSION_YYYY_MM_DD_X.md
        today = datetime.now()
        date_str = today.strftime("%Y_%m_%d")
        
        # Find existing sessions for today
        existing_sessions = sorted(
            cwd.glob(f"SESSION_{date_str}_*.md")
        )
        
        if existing_sessions:
            # Extract the highest letter
            letters = []
            for session_file in existing_sessions:
                match = re.search(rf"SESSION_{date_str}_([A-Z])\.md", session_file.name)
                if match:
                    letters.append(match.group(1))
            
            if letters:
                # Get next letter
                last_letter = max(letters)
                next_letter = chr(ord(last_letter) + 1)
            else:
                next_letter = "A"
        else:
            next_letter = "A"
        
        session_filename = f"SESSION_{date_str}_{next_letter}.md"
        session_path = cwd / session_filename
    
    # Get project metadata
    project_root = get_project_root()
    metadata = _extract_roadmap_metadata(project_root) if project_root else {
        "project": "Unknown Project",
        "phase": "Unknown Phase",
        "context_window": "medium",
        "session_type": "development",
    }
    
    # Get current date for metadata
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    date_display = today.strftime("%B %d, %Y")
    
    # Get template
    template_path = cwd / "docs" / "reference" / "SESSION_WORKING_TEMPLATE.md"
    if template_path.exists():
        template_content = read_text_file(template_path)
        
        # Replace metadata placeholders in template
        template_content = template_content.replace("[Project Name]", metadata["project"])
        template_content = template_content.replace("[Current Phase Number/Name]", metadata["phase"])
        template_content = template_content.replace("[Estimated context size: small/medium/large]", metadata["context_window"])
        template_content = template_content.replace("[development/review/planning/bugfix]", metadata["session_type"])
        template_content = template_content.replace("[YYYY-MM-DD]", date_str)
        template_content = template_content.replace("[Month Day, Year]", date_display)
        
        # Replace YYYY-MM-DD-X in title
        if existing_sessions:
            session_id = f"{date_str}_{next_letter}"
        else:
            session_id = f"{date_str}_A"
        template_content = re.sub(r'YYYY-MM-DD-X', session_id, template_content)
    else:
        # Fallback to basic template
        template_content = f"""# Session {datetime.now().strftime('%Y-%m-%d')}: [Session Title]

**Date:** {datetime.now().strftime('%B %d, %Y')}  
**Phase:** [Current Phase]  
**Focus:** [Brief description]

---

## 🎯 Session Goals

**Primary objectives:**
1. [Goal 1]
2. [Goal 2]

**Success criteria:**
- [ ] [Criterion 1]

---

## 🔧 Work Log

[Document your work here]

---

## ✅ Session Accomplishments

**Completed:**
- [List accomplishments]

---

"""
    
    # Write session file with UTF-8 encoding
    write_text_file(session_path, template_content)
    
    # Log session creation to history
    if project_root is None:
        project_root = get_project_root()
    log_session(session_path, project_root=project_root)
    
    return session_path

