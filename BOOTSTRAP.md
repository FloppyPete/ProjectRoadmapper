# 🚀 ProjectRoadmapper Bootstrap

**One file. Paste this into your project. Tell Cursor: "Read BOOTSTRAP.md and set up the workflow."**

---

## 🤖 Instructions for AI Assistant (Cursor)

**Your job:** Set up the ProjectRoadmapper workflow for this project automatically.

**Steps:**
1. ✅ Create directory structure: `docs/reference/` and `docs/archive/sessions/`
2. ✅ Create `PROJECT_ROADMAP.md` from template below
3. ✅ Create `docs/reference/SESSION_WORKING_TEMPLATE.md` from template below
4. ✅ Create first session file: `SESSION_YYYY_MM_DD_A.md` (use today's date)
5. ✅ Initialize git if not already initialized
6. ✅ Ask user a few questions to customize PROJECT_ROADMAP.md:
   - What is this project called?
   - What is the main goal?
   - What are 3-5 major phases/milestones?
7. ✅ Fill in PROJECT_ROADMAP.md with their answers
8. ✅ Make initial git commit

**Important:** Handle everything automatically. User should not manually copy or archive files.

---

## 📝 Template: PROJECT_ROADMAP.md

Create this file in project root:

```markdown
# 📖 Quick Start

**Living Roadmap** for [PROJECT_NAME]

**6-Step Workflow**: Plan → Consult (optional) → Implement → Document → Sanity Check → Repeat

**Philosophy**: *"Automate the predictable; document the decisions."*

---

## 🤖 AI Assistant Workflow

**Every conversation start:**
1. ✅ Read this file (PROJECT_ROADMAP.md) - Current Status section
2. ✅ Check for `SESSION_YYYY_MM_DD_X.md` in root
3. ✅ If exists: Read it, continue that session
4. ✅ If not: **Automatically create new session** (increment letter: A→B→C or new date)

**Starting a new session (when user says "new session" or "start new session"):**
- **Automatically archive** any existing `SESSION_*.md` file to `docs/archive/sessions/`
- **Automatically create** new `SESSION_YYYY_MM_DD_X.md` file from template
- **Automatically update** PROJECT_ROADMAP.md with brief summary of archived session
- User should NEVER manually archive or copy templates - you do this automatically

**During session:**
- Use SESSION file as scratchpad freely
- Git commit after each logical unit
- Ask before deleting/major changes
- Update working doc with progress

**Session end (when user says "end session" or "archive session"):**
- Update this roadmap briefly with session summary
- **Automatically archive** SESSION file to docs/archive/sessions/
- **Automatically create** new session file if user wants to continue
- Ensure git clean

**Key principle:** Always in a session. Always grounded in roadmap. Commit frequently. **YOU handle archiving and session creation automatically - never ask the user to do manual file operations.**

**Template:** `docs/reference/SESSION_WORKING_TEMPLATE.md`

---

# [PROJECT_NAME]

**Goal**: [PROJECT_GOAL]

**Last Updated**: [TODAY'S_DATE] (Status: 🆕 New Project)

---

## 📊 Current Status

**Project Health:** 🆕 New Project

**Phase Progress:**
- 🟢 Phase 0: Project Foundation (In Progress)

**Recent Work:** Project workflow initialized

---

## 📋 Phases

[PHASES_LIST]

---

## 🎯 Quick Reference

### Key Files
- [List important files as project develops]

### Running the Project
\`\`\`bash
# [Add commands as needed]
\`\`\`

---

## 💡 Recent Sessions

**Session 0: Project Foundation**
- Workflow structure created
- Roadmap initialized

**Archives:** [docs/archive/sessions/](docs/archive/sessions/)
```

---

## 📝 Template: SESSION_WORKING_TEMPLATE.md

Create this file at `docs/reference/SESSION_WORKING_TEMPLATE.md`:

```markdown
# Session YYYY-MM-DD-X: [Session Title]

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

**When user wants to start a new session, YOU (the AI assistant) should automatically:**
- Update PROJECT_ROADMAP.md with session summary
- Check that all git commits are made (git status clean)
- Archive this file to docs/archive/sessions/
- Create new SESSION_YYYY_MM_DD_X.md for next session (if continuing)

**User should NEVER manually archive or copy files - you handle this automatically.**

---

**Remember:** This is YOUR working document. Use it however helps you work best. Document freely, commit frequently, stay grounded in the roadmap.
```

---

## ✅ That's It!

**For the user:** Paste this file into your project root, then tell Cursor:
```
Read BOOTSTRAP.md and set up the workflow for this project
```

Cursor will do everything automatically. No CLI needed. No manual copying. Just paste and ask. ✨

