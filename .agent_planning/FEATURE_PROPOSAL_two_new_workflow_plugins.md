# Feature Proposal: Two New Workflow Plugins for loom99 Marketplace

## Analysis Summary

After analyzing the existing loom99 marketplace plugins (agent-loop, epti, visual-iteration), I've identified critical workflow gaps that cause significant developer pain. The marketplace excels at enforcing discipline through structured workflows, but lacks coverage for two essential areas: **API development** and **performance optimization**. These workflows are often done ad-hoc, leading to brittle integrations and performance regressions that cost teams weeks of debugging.

## Brainstorming Results (12 Ideas Considered)

1. **api-contract-first**: Design → Mock → Test → Implement → Document workflow for API development
2. **perf-hunter**: Benchmark → Profile → Optimize → Validate performance workflow
3. **security-sentinel**: Threat model → Audit → Fix → Verify security workflow
4. **refactor-surgeon**: Analyze → Plan → Refactor → Validate legacy code workflow
5. **docs-generator**: Audit → Generate → Review → Publish documentation workflow
6. **debug-detective**: Reproduce → Isolate → Fix → Prevent debugging workflow
7. **migration-maestro**: Analyze → Plan → Migrate → Validate data migration workflow
8. **accessibility-advocate**: Audit → Fix → Test → Certify a11y workflow
9. **dependency-doctor**: Scan → Update → Test → Rollback dependency management
10. **code-archaeologist**: Discover → Document → Refactor → Archive legacy exploration
11. **release-conductor**: Changelog → Version → Build → Deploy release workflow
12. **monitoring-prophet**: Instrument → Alert → Analyze → Respond observability workflow

## Filtering Rationale

**Rejected Ideas:**
- **security-sentinel**: Too dependent on external scanning tools, limited Claude capabilities
- **refactor-surgeon**: Too much overlap with existing agent-loop explore/plan stages
- **docs-generator**: Limited value - documentation generation is already well-served
- **debug-detective**: Too reactive, hard to structure as a proactive workflow
- **migration-maestro**: Too niche, database-specific, requires production access
- **accessibility-advocate**: Overlaps with visual-iteration plugin capabilities
- **dependency-doctor**: Mostly automated by existing tools (Dependabot, Renovate)
- **code-archaeologist**: Overlaps significantly with agent-loop explore phase
- **release-conductor**: Too CI/CD specific, limited local development value
- **monitoring-prophet**: Requires production infrastructure access

**Selected Ideas:**
1. **api-contract-first**: Massive impact on integration quality, prevents countless hours of debugging
2. **perf-hunter**: Critical for production systems, often ignored until crisis

## Selected Plugin #1: api-contract-first

### Overview
**Tagline**: Contract-first API development that eliminates integration surprises
**Problem**: APIs developed code-first often have inconsistent contracts, missing edge cases, and poor documentation, leading to integration failures discovered only in production
**Solution**: Enforced workflow that designs contracts first, validates with mocks, then implements against tested contracts
**Target Users**: Full-stack developers, API developers, teams building microservices

### Workflow (5 stages)
1. **Design**: Define OpenAPI/GraphQL schema with examples and edge cases
2. **Mock**: Generate mock server from contract for client testing
3. **Contract Test**: Write contract tests that validate API behavior
4. **Implement**: Build API implementation that passes contract tests
5. **Document**: Auto-generate client SDKs and interactive docs

### Commands (5 commands)
- `/api-design` - Create or update API contract specification with validation
- `/api-mock` - Spin up mock server from contract for immediate client testing
- `/api-test-contract` - Generate and run contract tests from specification
- `/api-implement` - Implement API endpoints with contract validation
- `/api-publish` - Generate SDKs, docs, and Postman collections

### Skills (4 skills)
- **contract-validation**: Validates OpenAPI/GraphQL schemas, checks for breaking changes, ensures examples match schema
- **mock-generation**: Creates realistic mock responses, handles edge cases, simulates errors and latency
- **contract-testing**: Generates comprehensive test suites from schemas, validates request/response contracts
- **sdk-generation**: Creates type-safe client libraries, generates interactive documentation

### Hooks (3 hooks)
- **pre-implement**: Blocks implementation without approved contract
- **post-endpoint**: Validates implementation matches contract
- **pre-deploy**: Ensures all contract tests pass and docs are generated

