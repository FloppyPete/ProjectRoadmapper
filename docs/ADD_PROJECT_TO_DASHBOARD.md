# 📊 Adding Projects to Dashboard

**How to make your projects appear in the ProjectRoadmapper dashboard**

---

## Quick Method: Manual Registration

If your project isn't automatically discovered, register it manually:

```bash
roadmapper projects register /path/to/your/project
```

**Example:**
```bash
# Windows
roadmapper projects register C:\Users\james\MyProject

# Linux/Mac
roadmapper projects register ~/projects/MyProject
```

**Requirements:**
- Project must have `PROJECT_ROADMAP.md` or `.roadmapper.toml` file
- Path must exist and be accessible

---

## Automatic Discovery

The dashboard automatically searches common project locations:

**Default search paths:**
- `~/Projects`
- `~/projects`
- `~/Documents/Projects`
- `~/Development`
- `~/dev`
- `~/source`
- `~/code`

**To discover projects:**
```bash
roadmapper projects discover
```

This will scan the default locations and register any projects it finds.

---

## If Your Project Isn't Found

### Option 1: Register Manually (Easiest)
```bash
roadmapper projects register /full/path/to/project
```

### Option 2: Move Project to Default Location
Move your project to one of the default search paths listed above, then run:
```bash
roadmapper projects discover
```

### Option 3: Check Project Has Required Files
Make sure your project has:
- `PROJECT_ROADMAP.md` in the root directory, OR
- `.roadmapper.toml` in the root directory

---

## Verify Registration

**List all registered projects:**
```bash
roadmapper projects list
```

**Check dashboard:**
- Launch dashboard: `launch_dashboard_silent.vbs` (or `roadmapper dashboard`)
- Your project should appear in the dashboard

---

## Update Project Info

If you update a project and want to refresh its info:

**Re-register it:**
```bash
roadmapper projects register /path/to/project
```

This will update:
- Last session info
- Health status
- Project metadata

---

## Troubleshooting

### "doesn't appear to be a roadmapper project"
- Make sure `PROJECT_ROADMAP.md` exists in project root
- Or create `.roadmapper.toml` file

### Project not showing in dashboard
- Check it's registered: `roadmapper projects list`
- Refresh dashboard (reload browser page)
- Re-register if needed: `roadmapper projects register /path`

### Discovery not finding projects
- Check project is in one of the default search paths
- Or register manually
- Make sure you have read permissions to the directory

---

**That's it!** Once registered, your project will appear in the dashboard automatically.

