# Clone Setup: Using ProjectRoadmapper on Multiple Computers

**Quick guide for setting up ProjectRoadmapper on a second computer via Git clone**

**Works on:** Windows, Mac, Linux (Ubuntu, etc.) - ProjectRoadmapper is cross-platform!

---

## Step 1: Clone ProjectRoadmapper on Computer 2

### On Linux/Ubuntu:

```bash
# Navigate to where you want to install it
cd ~/Projects
# Or just: cd ~

# Clone the repository
git clone https://github.com/FloppyPete/ProjectRoadmapper.git

# Go into the directory
cd ProjectRoadmapper

# Install it (you may need pip3 on some systems)
pip install -e .
# OR if pip3 is separate:
pip3 install -e .
```

**Test it worked:**
```bash
roadmapper --version
# OR if not in PATH:
python3 -m roadmapper.cli --version
```

### On Windows (for reference):

```powershell
# Navigate to where you want to install it
cd C:\Users\YourName\Projects

# Clone the repository
git clone https://github.com/FloppyPete/ProjectRoadmapper.git

# Go into the directory
cd ProjectRoadmapper

# Install it
pip install -e .
```

**Test it worked:**
```powershell
roadmapper --version
```

---

## Step 2: Set Up Your Existing Projects

For each project you want to use ProjectRoadmapper with:

### If Your Project is Already in Git:

**On Linux/Ubuntu:**
```bash
# Navigate to your project
cd ~/projects/your-project
# OR: cd /path/to/your/project

# Make sure you have the latest (if you worked on Computer 1)
git pull

# Initialize ProjectRoadmapper (won't overwrite existing files)
roadmapper init --no-git

# Register the project (for cross-project features)
roadmapper projects register
```

**On Windows:**
```powershell
# On Computer 2, navigate to your project
cd C:\path\to\your\project

# Make sure you have the latest (if you worked on Computer 1)
git pull

# Initialize ProjectRoadmapper (won't overwrite existing files)
roadmapper init --no-git

# Register the project (for cross-project features)
roadmapper projects register
```

### If Your Project is NOT in Git Yet:

**Option A: Put it in Git (Recommended)**

**On Linux/Ubuntu:**
```bash
# Initialize Git in your project
cd ~/projects/your-project
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-git-repo-url>
git push -u origin main
```

**On Windows:**
```powershell
# On Computer 1 (or 2), initialize Git in your project
cd C:\path\to\your\project
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-git-repo-url>
git push -u origin main
```

Then on Computer 2 (either OS):
```bash
git clone <your-git-repo-url>
cd project-name
roadmapper init --no-git
roadmapper projects register
```

**Option B: Use Network Drive (Linux)**
```bash
# On Linux, mount network drive first (if needed)
# Then navigate to mounted location
cd /mnt/network/Projects/YourProject

# Initialize
roadmapper init --no-git

# Register
roadmapper projects register
```

---

## Step 3: Verify Setup

**Check ProjectRoadmapper is working:**
```bash
roadmapper status
# OR if not in PATH:
python3 -m roadmapper.cli status
```

**Check your registered projects:**
```bash
roadmapper projects list
```

**Create a test session:**
```bash
roadmapper session
```

---

## Workflow: Switching Between Computers

### When Starting Work on Computer 2 (Linux):

```bash
# 1. Pull latest changes from Git
cd ~/projects/your-project
git pull

# 2. Create new session
roadmapper session

# 3. Tell your AI assistant:
# "Read PROJECT_ROADMAP.md and continue the current session"
```

### When Finishing Work:

```bash
# 1. Commit your work
git add .
git commit -m "Session work: [describe what you did]"

# 2. Push to remote
git push
```

### When Starting Work on Computer 1 (Windows) Again:

```powershell
# 1. Pull latest changes
git pull

# 2. Create new session
roadmapper session

# 3. Continue working
```

---

## What Gets Synced?

**Via Git (automatically synced):**
- ✅ `PROJECT_ROADMAP.md` - Project roadmap
- ✅ `SESSION_*.md` - Session files
- ✅ `.roadmapper/history.jsonl` - Project session history
- ✅ `.roadmapper.toml` - Project-specific config
- ✅ All your code and project files

**Separate per computer:**
- ⚠️ `~/.roadmapper/config.toml` - Your preferences (editor, etc.)
  - Windows: `C:\Users\YourName\.roadmapper\config.toml`
  - Linux: `~/.roadmapper/config.toml` (same location!)
- ⚠️ `~/.roadmapper/projects.json` - Project registry
- ⚠️ `~/.roadmapper/knowledge.json` - Knowledge base

**Note:** The separate items are fine - each computer can have its own preferences. If you want to sync knowledge base, see the full multi-computer guide.

---

## Quick Commands Reference

**Setup (one time) - Linux/Ubuntu:**
```bash
git clone https://github.com/FloppyPete/ProjectRoadmapper.git
cd ProjectRoadmapper
pip3 install -e .
```

**Setup (one time) - Windows:**
```powershell
git clone https://github.com/FloppyPete/ProjectRoadmapper.git
cd ProjectRoadmapper
pip install -e .
```

**For each project (works on both):**
```bash
cd /path/to/project
roadmapper init --no-git
roadmapper projects register
```

**Daily workflow (works on both):**
```bash
git pull                          # Get latest changes
roadmapper session                # Create/continue session
# ... work ...
git add . && git commit -m "..." # Commit work
git push                          # Push to remote
```

---

## Troubleshooting

### "Command not found" after installation

**On Linux/Ubuntu:**
```bash
# Try with python3:
python3 -m roadmapper.cli --version

# If that works, use python3 -m roadmapper.cli instead of roadmapper:
python3 -m roadmapper.cli init
python3 -m roadmapper.cli session

# Or add to PATH (if pip installed to user directory):
export PATH="$HOME/.local/bin:$PATH"
```

**On Windows:**
```powershell
# Try:
python -m roadmapper.cli --version

# If that works, use python -m roadmapper.cli instead of roadmapper:
python -m roadmapper.cli init
python -m roadmapper.cli session
```

### Project not showing in `roadmapper projects list`

Make sure you registered it:
```powershell
cd /path/to/project
roadmapper projects register
```

### Git conflicts on session files

**Prevent conflicts:**
- Always create new session when switching computers
- Commit and push before switching
- Archive old sessions before starting new one

**If conflict happens:**
- Git will mark the conflict
- Manually merge or choose one version
- Both sessions are preserved in history

---

## Repository Info

**GitHub:** https://github.com/FloppyPete/ProjectRoadmapper

**Clone URL:**
```
https://github.com/FloppyPete/ProjectRoadmapper.git
```

**Last verified:** November 4, 2025

---

**That's it!** You're ready to use ProjectRoadmapper on both computers. 🗺️

