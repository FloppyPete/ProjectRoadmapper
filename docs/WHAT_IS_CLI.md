# What is a CLI? (Simple Explanation for Non-Programmers)

---

## The Simple Answer

**CLI = Command Line Interface**

It's a way to control your computer by typing commands instead of clicking buttons.

---

## Real-World Analogy

**Think of your computer like a restaurant:**

- **GUI (Graphical User Interface)** = Looking at a menu and pointing at what you want
- **CLI** = Speaking directly to the chef and telling them exactly what you want

Both ways work! Some people prefer menus (GUI), some prefer talking (CLI).

---

## Visual Comparison

### Using GUI (What You Probably Do Now):
1. Open File Explorer
2. Navigate to your project folder
3. Right-click → New → Text Document
4. Type "SESSION_2025_11_04_E.md"
5. Open the file
6. Copy template content
7. Paste and edit

**Steps:** 7 steps, multiple clicks

### Using CLI (What CLI Does):
1. Open terminal/command prompt
2. Type: `roadmapper session`
3. Press Enter

**Steps:** 2 steps, one command

---

## What Do These Commands Actually Do?

### `roadmapper session`
**What it does:** Creates a new session file automatically
**Instead of:** Manually creating `SESSION_2025_11_04_E.md` yourself
**Benefit:** Always creates it correctly, automatically increments letters (A→B→C)

### `roadmapper status`
**What it does:** Shows you project status
**Instead of:** Manually checking what files exist, what's changed
**Benefit:** Shows current session, recent sessions, git status, activity stats - all in one view

### `roadmapper config set preferences.editor "code"`
**What it does:** Saves a preference setting
**Instead of:** Manually editing a config file
**Benefit:** Stores settings that apply to all your projects

### `roadmapper history stats`
**What it does:** Shows how many sessions you've had
**Instead of:** Manually counting session files
**Benefit:** Automatic tracking, shows trends (sessions per week, etc.)

---

## Do You Need to Learn CLI?

**Short Answer: No!**

**You can:**
- ✅ Keep using your current manual workflow
- ✅ Have someone else set up CLI for you
- ✅ Use CLI just for specific things you find useful
- ✅ Ignore CLI completely if you prefer manual

**The workflow works perfectly fine either way.**

---

## If You Want to Try CLI

**What You Need:**
1. **Terminal/Command Prompt** - Already on your computer
   - Windows: PowerShell or Command Prompt
   - Mac: Terminal
   - Usually found in your applications

2. **Python** - If not installed, someone can help install it

3. **Install roadmapper** - One command:
   ```bash
   pip install roadmapper
   ```

**Then You Can:**
- Type `roadmapper session` instead of manually creating files
- Type `roadmapper status` to see project status
- Use commands when convenient, manual workflow otherwise

---

## Bottom Line

**CLI = Typing commands instead of clicking**

**For this project:**
- CLI automates things you do manually now
- It's optional - your manual workflow works fine
- You can use it if you want, ignore it if you don't

**Think of it like:**
- Manual workflow = Writing with pen and paper
- CLI = Using a typewriter
- Both work! Use whichever you prefer.

---

**Don't worry about CLI if it sounds complicated.** Your current workflow is perfectly valid and will continue working forever. CLI is just a bonus convenience feature.

