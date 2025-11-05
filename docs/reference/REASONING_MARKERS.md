# Reasoning Markers Guide

**Purpose:** Standardized markers to help AI assistants understand your reasoning process and enable better context parsing.

---

## Available Markers

### 🧭 DECISION:
**When to use:** When making a design or implementation decision

**Example:**
```
🧭 DECISION: Using YAML frontmatter instead of JSON for better readability and compatibility with markdown parsers
```

**Why it helps:** Allows AI to quickly identify key decisions without parsing entire text. Enables decision tracking and review.

---

### 🤔 HYPOTHESIS:
**When to use:** When proposing a theory, assumption, or prediction

**Example:**
```
🤔 HYPOTHESIS: Metadata extraction will reduce context parsing time by 40% for larger LLMs
```

**Why it helps:** Identifies assumptions that can be verified later. Helps track what was expected vs. what actually happened.

---

### ✅ VERIFIED:
**When to use:** When confirming something works, is correct, or has been tested

**Example:**
```
✅ VERIFIED: Session creation correctly extracts project name "ProjectRoadmapper" from roadmap
```

**Why it helps:** Provides verification status. AI can quickly identify what's been tested and confirmed.

---

### ⚠️ WARNING:
**When to use:** When noting a potential issue, concern, or limitation

**Example:**
```
⚠️ WARNING: This approach may break with custom roadmap formats that don't follow standard structure
```

**Why it helps:** Highlights risks and concerns. Enables proactive issue identification.

---

### 💡 INSIGHT:
**When to use:** When discovering something important or non-obvious

**Example:**
```
💡 INSIGHT: Regex patterns work well for phase extraction, but need fallback for edge cases
```

**Why it helps:** Captures important discoveries. Enables knowledge accumulation and pattern recognition.

---

## Usage Guidelines

**Optional but recommended:**
- Use markers when they add clarity
- Don't overuse - markers should highlight important points
- Use consistently across sessions for better pattern recognition

**Best practices:**
- Put markers at the start of a sentence or paragraph
- Follow with a clear explanation
- Use markers to structure your thinking process

---

## Benefits for AI Assistants

1. **Faster Context Parsing:** AI can scan for markers instead of reading entire text
2. **Better Reasoning Extraction:** Clear markers make it easier to understand thought process
3. **Review Automation:** Markers enable automated extraction of decisions, hypotheses, and insights
4. **Pattern Recognition:** Consistent markers help identify patterns across sessions

---

**Last Updated:** November 4, 2025  
**Related:** See `SESSION_WORKING_TEMPLATE.md` for template with marker examples

