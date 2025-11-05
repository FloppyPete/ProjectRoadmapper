# 🚀 Dashboard Launcher Setup

**Easy one-click dashboard access - no typing required!**

---

## Quick Setup (Windows)

### Option 1: Silent Launcher (No Terminal Window) ⭐ Recommended

1. **Right-click** `launch_dashboard_silent.vbs` in the ProjectRoadmapper folder
2. Select **"Create shortcut"**
3. **Right-click** the shortcut and select **"Properties"**
4. Click **"Change Icon"** and choose a nice icon (or browse for one)
5. **Drag the shortcut** to your desktop
6. **Rename it** to "ProjectRoadmapper Dashboard" (or whatever you like)

**Done!** Now you can double-click the desktop icon to launch the dashboard **without any terminal window popping up!**

### Option 2: With Terminal Window (For Debugging)

If you want to see status messages:

1. **Right-click** `launch_dashboard.bat` in the ProjectRoadmapper folder
2. Select **"Create shortcut"**
3. **Right-click** the shortcut and select **"Properties"**
4. Set **"Run:"** to **"Minimized"** (optional - minimizes window)
5. Click **"Change Icon"** and choose a nice icon
6. **Drag the shortcut** to your desktop

**Done!** This version shows a terminal window with status messages.

---

### Option 2: Pin to Taskbar

1. Right-click `launch_dashboard.bat`
2. Select **"Pin to taskbar"**
3. Right-click the pinned icon → **"Properties"** → **"Change Icon"**

**Done!** Click the taskbar icon anytime to launch.

---

### Option 3: Start Menu

1. Right-click `launch_dashboard.bat`
2. Select **"Pin to Start"**

**Done!** Launch from Start menu.

---

## What Happens When You Launch

1. ✅ Dashboard server starts automatically
2. ✅ Browser opens automatically to `http://127.0.0.1:5000`
3. ✅ Dashboard shows all your projects and metrics
4. ✅ Server keeps running in the background (silent launcher) or visible window (batch file)

**No typing. No commands. No terminal window (with silent launcher). Just double-click and go!**

### Silent vs Visible

- **`launch_dashboard_silent.vbs`** - No terminal window, completely silent
- **`launch_dashboard.bat`** - Shows terminal window with status messages (useful for debugging)

---

## Troubleshooting

### "Python is not recognized"
- Make sure Python is installed and in your PATH
- You may need to use `python3` instead of `python`

### "Flask is required"
- Install Flask: `pip install flask`
- Or install dashboard support: `pip install 'roadmapper[dashboard]'`

### Dashboard doesn't open in browser
- Wait a few seconds for server to start
- Manually open: `http://127.0.0.1:5000`

### Port 5000 already in use
- Another dashboard instance might be running
- Close other instances or use a different port
- Edit `launch_dashboard.py` to change the port

---

## Advanced: Custom Port

To use a different port, edit `launch_dashboard.py`:

```python
# Change this line:
app.run(host="127.0.0.1", port=5000, debug=False)

# To:
app.run(host="127.0.0.1", port=8080, debug=False)  # or any port you want
```

---

## Linux/Mac Users

For Linux or Mac, use `launch_dashboard.py` directly:

```bash
# Make it executable
chmod +x launch_dashboard.py

# Run it
./launch_dashboard.py
```

Or create a desktop entry file (`.desktop` on Linux).

---

**Enjoy your one-click dashboard access!** 🎉

