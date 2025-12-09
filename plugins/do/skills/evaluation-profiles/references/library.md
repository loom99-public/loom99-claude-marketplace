# Library Evaluation Profile

## Characteristics
- Consumed by other developers
- API surface matters (public interface)
- Documentation critical
- Versioning concerns
- May have no executable entry point

## ALWAYS RUN (~45 seconds)

| Check | How | Pass Criteria |
|-------|-----|---------------|
| Build succeeds | `npm run build` or equivalent | No errors |
| Tests pass | `npm test` or equivalent | All tests green |
| Types valid | `tsc --noEmit` (if TypeScript) | No type errors |
| Exports accessible | Import main export | No resolution errors |
| README exists | Check file | Has basic usage example |

## RUN IF APPLICABLE

| Check | Condition | How |
|-------|-----------|-----|
| API docs | Has doc generation | Generate, verify not empty |
| Multiple entry points | Package has subpath exports | Import each entry point |
| Peer dependencies | Has peerDeps | Verify they're documented |
| Browser bundle | Targets browsers | Check bundle size, tree-shaking |
| Node compatibility | Targets Node | Test with target Node version |
| Example code | Has /examples folder | Run examples, verify they work |

## SKIP UNLESS USER REQUESTS

| Check | Why Skip | When User Might Request |
|-------|----------|------------------------|
| Performance benchmarks | Time-consuming | "Library feels slow" |
| Bundle analysis | Detailed | "Bundle too large" |
| Breaking change detection | Requires baseline | Pre-release review |
| Cross-platform testing | Complex setup | "Works on Mac, not Windows" |

## SKIP ENTIRELY

| Check | Reason |
|-------|--------|
| UI testing | Not a UI |
| E2E flows | No user flows |
| Session management | Not applicable |
| Authentication | Not applicable |

## Common Library Blind Spots

Check these specifically:
- **Export hygiene**: Are internal functions accidentally exported?
- **Type exports**: Can users import types they need?
- **Error types**: Are errors typed/documented?
- **Async behavior**: Promises resolve/reject correctly?
- **Default values**: Sensible defaults documented?
- **Edge cases**: null, undefined, empty arrays handled?

## API Surface Validation

```markdown
## Export Check

Public exports (from index/main):
- function foo() ✅ documented
- class Bar ✅ documented
- type Baz ✅ documented
- const CONFIG ❌ internal, should not be exported
```

## Test Quality Assessment

```markdown
## Test Assessment

| Area | Coverage | Quality |
|------|----------|---------|
| Core API | 80% | Real assertions |
| Edge cases | 40% | Missing null handling |
| Error paths | 60% | Some exceptions untested |
| Types | N/A | TypeScript validates |
```

## Evidence to Capture

```
Build: success/failure
Tests: n passed, m failed
Type check: success/failure
Exports: <list of public exports>
Missing docs: <list>
API issues: <list>
```

## User Validation Suggestions

> "To verify the library works for consumers:
> 1. Try importing in a fresh project
> 2. Follow the README example exactly
> 3. Check IDE autocomplete shows expected methods"
