---
project: "[Project Name]"
phase: "[Current Phase Number/Name]"
context_window: "[Estimated context size: small/medium/large]"
session_type: "[development/review/planning/bugfix]"
goals: ["[Goal 1]", "[Goal 2]", "[Goal 3]"]
status: "active"
created: "[YYYY-MM-DD]"
---

# Session YYYY-MM-DD-X: [Session Title]

**Date:** [Month Day, Year]  
**Phase:** [Current Phase Number/Name]  
**Focus:** [Brief description of session goals]

> ⚠️ **File Length Reminder:** This session file should stay between 150-250 lines. If approaching 250 lines, consider:
> - Extracting detailed action plans to separate files (e.g., `PHASE_X_ACTION_PLAN.md`)
> - Moving long implementation specs to planning documents
> - Archiving completed work to `docs/archive/sessions/`
> - Starting a new session for the next major feature/task
> 
> See `docs/reference/FILE_ORGANIZATION_GUIDE.md` for guidelines.
> 
> **🤖 AI Assistant Note:** The YAML frontmatter above provides machine-readable metadata. Use it to quickly understand project context, phase, and goals without reading the entire file.

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

**🤖 Reasoning Markers** (Optional but recommended for better LLM parsing):
Use these markers to help AI assistants understand your reasoning process:

- `🧭 DECISION:` - When making a design or implementation decision
  - Example: `🧭 DECISION: Using YAML frontmatter instead of JSON for better readability`
  
- `🤔 HYPOTHESIS:` - When proposing a theory or assumption
  - Example: `🤔 HYPOTHESIS: Metadata extraction will reduce context parsing time by 40%`
  
- `✅ VERIFIED:` - When confirming something works or is correct
  - Example: `✅ VERIFIED: Session creation correctly extracts project name from roadmap`
  
- `⚠️ WARNING:` - When noting a potential issue or concern
  - Example: `⚠️ WARNING: This approach may break with custom roadmap formats`
  
- `💡 INSIGHT:` - When discovering something important
  - Example: `💡 INSIGHT: Regex patterns work well for phase extraction`

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

**When user wants to start a new session, YOU (the AI assistant) should automatically:**
- Update PROJECT_ROADMAP.md with session summary
- Check that all git commits are made (git status clean)
- Archive this file to docs/archive/sessions/
- Create new SESSION_YYYY_MM_DD_X.md for next session (if continuing)

**User should NEVER manually archive or copy files - you handle this automatically.**

---

**Remember:** This is YOUR working document. Use it however helps you work best. Document freely, commit frequently, stay grounded in the roadmap.

