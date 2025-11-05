# LLM Review Template

**Purpose:** Template for creating structured LLM reviews

**Location:** `docs/guidance/[review_name]/`

---

## Review Structure

Each review should have two files:

1. **`[review_name]_request.md`** - The review request document
2. **`[review_name]_response.md`** - Blank template for the response

---

## Creating a New Review

### Manual Process

1. Create folder: `docs/guidance/[review_name]/`
2. Create request file: `[review_name]_request.md`
3. Copy response template: `docs/reference/REVIEW_TEMPLATE.md` → `[review_name]_response.md`
4. Customize response template with review-specific sections

### Automated Process (Current)

**When user asks for an LLM review:**

**AI Assistant should automatically:**
1. ✅ Create folder: `docs/guidance/[review_name]/`
2. ✅ Create request file: `[review_name]_request.md` (with review questions)
3. ✅ Create response file: `[review_name]_response.md` (from template)
   - Copy from `docs/reference/REVIEW_RESPONSE_TEMPLATE.md`
   - Update placeholders: `[review_name]`, `[review_topic]`
4. ✅ Update `docs/guidance/README.md` with new review entry
5. ✅ Inform user: "Review structure created. Request document ready for LLM review."

**Example:**
User: "Create an LLM review for the workflow"
AI: Creates `docs/guidance/workflow_review/` with both files automatically

---

## Review Naming Convention

**Format:** `[topic]_review`

**Examples:**
- `workflow_review`
- `architecture_review`
- `documentation_review`
- `ui_ux_review`

---

## Response Template Structure

See `docs/reference/REVIEW_RESPONSE_TEMPLATE.md` for the full template.

**Key sections:**
- Executive Summary
- Strengths
- Areas for Improvement (categorized)
- Specific Recommendations (prioritized)
- LLM-Specific Improvements
- Implementation Suggestions
- Priority Matrix
- Recommended Next Steps

---

## Usage

**For AI Assistants:**
When user asks for a review:
1. Create `docs/guidance/[review_name]/` folder
2. Create request document with review questions
3. Create blank response template
4. Inform user: "Review structure created. Review request is ready for LLM review."

**For Reviewers:**
1. Read the request document
2. Fill in the response template
3. Commit both files to git
4. Update roadmap with findings

---

## Index of Reviews

Keep a list of all reviews in `docs/guidance/README.md` or similar.

