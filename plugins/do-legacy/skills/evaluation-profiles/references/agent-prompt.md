# Agent/Prompt Evaluation Profile

## Characteristics
- Text-based definitions (markdown, YAML)
- No runtime execution (prompts don't "run")
- Quality is about clarity, completeness, guidance
- Validation is structural and semantic, not behavioral

## ALWAYS RUN (~15 seconds)

| Check | How | Pass Criteria |
|-------|-----|---------------|
| File syntax | Parse YAML frontmatter | Valid YAML, required fields present |
| Required fields | Check frontmatter | `name`, `description` present and non-empty |
| File references | Grep for file paths | Referenced files exist |
| Broken links | Check markdown links | Internal links resolve |
| Spelling/grammar | Scan for obvious errors | No egregious typos in key sections |

## RUN IF APPLICABLE

| Check | Condition | How |
|-------|-----------|-----|
| Tool references | Agent uses tools | Verify tool names are valid |
| Model specification | Has `model:` field | Model name is valid (sonnet, opus, haiku) |
| MCP references | Uses MCP tools | Verify MCP server configured |
| Example validation | Includes examples | Examples are consistent with instructions |
| Output format spec | Defines output format | Format is clear, parseable |

## SKIP UNLESS USER REQUESTS

| Check | Why Skip | When User Might Request |
|-------|----------|------------------------|
| Prompt injection testing | Specialized | Security-sensitive deployment |
| Token count analysis | Rarely blocking | "Prompt too long" |
| A/B comparison | Requires multiple versions | "Which prompt is better?" |

## SKIP ENTIRELY

| Check | Reason |
|-------|--------|
| Runtime testing | Prompts don't execute |
| Performance testing | Not applicable |
| Memory profiling | Not applicable |
| Database testing | Not applicable |
| Network testing | Not applicable |
| Concurrent access | Not applicable |
| Pagination | Not applicable |
| Form validation | Not applicable |

## Common Prompt Blind Spots

Check these specifically:
- **Ambiguous instructions**: "Handle errors appropriately" (what does that mean?)
- **Missing edge cases**: What if input is empty? Invalid?
- **Conflicting guidance**: Two sections contradict each other
- **Undefined terms**: Jargon without explanation
- **Scope creep**: Prompt tries to do too much
- **Missing examples**: Complex format without example

## Structural Validation

```markdown
## Required Structure Check

✅ Has clear purpose statement
✅ Instructions are in imperative form
✅ No TODO/FIXME placeholders
✅ No "Coming soon" sections
✅ File paths are absolute or clearly relative
✅ Referenced tools/skills exist
```

## Semantic Validation

```markdown
## Semantic Check

✅ Instructions are actionable (not vague)
✅ Success criteria are measurable
✅ Error handling is specified
✅ Output format is unambiguous
✅ No internal contradictions
```

## Evidence to Capture

```
File: <path>
Frontmatter valid: yes/no
Required fields: present/missing
Broken references: <list or none>
Structural issues: <list or none>
Semantic concerns: <list or none>
```

## User Validation Suggestions

Since prompts can't be automatically "run", suggest user verification:

> "To validate this prompt works as intended, try using it with:
> 1. A simple, straightforward request
> 2. An edge case (empty input, unusual format)
> 3. An ambiguous request (does it ask for clarification?)"
