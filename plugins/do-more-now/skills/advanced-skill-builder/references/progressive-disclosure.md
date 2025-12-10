# Progressive Disclosure Patterns

Skills use a three-level loading system. Only load what's needed, when it's needed.

## The Three Levels

```
Level 1: Metadata     → Always in context (~100 tokens)
Level 2: SKILL.md     → When skill triggers (<5k tokens)
Level 3: References   → As Claude determines needed (unlimited)
```

### Level 1: Metadata (Always Loaded)

```yaml
---
name: pdf-processing
description: Extracts text from PDFs, fills forms, merges documents...
---
```

This is ALL Claude sees until the skill triggers. Make it count.

### Level 2: SKILL.md Body (On Trigger)

The main instructions. Keep under 500 lines. Contains:
- Quick start / core workflow
- Navigation to reference files
- Essential constraints

### Level 3: References (On Demand)

Detailed content Claude reads only when needed:
- Domain-specific schemas
- Framework-specific patterns
- Detailed examples
- API documentation

## When to Split Content

| Content Size | Structure |
|--------------|-----------|
| <100 lines total | SKILL.md only |
| 100-300 lines | SKILL.md + 1 reference file |
| 300-500 lines | SKILL.md + 2-3 reference files |
| >500 lines | Must split - SKILL.md body limit |

## Pattern 1: High-Level Guide with References

Best for: Skills with detailed docs that aren't always needed.

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced features

- **Form filling**: See [references/forms.md](references/forms.md)
- **Merging PDFs**: See [references/merge.md](references/merge.md)
- **OCR for scans**: See [references/ocr.md](references/ocr.md)
```

Claude reads forms.md only when user needs form filling.

## Pattern 2: Domain-Specific Organization

Best for: Skills covering multiple domains/datasets.

```
bigquery-skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── finance.md (revenue, billing, ARR)
    ├── sales.md (pipeline, opportunities)
    ├── product.md (usage, features)
    └── marketing.md (campaigns, attribution)
```

**SKILL.md:**
```markdown
# BigQuery Analysis

## Available domains

| Domain | Schema | File |
|--------|--------|------|
| Finance | Revenue, ARR, billing | [references/finance.md](references/finance.md) |
| Sales | Pipeline, accounts | [references/sales.md](references/sales.md) |
| Product | API usage, features | [references/product.md](references/product.md) |
| Marketing | Campaigns, email | [references/marketing.md](references/marketing.md) |

Read the relevant domain file before writing queries.
```

When user asks about revenue → Claude reads only finance.md.

## Pattern 3: Framework/Variant Organization

Best for: Skills supporting multiple frameworks.

```
testing-skill/
├── SKILL.md (workflow + framework selection)
└── references/
    ├── pytest.md
    ├── jest.md
    ├── vitest.md
    └── go-test.md
```

**SKILL.md:**
```markdown
# Test Setup

## Select framework

| Language | Framework | Details |
|----------|-----------|---------|
| Python | pytest | [references/pytest.md](references/pytest.md) |
| JavaScript | Jest | [references/jest.md](references/jest.md) |
| TypeScript | Vitest | [references/vitest.md](references/vitest.md) |
| Go | go test | [references/go-test.md](references/go-test.md) |

Detect language from project files, then read appropriate reference.
```

## Pattern 4: Conditional Details

Best for: Skills with basic and advanced modes.

```markdown
# Document Editing

## Basic editing

For simple text changes, modify the XML directly in `word/document.xml`.

## Advanced features

**Tracked changes**: See [references/redlining.md](references/redlining.md)
**OOXML internals**: See [references/ooxml.md](references/ooxml.md)
**Styles and formatting**: See [references/styles.md](references/styles.md)
```

Claude reads advanced files only when user needs those features.

## Critical Rule: One Level Deep

References must link directly from SKILL.md. Never nest references.

**BAD - Too deep:**
```
SKILL.md → advanced.md → details.md → actual-info.md
```

Claude may use `head -100` on nested files, missing content.

**GOOD - Flat:**
```
SKILL.md → forms.md
SKILL.md → merge.md
SKILL.md → ocr.md
```

All information accessible in one read.

## Table of Contents for Long References

For reference files >100 lines, include TOC at top:

```markdown
# API Reference

## Contents
- [Authentication](#authentication)
- [Core Methods](#core-methods)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Authentication
...
```

Helps Claude navigate and find specific sections.

## Signaling When to Read

Be explicit about when to read reference files:

```markdown
## Domain schemas

**Before writing any query**, read the relevant domain schema:
- Revenue queries → Read [references/finance.md](references/finance.md)
- Pipeline queries → Read [references/sales.md](references/sales.md)
```

Don't assume Claude will figure out when to read files.
