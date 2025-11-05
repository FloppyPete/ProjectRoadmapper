# 🔄 Update Existing Project Workflow

**For projects that already have ProjectRoadmapper workflow set up.**

Tell Cursor: `"Read UPDATE.md and update the workflow for this project"`

---

## 🤖 Instructions for AI Assistant (Cursor)

**Your job:** Update an existing ProjectRoadmapper workflow to the latest version.

**Steps:**
1. ✅ **Check for ProjectRoadmapper updates:**
   - If ProjectRoadmapper repo exists (e.g., `../ProjectRoadmapper` or `~/ProjectRoadmapper`): Run `git pull` to get latest templates
   - This ensures you have the latest workflow improvements

2. ✅ **Read existing PROJECT_ROADMAP.md** - Check current "AI Assistant Workflow" section

3. ✅ **Update the "AI Assistant Workflow" section** in PROJECT_ROADMAP.md with the latest version below

4. ✅ **Update SESSION_WORKING_TEMPLATE.md** (if it exists at `docs/reference/SESSION_WORKING_TEMPLATE.md`) with the latest version below

5. ✅ **Create missing directories** if needed:
   - `docs/reference/` (if doesn't exist)
   - `docs/archive/sessions/` (if doesn't exist)

6. ✅ **Do NOT modify:**
   - Existing session files
   - Existing roadmap content (phases, status, etc.)
   - Existing git history

7. ✅ **Clean up this file (UPDATE.md) after completion:**
   - **Option 1 (Recommended):** Archive to `docs/archive/` or `docs/archive/workflow-updates/` if directory exists
   - **Option 2:** Delete UPDATE.md from project root (it's a one-time use file)
   - Commit the cleanup with message: "Update workflow to latest version - cleanup UPDATE.md"

**Important:** Only update the workflow instructions. Preserve all existing project content. Then clean up this file.

---

## 📝 Latest AI Assistant Workflow Section

Replace the "🤖 AI Assistant Workflow" section in PROJECT_ROADMAP.md with this:

```markdown
## 🤖 AI Assistant Workflow

**Every conversation start:**
1. ✅ **Check for ProjectRoadmapper updates** (optional but recommended):
   - If ProjectRoadmapper repo exists (e.g., `../ProjectRoadmapper` or configured path): Run `git pull` to get latest templates
   - This keeps workflow templates synchronized across all projects
2. ✅ Read this file (PROJECT_ROADMAP.md) - Current Status section
3. ✅ Check for `SESSION_YYYY_MM_DD_X.md` in root
4. ✅ If exists: Read it, continue that session
5. ✅ If not: **Automatically create new session** (increment letter: A→B→C or new date)

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
- **Quick documentation check** (2-3 min):
  - Verify PROJECT_ROADMAP.md status is current
  - Check README.md features list matches current state (if phase completed)
  - Fix any obvious inconsistencies
- **Automatically archive** SESSION file to docs/archive/sessions/
- **Automatically create** new session file if user wants to continue
- Ensure git clean

**Key principle:** Always in a session. Always grounded in roadmap. Commit frequently. **YOU handle archiving and session creation automatically - never ask the user to do manual file operations.**

**Template:** `docs/reference/SESSION_WORKING_TEMPLATE.md`
```

---

## 📝 Latest SESSION_WORKING_TEMPLATE.md

Update or create `docs/reference/SESSION_WORKING_TEMPLATE.md` with this:

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

**For existing projects:** Tell Cursor:
```
Read UPDATE.md and update the workflow for this project
```

Cursor will:
- ✅ Pull latest updates from ProjectRoadmapper repo (if it exists)
- ✅ Update only the workflow section in PROJECT_ROADMAP.md
- ✅ Update SESSION_WORKING_TEMPLATE.md
- ✅ Preserve all your existing project content
- ✅ Create missing directories if needed
- ✅ **Archive or delete UPDATE.md** (one-time use file - don't leave it in project root)

**Safe for existing projects** - won't overwrite your sessions or roadmap content! ✨

**Note:** UPDATE.md is a one-time use file. After updating the workflow, it should be archived or deleted to keep the project root clean.

