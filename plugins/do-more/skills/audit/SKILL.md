---
name: audit
description: Deep forensic examination of the codebase. Use for comprehensive quality, security, architecture, or debt analysis.
---

# Audit

Comprehensive examination across multiple dimensions. Each dimension can be invoked independently or combined.

## Dimension Selection

**If user specifies dimensions explicitly** (e.g., "audit security", "audit plans"), run those dimensions only.

**If user says "audit" without specifying dimensions**, use AskUserQuestion to prompt:

```
Which audit dimensions would you like to run?

Options (multiSelect):
1. Code Quality - Architecture, design, efficiency, correctness (Recommended)
2. Planning Alignment - Strategy→Architecture→Plans→Implementation
3. Security - Dependencies, secrets, auth, OWASP Top 10
4. Competitive - Compare against alternatives in the market
```

**If user says "audit everything" or "comprehensive audit"**, run ALL dimensions.

## Available Dimensions

| Dimension | Skill | What It Assesses |
|-----------|-------|------------------|
| Code Quality | `do:deep-audit` | Architecture, design, efficiency, correctness, domain-specific |
| Planning | `do:planning-audit` | Strategy coherence, alignment across planning layers |
| Security | `do:security-audit` | CVEs, secrets, auth, OWASP Top 10 |
| Competitive | `do:competitive-audit` | Feature parity, gaps, differentiation vs alternatives |

## Routing

### Code Quality (Default)

**Trigger**: "audit", "code audit", "quality", "architecture", "design", "efficiency"

**Process**: Use `do:project-evaluator` in audit mode with `do:deep-audit` checklists

**Covers**:
- Correctness (does it work?)
- Architecture (structure sound?)
- Design Quality (intentional design?)
- Efficiency (dead code, performance?)
- Feature Cohesion (features make sense?)
- Domain-Specific (domain anti-patterns?)

### Planning Alignment

**Trigger**: "audit plans", "planning audit", "alignment", "strategy audit"

**Process**: Invoke `do:planning-audit` skill

**Intensity**:
| Level | Trigger | Time |
|-------|---------|------|
| Quick | "quick" | 2-5 min |
| Medium | default | 10-20 min |
| Thorough | "thorough", "forensic" | 30-60 min |

**Covers**:
- Strategy coherence
- Strategy → Architecture alignment
- Architecture → Plans alignment
- Plans → Implementation alignment
- Planning horizon appropriateness

### Security

**Trigger**: "audit security", "security audit", "vulnerabilities", "CVE"

**Process**: Invoke `do:security-audit` skill

**Intensity**:
| Level | Scope |
|-------|-------|
| Quick | Dependency scan + secret scan |
| Medium | + Auth review + OWASP quick check |
| Thorough | Full OWASP + manual code review |

**Covers**:
- Dependency vulnerabilities (CVEs)
- Hardcoded secrets
- Authentication patterns
- Authorization controls
- OWASP Top 10

### Competitive

**Trigger**: "audit competitive", "competitive audit", "compare to competitors", "market audit"

**Process**: Invoke `do:competitive-audit` skill (requires external research)

**Intensity**:
| Level | Competitors | Depth |
|-------|-------------|-------|
| Quick | 2-3 direct | Feature list |
| Medium | 4-6 mixed | Features + approach |
| Thorough | 8+ | Full analysis |

**Covers**:
- Competitor identification
- Feature comparison matrix
- Gap analysis
- Opportunity identification
- Differentiation assessment

## Combined Audit Output

When multiple dimensions run:

```
═══════════════════════════════════════
Audit Complete - [dimensions run]

Code Quality:
  Architecture: [rating] | Design: [rating] | Efficiency: [rating]
  Findings: P0: n | P1: n | P2: n | P3: n

Planning:
  Strategy: [rating] | Alignment: [rating]
  Gaps: n | Stale docs: n

Security:
  Risk Level: [Critical/High/Medium/Low]
  CVEs: n critical, n high | Secrets: [status]

Competitive:
  Position: [assessment]
  Gaps: n | Opportunities: n

Reports:
  - STATUS-<timestamp>.md
  - PLANNING-AUDIT-<timestamp>.md
  - SECURITY-AUDIT-<timestamp>.md
  - COMPETITIVE-AUDIT-<timestamp>.md
═══════════════════════════════════════
```

## Priority Levels

| Priority | Meaning |
|----------|---------|
| P0 | Critical - fix immediately |
| P1 | High - fix soon |
| P2 | Medium - plan to address |
| P3 | Low - nice to have |

## When to Use

- **Code Quality**: General health check, before major work, assessing debt
- **Planning**: Strategy changes, sprint planning, feeling "lost"
- **Security**: Pre-deployment, after adding auth/sensitive features, periodic review
- **Competitive**: Product planning, positioning, identifying gaps/opportunities
