# Migration Guide: Upgrading Existing Projects

**For projects using the workflow before ProjectRoadmapper CLI tool**

**Don't know what CLI is?** See [WHAT_IS_CLI.md](WHAT_IS_CLI.md) for a simple explanation.

---

## What Changed?

Since spinning off ProjectRoadmapper, we've added:

1. **CLI Tool** - `roadmapper` commands for automation
2. **Configuration System** - Global and project-level TOML config
3. **History Tracking** - Automatic session history with analytics
4. **Enhanced Documentation** - Multi-agent notes, troubleshooting guide
5. **Workflow Improvements** - Better error handling, Windows support

---

## Do You Need to Upgrade?

**Short Answer:** Not required, but recommended for benefits.

**Your project will continue working** with the existing workflow files. The CLI tool is **optional** - you can:
- Keep using manual workflow (copy ROADMAP_CREATOR.md, create files manually)
- Migrate to CLI tool for automation and features
- Hybrid approach (keep manual workflow, add CLI for some features)

---

## Upgrade Options

### Option 1: Keep Manual Workflow (No Changes Needed)

**What to update:**
- ✅ Add multi-agent note to `PROJECT_ROADMAP.md` AI Assistant Workflow section (if using multi-agent)
- ✅ Update `ROADMAP_CREATOR.md` with any improvements (optional)

**What stays the same:**
- ✅ All existing session files
- ✅ Existing PROJECT_ROADMAP.md structure
- ✅ Current workflow process

**Time:** 5 minutes (just add multi-agent note if needed)

---

### Option 2: Migrate to CLI Tool (Recommended)

**Benefits:**
- Automated session creation
- Configuration management
- History tracking and analytics
- Better status display

**Steps:**

1. **Install roadmapper CLI:**
   ```bash
   pip install roadmapper
   # Or install from source:
   cd /path/to/ProjectRoadmapper
   pip install -e .
   ```

2. **Initialize CLI in your project (non-destructive):**
   ```bash
   cd /path/to/LocalAgent
   roadmapper init --no-git  # Don't re-init git if already initialized
   ```
   
   This creates:
   - `.roadmapper/` directory (if doesn't exist)
   - Updates `docs/reference/SESSION_WORKING_TEMPLATE.md` if missing
   - Does NOT overwrite existing PROJECT_ROADMAP.md

3. **Optional: Set up configuration:**
   ```bash
   roadmapper config set preferences.editor "code"
   roadmapper config set preferences.ai_assistant "cursor"
   ```

4. **Start using CLI commands:**
   ```bash
   # Create sessions
   roadmapper session
   
   # Check status
   roadmapper status
   
   # View history
   roadmapper history list
   roadmapper history stats
   ```

**Migration notes:**
- Existing session files remain valid
- PROJECT_ROADMAP.md stays as-is (CLI doesn't modify it)
- History tracking starts from first CLI session
- Old sessions won't appear in history (but still exist in files)

**Time:** 10-15 minutes

---

### Option 3: Hybrid Approach

**Use CLI for some features, keep manual workflow for others:**

**Use CLI for:**
- Session creation (`roadmapper session`)
- Status checking (`roadmapper status`)
- History analytics (`roadmapper history stats`)

**Keep manual for:**
- PROJECT_ROADMAP.md updates
- Session file editing
- Workflow decisions

**Setup:**
- Install CLI (see Option 2, step 1)
- Use CLI commands as convenient
- Continue manual workflow otherwise

**Time:** 5 minutes (just install CLI)

---

## What Files Need Updating?

### Required Updates (All Options)

**PROJECT_ROADMAP.md:**
Add this note to the AI Assistant Workflow section:

```markdown
**Note:** Current workflow assumes single-agent mode. For multi-agent scenarios 
(e.g., Cursor 2.0), see analysis in Session "Getting the Developer Up to Speed" 
or use agent-specific session files (`SESSION_YYYY_MM_DD_X_AGENT_NAME.md`).
```

**Time:** 2 minutes

### Optional Updates

**ROADMAP_CREATOR.md:**
- Update with latest improvements (optional)
- Add note about CLI tool availability
- Add multi-agent guidance

**Time:** 10-15 minutes

---

## Backwards Compatibility

**What's compatible:**
- ✅ All existing session files (`SESSION_YYYY_MM_DD_X.md`)
- ✅ Existing PROJECT_ROADMAP.md structure
- ✅ Current workflow process
- ✅ All markdown files

**What's new (optional):**
- CLI commands
- Configuration files (`.roadmapper.toml`, `~/.roadmapper/config.toml`)
- History tracking (`.roadmapper/history.jsonl`)

**Key Point:** The CLI tool enhances the workflow but doesn't break existing usage.

---

## Recommended Upgrade Path

**For LocalAgent project (original spawn project):**

1. **Quick Update (5 minutes):**
   - Add multi-agent note to PROJECT_ROADMAP.md
   - Document that you're using manual workflow
   - No other changes needed

2. **Optional CLI Migration (15 minutes):**
   - Install roadmapper CLI
   - Run `roadmapper init --no-git` (non-destructive)
   - Start using `roadmapper session` and `roadmapper status`
   - Keep existing PROJECT_ROADMAP.md as-is

3. **Future (when convenient):**
   - Migrate to CLI-driven workflow fully
   - Set up global config for preferences
   - Use history tracking for analytics

---

## Checking Your Current Setup

**Files you should have:**
- `PROJECT_ROADMAP.md` ✅
- `SESSION_YYYY_MM_DD_X.md` files ✅
- `docs/reference/SESSION_WORKING_TEMPLATE.md` (optional)
- `docs/archive/sessions/` directory (optional)

**What the CLI adds:**
- `.roadmapper/` directory (for history)
- `.roadmapper.toml` (project config, if you set config)
- `~/.roadmapper/config.toml` (global config, if you set global config)

---

## Common Questions

**Q: Will upgrading break my existing workflow?**  
A: No. The CLI tool is completely optional and non-destructive. Your existing files continue to work.

**Q: Do I need to migrate all my old sessions?**  
A: No. Old sessions remain valid. History tracking only starts from when you begin using CLI commands.

**Q: Can I use both manual workflow and CLI?**  
A: Yes! They're fully compatible. Use whichever is convenient.

**Q: What if I don't want the CLI?**  
A: That's fine! Just add the multi-agent note to PROJECT_ROADMAP.md and you're done.

---

## Quick Reference

**Minimal upgrade (5 minutes):**
1. Add multi-agent note to PROJECT_ROADMAP.md AI Assistant Workflow section
2. Done ✅

**Full CLI migration (15 minutes):**
1. `pip install roadmapper` (or install from source)
2. `cd /path/to/LocalAgent`
3. `roadmapper init --no-git`
4. Start using `roadmapper session`, `roadmapper status`
5. Optional: Set config preferences

**Status check:**
```bash
roadmapper status  # Works even if you haven't migrated
```

---

**Last Updated:** November 4, 2025  
**Compatible with:** All workflow versions since LocalAgent project

