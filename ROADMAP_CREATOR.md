# 🚀 Roadmap Workflow Creator

**Purpose:** Bootstrap a structured, multi-session development workflow for any project.

**Philosophy:** *"Automate the predictable; document the decisions."* Structure via templates, record architectural choices manually.

**When to use:** Complex projects requiring multiple sessions, clear progress tracking, and maintainable documentation.

---

## 📖 What This Workflow Provides

### For You (The Developer)
- **Session continuity:** Never lose context between work sessions
- **Clear progress tracking:** Know exactly where you are and what's next
- **Decision documentation:** Capture why choices were made, not just what was done
- **Living roadmap:** Single source of truth that evolves with the project

### For AI Assistants (Like Cursor)
- **Consistent onboarding:** AI reads roadmap and session file every time
- **Structured communication:** Clear templates and expectations
- **Progress awareness:** Understands project state, recent work, and next steps
- **Guided autonomy:** Knows when to ask vs. proceed independently

---

## 🎯 Core Workflow (6 Steps)

```
Plan → Consult (optional) → Implement → Document → Sanity Check → Repeat
```

### The Cycle
1. **Plan:** Define session goals and success criteria
2. **Consult:** (Optional) Get external validation or review when needed
3. **Implement:** Write code, run tests, make progress
4. **Document:** Update session notes and roadmap as you go
5. **Sanity Check:** Verify everything works, commit to git
6. **Repeat:** Archive session, start fresh next time

---

## 📂 Required File Structure

Create this structure in your project root:

```
your-project/
├── PROJECT_ROADMAP.md           # Living roadmap (see template below)
├── SESSION_YYYY_MM_DD_X.md      # Active session file (created as needed)
├── docs/
│   ├── WORKFLOW_GUIDE.md        # Detailed methodology (optional but recommended)
│   ├── reference/
│   │   └── SESSION_WORKING_TEMPLATE.md  # Template for session files
│   └── archive/
│       ├── sessions/            # Archived session files
│       └── COMPLETED_PHASES.md  # Historical record (optional)
└── .gitignore                   # Ensure SESSION files tracked, not ignored
```

---

## 🤖 AI Assistant Instructions

**Copy this section into your PROJECT_ROADMAP.md:**

```markdown
## 🤖 AI Assistant Workflow

**Every conversation start:**
1. ✅ **Check for ProjectRoadmapper updates** (optional but recommended):
   - If ProjectRoadmapper repo exists (e.g., `../ProjectRoadmapper` or configured path): Run `git pull` to get latest templates
   - This keeps workflow templates synchronized across all projects
2. ✅ Read this file (PROJECT_ROADMAP.md) - Current Status section
3. ✅ Check for `SESSION_YYYY_MM_DD_X.md` in root
4. ✅ If exists: Read it, continue that session
5. ✅ If not: **Automatically create new session** (increment letter: A→B→C or new date)

**Starting a new session (when user says "new session" or "start new session"):**
- **Automatically archive** any existing `SESSION_*.md` file to `docs/archive/sessions/`
- **Automatically create** new `SESSION_YYYY_MM_DD_X.md` file from template
- **Automatically update** PROJECT_ROADMAP.md with brief summary of archived session
- User should NEVER manually archive or copy templates - you do this automatically

**During session:**
- Use SESSION file as scratchpad freely
- Git commit after each logical unit
- Ask before deleting/major changes
- Update working doc with progress
- **When user asks for LLM review:**
  - Create `docs/guidance/[review_name]/` folder automatically
  - Create `[review_name]_request.md` with review questions
  - Create `[review_name]_response.md` from `docs/reference/REVIEW_RESPONSE_TEMPLATE.md`
  - Update `docs/guidance/README.md` with new review entry
  - User should NEVER manually create review structure - you do this automatically

**Session end (when user says "end session" or "archive session"):**
- Update this roadmap briefly with session summary
- **Quick documentation check** (2-3 min):
  - Verify PROJECT_ROADMAP.md status is current
  - Check README.md features list matches current state (if phase completed)
  - Fix any obvious inconsistencies
- **Automatically archive** SESSION file to docs/archive/sessions/
- **Automatically create** new session file if user wants to continue
- Ensure git clean

**Key principle:** Always in a session. Always grounded in roadmap. Commit frequently.

**Template:** `docs/reference/SESSION_WORKING_TEMPLATE.md`
```

