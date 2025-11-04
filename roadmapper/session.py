"""Session management functionality."""

from datetime import datetime
from pathlib import Path
from typing import Optional
import re

from roadmapper.utils import ensure_utf8_console, read_text_file, write_text_file
from roadmapper.history import log_session
from roadmapper.paths import get_project_root


def create_session(name: Optional[str] = None) -> Path:
    """
    Create a new session file with proper naming.
    
    Args:
        name: Optional custom session name. If not provided, uses date-based naming.
    
    Returns:
        Path to the created session file
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
    
    # Get template
    template_path = cwd / "docs" / "reference" / "SESSION_WORKING_TEMPLATE.md"
    if template_path.exists():
        template_content = read_text_file(template_path)
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
    project_root = get_project_root()
    log_session(session_path, project_root=project_root)
    
    return session_path

