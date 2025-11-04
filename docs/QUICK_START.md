# Quick Start: Setting Up ProjectRoadmapper in an Existing Project

**Simple guide to get ProjectRoadmapper working in your project**

**Don't know what CLI is?** See [WHAT_IS_CLI.md](WHAT_IS_CLI.md) for a simple explanation.

---

## Step 1: Install ProjectRoadmapper

Since ProjectRoadmapper is still in development, you'll install it from source (the current project):

### On Windows (PowerShell):

```powershell
# Navigate to ProjectRoadmapper directory
cd C:\Users\james\ProjectRoadmapper

# Install in "editable" mode (changes update automatically)
pip install -e .
```

### On Mac/Linux:

```bash
# Navigate to ProjectRoadmapper directory
cd /path/to/ProjectRoadmapper

# Install in "editable" mode
pip install -e .
```

**What this does:** Makes the `roadmapper` command available everywhere on your computer.

**Test it worked:**
```bash
roadmapper --version
```

You should see the version number.

---

## Step 2: Navigate to Your Existing Project

Open a terminal/PowerShell and go to your project folder:

```bash
cd /path/to/your/existing/project
```

---

## Step 3: Initialize ProjectRoadmapper

Run this command in your project directory:

```bash
roadmapper init
```

**What this does:**
- Creates `.roadmapper/` directory (for history tracking)
- Creates `docs/reference/SESSION_WORKING_TEMPLATE.md` (session template)
- Creates `PROJECT_ROADMAP.md` (if it doesn't exist)
- Sets up the project structure

**Important:** This is **non-destructive** - it won't delete or overwrite existing files. If you already have a `PROJECT_ROADMAP.md`, it will leave it alone.

**If you don't want to initialize Git** (already have Git set up):
```bash
roadmapper init --no-git
```

---

## Step 4: Create Your First Session

Now create a session file:

```bash
roadmapper session
```

**What this does:**
- Creates a new `SESSION_YYYY_MM_DD_X.md` file (e.g., `SESSION_2025_11_04_A.md`)
- Uses the template to set up the structure
- Automatically logs it to history

---

## Step 5: Configure (Optional)

Set your preferences:

```bash
# Set your preferred editor (optional)
roadmapper config set preferences.editor "code"

# Set your AI assistant (optional)
roadmapper config set preferences.ai_assistant "cursor"
```

These settings are saved in `.roadmapper.toml` in your project.

---

## Step 6: Check Status

See what's going on in your project:

```bash
roadmapper status
```

This shows:
- Current session file
- Recent activity
- Project health
- Session statistics

---

## What Files Were Created?

After setup, you'll have:

```
your-project/
├── PROJECT_ROADMAP.md          # Main roadmap (or existing one untouched)
├── SESSION_YYYY_MM_DD_X.md     # Current session file
├── .roadmapper/                 # Hidden directory for tracking
│   └── history.jsonl           # Session history
├── .roadmapper.toml            # Project config (if you set preferences)
└── docs/
    └── reference/
        └── SESSION_WORKING_TEMPLATE.md  # Template for sessions
```

---

## Common Commands

### Create a New Session
```bash
roadmapper session
```

### Check Project Status
```bash
roadmapper status
```

### View Session History
```bash
roadmapper history list
roadmapper history stats
```

### Search Across Projects (if multiple projects registered)
```bash
roadmapper search "query"
roadmapper projects list
```

### Query Knowledge Base
```bash
roadmapper knowledge index      # Extract knowledge from sessions
roadmapper knowledge learn "topic"  # What did I learn about X?
roadmapper knowledge search "query"
```

---

## Next Steps

1. **Tell your AI assistant** (Cursor, etc.):
   ```
   Read PROJECT_ROADMAP.md and continue the current session.
   ```

2. **Start working** - Your AI assistant will:
   - Read the roadmap for context
   - Continue from the current session file
   - Maintain context across sessions

3. **When done for the day:**
   - Archive the session file (move to `docs/archive/sessions/`)
   - Update `PROJECT_ROADMAP.md` with what you accomplished
   - Next time, create a new session with `roadmapper session`

---

## Troubleshooting

### "Command not found" after installation

Make sure Python scripts are in your PATH. Try:
```bash
python -m roadmapper.cli --version
```

If that works, you can use `python -m roadmapper.cli` instead of `roadmapper`:
```bash
python -m roadmapper.cli init
python -m roadmapper.cli session
```

### Already have PROJECT_ROADMAP.md?

That's fine! `roadmapper init` won't overwrite it. You can:
- Keep using your existing roadmap
- Use CLI commands for sessions and status
- Everything will work together

### Want to use multiple projects?

Register projects for cross-project features:
```bash
# In each project directory:
roadmapper projects register

# List all registered projects:
roadmapper projects list

# Search across all projects:
roadmapper search "query"
```

---

## Quick Reference

**Setup (one time):**
```bash
pip install -e /path/to/ProjectRoadmapper
cd /path/to/your/project
roadmapper init
roadmapper session
```

**Daily workflow:**
```bash
roadmapper session          # Create new session
roadmapper status           # Check status
roadmapper history stats    # See activity
```

**For AI assistants:**
- Read `PROJECT_ROADMAP.md` first
- Check for `SESSION_*.md` files
- Continue existing session or create new one

---

**That's it!** You're ready to use ProjectRoadmapper. 🗺️

For more details, see:
- [Migration Guide](MIGRATION_GUIDE.md) - If upgrading from manual workflow
- [Configuration Guide](reference/config.md) - Advanced configuration
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and fixes