---

## 📝 Template: PROJECT_ROADMAP.md

Create `PROJECT_ROADMAP.md` in your project root:

```markdown
# 📖 Quick Start

**Living Roadmap** for [Your Project Name]

**6-Step Workflow**: Plan → Consult (optional) → Implement → Document → Sanity Check → Repeat

**Philosophy**: *"Automate the predictable; document the decisions."*

---

## 🤖 AI Assistant Workflow

[Copy the AI Assistant Instructions section from above]

---

# [Your Project Name]

**Goal**: [Brief description of what this project does/achieves]

**Approach**: [Your development philosophy or methodology]

**Last Updated**: [Date] (Status: [In Progress / Production-Ready / etc.])

---

## 📊 Current Status

**Project Health:** [✅ Healthy / ⚠️ Issues / 🔧 In Development]

**Phase Progress:**
- ✅ Phase 1: [Completed phase]
- 🟢 Phase 2: [Current phase in progress]
- 🔵 Phase 3: [Planned phase]

**Key Metrics:**
- [Relevant metric 1]
- [Relevant metric 2]
- [Test coverage, performance, etc.]

**Recent Work:** [Brief summary of last session]

---

## 📋 Quick Navigation

- [Current Status](#-current-status)
- [Phase Details](#-phase-1-name)
- [Quick Reference](#-quick-reference)
- [Recent Sessions](#-recent-sessions)

---

## 🔵 Phase 1: [Phase Name]

**Priority:** ⭐⭐⭐ HIGH / ⭐⭐ MEDIUM / ⭐ LOW  
**Estimated:** [Time estimate]

**Goals:**
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

**Success Criteria:**
- Define what "done" looks like for this phase
- Include measurable outcomes

---

## 🎯 Quick Reference

### Key Files
- [List important files and their purposes]

### Running the Project
```bash
# Commands to run, test, or deploy
```

### Configuration
```bash
# Environment variables or config settings
```

---

## 💡 Key Insights

**Lessons Learned:**
- [Document important discoveries]
- [Record what worked and what didn't]

**Trade-offs:**
- [Document technical decisions and their reasoning]

---

## 💡 Recent Sessions

**[Date Range]:**
- Session A: [Brief summary]
- Session B: [Brief summary]

**Archives:**
- Session notes: [docs/archive/sessions/](docs/archive/sessions/)
```

---

## 📝 Template: SESSION_WORKING_TEMPLATE.md

Create `docs/reference/SESSION_WORKING_TEMPLATE.md`:

```markdown
# Session YYYY-MM-DD-X: [Session Title]

**Date:** [Month Day, Year]  
**Phase:** [Current Phase Number/Name]  
**Focus:** [Brief description of session goals]

---

## 📊 Project Context (Brief Roadmap Synopsis)

**From PROJECT_ROADMAP.md:**

**Current Phase:**
- [Copy current phase from roadmap]

**Recent Completions:**
- [1-2 key recent achievements]

**System Status:**
- [Brief health check - tests passing? builds working?]

---

## 🎯 Session Goals

**Primary objectives:**
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

**Success criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

## 🔧 Work Log

### [Task/Investigation Name]

**[Document your work here freely]**

Use this space as scratchpad:
- Findings and discoveries
- Code snippets and analysis
- Decisions and rationale
- Questions and answers
- Progress tracking

**Git commits:**
- `<hash>` - [Brief description]

---

## ✅ Session Accomplishments

**Completed:**
- [List what got done]

**Deferred:**
- [What was postponed and why]

**Discoveries:**
- [Important findings or insights]

---

## 📝 Before Archiving This Session

**Checklist:**
- [ ] Update PROJECT_ROADMAP.md with session summary
- [ ] All git commits made (git status clean)
- [ ] Valuable insights added to roadmap if applicable
- [ ] Archive this file to docs/archive/sessions/
- [ ] Create new SESSION_YYYY_MM_DD_X.md for next session (if continuing)

---

**Remember:** This is YOUR working document. Use it however helps you work best. Document freely, commit frequently, stay grounded in the roadmap.
```

