"""Session management functionality."""

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import re


def _ensure_utf8():
    """Ensure UTF-8 encoding for Windows console."""
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except AttributeError:
            # Python < 3.7
            pass


def create_session(name: Optional[str] = None) -> Path:
    """
    Create a new session file with proper naming.
    
    Args:
        name: Optional custom session name. If not provided, uses date-based naming.
    
    Returns:
        Path to the created session file
    """
    _ensure_utf8()
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
        template_content = template_path.read_text(encoding='utf-8')
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
    session_path.write_text(template_content, encoding='utf-8')
    
    return session_path

