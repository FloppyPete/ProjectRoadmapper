# 📚 Guidance & Reviews

**Structured LLM reviews and guidance documents**

---

## Purpose

This folder contains structured reviews and guidance documents, typically created for larger LLM analysis. Each review consists of:
- **Request document** - Questions and context for the review
- **Response document** - Template for the review response

---

## Structure

```
docs/guidance/
├── README.md (this file)
├── [review_name]/
│   ├── [review_name]_request.md
│   └── [review_name]_response.md
└── ...
```

---

## Active Reviews

### workflow_review
- **Request:** [workflow_review/workflow_review_request.md](workflow_review/workflow_review_request.md)
- **Response:** [workflow_review/workflow_review_response.md](workflow_review/workflow_review_response.md)
- **Status:** 🔵 Request created, awaiting review
- **Created:** November 4, 2025
- **Topic:** Comprehensive workflow review and improvement suggestions

---

## Creating a New Review

**When creating a new review, create:**
1. Folder: `docs/guidance/[review_name]/`
2. Request file: `[review_name]_request.md`
3. Response template: Copy from `docs/reference/REVIEW_RESPONSE_TEMPLATE.md`

**Or ask AI assistant:** "Create a new LLM review for [topic]"

---

## Review Process

1. **Create Review** - AI assistant creates request and response template
2. **Conduct Review** - Share request with larger LLM or reviewer
3. **Fill Response** - Reviewer fills in response template
4. **Integrate Findings** - Update roadmap and implement improvements
5. **Archive** - Move completed reviews to archive if needed

---

## Best Practices

- **Be specific** - Clear questions get better answers
- **Provide context** - Include relevant background information
- **Structure responses** - Use templates for consistency
- **Prioritize** - Mark recommendations by priority and impact
- **Follow up** - Track implementation of recommendations

---

**See also:** `docs/reference/REVIEW_TEMPLATE.md` for template details