---

## 🛠️ Setup Instructions for New Projects

### Option 1: Bootstrap with AI Assistant (Recommended)

1. Copy this file (`ROADMAP_CREATOR.md`) to your project root
2. Open your AI assistant (Cursor, etc.)
3. Say: **"Read ROADMAP_CREATOR.md and set up the workflow for this project"**
4. The AI will:
   - Create directory structure (`docs/reference/`, `docs/archive/sessions/`)
   - Generate PROJECT_ROADMAP.md from template
   - Create SESSION_WORKING_TEMPLATE.md
   - **Create first session file (SESSION_YYYY_MM_DD_A.md)**
   - **Begin Session 0 workflow** (see below)
   - Add to .gitignore if needed

**Session 0: Project Foundation**

The first session is special - it helps establish the project foundation:
- **Determine project type:** New project or existing codebase?
- **Establish goals:** What is this project trying to achieve?
- **Define phases:** What are the major milestones?
- **Identify metrics:** How will success be measured?
- **Set up quick reference:** Commands, config, key files

The AI assistant will guide you through these questions to create a solid roadmap.

### Option 2: Manual Setup

```bash
# 1. Create directory structure
mkdir -p docs/reference docs/archive/sessions

# 2. Copy templates to create initial files
# - Create PROJECT_ROADMAP.md from template above
# - Create docs/reference/SESSION_WORKING_TEMPLATE.md
# - Create SESSION_YYYY_MM_DD_A.md for first session

# 3. Customize PROJECT_ROADMAP.md for your project
# - Update project name and goal
# - Define your phases
# - Add relevant quick reference info

# 4. Update .gitignore if needed
# Make sure SESSION_*.md files are tracked (not ignored)

# 5. Optional: Set up GitHub repository (see GitHub Setup section below)
```

### Option 3: Clone from Reference Project

If you have access to the DeepAgent project (where this workflow originated):

```bash
# Copy workflow files to your new project
cp /path/to/deepagent/PROJECT_ROADMAP.md ./
cp -r /path/to/deepagent/docs/reference ./docs/
cp /path/to/deepagent/docs/WORKFLOW_GUIDE.md ./docs/

# Customize for your project
# Edit PROJECT_ROADMAP.md to match your project
```

---

## 🔧 GitHub Setup (Optional but Recommended)

### Why GitHub CLI?

GitHub CLI (`gh`) enables:
- **Automatic repository creation** - No manual browser steps
- **Seamless authentication** - Secure, token-based access
- **Better AI workflow** - AI can create repos during bootstrap
- **Future automation** - Issues, PRs, releases from command line

### TL;DR - Quick Start

**For Cursor users (validated Nov 4, 2025):**
1. Open **separate PowerShell** window (not Cursor terminal)
2. Run: `winget install --id GitHub.cli`
3. Run: `gh auth login` (follow prompts, use web browser option)
4. Return to Cursor - now `gh repo create` commands work!

**Why separate terminal?** Interactive prompts crash Cursor. Authentication is one-time - after that, all `gh` commands work in Cursor.

### Setup Instructions

**⚠️ Important for Cursor/AI IDE Users:**

Interactive commands (like `winget install` with Terms & Conditions prompts or `gh auth login`) **do not work reliably in Cursor's integrated terminal**. These commands may cause crashes or hang indefinitely.

**Solution:** Run interactive commands in a **separate terminal window**:
- Windows: Open regular PowerShell (Win+X → Windows PowerShell)
- Mac/Linux: Open Terminal app
- Once authenticated, `gh` commands work from anywhere (including Cursor terminal)

---

**For AI Assistants:** When bootstrapping a project, offer to set up GitHub integration:

1. **Check if GitHub CLI is installed:**

```bash
# Windows (PowerShell)
gh --version

# Mac/Linux
gh --version
```

If not installed, **guide user to run installation in separate terminal window** (not Cursor terminal):

