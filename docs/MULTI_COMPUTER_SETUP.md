# Multi-Computer Setup Guide

**Using ProjectRoadmapper on multiple computers on the same network**

---

## Understanding How Data is Stored

ProjectRoadmapper stores data in two places:

### 1. Global Data (Per User, Per Computer)
**Location:** `~/.roadmapper/` (Windows: `C:\Users\YourName\.roadmapper\`)

Contains:
- `config.toml` - Your global preferences (editor, AI assistant, etc.)
- `projects.json` - Registry of all your projects (for cross-project features)
- `knowledge.json` - Knowledge base extracted from all projects

**Important:** This is stored separately on each computer by default.

### 2. Project Data (Per Project)
**Location:** Inside each project directory

Contains:
- `.roadmapper.toml` - Project-specific configuration
- `.roadmapper/history.jsonl` - Session history for that project
- `PROJECT_ROADMAP.md` - Project roadmap
- `SESSION_*.md` - Session files

**Important:** This stays with the project, so if projects are shared (via Git or network drive), this data is shared too.

---

## Setup Options

### Option 1: Independent Setup (Simplest)

**Each computer has its own data, projects are shared via Git/network drive.**

**Steps:**

1. **Install on second computer:**
   ```bash
   # On Computer 2
   cd /path/to/ProjectRoadmapper
   pip install -e .
   ```

2. **Initialize projects on second computer:**
   ```bash
   # Navigate to your project (on network drive or Git clone)
   cd /path/to/shared/project
   
   # Initialize (won't overwrite existing files)
   roadmapper init --no-git
   ```

3. **Register projects:**
   ```bash
   # On Computer 2, register projects you work on
   roadmapper projects register
   ```

**What happens:**
- ✅ Each computer tracks its own session history
- ✅ Each computer has its own knowledge base
- ✅ Projects are shared (via Git/network drive)
- ✅ Can work on same project from either computer
- ⚠️ Knowledge base and project registry are separate per computer

**Best for:** Most users - simple and works well

---

### Option 2: Shared Global Data (Advanced)

**Share global config, knowledge base, and project registry between computers.**

**Steps:**

1. **Set up shared folder on network drive:**
   ```
   \\NetworkDrive\SharedFolder\.roadmapper\
   ```

2. **On Computer 1:**
   ```bash
   # Move existing global data to shared location
   # (Optional - or start fresh)
   ```

3. **On Computer 2:**
   ```bash
   # Create symbolic link pointing to shared location
   # Windows:
   mklink /D C:\Users\YourName\.roadmapper \\NetworkDrive\SharedFolder\.roadmapper
   
   # Mac/Linux:
   ln -s /path/to/shared/.roadmapper ~/.roadmapper
   ```

4. **On Computer 1 (if moving existing data):**
   ```bash
   # Create same symbolic link
   mklink /D C:\Users\YourName\.roadmapper \\NetworkDrive\SharedFolder\.roadmapper
   ```

**What happens:**
- ✅ Shared knowledge base across computers
- ✅ Shared project registry
- ✅ Shared global config
- ⚠️ Only one computer can update global data at a time (to avoid conflicts)
- ⚠️ Requires network drive access

**Best for:** Power users who want unified knowledge base

---

### Option 3: Git-Synced Projects (Recommended)

**Projects are in Git, each computer has independent global data.**

**Steps:**

1. **On Computer 1:**
   ```bash
   # Make sure project is in Git
   git add .
   git commit -m "Add ProjectRoadmapper setup"
   git push
   ```

2. **On Computer 2:**
   ```bash
   # Clone or pull project
   git clone /path/to/repo
   # OR
   git pull
   
   # Install roadmapper
   cd /path/to/ProjectRoadmapper
   pip install -e .
   
   # Initialize (won't overwrite existing files)
   cd /path/to/project
   roadmapper init --no-git
   ```

3. **Register projects on Computer 2:**
   ```bash
   roadmapper projects register
   ```

**What happens:**
- ✅ Project files (roadmap, sessions) sync via Git
- ✅ Project history syncs via Git (`.roadmapper/history.jsonl`)
- ✅ Each computer has its own global data (config, knowledge)
- ✅ Can work on same project from either computer
- ✅ Git handles conflict resolution

**Best for:** Developers using Git - cleanest solution

---

## Recommended Setup

**For most users, we recommend Option 3 (Git-Synced Projects):**

1. **Projects in Git** - Session files, roadmap, history all sync automatically
2. **Independent global data** - Each computer has its own config/knowledge
3. **Register projects per computer** - Each computer knows about its projects

**Why this works well:**
- Git handles syncing automatically
- No conflicts on global data
- Each computer can have different preferences
- Knowledge base grows per computer (focused on what you work on there)

---

## Sharing Projects on Network Drive

If your projects are on a network drive (not Git):

### Setup:

1. **On Computer 1:**
   ```bash
   cd \\NetworkDrive\Projects\MyProject
   roadmapper init --no-git
   roadmapper session
   ```

2. **On Computer 2:**
   ```bash
   cd \\NetworkDrive\Projects\MyProject
   roadmapper init --no-git  # Won't overwrite existing files
   roadmapper projects register
   ```

**What happens:**
- ✅ Same project files on both computers
- ✅ Project history is shared (`.roadmapper/history.jsonl` is in project)
- ✅ Each computer tracks sessions independently (but history file is shared)
- ⚠️ Be careful not to edit same session file simultaneously

**Best practice:** 
- Create new sessions when switching computers: `roadmapper session`
- Let the previous session be archived
- History will show sessions from both computers

---

## Syncing Knowledge Base (Optional)

If you want to share knowledge base between computers:

### Manual Sync:

1. **Export from Computer 1:**
   ```bash
   # Copy knowledge.json
   copy C:\Users\YourName\.roadmapper\knowledge.json \\NetworkDrive\Shared\
   ```

2. **Import to Computer 2:**
   ```bash
   # Copy to Computer 2
   copy \\NetworkDrive\Shared\knowledge.json C:\Users\YourName\.roadmapper\
   ```

3. **Or merge manually:**
   - Both files are JSON
   - Can combine entries (watch for duplicates)

### Using Symbolic Links (Advanced):

See Option 2 above - share the entire `~/.roadmapper/` directory.

---

## Common Scenarios

### Scenario 1: Laptop + Desktop

**Setup:**
- Projects in Git
- Each computer has independent global data
- Pull/push when switching computers

**Workflow:**
```bash
# On Desktop:
roadmapper session
# ... work ...
git add . && git commit -m "Session work"
git push

# On Laptop:
git pull
roadmapper session  # New session
# ... work ...
git add . && git commit -m "Session work"
git push
```

### Scenario 2: Multiple Projects on Network Drive

**Setup:**
- Projects on network drive (`\\NetworkDrive\Projects\`)
- Each computer registers projects it works on
- Project data syncs automatically (same files)

**Workflow:**
```bash
# Register projects you work on:
cd \\NetworkDrive\Projects\ProjectA
roadmapper projects register

cd \\NetworkDrive\Projects\ProjectB
roadmapper projects register

# Work on any project:
cd \\NetworkDrive\Projects\ProjectA
roadmapper session
```

### Scenario 3: Shared Knowledge Base

**Setup:**
- Projects in Git
- Global data on network drive (symbolic link)
- Knowledge base shared across computers

**Workflow:**
```bash
# Same as normal, but knowledge base is shared
roadmapper knowledge index  # Updates shared knowledge base
roadmapper knowledge learn "topic"  # Queries shared knowledge
```

---

## Troubleshooting

### "Project not found" on second computer

**Problem:** Registered on Computer 1, but Computer 2 doesn't see it.

**Solution:**
```bash
# On Computer 2, register the project:
cd /path/to/project
roadmapper projects register
```

### Knowledge base empty on second computer

**Problem:** Knowledge indexed on Computer 1, but Computer 2 has empty knowledge base.

**Solution:** This is expected if using independent setup. Either:
- Index knowledge on Computer 2: `roadmapper knowledge index`
- Or set up shared knowledge base (Option 2)

### Conflicting session files

**Problem:** Two computers editing same session file.

**Solution:**
- Always create new session when switching computers: `roadmapper session`
- Archive old sessions before switching
- Or use Git to manage conflicts

### Path issues on network drive

**Problem:** Paths don't work on second computer (different drive letters).

**Solution:**
- Use UNC paths consistently: `\\Server\Share\Projects\`
- Or use same drive mapping on both computers
- ProjectRoadmapper handles paths relative to project root, so usually fine

---

## Quick Reference

**Independent Setup (Recommended):**
```bash
# Computer 1 & 2: Install
pip install -e /path/to/ProjectRoadmapper

# Each computer: Initialize projects
cd /path/to/project
roadmapper init --no-git
roadmapper projects register
```

**Shared Global Data:**
```bash
# Set up symbolic link to shared .roadmapper folder
# Windows:
mklink /D C:\Users\YourName\.roadmapper \\NetworkDrive\Shared\.roadmapper
```

**Git-Synced Projects:**
```bash
# Each computer: Clone/pull project
git clone /path/to/repo
cd project
roadmapper init --no-git
roadmapper projects register
```

---

**Last Updated:** November 4, 2025

