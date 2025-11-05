# Structured Task Blocks Guide

**Purpose:** Optional structured format for tracking tasks within session work logs. Enables better LLM parsing and automatic task list generation.

---

## Format

Use this format for tracking specific tasks:

```
[TASK] Task description or objective
[STATUS] in_progress | completed | blocked | deferred
[NOTES] Additional context, blockers, or implementation details
```

---

## Status Values

- **in_progress** - Task is currently being worked on
- **completed** - Task is finished
- **blocked** - Task cannot proceed due to external dependency or blocker
- **deferred** - Task postponed to later session or phase

---

## Examples

### Basic Task Tracking

```
[TASK] Add YAML frontmatter to session template
[STATUS] completed
[NOTES] Includes all required fields: project, phase, context_window, session_type, goals, status, created
```

### Task with Blocker

```
[TASK] Implement semantic search with vector embeddings
[STATUS] blocked
[NOTES] Waiting for decision on embedding library (FAISS vs Chroma). Need to evaluate performance trade-offs.
```

### In-Progress Task

```
[TASK] Update AI assistant instructions for reasoning markers
[STATUS] in_progress
[NOTES] Adding examples to PROJECT_ROADMAP.md workflow section. Need to test with actual AI assistant.
```

### Deferred Task

```
[TASK] Create knowledge graph visualization
[STATUS] deferred
[NOTES] Moving to Phase 4.3 when graph layer is implemented. Will need visualization library integration.
```

---

## Multiple Tasks

You can track multiple tasks in sequence:

```
[TASK] Add reasoning markers to template
[STATUS] completed
[NOTES] Added 5 marker types: DECISION, HYPOTHESIS, VERIFIED, WARNING, INSIGHT

[TASK] Create reasoning markers documentation
[STATUS] completed
[NOTES] Created REASONING_MARKERS.md with usage guide and examples

[TASK] Update AI instructions
[STATUS] in_progress
[NOTES] Updating PROJECT_ROADMAP.md workflow section
```

---

## Benefits

1. **Auto-Generation:** LLMs can extract task lists and generate summaries automatically
2. **Progress Tracking:** Clear status makes it easy to see what's done vs. in progress
3. **Structured Parsing:** Consistent format enables better LLM understanding
4. **Reduced Chaos:** Structure reduces free-form text complexity

---

## Usage Guidelines

**Optional but recommended:**
- Use for tasks that span multiple work sessions
- Use when you want to track specific objectives
- Use when blockers or dependencies exist

**When to skip:**
- Very short tasks that complete immediately
- Exploratory work without clear objectives
- Quick fixes or minor changes

**Best practices:**
- Update status as tasks progress
- Keep NOTES concise but informative
- Use consistent status values
- Group related tasks together

---

## Integration with AI Assistants

AI assistants can:
- Extract all tasks from a session automatically
- Generate task completion summaries
- Identify blocked or deferred tasks
- Track task dependencies across sessions
- Generate progress reports

---

**Last Updated:** November 4, 2025  
**Related:** See `SESSION_WORKING_TEMPLATE.md` for template with task block examples

