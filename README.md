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

### Current (Phase 1 & 2)
- ✅ **ROADMAP_CREATOR.md** - Complete bootstrap guide (795 lines, battle-tested)
- ✅ **CLI Tool** - `roadmapper init`, `roadmapper session`, `roadmapper status`
- ✅ **Configuration** - Global and project-level TOML config with `roadmapper config`
- ✅ **Session History** - Track sessions with `roadmapper history`
- ✅ **Analytics** - View session statistics and activity trends

### Planned (See [Roadmap](#roadmap))
- 🔜 **Cross-Project Intelligence** - Search across all your projects
- 🔜 **Dashboard** - Visual overview of all projects
- 🔜 **AI IDE Integrations** - Native Cursor/Copilot extensions

---

## 🚀 Quick Start

### Option 1: Use the Bootstrap Guide (Current)

1. Copy `ROADMAP_CREATOR.md` to your project root
2. Tell your AI assistant (Cursor, etc.):
   ```
   Read ROADMAP_CREATOR.md and set up the workflow for this project
   ```
3. Answer the Session 0 discovery questions
4. Start working with full context preservation!

### Option 2: CLI Tool (Available Now!)

```bash
# Install
pip install roadmapper

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

### 🔵 Phase 3: Cross-Project Intelligence (Next)
**Estimated: 3-4 weeks**
- Cross-project search
- Web-based dashboard
- Knowledge base extraction

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
- **Troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **Origin Project**: [LocalAgent](https://github.com/FloppyPete/LocalAgent)

---

## 📬 Contact

Created by [@FloppyPete](https://github.com/FloppyPete)

**Have questions or want to share how you're using it?** Open a discussion or issue!

---

**Remember**: *"Automate the predictable; document the decisions."*

This tool helps you do both. 🎯

