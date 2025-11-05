# ProjectRoadmapper 🗺️

**Multi-session development workflow tool for AI-assisted coding projects**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Alpha](https://img.shields.io/badge/Status-Alpha-orange.svg)]()

---

## 🎯 What Is This?

ProjectRoadmapper helps you maintain context and momentum across multiple development sessions, especially when working with AI assistants like Cursor, GitHub Copilot, or similar tools.

**The Problem:**
- Complex projects span multiple sessions
- Context gets lost between work sessions
- Decisions and discoveries aren't captured
- AI assistants restart from scratch each time

**The Solution:**
- Structured workflow with living roadmap
- Session files maintain continuity
- AI assistants read roadmap and continue where you left off
- Decisions and discoveries are preserved

---

## ✨ Features

### Current (Phase 1, 2 & 3)
- ✅ **ROADMAP_CREATOR.md** - Complete bootstrap guide (795 lines, battle-tested)
- ✅ **BOOTSTRAP.md** - Single-file setup for new projects (no CLI needed)
- ✅ **UPDATE.md** - Single-file update for existing projects
- ✅ **CLI Tool** - `roadmapper init`, `roadmapper session`, `roadmapper status`
- ✅ **Configuration** - Global and project-level TOML config with `roadmapper config`
- ✅ **Session History** - Track sessions with `roadmapper history`
- ✅ **Analytics** - View session statistics and activity trends
- ✅ **Cross-Project Search** - `roadmapper search` across all projects
- ✅ **Project Registry** - `roadmapper projects` to manage multiple projects
- ✅ **Web Dashboard** - `roadmapper dashboard` for visual overview
- ✅ **Dashboard Launcher** - One-click desktop shortcut (no typing required!)
- ✅ **Knowledge Base** - `roadmapper knowledge` to extract and query insights

### Planned (See [Roadmap](#roadmap))
- 🔜 **AI IDE Integrations** - Native Cursor/Copilot extensions
- 🔜 **Template Marketplace** - Share and discover workflow templates
- 🔜 **Multi-Agent Support** - Built-in coordination for Cursor 2.0+

---

## 🚀 Quick Start

### ⭐ Easiest Method: Bootstrap File (No CLI Required!)

**For NEW projects:**

1. Copy `BOOTSTRAP.md` from this repo to your project root
2. Tell Cursor: `"Read BOOTSTRAP.md and set up the workflow for this project"`
3. Done! ✨

**For EXISTING projects with older workflow:**

1. Copy `UPDATE.md` from this repo to your project root
2. Tell Cursor: `"Read UPDATE.md and update the workflow for this project"`
3. Done! ✨ (Preserves all your existing content)

Cursor will automatically:
- Create all directories
- Generate/update PROJECT_ROADMAP.md
- Create/update session templates
- Set up your first session (new projects only)
- Initialize git if needed
- Pull latest updates from ProjectRoadmapper repo

**No CLI. No installation. No manual copying. Just paste and ask.**

---

### For Existing Projects (CLI Method)

**Step-by-step guide:** See [docs/QUICK_START.md](docs/QUICK_START.md) for detailed instructions.

**Quick version:**

```bash
# 1. Install from source (since we're in active development)
cd /path/to/ProjectRoadmapper
pip install -e .

# 2. Navigate to your existing project
cd /path/to/your/project

# 3. Initialize (non-destructive - won't overwrite existing files)
roadmapper init --no-git  # Use --no-git if you already have Git

# 4. Create your first session
roadmapper session

# 5. Check status
roadmapper status
```

**That's it!** Now tell your AI assistant: *"Read PROJECT_ROADMAP.md and continue the current session."*

### For New Projects

```bash
# Install
pip install -e /path/to/ProjectRoadmapper  # Or wait for: pip install roadmapper

# Initialize your project
roadmapper init

# Start a session
roadmapper session

# Check status
roadmapper status

# Configure preferences
roadmapper config set preferences.editor "code"
roadmapper config set preferences.ai_assistant "cursor"

# View session history
roadmapper history list
roadmapper history stats
```

---

## 📖 How It Works

### The 6-Step Workflow

```
Plan → Consult (optional) → Implement → Document → Sanity Check → Repeat
```

1. **Plan**: Define session goals and success criteria
2. **Consult**: (Optional) Get external validation when needed
3. **Implement**: Write code, run tests, make progress
4. **Document**: Update session notes as you go
5. **Sanity Check**: Verify everything works, commit to git
6. **Repeat**: Archive session, start fresh next time

### Key Files

- `PROJECT_ROADMAP.md` - Living roadmap with phases, status, metrics
- `SESSION_YYYY_MM_DD_X.md` - Active session file (A, B, C...)
- `docs/reference/SESSION_WORKING_TEMPLATE.md` - Template for sessions
- `docs/archive/sessions/` - Completed sessions

### For AI Assistants

AI assistants (like Cursor) are instructed to:
1. Read `PROJECT_ROADMAP.md` at conversation start
2. Check for existing `SESSION_YYYY_MM_DD_X.md`
3. Continue that session or create new one
4. Update documentation as work progresses
5. Maintain context across sessions

**Multi-Agent Support:** The workflow supports single-agent mode by default. For multi-agent scenarios (e.g., Cursor 2.0), use agent-specific session files (`SESSION_YYYY_MM_DD_X_AGENT_NAME.md`) or coordinate via git branches. Full multi-agent support planned for Phase 4.

---

## 🤯 The Meta Moment

**This project was built using its own workflow.**

ProjectRoadmapper started as documentation (ROADMAP_CREATOR.md) in another project (LocalAgent). When it grew beyond documentation into software, we spun it off as its own project and used ROADMAP_CREATOR.md to bootstrap it.

**The tool that teaches workflow is using its own workflow to build itself.**

This is the ultimate validation - dogfooding from day one.

---

## 📊 Roadmap

### ✅ Phase 0: Project Foundation (Complete)
- Bootstrap new project structure
- Capture all vision as actionable items
- Set up GitHub repository
- **Status**: Complete

### ✅ Phase 1: Core Documentation & CLI Foundation (Complete)
- Python CLI tool with `init`, `session`, `status` commands
- Modern packaging with pyproject.toml
- Windows encoding fixes
- **Status**: Complete

### ✅ Phase 2: Persistence & User Preferences (Complete)
- Global and project-level TOML configuration
- `roadmapper config` command (set/get/list/reset)
- Session history tracking and analytics
- `roadmapper history` command (list/stats)
- **Status**: Complete

### ✅ Phase 3: Cross-Project Intelligence (Complete)
**Completed: November 4, 2025**
- ✅ Cross-project search (`roadmapper search`)
- ✅ Project registry system (`roadmapper projects`)
- ✅ Web-based dashboard (`roadmapper dashboard`)
- ✅ Knowledge base extraction (`roadmapper knowledge`)

### 🔵 Phase 4: AI IDE Integration & Ecosystem
**Estimated: 4-6 weeks**
- Cursor/Copilot extensions
- Template marketplace
- Community contributions
- Integration ecosystem

**See [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) for detailed breakdown of all 42+ action items.**

---

## 🎓 Origin Story

**November 4, 2025** - During development of LocalAgent (an AI agent project), we created a structured workflow that proved incredibly effective:
- 10+ sessions in a single day
- Clear progress tracking
- No lost context
- AI assistant maintained continuity perfectly

The workflow documentation (ROADMAP_CREATOR.md) grew to 795 lines and was validated end-to-end during GitHub CLI setup.

Then the question: *"I envision adding functionality... persistent user info... queries between projects?"*

That was the signal: **Documentation → Software**

ProjectRoadmapper was born. 🚀

---

## 🤝 Contributing

This project is in active early development (Phase 0). Contributions, ideas, and feedback are welcome!

- **Issues**: Bug reports, feature requests
- **Discussions**: Ideas, questions, use cases
- **PRs**: Improvements to documentation or (soon) code

See [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) for planned features and priorities.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Repository**: https://github.com/FloppyPete/ProjectRoadmapper
- **Issues**: https://github.com/FloppyPete/ProjectRoadmapper/issues
- **Roadmap**: [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)
- **Quick Start**: [docs/QUICK_START.md](docs/QUICK_START.md) (setup guide for existing projects)
- **Multi-Computer Setup**: [docs/MULTI_COMPUTER_SETUP.md](docs/MULTI_COMPUTER_SETUP.md) (using on multiple computers)
- **Troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **Migration Guide**: [docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) (for upgrading existing projects)
- **What is CLI?**: [docs/WHAT_IS_CLI.md](docs/WHAT_IS_CLI.md) (simple explanation for non-programmers)
- **Origin Project**: [LocalAgent](https://github.com/FloppyPete/LocalAgent)

---

## 📬 Contact

Created by [@FloppyPete](https://github.com/FloppyPete)

**Have questions or want to share how you're using it?** Open a discussion or issue!

---

**Remember**: *"Automate the predictable; document the decisions."*

This tool helps you do both. 🎯