**Windows:**
```powershell
# Option 1: Using winget (Windows 10+)
winget install --id GitHub.cli

# Option 2: Using Chocolatey
choco install gh

# Option 3: Using Scoop
scoop install gh

# Option 4: Download installer
# Visit: https://github.com/cli/cli/releases/latest
```

**Mac:**
```bash
# Using Homebrew
brew install gh
```

**Linux:**
```bash
# Debian/Ubuntu
sudo apt install gh

# Fedora/CentOS
sudo dnf install gh

# Arch
sudo pacman -S github-cli
```

2. **Authenticate with GitHub:**

**⚠️ Run this in a separate terminal window (not Cursor terminal):**

```bash
gh auth login
# Follow the prompts:
# - Choose GitHub.com
# - Choose HTTPS or SSH  
# - Choose "Login with a web browser"
# - Press Enter to confirm selection
# - Copy the one-time code displayed
# - Open github.com/login/device (or let it open automatically)
# - Paste the code and authorize
# - See "✓ Authentication complete" message
```

**Note:** After authentication completes in the separate terminal, `gh` commands will work in Cursor terminal too.

3. **Create repository automatically:**

```bash
# Create public repo
gh repo create project-name --public --source=. --push

# Create private repo
gh repo create project-name --private --source=. --push

# With description
gh repo create project-name --public --description "Project description" --source=. --push
```

4. **Verify setup:**

```bash
# Check repository was created
gh repo view

# Check remotes
git remote -v
```

### Manual GitHub Setup (Without CLI)

If user prefers manual setup or CLI isn't available:

1. **Create repository on GitHub:**
   - Visit https://github.com/new
   - Enter repository name
   - Choose public or private
   - **Do NOT initialize with README** (if you have existing files)
   - Click "Create repository"

2. **Add remote and push:**

```bash
# Add GitHub as remote
git remote add origin https://github.com/username/repo-name.git

# Push initial commit
git branch -M main
git push -u origin main
```

### AI Assistant Workflow for GitHub Setup

When bootstrapping a new project, ask user:

```
Would you like to set up GitHub integration for this project?
Options:
1. Yes - Use GitHub CLI (automatic) [Recommended]
2. Yes - Manual setup (I'll create it on github.com)
3. No - Local only for now
```

