# Troubleshooting Guide

**Common issues and solutions**

---

## Installation Issues

### "build backend is missing the 'build_editable' hook" (Ubuntu/Linux)

**Error:**
```
ERROR: Project file:///... has a 'pyproject.toml' and its build backend is missing the 'build_editable' hook.
```

**Solution:**

Update setuptools first:
```bash
pip install --upgrade setuptools wheel
pip install -e .
```

Or use regular install instead of editable:
```bash
pip install .
```

**Note:** This was fixed in the latest version. Make sure you have the latest code:
```bash
cd ProjectRoadmapper
git pull
pip install --upgrade setuptools wheel
pip install -e .
```

---

### "Command not found" after installation

**On Linux/Ubuntu:**
```bash
# Try with python3 module:
python3 -m roadmapper.cli --version

# If that works, use:
python3 -m roadmapper.cli init
python3 -m roadmapper.cli session

# Or add to PATH:
export PATH="$HOME/.local/bin:$PATH"
```

**On Windows:**
```powershell
# Try:
python -m roadmapper.cli --version

# If that works, use:
python -m roadmapper.cli init
python -m roadmapper.cli session
```

---

## Windows Console Encoding Errors

### "'charmap' codec can't encode character"

**Error:** When running commands, you see encoding errors with emojis or special characters.

**Solution:** This is fixed in the latest version. ProjectRoadmapper automatically sets UTF-8 encoding on Windows.

If you still see errors, make sure you have the latest version:
```powershell
cd ProjectRoadmapper
git pull
pip install -e .
```

---

## File Encoding Errors

### "'charmap' codec can't decode byte"

**Error:** When reading template files or session files.

**Solution:** All file operations use UTF-8 encoding. If you see this error:

1. Make sure files are saved as UTF-8
2. Update to latest version (has UTF-8 fixes)
3. Check file isn't corrupted

---

## Configuration Issues

### Configuration not found

**Problem:** `roadmapper config get` returns "not found"

**Solution:**
- Check spelling: `roadmapper config list` to see available keys
- Configuration uses dot notation: `preferences.editor` not `preferences/editor`
- Keys are case-sensitive

---

### Configuration not applied

**Problem:** Settings don't seem to take effect

**Solution:**
- Remember precedence: project > global > defaults
- Check both configs: `roadmapper config list --scope global` and `roadmapper config list --scope project`
- Project config is in `.roadmapper.toml` in project root
- Global config is in `~/.roadmapper/config.toml`

---

## History Tracking Issues

### History shows no sessions

**Problem:** `roadmapper history list` is empty

**Solution:**
- History only tracks sessions created with `roadmapper session` command
- Old sessions (created manually) won't appear
- Check `.roadmapper/history.jsonl` exists in project root
- Make sure you're in a project directory (has `PROJECT_ROADMAP.md`)

---

### "can't compare offset-naive and offset-aware datetimes"

**Error:** When running `roadmapper history stats`

**Solution:** This was fixed in a recent update. Update to latest version:
```bash
cd ProjectRoadmapper
git pull
pip install -e .
```

---

## Project Registry Issues

### Project not showing in `roadmapper projects list`

**Problem:** Registered project doesn't appear

**Solution:**
- Make sure you registered it: `roadmapper projects register`
- Check you're looking at the right registry: `roadmapper projects list`
- Project must have `PROJECT_ROADMAP.md` to be registered
- Registry is stored in `~/.roadmapper/projects.json`

---

### "Project not found" when searching

**Problem:** `roadmapper search` doesn't find projects

**Solution:**
- Register projects first: `roadmapper projects register`
- Or use `roadmapper projects discover` to auto-discover
- Check project has session files or roadmap to search

---

## Dashboard Issues

### Dashboard won't start

**Error:** Flask import error or server won't start

**Solution:**
- Dashboard requires Flask (optional dependency)
- Install with: `pip install 'roadmapper[dashboard]'`
- Or: `pip install flask` then `roadmapper dashboard`

---

### Dashboard shows no projects

**Problem:** Dashboard loads but shows empty

**Solution:**
- Register projects first: `roadmapper projects register`
- Make sure projects have `PROJECT_ROADMAP.md`
- Check browser console for errors

---

## Knowledge Base Issues

### Knowledge base empty

**Problem:** `roadmapper knowledge stats` shows 0 entries

**Solution:**
- Index knowledge first: `roadmapper knowledge index`
- Knowledge is extracted from session files
- Make sure you have session files with "Discoveries" or "Accomplishments" sections
- Knowledge is stored in `~/.roadmapper/knowledge.json`

---

### Knowledge search returns nothing

**Problem:** `roadmapper knowledge search "query"` finds nothing

**Solution:**
- Index knowledge first: `roadmapper knowledge index`
- Search is case-insensitive but exact text matching
- Try broader search terms
- Check knowledge entries: `roadmapper knowledge stats`

---

## Git Integration Issues

### Git conflicts on session files

**Problem:** Git merge conflicts when switching computers

**Prevention:**
- Always create new session when switching computers
- Commit and push before switching
- Archive old sessions before starting new one

**If conflict happens:**
- Git will mark conflicts in files
- Manually merge or choose one version
- Both sessions preserved in history (if indexed)

---

## Multi-Computer Setup Issues

### Projects not syncing between computers

**Problem:** Changes on one computer don't appear on other

**Solution:**
- Make sure projects are in Git and pushed/pulled
- Project files (roadmap, sessions) sync via Git
- Global data (config, knowledge) is separate per computer
- Register projects on each computer: `roadmapper projects register`

---

### Path issues on network drive

**Problem:** Paths don't work on second computer

**Solution:**
- Use consistent paths (UNC paths on Windows)
- Or use Git instead of network drive
- ProjectRoadmapper uses relative paths, usually fine

---

## Getting Help

If you're still stuck:

1. **Check the version:**
   ```bash
   roadmapper --version
   # OR
   python3 -m roadmapper.cli --version
   ```

2. **Update to latest:**
   ```bash
   cd ProjectRoadmapper
   git pull
   pip install -e .
   ```

3. **Check documentation:**
   - [Quick Start](QUICK_START.md)
   - [Multi-Computer Setup](MULTI_COMPUTER_SETUP.md)
   - [Configuration Guide](reference/config.md)

4. **Report the issue:**
   - Open an issue on GitHub: https://github.com/FloppyPete/ProjectRoadmapper/issues
   - Include:
     - Your OS (Windows/Linux/Mac)
     - Python version: `python --version`
     - Error message (full output)
     - Steps to reproduce

---

**Last Updated:** November 4, 2025
