# 📚 Document Cleanup Guide

**Purpose:** Maintain documentation consistency, accuracy, and clarity across the project.

**When to use:** 
- End of each session (quick check)
- End of each phase (comprehensive review)
- Before major releases
- When inconsistencies are noticed

---

## 🔄 Cleanup Workflow Integration

### As Part of Session End

**After completing work, before archiving session:**

1. ✅ **Quick Documentation Check** (2-3 minutes):
   - Update PROJECT_ROADMAP.md status if phase changed
   - Verify README.md features list matches current state
   - Check that session accomplishments are documented

2. ✅ **Archive Session File**
   - Move to `docs/archive/sessions/`
   - Update roadmap with session summary

3. ✅ **Commit Changes**
   - Commit with descriptive message
   - Push to remote

### As Part of Phase Completion

**When completing a phase:**

1. ✅ **Comprehensive Documentation Review** (15-20 minutes):
   - Review all docs for consistency
   - Update version numbers, status, features
   - Check cross-references between docs
   - Verify examples still work
   - Update README.md feature list
   - Update PROJECT_ROADMAP.md status

2. ✅ **Archive Phase Sessions**
   - Ensure all sessions archived
   - Update roadmap phase status

3. ✅ **Update Distribution Files**
   - Update BOOTSTRAP.md templates if needed
   - Update UPDATE.md templates if needed
   - Update ROADMAP_CREATOR.md if workflow changed

---

## ✅ Cleanup Checklist

### Status & Consistency

- [ ] PROJECT_ROADMAP.md status matches actual project state
- [ ] README.md features list is current
- [ ] README.md roadmap section matches PROJECT_ROADMAP.md
- [ ] All phase completion statuses are accurate
- [ ] Last updated dates are reasonable

### Cross-References

- [ ] Links between docs work correctly
- [ ] References to other docs are accurate
- [ ] File paths mentioned are correct
- [ ] Command examples match current CLI

### Content Accuracy

- [ ] Code examples are current
- [ ] Command syntax is correct
- [ ] File structures match actual project
- [ ] Feature descriptions match implementation
- [ ] Installation instructions work

### Structure & Organization

- [ ] Root directory has only active session
- [ ] Completed sessions are archived
- [ ] Build artifacts are gitignored
- [ ] Documentation files are in correct locations
- [ ] Directory structure matches documentation

### Templates & Distribution Files

- [ ] BOOTSTRAP.md templates are current
- [ ] UPDATE.md templates are current
- [ ] ROADMAP_CREATOR.md workflow matches PROJECT_ROADMAP.md
- [ ] SESSION_WORKING_TEMPLATE.md is up to date

---

## 🎯 Specific Areas to Check

### README.md
- [ ] Features list shows current phases
- [ ] Roadmap section matches PROJECT_ROADMAP.md
- [ ] Quick start instructions work
- [ ] Installation commands are correct
- [ ] Links to other docs work

### PROJECT_ROADMAP.md
- [ ] Current Status section is accurate
- [ ] Phase completion statuses are correct
- [ ] Recent Sessions list is up to date
- [ ] Key Metrics are current
- [ ] Last Updated date is recent

### Documentation Files (docs/)
- [ ] TROUBLESHOOTING.md has latest errors
- [ ] MIGRATION_GUIDE.md reflects current state
- [ ] QUICK_START.md matches README.md
- [ ] Reference docs match code

### Distribution Files
- [ ] BOOTSTRAP.md has latest workflow
- [ ] UPDATE.md has latest workflow
- [ ] ROADMAP_CREATOR.md is consistent

---

## 🔍 Common Issues to Fix

### Outdated Status
**Problem:** README says "Phase 1 & 2" but Phase 3 is complete  
**Fix:** Update to "Phase 1, 2 & 3" or current phase

### Inconsistent Phase Status
**Problem:** PROJECT_ROADMAP.md says Phase 3 complete, README says Phase 3 next  
**Fix:** Make both match actual state

### Missing Updates
**Problem:** New features implemented but not in README  
**Fix:** Add features to README features list

### Broken Links
**Problem:** Docs reference files that moved  
**Fix:** Update paths or create redirects

### Stale Examples
**Problem:** Code examples don't match current API  
**Fix:** Update examples to match current code

---

## 📝 Cleanup Log Template

```markdown
## Document Cleanup - [Date]

**Trigger:** [Session end / Phase completion / Release prep]

**Issues Found:**
- [List any inconsistencies or problems]

**Fixes Applied:**
- [List what was fixed]

**Files Updated:**
- [List files changed]

**Time Spent:** [Duration]
```

---

## 🎯 Integration with Workflow

**Add to AI Assistant Workflow:**

```markdown
**Session end (when user says "end session" or "archive session"):**
- Update this roadmap briefly with session summary
- **Quick documentation check** (2-3 min):
  - Verify PROJECT_ROADMAP.md status is current
  - Check README.md features list matches current state
  - Fix any obvious inconsistencies
- **Automatically archive** SESSION file to docs/archive/sessions/
- **Automatically create** new session file if user wants to continue
- Ensure git clean
```

**Add to Phase Completion:**

```markdown
**Phase completion:**
- Update PROJECT_ROADMAP.md phase status
- **Comprehensive documentation review** (15-20 min):
  - Review all docs for consistency
  - Update README.md features
  - Check cross-references
  - Verify examples
- Update distribution files if workflow changed
- Commit phase completion
```

---

## 💡 Best Practices

1. **Little and often** - Quick checks at session end prevent big cleanup tasks
2. **Be systematic** - Use checklist to ensure nothing missed
3. **Document changes** - Keep cleanup log to track what was fixed
4. **Test after cleanup** - Verify links and examples still work
5. **Commit cleanup separately** - Makes history cleaner

---

**Remember:** Documentation is part of the product. Keep it accurate, current, and helpful!

