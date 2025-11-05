# File Organization Guide

**Purpose:** Guidelines for keeping project files organized, manageable, and focused.

---

## 📏 File Length Guidelines

### Session Files (`SESSION_*.md`)
**Target:** 150-250 lines maximum  
**Rationale:** Session files are working documents/scatchpads. When they grow too large, they become hard to navigate and review.

**What belongs in sessions:**
- Current work log and progress
- Discoveries and insights
- Discussion notes
- Quick reference to related files
- Session accomplishments summary

**What should be extracted:**
- Detailed action plans (>100 lines) → Move to dedicated action plan files
- Long implementation specs → Move to planning documents
- Comprehensive documentation → Move to `docs/` directory
- Code examples/designs → Move to appropriate technical docs

**Example:** If creating a detailed Phase 4 action plan, extract it to `PHASE_4_ACTION_PLAN.md` and reference it from the session.

---

### Roadmap Files (`PROJECT_ROADMAP.md`)
**Target:** 400-600 lines for overview, details in separate files  
**Rationale:** Roadmap should provide high-level overview and status. Detailed implementation plans belong elsewhere.

**What belongs in roadmap:**
- Current status and health
- Phase overviews (what, why, priority, timeline)
- Quick navigation and reference
- Recent session summaries
- Links to detailed plans

**What should be extracted:**
- Detailed implementation steps → Move to action plan files
- Comprehensive feature specs → Move to planning documents
- Long priority matrices → Move to action plan files
- Week-by-week breakdowns → Move to action plan files

**Example:** Phase 4 has 8 sub-phases with detailed specs. Roadmap shows overview and links to `PHASE_4_ACTION_PLAN.md` for details.

---

### Action Plan Files (`*_ACTION_PLAN.md`)
**Target:** No strict limit, but keep focused  
**Rationale:** Action plans can be comprehensive but should stay focused on their phase/feature.

**What belongs in action plans:**
- Detailed implementation steps
- Priority matrices
- Week-by-week breakdowns
- Technical specifications
- Dependencies and prerequisites

**What might be extracted:**
- Very large action plans (>500 lines) → Consider splitting by sub-phase
- Cross-cutting concerns → Move to shared planning docs

---

## 📁 File Organization Structure

```
ProjectRoot/
├── SESSION_*.md              # Working documents (150-250 lines)
├── PROJECT_ROADMAP.md         # High-level overview (400-600 lines)
├── PHASE_*_ACTION_PLAN.md     # Detailed implementation plans
├── BOOTSTRAP.md              # Setup instructions
├── UPDATE.md                  # Update instructions
├── README.md                  # Project documentation
│
└── docs/
    ├── reference/             # Reference materials
    │   ├── SESSION_WORKING_TEMPLATE.md
    │   ├── FILE_ORGANIZATION_GUIDE.md (this file)
    │   └── ...
    ├── guidance/              # LLM reviews and guidance
    ├── archive/              # Archived sessions and docs
    └── ...
```

---

## 🔄 When to Extract Content

**Extract from session when:**
- Session file exceeds 250 lines
- Action plan or spec exceeds 100 lines
- Content will be referenced across multiple sessions
- Content is a complete planning document

**Extract from roadmap when:**
- Phase description exceeds 50-100 lines per sub-phase
- Detailed implementation steps included
- Priority matrices or detailed breakdowns
- Content would be better as standalone planning doc

**Extract from action plan when:**
- Action plan exceeds 500 lines
- Multiple independent sub-phases can be split
- Cross-cutting concerns that affect multiple phases

---

## ✅ Best Practices

1. **Keep files focused:** Each file should have a clear, single purpose
2. **Link, don't duplicate:** Reference other files rather than copying content
3. **Regular cleanup:** When files grow, extract content proactively
4. **Session-per-feature:** Major features/sub-phases get their own sessions
5. **Progressive detail:** Roadmap → Action Plan → Implementation → Session Log

---

## 📝 Example Workflow

**Before extraction:**
- `SESSION_2025_11_04_H.md`: 450 lines (includes full Phase 4 action plan)
- `PROJECT_ROADMAP.md`: 716 lines (includes detailed Phase 4 specs)

**After extraction:**
- `SESSION_2025_11_04_H.md`: ~250 lines (working document with references)
- `PROJECT_ROADMAP.md`: ~350 lines (overview with links)
- `PHASE_4_ACTION_PLAN.md`: ~400 lines (dedicated action plan)

**Result:** Each file is focused, manageable, and easy to navigate.

---

**Last Updated:** November 4, 2025  
**Related:** See `PROJECT_ROADMAP.md` for project structure overview