**If option 1 (Automatic):**
- Check if `gh` is installed
- If not, **instruct user to run installation in separate terminal window** (interactive prompts don't work in Cursor)
- Check if authenticated: `gh auth status`
- If not, **instruct user to run `gh auth login` in separate terminal window** (interactive prompts don't work in Cursor)
- Ask for repo name and visibility (public/private)
- Create repo: `gh repo create [name] --[visibility] --source=. --push` (this command works in Cursor terminal)

**If option 2 (Manual):**
- Guide user to https://github.com/new
- Wait for confirmation repo is created
- Ask for repo URL
- Add remote and push

**If option 3 (Local only):**
- Skip GitHub setup
- Initialize local git only: `git init`
- User can add GitHub later

---

## 🎨 Customization Guide

### For Different Project Types

**Web Applications:**
- Add deployment status to Quick Reference
- Include environment/staging URLs
- Track database migrations in phases

**Libraries/Packages:**
- Track API stability and versioning
- Document breaking changes in sessions
- Include usage examples in Quick Reference

**Data Science/ML:**
- Track model performance metrics in Current Status
- Document experiment results in sessions
- Include hyperparameters in Quick Reference

**Research Projects:**
- Track hypothesis testing in phases
- Document experiment protocols in sessions
- Include references/citations in roadmap

### Adapting Phase Structure

**Phases can represent:**
- Feature development stages
- Architectural milestones
- Research questions/hypotheses
- Integration steps
- Optimization cycles

**Choose what makes sense for your project!**

---

## ✨ Best Practices

### Do's ✅
- **Read roadmap at start of every session** - Keeps context fresh
- **Commit frequently** - Small, logical units
- **Update session file as you go** - Don't wait until the end
- **Archive completed sessions** - Keeps root clean
- **Document decisions, not just actions** - Future you will thank you
- **Use session file as scratchpad** - It's for thinking, not just reporting

### Don'ts ❌
- **Don't let roadmap get stale** - Update it when status changes
- **Don't skip session files** - Even quick sessions benefit from structure
- **Don't over-engineer** - Start simple, add complexity as needed
- **Don't treat it as bureaucracy** - It should help, not hinder
- **Don't neglect git commits** - Frequent commits = safety net

---

## 📚 Philosophy & Principles

### Why This Works

1. **Cognitive offload:** Roadmap holds context so you don't have to
2. **AI collaboration:** AI can maintain context across sessions
3. **Decision preservation:** Capture the "why" before you forget
4. **Async communication:** Leave notes for future self or teammates
5. **Proof of progress:** Visible accomplishments combat impostor syndrome

### Core Principles

- **Living documents:** Roadmap and sessions evolve with the project
- **Lightweight structure:** Just enough process, not too much
- **Human-readable:** Markdown is universal and version-controllable
- **AI-friendly:** Clear templates help AI assistants be more effective
- **Git-integrated:** Everything tracked, everything recoverable

---

## 🔗 Reference: Original Implementation

This workflow was developed during the DeepAgent → Local Agent migration project:
- 10+ sessions in a single day
- Complex multi-phase technical migration
- High collaboration with AI assistants
- Resulted in production-ready system

**Key success factors:**
- Clear phase structure with priorities
- Session files as working scratchpad
- Frequent git commits
- Regular roadmap updates
- AI assistant following consistent workflow

---

## 💡 Tips for AI Assistants

When a user asks you to set up this workflow:

1. **Read this document fully** - Understand the structure
2. **Create directory structure** - Use mkdir for folders
3. **Check/setup git** - Ensure project has git initialized
4. **Setup GitHub (optional)** - Ask user if they want GitHub integration:
   - Check for GitHub CLI: `gh --version`
   - If not installed, **instruct user to install in separate terminal** (interactive prompts crash Cursor)
   - If installed, check auth: `gh auth status`
   - If not authenticated, **instruct user to run `gh auth login` in separate terminal** (interactive prompts crash Cursor)
   - Once authenticated, offer to create repo automatically with `gh repo create` (this works in Cursor)
   - Or guide through manual setup
5. **Generate PROJECT_ROADMAP.md** - Use template, customize for project
6. **Generate SESSION_WORKING_TEMPLATE.md** - Copy template exactly
7. **Create first session file** - Use today's date: SESSION_YYYY_MM_DD_A.md
8. **Begin Session 0 (Project Foundation)** - Guide user through:
   - Is this a new project or existing codebase?
   - What is the project goal/purpose?
   - What are the major phases or milestones?
   - What metrics matter (tests, performance, etc.)?
   - What commands/config are important?
9. **Populate PROJECT_ROADMAP.md** - Use answers to fill in template
10. **Initial commit** - Commit workflow files to git
11. **Confirm setup complete** - List files created and next steps

**Session 0 Template:**

```markdown
# Session YYYY-MM-DD-A: Project Foundation

**Date:** [Today's date]
**Phase:** Phase 0 (Workflow Bootstrap)
**Focus:** Establish project goals, structure, and roadmap

---

## 🎯 Session Goals

**Primary objectives:**
1. Determine project type (new vs existing)
2. Establish project goals and scope
3. Define phases and milestones
4. Set up PROJECT_ROADMAP.md with initial structure
5. Identify key files, commands, and configuration

**Discovery questions:**
- [ ] Is this a new project or existing codebase?
- [ ] What is the main goal/purpose of this project?
- [ ] What are 3-5 major phases or milestones?
- [ ] What metrics matter (test coverage, performance, etc.)?
- [ ] What are the key commands to run/test/build?
- [ ] What configuration or environment setup is needed?

---

## 🔧 Work Log

### Project Discovery

**Project type:** [New / Existing]

**Project goal:** [User's description]

**Major phases identified:**
1. Phase 1: [Name and brief description]
2. Phase 2: [Name and brief description]
3. Phase 3: [Name and brief description]

**Key metrics to track:**
- [Metric 1]
- [Metric 2]

**Quick reference info:**
- Commands: [List key commands]
- Config: [Important settings or env vars]
- Key files: [Essential files and their purposes]

---

## ✅ Session Accomplishments

**Completed:**
- ✅ Workflow structure created
- ✅ PROJECT_ROADMAP.md initialized
- ✅ Project goals and phases defined
- ✅ First session documented

**Next steps:**
- Begin Phase 1 work in next session
- Refine roadmap as project evolves
```

**Remember:** The workflow should feel helpful, not bureaucratic. Start simple and let it evolve. Session 0 is about discovery and foundation-setting.

---

## 📞 Questions?

**Common Questions:**

**Q: How often should I update the roadmap?**  
A: Update Current Status section after each session. Update phases when major progress happens or priorities shift.

**Q: What if I'm working solo, not with an AI?**  
A: Still useful! Session files help you resume context. Roadmap keeps you focused on priorities.

**Q: Can I modify the templates?**  
A: Absolutely! These are starting points. Adapt to your needs.

**Q: What is Session 0 (Project Foundation)?**  
A: The first session created during workflow bootstrap. It's a guided discovery process where the AI asks about project type, goals, phases, and metrics to properly set up your PROJECT_ROADMAP.md. Think of it as the foundation-laying session.

**Q: What about existing projects?**  
A: Perfect! Session 0 will ask "Is this new or existing?" and guide you through documenting current state, defining phases for remaining work, and establishing the roadmap structure.

**Q: Do I need all the optional files?**  
A: No! Minimum: PROJECT_ROADMAP.md and SESSION template. Add WORKFLOW_GUIDE.md and archives as project grows.

**Q: Do I need GitHub CLI or can I use manual GitHub setup?**  
A: Either works! GitHub CLI (`gh`) enables automatic repo creation and is recommended for best experience, but manual setup via github.com works perfectly fine. You can also skip GitHub entirely and use local git only.

**Q: Can I add GitHub later if I skip it during initial setup?**  
A: Absolutely! Just follow the GitHub Setup section whenever you're ready. The workflow works great with local git only.

**Q: Why doesn't `gh auth login` work in Cursor's terminal?**  
A: Cursor's integrated terminal has issues with interactive prompts that require user input (like accepting Terms & Conditions or entering authentication codes). This is a known Cursor limitation. **Solution:** Run interactive commands (`winget install`, `gh auth login`) in a separate PowerShell/Terminal window. Once authenticated, all `gh` commands work fine in Cursor's terminal.

---

## 🎯 Next Steps

### For New Project Setup:
1. ✅ Copy ROADMAP_CREATOR.md to your project root
2. ✅ Tell AI: "Read ROADMAP_CREATOR.md and set up the workflow"
3. ✅ AI creates structure and starts Session 0 (Project Foundation)
4. ✅ Answer discovery questions (project type, goals, phases)
5. ✅ AI populates PROJECT_ROADMAP.md with your answers
6. ✅ Session 0 complete - ready for Phase 1 work!

### For AI Assistants Bootstrapping Workflow:
1. ✅ Read ROADMAP_CREATOR.md fully
2. ✅ Create directory structure
3. ✅ Check git status and initialize if needed
4. ✅ **Ask about GitHub setup** (CLI automatic vs manual vs skip)
5. ✅ Generate PROJECT_ROADMAP.md and SESSION_WORKING_TEMPLATE.md
6. ✅ Create SESSION_YYYY_MM_DD_A.md (Session 0: Project Foundation)
7. ✅ Guide user through discovery questions
8. ✅ Populate roadmap with answers
9. ✅ Make initial commit
10. ✅ Push to GitHub (if setup in step 4)
11. ✅ Confirm setup complete

### For AI Assistants Starting Regular Sessions:
1. ✅ Read PROJECT_ROADMAP.md
2. ✅ Check for existing SESSION_YYYY_MM_DD_X.md
3. ✅ Create new session if none exists (increment letter or date)
4. ✅ Reference session template
5. ✅ Begin working with context

---

**Ready to implement this workflow in your project? Tell your AI assistant: "Read ROADMAP_CREATOR.md and set up the workflow" and watch the magic happen! ✨**

