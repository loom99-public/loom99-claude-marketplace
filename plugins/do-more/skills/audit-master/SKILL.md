---
name: audit-master
description: Comprehensive audit across multiple dimensions - code quality, planning alignment, security, competitive analysis, and test coverage. Use when auditing any aspect of a project. Supports quick, medium, and thorough intensity levels.
---

# Audit Master

Comprehensive examination across multiple dimensions. Each dimension can be invoked independently or combined.

---

## Table of Contents

- [Dimension Selection](#dimension-selection)
- [Available Dimensions](#available-dimensions)
- [Intensity Levels](#intensity-levels)
- [Dimension 1: Code Quality](#dimension-1-code-quality)
  - [Code Quality Workflow](#code-quality-workflow)
  - [Code Quality Reference Documents](#code-quality-reference-documents)
- [Dimension 2: Planning Alignment](#dimension-2-planning-alignment)
  - [The Planning Stack](#the-planning-stack)
  - [Planning Audit Process](#planning-audit-process)
  - [Planning Reference Documents](#planning-reference-documents)
- [Dimension 3: Security](#dimension-3-security)
  - [Security Audit Process](#security-audit-process)
  - [Security Reference Documents](#security-reference-documents)
- [Dimension 4: Competitive](#dimension-4-competitive)
  - [Competitive Audit Process](#competitive-audit-process)
  - [Competitive Reference Documents](#competitive-reference-documents)
- [Dimension 5: Test Coverage](#dimension-5-test-coverage)
  - [Testing Philosophy](#testing-philosophy)
  - [Test Coverage Audit Process](#test-coverage-audit-process)
  - [Test Coverage Reference Documents](#test-coverage-reference-documents)
- [Combined Audit Output](#combined-audit-output)
- [Complete Reference Index](#complete-reference-index)
- [Related Skills](#related-skills)

---

## Dimension Selection

**If user specifies dimensions explicitly** (e.g., "audit security", "audit plans", "audit tests"), run those dimensions only.

**If user says "audit" without specifying dimensions**, use AskUserQuestion to prompt:

```
Which audit dimensions would you like to run?

Options (multiSelect):
1. Code Quality - Architecture, design, efficiency, correctness (Recommended)
2. Planning Alignment - Strategy→Architecture→Plans→Implementation
3. Security - Dependencies, secrets, auth, OWASP Top 10
4. Competitive - Compare against alternatives in the market
5. Test Coverage - Test quality, gaps, coverage analysis
```

**If user says "audit everything" or "comprehensive audit"**, run ALL dimensions.

---

## Available Dimensions

| Dimension | Trigger Words | What It Assesses |
|-----------|---------------|------------------|
| Code Quality | "code", "quality", "architecture", "design", "efficiency" | Architecture, design, efficiency, correctness, domain-specific |
| Planning | "plans", "planning", "alignment", "strategy" | Strategy coherence, alignment across planning layers |
| Security | "security", "vulnerabilities", "CVE", "secrets" | CVEs, secrets, auth, OWASP Top 10 |
| Competitive | "competitive", "competitors", "market", "alternatives" | Feature parity, gaps, differentiation vs alternatives |
| Test Coverage | "tests", "testing", "coverage", "test quality" | Test quality, coverage gaps, testing strategy |

---

## Intensity Levels

All dimensions support three intensity levels:

| Level | Trigger Words | Typical Time | Depth |
|-------|---------------|--------------|-------|
| **Quick** | "quick", "glance", "overview", "fast" | 5-15 min | Spot-check, flag obvious issues |
| **Medium** | (default), "check", "review" | 20-45 min | Systematic verification |
| **Thorough** | "thorough", "comprehensive", "deep", "forensic" | 1-2 hours | Leave no stone unturned |

---

## Dimension 1: Code Quality

Comprehensive technical audit for architecture, design, efficiency, and correctness.

### When to Use Code Quality

- General health check
- Before major work
- Assessing technical debt
- After significant changes

### Code Quality Workflow

1. **Identify audit scope** - whole project or specific area?
2. **Select applicable sub-dimensions** - not all apply to every project
3. **Load reference files** for selected sub-dimensions
4. **Execute checklists** systematically
5. **Document findings** with evidence (file:line references)

### Code Quality Sub-Dimensions

| Sub-Dimension | Reference File | Focus |
|---------------|----------------|-------|
| Architecture | [references/code-quality/architecture.md](references/code-quality/architecture.md) | Structure, alignment, violations |
| Design Quality | [references/code-quality/design-quality.md](references/code-quality/design-quality.md) | Patterns, smells, intentionality |
| Efficiency | [references/code-quality/efficiency.md](references/code-quality/efficiency.md) | Dead code, redundancy, performance |
| Domains | [references/code-quality/domains.md](references/code-quality/domains.md) | Domain-specific anti-patterns |

### Code Quality Output

```
Code Quality Audit:
  Architecture: [rating] | Design: [rating] | Efficiency: [rating]
  Findings: P0: n | P1: n | P2: n | P3: n
```

### Code Quality Reference Documents

| Topic | Reference |
|-------|-----------|
| Architecture checklists | [references/code-quality/architecture.md](references/code-quality/architecture.md) |
| Design quality patterns | [references/code-quality/design-quality.md](references/code-quality/design-quality.md) |
| Efficiency analysis | [references/code-quality/efficiency.md](references/code-quality/efficiency.md) |
| Domain-specific patterns | [references/code-quality/domains.md](references/code-quality/domains.md) |

---

## Dimension 2: Planning Alignment

Hierarchical alignment audit across the planning stack:

```
Strategy/Vision → Architecture → Plans → Implementation
```

Each layer should logically derive from the one above. This dimension audits for alignment gaps, staleness, completeness, and coherence at each level.

### When to Use Planning Alignment

- Plans feel disconnected from reality
- Before major planning sessions
- After strategy changes to check downstream impact
- Feeling "lost" about project direction

### The Planning Stack

#### Layer 1: Strategy/Vision
**Files**: `PROJECT_SPEC.md`, `VISION.md`, `STRATEGY.md`, `PROJECT.md`

What this layer defines:
- What are we building and why?
- Who is it for?
- What problems does it solve?
- What is success?

#### Layer 2: Architecture
**Files**: `ARCHITECTURE.md`, system diagrams, ADRs (Architecture Decision Records)

What this layer defines:
- How will we structure the solution?
- What are the major components?
- How do they interact?
- What technologies/patterns?

#### Layer 3: Plans
**Files**: `PLAN-*.md`, `BACKLOG-*.md`, `SPRINT-*.md`, `ROADMAP.md`

What this layer defines:
- What work needs to be done?
- In what order?
- What are the dependencies?

#### Layer 4: Implementation
**Files**: Actual code, `EVALUATION-*.md`, `TODO-*.md`

What this layer defines:
- What has actually been built?
- Does it match the plans?

### Planning Audit Process

#### Quick Planning Audit

1. **Locate documents** - Find what exists at each layer
2. **Spot-check alignment** - Do adjacent layers reference each other?
3. **Flag obvious issues** - Missing layers, stale dates, obvious contradictions
4. **Output** - Brief summary with red flags

See [references/planning/quick-audit.md](references/planning/quick-audit.md) for checklist.

#### Medium Planning Audit

All of Quick, plus:

1. **Layer completeness** - Is each layer sufficiently detailed for its purpose?
2. **Vertical traceability** - Can you trace from strategy → architecture → plan → code?
3. **Horizontal consistency** - Do documents at same layer agree?
4. **Staleness detection** - Are documents outdated vs. reality?
5. **Output** - Layer-by-layer assessment with specific gaps

See [references/planning/medium-audit.md](references/planning/medium-audit.md) for checklist.

#### Thorough Planning Audit

All of Medium, plus:

1. **Strategy coherence** - Does the strategy itself make sense? Gaps? Overlaps?
2. **Architecture sufficiency** - Does architecture enable all strategy goals?
3. **Plan coverage** - Is all strategy/architecture work planned?
4. **Plan realism** - Are plans achievable? Dependencies identified?
5. **Implementation alignment** - Does code match plans? Drift detected?
6. **Temporal consistency** - Planning horizon appropriate per layer?
7. **Output** - Comprehensive report with traceability matrix

See [references/planning/thorough-audit.md](references/planning/thorough-audit.md) for checklist.

### Planning Horizon Guidelines

| Distance | Detail Level | What Should Exist |
|----------|--------------|-------------------|
| Current sprint | Ready to pull | Full task breakdown, acceptance criteria |
| Sprint +1, +2 | Concrete | Stories identified, rough effort known |
| Sprint +3+ | Directional | Epics/themes, not detailed stories |
| Exception | Known critical work | Can be detailed regardless of distance |

**Anti-pattern**: Detailed task breakdowns for work 3+ sprints out (waste, will change)

**Anti-pattern**: No visibility beyond current sprint (no strategic alignment)

### Planning Output

```
Planning Audit:
  Strategy:     [rating] [issues]
  Architecture: [rating] [issues]
  Plans:        [rating] [issues]
  Alignment:    [rating] [issues]

Critical Gaps: [n]
Stale Documents: [n]
```

### Planning Ratings

| Rating | Meaning |
|--------|---------|
| ✅ Healthy | Layer complete, aligned, current |
| ⚠️ Attention | Minor gaps or staleness |
| ❌ Critical | Major gaps, misalignment, or severely stale |
| ❓ Missing | Layer doesn't exist |

### Planning Reference Documents

| Topic | Reference |
|-------|-----------|
| Quick audit checklist | [references/planning/quick-audit.md](references/planning/quick-audit.md) |
| Medium audit checklist | [references/planning/medium-audit.md](references/planning/medium-audit.md) |
| Thorough audit checklist | [references/planning/thorough-audit.md](references/planning/thorough-audit.md) |

---

## Dimension 3: Security

Systematic security assessment of the codebase and dependencies.

### When to Use Security

- Before deployment to production
- After adding auth/payment/sensitive data handling
- Periodic security review
- After dependency updates

### Security Scope

| In Scope | Out of Scope |
|----------|--------------|
| Dependency CVEs | Penetration testing |
| Code-level vulnerabilities | Infrastructure security |
| Auth/authz patterns | Network security |
| Data exposure risks | Physical security |
| OWASP Top 10 | Compliance audits (HIPAA, SOC2) |
| Secret management | Social engineering |

### Security Audit Process

#### Step 1: Dependency Audit

**Check for known vulnerabilities:**

```bash
# Node.js
npm audit
# or
npx better-npm-audit audit

# Python
pip-audit
# or
safety check

# Go
govulncheck ./...

# Rust
cargo audit

# General (Snyk, if available)
snyk test
```

**Document findings:**
| Dependency | CVE | Severity | Fix Available? |
|------------|-----|----------|----------------|
| [pkg@version] | [CVE-XXXX-XXXXX] | Critical/High/Med/Low | Yes/No |

#### Step 2: Secret Detection

**Scan for hardcoded secrets:**

```bash
# Using gitleaks
gitleaks detect --source . --verbose

# Using trufflehog
trufflehog filesystem .

# Manual patterns
grep -rn "password\s*=\|api_key\s*=\|secret\s*=\|token\s*=" --include="*.{js,ts,py,go,java}" .
grep -rn "-----BEGIN.*PRIVATE KEY" .
grep -rn "sk_live_\|pk_live_\|ghp_\|glpat-" .
```

**Check for:**
- API keys in code
- Passwords in config files
- Private keys committed
- .env files in repo
- Secrets in comments

#### Step 3: Authentication Review

See [references/security/auth-checklist.md](references/security/auth-checklist.md) for detailed checklist.

**Quick checks:**
| Check | Status |
|-------|--------|
| Password hashing (bcrypt/argon2/scrypt)? | ✅/❌ |
| Session management secure? | ✅/❌ |
| JWT implementation correct? | ✅/❌ |
| OAuth flow secure? | ✅/❌ |
| MFA available? | ✅/❌/N/A |
| Account lockout after failed attempts? | ✅/❌ |
| Secure password reset flow? | ✅/❌ |

#### Step 4: Authorization Review

| Check | Status |
|-------|--------|
| Access controls enforced server-side? | ✅/❌ |
| IDOR vulnerabilities checked? | ✅/❌ |
| Role-based access consistent? | ✅/❌ |
| Privilege escalation paths reviewed? | ✅/❌ |

#### Step 5: Data Exposure Review

**Sensitive data handling:**
| Data Type | Encrypted at Rest? | Encrypted in Transit? | Access Logged? |
|-----------|-------------------|----------------------|----------------|
| Passwords | [status] | [status] | [status] |
| PII | [status] | [status] | [status] |
| Financial | [status] | [status] | [status] |
| API keys | [status] | [status] | [status] |

**Data leakage vectors:**
- [ ] Error messages exposing internals
- [ ] Debug logging in production
- [ ] Verbose API responses
- [ ] Stack traces to users
- [ ] Database IDs exposed unnecessarily

#### Step 6: OWASP Top 10 Review

See [references/security/owasp-checklist.md](references/security/owasp-checklist.md) for detailed checklist.

| # | Vulnerability | Status | Evidence |
|---|---------------|--------|----------|
| A01 | Broken Access Control | ✅/⚠️/❌ | [notes] |
| A02 | Cryptographic Failures | ✅/⚠️/❌ | [notes] |
| A03 | Injection | ✅/⚠️/❌ | [notes] |
| A04 | Insecure Design | ✅/⚠️/❌ | [notes] |
| A05 | Security Misconfiguration | ✅/⚠️/❌ | [notes] |
| A06 | Vulnerable Components | ✅/⚠️/❌ | [notes] |
| A07 | Auth Failures | ✅/⚠️/❌ | [notes] |
| A08 | Data Integrity Failures | ✅/⚠️/❌ | [notes] |
| A09 | Logging Failures | ✅/⚠️/❌ | [notes] |
| A10 | SSRF | ✅/⚠️/❌ | [notes] |

#### Step 7: Input Validation Review

```bash
# Find user input handlers
grep -rn "req\.body\|req\.params\|req\.query" --include="*.ts" --include="*.js"
grep -rn "request\.form\|request\.args\|request\.json" --include="*.py"

# Check for validation
# Look for validation libraries, sanitization, type checking near input handling
```

| Input Point | Validation Present? | Sanitization? |
|-------------|--------------------| --------------|
| [endpoint/form] | ✅/❌ | ✅/❌ |

### Security Intensity Levels

| Level | Scope | Time |
|-------|-------|------|
| Quick | Dependency scan + secret scan | 5-10 min |
| Medium | + Auth review + OWASP quick check | 20-30 min |
| Thorough | Full OWASP + manual code review | 1-2 hours |

### Security Output

```
Security Audit:
  Risk Level: [Critical/High/Medium/Low]
  CVEs: n critical, n high | Secrets: [status]
  OWASP: [summary]
```

### Security Severity Definitions

| Severity | Criteria |
|----------|----------|
| Critical | Active exploit available, data breach possible, no auth required |
| High | Exploitable with some effort, significant data/functionality at risk |
| Medium | Requires specific conditions, limited impact |
| Low | Theoretical, defense in depth, best practice |

### Security Tools Referenced

| Tool | Purpose | Install |
|------|---------|---------|
| npm audit | Node.js dependency scan | Built-in |
| pip-audit | Python dependency scan | `pip install pip-audit` |
| gitleaks | Secret detection | `brew install gitleaks` |
| trufflehog | Secret detection | `pip install trufflehog` |
| govulncheck | Go vulnerability scan | `go install golang.org/x/vuln/cmd/govulncheck@latest` |
| cargo audit | Rust dependency scan | `cargo install cargo-audit` |

### Security Reference Documents

| Topic | Reference |
|-------|-----------|
| Authentication checklist | [references/security/auth-checklist.md](references/security/auth-checklist.md) |
| OWASP Top 10 checklist | [references/security/owasp-checklist.md](references/security/owasp-checklist.md) |

---

## Dimension 4: Competitive

Systematic comparison of this project against competitors and alternatives in the market.

### When to Use Competitive

- Before major feature planning (what should we build?)
- When positioning the product
- To identify gaps and opportunities
- To validate differentiation claims

### What Competitive Audit Does

1. **Identify competitors** - Direct competitors, alternatives, adjacent solutions
2. **Analyze their approach** - Features, architecture, UX, pricing
3. **Compare systematically** - Feature-by-feature, capability-by-capability
4. **Find gaps** - What do they have that we don't?
5. **Find opportunities** - What could we do better? What's missing in market?
6. **Assess differentiation** - Is our differentiation real and valuable?

### Competitive Audit Process

#### Step 1: Understand Our Project

Before comparing, document what WE do:
- Core features
- Target users
- Key differentiators (claimed)
- Technical approach

#### Step 2: Identify Competitors

**Sources**:
- User-provided list
- Web search: "[product type] alternatives"
- GitHub: similar projects
- Product Hunt, G2, Capterra for commercial products

**Categorize**:
| Category | Description |
|----------|-------------|
| Direct | Same problem, same audience |
| Indirect | Same problem, different approach |
| Adjacent | Related problem, overlapping audience |
| Emerging | New entrants, early stage |

#### Step 3: Research Each Competitor

Use `do:researcher` with WebSearch for each:

| Aspect | What to Find |
|--------|--------------|
| Features | What does it do? Feature list |
| Approach | How does it work? Architecture if OSS |
| Users | Who uses it? What scale? |
| Strengths | What do users praise? |
| Weaknesses | What do users complain about? |
| Pricing | Free? Paid? Model? |
| Momentum | Growing? Stagnant? Declining? |

#### Step 4: Feature Comparison Matrix

```markdown
| Feature | Us | Competitor A | Competitor B | Competitor C |
|---------|-----|--------------|--------------|--------------|
| [Feature 1] | ✅ Full | ✅ Full | ⚠️ Partial | ❌ None |
| [Feature 2] | ⚠️ Partial | ✅ Full | ✅ Full | ✅ Full |
| [Feature 3] | ❌ None | ❌ None | ✅ Full | ❌ None |
```

#### Step 5: Gap Analysis

**They have, we don't**:
| Gap | Competitor(s) | Impact | Should We? |
|-----|---------------|--------|------------|
| [Feature] | A, B | High/Med/Low | Yes/No/Maybe |

**We have, they don't**:
| Differentiator | Value | Defensible? |
|----------------|-------|-------------|
| [Feature] | [Why it matters] | Yes/No |

#### Step 6: Opportunity Analysis

| Opportunity | Description | Effort | Impact |
|-------------|-------------|--------|--------|
| [Gap to fill] | [What and why] | H/M/L | H/M/L |
| [Improvement] | [What and why] | H/M/L | H/M/L |

### Competitive Intensity Levels

| Level | Competitors Analyzed | Depth |
|-------|---------------------|-------|
| Quick | 2-3 direct | Feature list only |
| Medium | 4-6 mixed | Features + approach |
| Thorough | 8+ comprehensive | Full analysis + user research |

### Competitive Output

```
Competitive Audit:
  Position: [assessment]
  Gaps: n | Opportunities: n
  Differentiators: n validated
```

### Competitive Reference Documents

| Topic | Reference |
|-------|-----------|
| Research template | [references/competitive/research-template.md](references/competitive/research-template.md) |

---

## Dimension 5: Test Coverage

Forensic analysis of test coverage quality. Not just "do you have tests" but "are you testing the right things at the right level?"

### When to Use Test Coverage

- Reviewing test quality
- Identifying testing gaps
- Auditing test strategy
- Before planning test improvements

### Testing Philosophy

#### The Testing Pyramid

```
         ╱╲
        ╱E2E╲          Few, slow, high-confidence
       ╱──────╲
      ╱ Integ  ╲       Medium count, medium speed
     ╱──────────╲
    ╱    Unit    ╲     Many, fast, focused
   ╱──────────────╲
```

**Comprehensive Testing Level Definitions**: [references/testing/concepts/testing-levels.md](references/testing/concepts/testing-levels.md)

| Level | Tests | Speed | Scope | Confidence |
|-------|-------|-------|-------|------------|
| Unit | Many | Fast | Single function/class | Logic correctness |
| Integration | Medium | Medium | Component boundaries | Pieces work together |
| E2E | Few | Slow | Full user journey | System actually works |

#### Testing at the Right Level

**Wrong level** → wasted effort, false confidence, or fragile tests

| Symptom | Problem | Fix |
|---------|---------|-----|
| 500 unit tests, login broken | Missing e2e | Add e2e for critical paths |
| All e2e, CI takes 2 hours | Over-reliance on slow tests | Push more to unit/integration |
| Tests break on every refactor | Testing implementation, not behavior | Test contracts, not internals |
| High coverage, bugs slip through | Testing wrong things | Focus on user-facing behavior |

#### Common AI/LLM Testing Mistakes

When AI generates tests, it often makes systematic errors. **Read**: [references/testing/concepts/llm-testing-mistakes.md](references/testing/concepts/llm-testing-mistakes.md)

| Mistake | What It Looks Like | Why It's Harmful |
|---------|-------------------|------------------|
| Tautological tests | `expect(mock).toHaveBeenCalled()` after `mock()` | Tests nothing real |
| Over-mocking | Every dependency mocked | Tests mocks, not code |
| Happy path only | No error/edge cases | Misses real failures |
| Testing implementation | Breaks on refactor | Fragile, not behavioral |

### Test Coverage Audit Process

#### Phase 1: Complexity Source Detection

**Goal**: Create an exhaustive inventory of everything that needs testing.

##### 1.1 Architecture Detection

**Is this a microservices/distributed system?**

Read: [references/testing/detection/microservices.md](references/testing/detection/microservices.md)

| Signal | Detection Method |
|--------|------------------|
| Docker Compose | `ls docker-compose*.yml` |
| Kubernetes | `find . -name "*.yaml" \| xargs grep "kind: Deployment"` |
| Service URLs in env | `grep -E ".*_URL=.*_HOST=" .env*` |
| Multiple repos/services | Directory structure analysis |

##### 1.2 Data Interaction Detection

**What data does this system touch?**

Read: [references/testing/detection/data-interactions.md](references/testing/detection/data-interactions.md)

| Category | Detection |
|----------|-----------|
| Databases | Grep for ORM imports, connection strings |
| Caches | Grep for Redis/Memcached clients |
| File system | Grep for fs/pathlib operations |
| User config | Look for config loading patterns |
| Secrets | Check for secret manager integrations |

##### 1.3 External API Detection

**What external services does this call?**

Read: [references/testing/detection/external-apis.md](references/testing/detection/external-apis.md)

| Category | Detection |
|----------|-----------|
| HTTP clients | Grep for requests/axios/fetch |
| Payment SDKs | Grep for stripe/paypal |
| Auth providers | Grep for oauth/auth0/cognito |
| Cloud services | Grep for boto3/gcloud/azure |
| Webhooks | Grep for webhook endpoints |

##### 1.4 Interactive/User Input Detection

**Does this require user interaction for testing?**

Read: [references/testing/concepts/interactive-testing.md](references/testing/concepts/interactive-testing.md)

| Pattern | Testing Approach |
|---------|-----------------|
| CLI prompts | PTY/pexpect testing |
| Shell completions | Completion script testing |
| TUI (full-screen) | Virtual terminal (pyte) |
| Desktop GUI | Platform-specific (Playwright/XCTest) |
| Device-specific | Hardware test farms or mocks |

#### Phase 2: Detect Project Type & Language

##### 2.1 Project Type Detection

**Identify the scenario to set testing expectations**:

| Signal | Project Type | Scenario Reference |
|--------|--------------|-------------------|
| `bin/`, CLI entry point, argparse | CLI Tool | [references/testing/scenarios/cli.md](references/testing/scenarios/cli.md) |
| React/Vue/Angular, pages/, components/ | Web Frontend | [references/testing/scenarios/web-frontend.md](references/testing/scenarios/web-frontend.md) |
| Express/FastAPI/Rails, routes/ | Web Backend/API | [references/testing/scenarios/web-backend.md](references/testing/scenarios/web-backend.md) |
| Both frontend + backend | Full Stack | [references/testing/scenarios/fullstack.md](references/testing/scenarios/fullstack.md) |
| npm package, library exports | Library/SDK | [references/testing/scenarios/library.md](references/testing/scenarios/library.md) |
| iOS/Android, mobile frameworks | Mobile App | [references/testing/scenarios/mobile.md](references/testing/scenarios/mobile.md) |
| Dockerfile, k8s manifests, terraform | Infrastructure | [references/testing/scenarios/infrastructure.md](references/testing/scenarios/infrastructure.md) |
| agents/, prompts/, LLM calls | AI/Agent System | [references/testing/scenarios/ai-agents.md](references/testing/scenarios/ai-agents.md) |
| Airflow DAGs, Spark jobs, ETL | Data Pipeline | [references/testing/scenarios/data-pipelines.md](references/testing/scenarios/data-pipelines.md) |
| Kafka, WebSockets, real-time streams | Real-time System | [references/testing/scenarios/realtime-systems.md](references/testing/scenarios/realtime-systems.md) |
| Firmware, HAL, microcontrollers | Embedded/IoT | [references/testing/scenarios/embedded-iot.md](references/testing/scenarios/embedded-iot.md) |
| Electron, Qt, WPF, native GUI | Desktop App | [references/testing/scenarios/desktop-apps.md](references/testing/scenarios/desktop-apps.md) |
| manifest.json, Chrome/Firefox extension | Browser Extension | [references/testing/scenarios/browser-extensions.md](references/testing/scenarios/browser-extensions.md) |
| Unity, Unreal, game engine | Game Development | [references/testing/scenarios/game-development.md](references/testing/scenarios/game-development.md) |
| Solidity, smart contracts, Web3 | Blockchain/Web3 | [references/testing/scenarios/blockchain.md](references/testing/scenarios/blockchain.md) |

##### 2.2 Language/Framework Detection

| Language | Reference |
|----------|-----------|
| Python | [references/testing/languages/python.md](references/testing/languages/python.md) |
| TypeScript/JavaScript | [references/testing/languages/typescript.md](references/testing/languages/typescript.md) |
| Go | [references/testing/languages/go.md](references/testing/languages/go.md) |
| Rust | [references/testing/languages/rust.md](references/testing/languages/rust.md) |
| Java/Kotlin | [references/testing/languages/java.md](references/testing/languages/java.md) |
| Ruby | [references/testing/languages/ruby.md](references/testing/languages/ruby.md) |

#### Phase 3: Test Inventory

##### 3.1 Locate Test Files

```bash
# Common patterns
find . -name "*_test.*" -o -name "*.test.*" -o -name "test_*" 2>/dev/null | head -50
find . -path "*/tests/*" -o -path "*/test/*" -o -path "*/__tests__/*" 2>/dev/null | head -50

# Framework-specific
find . -name "*.spec.ts" -o -name "*.spec.js" 2>/dev/null  # Jest/Vitest
find . -path "**/cypress/**/*.cy.*" 2>/dev/null            # Cypress
find . -name "conftest.py" -o -name "pytest.ini" 2>/dev/null  # pytest
```

##### 3.2 Categorize Each Test

| Test Type | Indicators |
|-----------|------------|
| Unit | Single module import, no external deps, mocks everything |
| Integration | Multiple modules, may use test DB, some real services |
| E2E | Browser automation, real API calls, full system running |
| Contract | Pact/OpenAPI validation between services |

#### Phase 4: Coverage Mapping

**For each complexity source detected in Phase 1, determine test coverage**:

```markdown
### Coverage Matrix

#### Database Operations
| Operation | Location | Unit Test? | Integration Test? | E2E? |
|-----------|----------|------------|-------------------|------|
| User.create() | models/user.py:23 | ❌ | ❌ | ✅ (login e2e) |
| Order.validate() | models/order.py:45 | ✅ | ❌ | ❌ |

#### External API Calls
| API | Endpoint | Mocked? | Real Test? | Error Handling Tested? |
|-----|----------|---------|------------|------------------------|
| Stripe | create_payment | ✅ | ❌ | ❌ |
| SendGrid | send_email | ❌ | ❌ | ❌ |
```

#### Phase 5: Quality Assessment

##### 5.1 Red Flag Detection

| Red Flag | Detection Method | Severity |
|----------|-----------------|----------|
| Tautological tests | Grep for `assert True`, `expect(mock)` patterns | High |
| Over-mocked | Count mocks vs real interactions | High |
| Flaky tests | Grep for `sleep()`, timing dependencies | Medium |
| Test data coupling | Hardcoded IDs, magic numbers | Medium |
| No cleanup | Missing fixtures/teardown | Medium |
| Happy path only | No error assertions | High |

##### 5.2 Test Quality Checklist

For a sample of tests, verify:
- [ ] Tests fail when functionality breaks
- [ ] Tests don't break on refactoring internals
- [ ] Test names describe behavior, not implementation
- [ ] Setup/teardown is reliable
- [ ] Can run tests in isolation
- [ ] Edge cases are covered
- [ ] Error paths are tested

#### Phase 6: Gap Analysis

**Compare detected complexity sources against test inventory**:

```markdown
### Critical Gaps (P0)
| Gap | Complexity Source | Risk | Why P0 |
|-----|-------------------|------|--------|
| No payment error tests | Stripe integration | High | User funds at risk |
| No auth flow e2e | Auth0 integration | High | Users locked out |

### Significant Gaps (P1)
| Gap | Complexity Source | Risk | Why P1 |
|-----|-------------------|------|--------|
| No cache invalidation tests | Redis cache | Medium | Stale data shown |
| No webhook tests | Stripe webhooks | Medium | Orders not processed |

### Minor Gaps (P2)
| Gap | Complexity Source | Risk | Why P2 |
|-----|-------------------|------|--------|
| No config validation tests | pydantic settings | Low | Caught at startup |
```

### Test Coverage Intensity Levels

| Level | Scope | Depth |
|-------|-------|-------|
| Quick | Architecture + high-level gaps | 10-15 min |
| Medium | + Quality assessment + coverage matrix | 30-45 min |
| Thorough | + Test-by-test review + risk analysis | 60-90 min |

### Test Coverage Output

```
Test Coverage Audit:
  Overall Health: [Healthy | Needs Work | Critical Gaps]
  Coverage Distribution: Unit n% | Integration n% | E2E n%
  Critical Gaps: [n] | Quality Issues: [n]
```

### Test Coverage Reference Documents

#### Concepts
| Topic | Reference |
|-------|-----------|
| Testing levels defined | [references/testing/concepts/testing-levels.md](references/testing/concepts/testing-levels.md) |
| AI/LLM testing mistakes | [references/testing/concepts/llm-testing-mistakes.md](references/testing/concepts/llm-testing-mistakes.md) |
| Interactive system testing | [references/testing/concepts/interactive-testing.md](references/testing/concepts/interactive-testing.md) |
| Unknown UI testing | [references/testing/concepts/unknown-ui-testing.md](references/testing/concepts/unknown-ui-testing.md) |

#### Detection
| Area | Reference |
|------|-----------|
| Microservices detection | [references/testing/detection/microservices.md](references/testing/detection/microservices.md) |
| Data interaction detection | [references/testing/detection/data-interactions.md](references/testing/detection/data-interactions.md) |
| External API detection | [references/testing/detection/external-apis.md](references/testing/detection/external-apis.md) |

#### Scenarios (15)
| Category | Reference |
|----------|-----------|
| CLI Tools | [references/testing/scenarios/cli.md](references/testing/scenarios/cli.md) |
| Web Frontend | [references/testing/scenarios/web-frontend.md](references/testing/scenarios/web-frontend.md) |
| Web Backend/API | [references/testing/scenarios/web-backend.md](references/testing/scenarios/web-backend.md) |
| Full Stack | [references/testing/scenarios/fullstack.md](references/testing/scenarios/fullstack.md) |
| Library/SDK | [references/testing/scenarios/library.md](references/testing/scenarios/library.md) |
| Mobile App | [references/testing/scenarios/mobile.md](references/testing/scenarios/mobile.md) |
| Infrastructure | [references/testing/scenarios/infrastructure.md](references/testing/scenarios/infrastructure.md) |
| AI/Agent System | [references/testing/scenarios/ai-agents.md](references/testing/scenarios/ai-agents.md) |
| Data Pipeline/ETL | [references/testing/scenarios/data-pipelines.md](references/testing/scenarios/data-pipelines.md) |
| Real-time System | [references/testing/scenarios/realtime-systems.md](references/testing/scenarios/realtime-systems.md) |
| Embedded/IoT | [references/testing/scenarios/embedded-iot.md](references/testing/scenarios/embedded-iot.md) |
| Desktop App | [references/testing/scenarios/desktop-apps.md](references/testing/scenarios/desktop-apps.md) |
| Browser Extension | [references/testing/scenarios/browser-extensions.md](references/testing/scenarios/browser-extensions.md) |
| Game Development | [references/testing/scenarios/game-development.md](references/testing/scenarios/game-development.md) |
| Blockchain/Web3 | [references/testing/scenarios/blockchain.md](references/testing/scenarios/blockchain.md) |

#### Languages (6)
| Language | Reference |
|----------|-----------|
| Python | [references/testing/languages/python.md](references/testing/languages/python.md) |
| TypeScript/JS | [references/testing/languages/typescript.md](references/testing/languages/typescript.md) |
| Go | [references/testing/languages/go.md](references/testing/languages/go.md) |
| Rust | [references/testing/languages/rust.md](references/testing/languages/rust.md) |
| Java/Kotlin | [references/testing/languages/java.md](references/testing/languages/java.md) |
| Ruby | [references/testing/languages/ruby.md](references/testing/languages/ruby.md) |

---

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

Test Coverage:
  Health: [rating] | Gaps: n critical, n significant
  Distribution: Unit n% | Integration n% | E2E n%

Reports:
  - EVALUATION-<timestamp>.md
  - PLANNING-AUDIT-<timestamp>.md (if planning dimension)
  - SECURITY-AUDIT-<timestamp>.md (if security dimension)
  - COMPETITIVE-AUDIT-<timestamp>.md (if competitive dimension)
  - TEST-COVERAGE-AUDIT-<timestamp>.md (if test dimension)
═══════════════════════════════════════
```

---

## Priority Levels

| Priority | Meaning | Action |
|----------|---------|--------|
| P0 | Critical - blocks functionality or causes harm | Fix immediately |
| P1 | High - significant quality/maintenance issue | Fix soon |
| P2 | Medium - noticeable but not urgent | Plan to address |
| P3 | Low - polish, nice-to-have | Backlog |

---

## Complete Reference Index

### Code Quality References
| File | Purpose |
|------|---------|
| [references/code-quality/architecture.md](references/code-quality/architecture.md) | Architecture audit checklists |
| [references/code-quality/design-quality.md](references/code-quality/design-quality.md) | Design pattern analysis |
| [references/code-quality/efficiency.md](references/code-quality/efficiency.md) | Efficiency and dead code detection |
| [references/code-quality/domains.md](references/code-quality/domains.md) | Domain-specific anti-patterns |

### Planning References
| File | Purpose |
|------|---------|
| [references/planning/quick-audit.md](references/planning/quick-audit.md) | Quick planning audit checklist |
| [references/planning/medium-audit.md](references/planning/medium-audit.md) | Medium planning audit checklist |
| [references/planning/thorough-audit.md](references/planning/thorough-audit.md) | Thorough planning audit checklist |

### Security References
| File | Purpose |
|------|---------|
| [references/security/auth-checklist.md](references/security/auth-checklist.md) | Authentication audit checklist |
| [references/security/owasp-checklist.md](references/security/owasp-checklist.md) | OWASP Top 10 checklist |

### Competitive References
| File | Purpose |
|------|---------|
| [references/competitive/research-template.md](references/competitive/research-template.md) | Competitor research template |

### Testing References

#### Concepts
| File | Purpose |
|------|---------|
| [references/testing/concepts/testing-levels.md](references/testing/concepts/testing-levels.md) | Testing level definitions |
| [references/testing/concepts/llm-testing-mistakes.md](references/testing/concepts/llm-testing-mistakes.md) | Common AI testing errors |
| [references/testing/concepts/interactive-testing.md](references/testing/concepts/interactive-testing.md) | Interactive system testing |
| [references/testing/concepts/unknown-ui-testing.md](references/testing/concepts/unknown-ui-testing.md) | Unknown UI testing |

#### Detection
| File | Purpose |
|------|---------|
| [references/testing/detection/microservices.md](references/testing/detection/microservices.md) | Microservices detection |
| [references/testing/detection/data-interactions.md](references/testing/detection/data-interactions.md) | Data interaction detection |
| [references/testing/detection/external-apis.md](references/testing/detection/external-apis.md) | External API detection |

#### Languages
| File | Purpose |
|------|---------|
| [references/testing/languages/python.md](references/testing/languages/python.md) | Python testing |
| [references/testing/languages/typescript.md](references/testing/languages/typescript.md) | TypeScript testing |
| [references/testing/languages/go.md](references/testing/languages/go.md) | Go testing |
| [references/testing/languages/rust.md](references/testing/languages/rust.md) | Rust testing |
| [references/testing/languages/java.md](references/testing/languages/java.md) | Java testing |
| [references/testing/languages/ruby.md](references/testing/languages/ruby.md) | Ruby testing |

#### Scenarios
| File | Purpose |
|------|---------|
| [references/testing/scenarios/cli.md](references/testing/scenarios/cli.md) | CLI testing |
| [references/testing/scenarios/web-frontend.md](references/testing/scenarios/web-frontend.md) | Web frontend testing |
| [references/testing/scenarios/web-backend.md](references/testing/scenarios/web-backend.md) | Web backend testing |
| [references/testing/scenarios/fullstack.md](references/testing/scenarios/fullstack.md) | Full stack testing |
| [references/testing/scenarios/library.md](references/testing/scenarios/library.md) | Library testing |
| [references/testing/scenarios/mobile.md](references/testing/scenarios/mobile.md) | Mobile testing |
| [references/testing/scenarios/infrastructure.md](references/testing/scenarios/infrastructure.md) | Infrastructure testing |
| [references/testing/scenarios/ai-agents.md](references/testing/scenarios/ai-agents.md) | AI/Agent testing |
| [references/testing/scenarios/data-pipelines.md](references/testing/scenarios/data-pipelines.md) | Data pipeline testing |
| [references/testing/scenarios/realtime-systems.md](references/testing/scenarios/realtime-systems.md) | Real-time testing |
| [references/testing/scenarios/embedded-iot.md](references/testing/scenarios/embedded-iot.md) | Embedded/IoT testing |
| [references/testing/scenarios/desktop-apps.md](references/testing/scenarios/desktop-apps.md) | Desktop app testing |
| [references/testing/scenarios/browser-extensions.md](references/testing/scenarios/browser-extensions.md) | Browser extension testing |
| [references/testing/scenarios/game-development.md](references/testing/scenarios/game-development.md) | Game testing |
| [references/testing/scenarios/blockchain.md](references/testing/scenarios/blockchain.md) | Blockchain testing |

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `testing-master` | Test setup, recommendations, and implementation planning |
| `do:status-check` | Quick project status diagnostic |
| `do:feature-proposal` | Design new features based on gaps found |
| `do:market-research` | Broader market analysis beyond competitors |