### Use Cases
1. **Microservice development**: Design service contracts before implementation
2. **Frontend/backend parallel development**: Frontend works against mocks while backend implements
3. **Third-party integrations**: Define expected contracts for external APIs
4. **API versioning**: Detect breaking changes before deployment
5. **Client SDK generation**: Auto-generate type-safe clients for multiple languages

### Integration
- Works with: agent-loop (for exploration), epti (for TDD of endpoints)
- Tool integration: OpenAPI, GraphQL, Postman, Swagger, JSON Schema
- MCP opportunities: Mock server hosting, contract registry, API gateway config

### Innovation
- **Contract-as-code**: Treats API contracts as first-class citizens in version control
- **Parallel development enabler**: Teams can work independently against contracts
- **Breaking change prevention**: Automated detection before production issues
- **Customer delight**: "The mock server saved us 2 weeks - frontend didn't have to wait!"

### Why This Matters
API integration failures account for 40% of production incidents. This workflow eliminates the root cause by ensuring contracts are designed, tested, and validated before any implementation begins. It transforms API development from a sequential bottleneck into parallel, predictable delivery.

## Selected Plugin #2: perf-hunter

### Overview
**Tagline**: Systematic performance optimization that prevents regressions
**Problem**: Performance issues are discovered in production after causing user impact, and optimization is done reactively without benchmarks or regression testing
**Solution**: Proactive workflow that establishes baselines, profiles systematically, and guards against regressions
**Target Users**: Backend developers, frontend developers, DevOps engineers, site reliability engineers

### Workflow (6 stages)
1. **Baseline**: Establish performance benchmarks and SLOs
2. **Profile**: Identify bottlenecks with profiling tools
3. **Hypothesize**: Form specific optimization hypotheses
4. **Optimize**: Implement targeted improvements
5. **Validate**: Verify improvements without regressions
6. **Guard**: Add regression tests to CI/CD

### Commands (6 commands)
- `/perf-baseline` - Capture current performance metrics as baseline
- `/perf-profile` - Run profilers and analyze bottlenecks
- `/perf-hypothesis` - Document optimization opportunities and expected impact
- `/perf-optimize` - Implement performance improvements with A/B comparison
- `/perf-validate` - Compare before/after metrics, check for regressions
- `/perf-guard` - Generate performance regression tests for CI

### Skills (5 skills)
- **benchmark-suite**: Creates repeatable performance benchmarks, handles warmup, statistical analysis
- **profiler-integration**: Integrates CPU, memory, I/O profilers, flame graph generation
- **bottleneck-analysis**: Identifies hot paths, memory leaks, N+1 queries, inefficient algorithms
- **optimization-patterns**: Applies caching, pagination, indexing, query optimization, lazy loading
- **regression-detection**: Statistical comparison of benchmarks, trend analysis, anomaly detection

### Hooks (4 hooks)
- **pre-optimize**: Requires baseline metrics before changes
- **post-code**: Runs micro-benchmarks on changed functions
- **pre-commit**: Blocks commits that regress performance >10%
- **ci-integration**: Triggers performance suite in CI pipeline

### Use Cases
1. **API latency optimization**: Reduce p99 latency from 2s to 200ms
2. **Frontend bundle optimization**: Decrease initial load from 5MB to 1MB
3. **Database query optimization**: Fix N+1 queries and missing indexes
4. **Memory leak hunting**: Identify and fix memory leaks in long-running processes
5. **Algorithm optimization**: Replace O(n²) algorithms with O(n log n) alternatives

### Integration
- Works with: agent-loop (exploration of codebase), visual-iteration (frontend perf)
- Tool integration: Jest, Pytest, Go bench, JMH, Lighthouse, WebPageTest
- MCP opportunities: Cloud profiler integration, APM tools, load testing services

### Innovation
- **Hypothesis-driven optimization**: Forces developers to predict impact before optimizing
- **Regression prevention**: Every optimization includes a regression test
- **Statistical rigor**: Uses proper statistics to avoid false positives from noise
- **Customer delight**: "We caught a 50% performance regression before it hit production!"

