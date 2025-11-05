# Context Compression Layer Guide

**Purpose:** Optional cache file (`.roadmapper/context.json`) that stores condensed summaries, key decisions, and pointers to enable efficient context retrieval for large-context LLMs.

---

## Overview

The context compression layer allows large-context LLMs (e.g., GPT-4, Grok 4) to retrieve and reason over just the relevant parts of long projects without loading entire session histories.

**Benefits:**
- Faster context ingestion for large-context models
- Efficient retrieval of relevant past context
- Key decision tracking across sessions
- Enables "Session Primer" generation (Phase 4.3)

---

## Schema

The `.roadmapper/context.json` file follows this schema:

```json
{
  "version": "1.0",
  "project": "ProjectName",
  "sessions": [
    {
      "id": "SESSION_2025_11_04_I",
      "file": "docs/archive/sessions/SESSION_2025_11_04_I.md",
      "summary": "Condensed summary of session accomplishments and key work",
      "accomplishments": [
        "Completed Phase 4.1.1: YAML Metadata Headers",
        "Completed Phase 4.1.2: Reasoning Markers"
      ],
      "decisions": [
        "Using YAML frontmatter for better readability",
        "Adding reasoning markers for better LLM parsing"
      ],
      "archived_at": "2025-11-04T12:00:00"
    }
  ],
  "summaries": {
    "SESSION_2025_11_04_I": "Condensed summary...",
    "SESSION_2025_11_04_H": "Another summary..."
  },
  "key_decisions": [
    {
      "session_id": "SESSION_2025_11_04_I",
      "decision": "Using YAML frontmatter for better readability",
      "timestamp": "2025-11-04T12:00:00"
    }
  ],
  "embeddings": {}
}
```

**Fields:**
- `version`: Schema version (currently "1.0")
- `project`: Project name (auto-extracted from roadmap)
- `sessions`: List of archived session summaries
- `summaries`: Quick lookup dictionary by session ID
- `key_decisions`: Chronological list of important decisions
- `embeddings`: Reserved for future embedding storage (requires optional dependencies)

---

## Usage

### Automatic Integration

The context compression layer integrates with session archiving. When a session is archived:

1. Session summary is automatically extracted
2. Key accomplishments are identified
3. Decisions are extracted (using reasoning markers)
4. Context is updated

**Note:** Currently, session archiving is handled by AI assistant instructions. Automatic integration will be added in Phase 4.2 (Enhanced Automation).

### Manual Usage

```python
from roadmapper.context import (
    add_session_summary,
    get_session_summary,
    get_recent_decisions,
    get_session_pointers,
)

# Add a session summary
add_session_summary(
    session_file=Path("docs/archive/sessions/SESSION_2025_11_04_I.md"),
    summary="Completed Phase 4.1.1-4.1.3: Added semantic structure",
    accomplishments=["YAML metadata", "Reasoning markers", "Structured tasks"],
    decisions=["Using YAML for readability", "Adding markers for LLM parsing"],
)

# Retrieve session summary
summary = get_session_summary("SESSION_2025_11_04_I")

# Get recent decisions
decisions = get_recent_decisions(limit=10)

# Get session pointers for context retrieval
pointers = get_session_pointers(query="metadata")
```

---

## Integration with AI Assistants

**When archiving a session:**
1. Extract summary from "Session Accomplishments" section
2. Extract accomplishments (completed items)
3. Extract decisions (using 🧭 DECISION: markers)
4. Call `add_session_summary()` to update context

**When starting a new session:**
1. Read `.roadmapper/context.json` for project context
2. Use `get_recent_decisions()` for relevant past decisions
3. Use `get_session_pointers()` to find related sessions
4. Generate "Session Primer" from context (Phase 4.3 feature)

---

## Future Enhancements

**Embeddings (Phase 4.3):**
- Store vector embeddings of session content
- Enable semantic search across sessions
- Requires optional dependencies (FAISS, Chroma, etc.)

**Auto-Summarization (Phase 4.2):**
- Automatic summary generation from session content
- Extraction of accomplishments and decisions
- Integration with session archiving workflow

**Session Primers (Phase 4.3):**
- Auto-generate context primers at session start
- Tailor to current goals using context compression
- Summarize relevant past context

---

## File Location

- **Path:** `.roadmapper/context.json`
- **Location:** Project root directory
- **Created:** Automatically when first session is archived
- **Updated:** When sessions are archived or context is refreshed

---

**Last Updated:** November 4, 2025  
**Related:** See `roadmapper/context.py` for implementation details

