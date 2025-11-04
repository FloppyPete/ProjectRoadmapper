"""Template management functionality."""

from pathlib import Path
from typing import Dict

from roadmapper.utils import read_text_file


# Template storage - will be populated from files or embedded
_TEMPLATES: Dict[str, Dict[str, str]] = {}


def get_template(template_name: str, variant: str = "default") -> str:
    """
    Get a template by name and variant.
    
    Args:
        template_name: Name of the template (e.g., "PROJECT_ROADMAP.md")
        variant: Template variant ("default", "minimal", "detailed")
    
    Returns:
        Template content as string
    """
    # For now, use embedded templates
    # Later, can load from templates/ directory
    
    if template_name == "PROJECT_ROADMAP.md":
        return _get_roadmap_template(variant)
    elif template_name == "SESSION_WORKING_TEMPLATE.md":
        return _get_session_template(variant)
    else:
        raise ValueError(f"Unknown template: {template_name}")


def _get_roadmap_template(variant: str) -> str:
    """Get PROJECT_ROADMAP.md template."""
    # This is a simplified version - full template should be in templates/ directory
    return """# 📖 Quick Start

**Living Roadmap** for [Project Name]

**6-Step Workflow**: Plan → Consult (optional) → Implement → Document → Sanity Check → Repeat

**Philosophy**: *"Automate the predictable; document the decisions."*

---

## 🤖 AI Assistant Workflow

**Every conversation start:**
1. ✅ Read this file (PROJECT_ROADMAP.md) - Current Status section
2. ✅ Check for `SESSION_YYYY_MM_DD_X.md` in root
3. ✅ If exists: Read it, continue that session
4. ✅ If not: Create new session (increment letter: A→B→C or new date)

**During session:**
- Use SESSION file as scratchpad freely
- Git commit after each logical unit
- Ask before deleting/major changes
- Update working doc with progress

**Session end:**
- Update this roadmap briefly
- Archive SESSION file to docs/archive/sessions/
- Ensure git clean

**Key principle:** Always in a session. Always grounded in roadmap. Commit frequently.

**Template:** `docs/reference/SESSION_WORKING_TEMPLATE.md`

---

# [Project Name]

**Goal**: [Project goal]

**Vision**: [Project vision]

**Last Updated**: [Date]

---

## 📊 Current Status

**Project Health:** 🆕 New Project

**Phase Progress:**
- 🟢 Phase 0: Project Foundation (In Progress)

---

## 📋 Phases

[Add your phases here]

---

**Note:** This roadmap was created using ProjectRoadmapper. 🗺️
"""


def _get_session_template(variant: str) -> str:
    """Get SESSION_WORKING_TEMPLATE.md template."""
    # Try to load from project directory first
    cwd = Path.cwd()
    template_path = cwd / "docs" / "reference" / "SESSION_WORKING_TEMPLATE.md"
    
    if template_path.exists():
        return read_text_file(template_path)
    
    # Fallback to embedded template
    return """# Session YYYY-MM-DD-X: [Session Title]

**Date:** [Month Day, Year]  
**Phase:** [Current Phase Number/Name]  
**Focus:** [Brief description of session goals]

---

## 📊 Project Context (Brief Roadmap Synopsis)

**From PROJECT_ROADMAP.md:**

**Current Phase:**
- [Copy current phase from roadmap]

**Recent Completions:**
- [1-2 key recent achievements]

**System Status:**
- [Brief health check - tools working? tests passing?]

---

## 🎯 Session Goals

**Primary objectives:**
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

**Success criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

## 🔧 Work Log

### [Task/Investigation Name]

**[Document your work here freely]**

Use this space as scratchpad:
- Findings and discoveries
- Code snippets and analysis
- Decisions and rationale
- Questions and answers
- Progress tracking

**Git commits:**
- `<hash>` - [Brief description]

---

## ✅ Session Accomplishments

**Completed:**
- [List what got done]

**Deferred:**
- [What was postponed and why]

**Discoveries:**
- [Important findings or insights]

---

## 📝 Before Archiving This Session

**Checklist:**
- [ ] Update PROJECT_ROADMAP.md with session summary
- [ ] All git commits made (git status clean)
- [ ] Valuable insights added to roadmap if applicable
- [ ] Archive this file to docs/archive/sessions/
- [ ] Create new SESSION_YYYY_MM_DD_X.md for next session (if continuing)

---

**Remember:** This is YOUR working document. Use it however helps you work best. Document freely, commit frequently, stay grounded in the roadmap.
"""