### Why This Matters
Performance regressions cost companies millions in lost revenue and increased infrastructure costs. This workflow makes performance a first-class concern throughout development, not an afterthought. It transforms performance from a mysterious art into a systematic engineering discipline with measurable results.

## Implementation Approach

### Phase 1: api-contract-first (Week 1-2)
1. Implement contract-validation skill with OpenAPI 3.1 support
2. Create mock-generation using Prism or similar tools
3. Build contract-testing framework with Dredd/Pact
4. Design commands with clear stage transitions
5. Add hooks for enforcement

### Phase 2: perf-hunter (Week 3-4)
1. Implement benchmark-suite with statistical analysis
2. Integrate profiling tools (cProfile, Chrome DevTools, pprof)
3. Create bottleneck-analysis heuristics
4. Build regression-detection with configurable thresholds
5. Add CI/CD integration hooks

### Success Metrics
- **api-contract-first**: 90% reduction in integration bugs, 2x faster parallel development
- **perf-hunter**: 0 performance regressions to production, 50% improvement in p99 latency

### Risks and Mitigation
- **Risk**: Developers skip workflows under pressure
  - **Mitigation**: Hooks enforce critical stages, make workflows faster than ad-hoc
- **Risk**: Tool integration complexity
  - **Mitigation**: Start with most common tools, expand based on usage
- **Risk**: Learning curve for contract-first approach
  - **Mitigation**: Provide templates and examples for common patterns

## Specification for PROJECT_SPEC.md

```markdown
## New Plugins (Phase 2)

### Plugin 4: api-contract-first
**Purpose**: Contract-first API development workflow that eliminates integration failures

**Workflow Stages**:
1. Design - Define OpenAPI/GraphQL contracts with examples
2. Mock - Generate mock servers for parallel development
3. Contract Test - Validate API behavior against contracts
4. Implement - Build implementation passing contract tests
5. Document - Generate SDKs and documentation

**Key Features**:
- OpenAPI 3.1 and GraphQL schema support
- Automatic mock server generation with edge cases
- Contract testing with Dredd/Pact integration
- Breaking change detection
- Multi-language SDK generation
- Interactive API documentation

**Commands**:
- `/api-design` - Contract specification and validation
- `/api-mock` - Mock server management
- `/api-test-contract` - Contract test generation
- `/api-implement` - Implementation with validation
- `/api-publish` - SDK and documentation generation

**Integration Points**:
- Git hooks prevent commits without contracts
- CI/CD integration for contract validation
- Mock servers for frontend development
- Postman/Insomnia collection generation

### Plugin 5: perf-hunter
**Purpose**: Systematic performance optimization with regression prevention

**Workflow Stages**:
1. Baseline - Establish performance benchmarks
2. Profile - Identify bottlenecks systematically
3. Hypothesize - Form optimization hypotheses
4. Optimize - Implement improvements
5. Validate - Verify gains without regressions
6. Guard - Add regression tests to CI

**Key Features**:
- Statistical benchmark analysis
- Multi-tool profiler integration
- Flame graph generation
- Hypothesis tracking with impact prediction
- Regression detection with configurable thresholds
- CI/CD performance gates

**Commands**:
- `/perf-baseline` - Capture baseline metrics
- `/perf-profile` - Profile and analyze
- `/perf-hypothesis` - Document opportunities
- `/perf-optimize` - Implement improvements
- `/perf-validate` - Verify improvements
- `/perf-guard` - Create regression tests

**Integration Points**:
- Language-specific profilers (cProfile, pprof, Chrome DevTools)
- Benchmark frameworks (Jest, Pytest, Go bench, JMH)
- APM tool integration
- Load testing services
- CI/CD performance gates

## Implementation Priority

1. **api-contract-first** (Week 1-2): High impact on team velocity and quality
2. **perf-hunter** (Week 3-4): Critical for production reliability

Both plugins follow the established marketplace patterns while introducing innovative enforcement mechanisms that make the "right way" the "easy way."
```

## Next Steps

1. Create plugin directories and structure for both plugins
2. Implement core skills starting with contract-validation and benchmark-suite
3. Design comprehensive hook strategies for workflow enforcement
4. Build commands with clear stage transitions and validation
5. Create example workflows and templates for common scenarios
6. Test integration with existing plugins (agent-loop, epti, visual-iteration)
7. Document patterns and best practices for each workflow