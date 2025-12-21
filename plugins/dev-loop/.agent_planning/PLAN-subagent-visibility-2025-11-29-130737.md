# Implementation Plan: Subagent Output Visibility

**Generated**: 2025-11-29 13:07:37
**Source STATUS**: STATUS-2025-11-29-130418.md
**Spec**: plugins/dev-loop/CLAUDE.md
**Planner**: status-planner agent

---

## Executive Summary

**Problem**: Users running dev-loop slash commands cannot see subagent completion summaries without pressing ctrl-o. All 7 agents produce "Final Summary (Required)" sections, but Claude Code's subagent isolation architecture hides these summaries from users by default.

**Impact**: Users have zero visibility into:
- What work was completed
- Which files were generated (STATUS-*.md, PLAN-*.md, WORK-EVALUATION-*.md)
- What issues were found
- What next steps are recommended
- Whether the subagent succeeded or encountered blockers

**Solution**: Hybrid approach combining file-based summaries (durable, discoverable) with console echo (immediate visibility).

**Scope**:
- 7 agent files requiring summary output updates
- 4 command files requiring result display logic
- 12 total files modified across 3 phases

**Effort**: Medium complexity - structured modifications with clear patterns across similar files.

---

## Implementation Phases

### Phase 1: File-Based Summary Output (P0 - Critical)

**Goal**: Each agent writes human-readable summary file that persists in `.agent_planning/` directory alongside STATUS/PLAN files.

**Acceptance Criteria**:
- [ ] All 7 agents write `SUMMARY-<agent-name>-<timestamp>.txt` files
- [ ] Summary files follow consistent template format
- [ ] Summary files appear in `.agent_planning/` directory
- [ ] Agents output message to user indicating summary file location
- [ ] Summary includes key metrics, files generated, and recommendations

**Files to Modify**: 7 agent files

#### Work Item 1.1: Update project-evaluator.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/project-evaluator.md`

**Location**: Lines 74-88 (existing "Final Summary (Required)" section)

**Changes**:
Replace existing section with:

```markdown
## Final Summary (Required)

At the end of your work:

1. Write summary to file: `.agent_planning/SUMMARY-project-evaluator-<YYYY-MM-DD-HHmmss>.txt`

Use this exact template:
```
Summary: [1-sentence description of evaluation outcome]
Agent: project-evaluator
Timestamp: <YYYY-MM-DD HH:MM:SS>

Key Results:
- Completion: X% (n/m components)
- Critical gaps: n ([brief list])
- Status taxonomy: NOT_STARTED: n, PARTIAL: n, COMPLETE: n

Files Generated:
- STATUS-<YYYY-MM-DD-HHmmss>.md

Recommendation: [next action - usually "Proceed with status-planner to create backlog"]
```

2. After writing the file, output this message to the user:

"Project evaluation complete. Summary available at:
.agent_planning/SUMMARY-project-evaluator-<timestamp>.txt

Quick results:
- Completion: X% (n/m components)
- Critical gaps: n ([list top 3])
- STATUS file: STATUS-<timestamp>.md
- Recommendation: [next step]"

Keep the console output under 8 lines. The file contains full details.
```

**Complexity**: Low - Template replacement with specific format requirements.

**Testing**: Run `/dev-loop:evaluate-and-plan`, verify SUMMARY-project-evaluator-*.txt exists and contains expected content.

---

#### Work Item 1.2: Update status-planner.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/status-planner.md`

**Location**: Lines 132-146 (existing "Final Summary (Required)" section)

**Changes**:
Replace existing section with:

```markdown
## Final Summary (Required)

At the end of your work:

1. Write summary to file: `.agent_planning/SUMMARY-status-planner-<YYYY-MM-DD-HHmmss>.txt`

Use this exact template:
```
Summary: [1-sentence description of planning outcome]
Agent: status-planner
Timestamp: <YYYY-MM-DD HH:MM:SS>

Key Results:
- Work items: n total (P0: x, P1: y, P2: z, P3: w)
- Top priority item: [name of highest priority item]
- Estimated complexity: [aggregate complexity assessment]

Files Generated:
- PLAN-<YYYY-MM-DD-HHmmss>.md
- SPRINT-<YYYY-MM-DD-HHmmss>.md (if sprint plan created)

Files Archived: n (moved to archive/ due to staleness/conflicts)

Recommendation: [next action - usually "Proceed with /dev-loop:test-and-implement or /dev-loop:impl-and-iterate"]
```

2. After writing the file, output this message to the user:

"Planning complete. Summary available at:
.agent_planning/SUMMARY-status-planner-<timestamp>.txt

Quick results:
- Work items: n (P0: x, P1: y, P2: z)
- Top priority: [highest priority item name]
- PLAN file: PLAN-<timestamp>.md
- Recommendation: [next step]"

Keep the console output under 8 lines. The file contains full details.
```

**Complexity**: Low - Template replacement following same pattern as 1.1.

**Testing**: Run `/dev-loop:evaluate-and-plan`, verify SUMMARY-status-planner-*.txt exists and contains expected content.

---

#### Work Item 1.3: Update work-evaluator.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/work-evaluator.md`

**Location**: Lines 84-98 (existing "Final Summary (Required)" section)

**Changes**:
Replace existing section with:

```markdown
## Final Summary (Required)

At the end of your work:

1. Write summary to file: `.agent_planning/SUMMARY-work-evaluator-<YYYY-MM-DD-HHmmss>.txt`

Use this exact template:
```
Summary: [1-sentence description of evaluation outcome]
Agent: work-evaluator
Timestamp: <YYYY-MM-DD HH:MM:SS>

Evaluation Result: [COMPLETE | INCOMPLETE | BLOCKED]

Key Results:
- Goals achieved: n of m
- Evidence collected: [screenshot count, log analysis, command outputs]
- Issues found: n ([brief list])

Files Generated:
- WORK-EVALUATION-<YYYY-MM-DD-HHmmss>.md
- screenshots/*.png (if web UI evaluated)

Recommendation: [COMPLETE: Proceed to next task | INCOMPLETE: Continue iteration | BLOCKED: User guidance needed]
```

2. After writing the file, output this message to the user:

"Work evaluation complete. Summary available at:
.agent_planning/SUMMARY-work-evaluator-<timestamp>.txt

Quick results:
- Status: [COMPLETE/INCOMPLETE/BLOCKED]
- Goals: n of m achieved
- Evidence: [key evidence summary]
- Recommendation: [next step]"

Keep the console output under 8 lines. The file contains full details.
```

**Complexity**: Low - Template replacement following same pattern.

**Testing**: Run `/dev-loop:impl-and-iterate` (includes work-evaluator), verify SUMMARY-work-evaluator-*.txt exists.

---

#### Work Item 1.4: Update functional-tester.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/functional-tester.md`

**Location**: Lines 487-500 (existing "Final Summary (Required)" section)

**Changes**:
Replace existing section with:

```markdown
## Final Summary (Required)

At the end of your work:

1. Write summary to file: `.agent_planning/SUMMARY-functional-tester-<YYYY-MM-DD-HHmmss>.txt`

Use this exact template:
```
Summary: [1-sentence description of test writing outcome]
Agent: functional-tester
Timestamp: <YYYY-MM-DD HH:MM:SS>

Key Results:
- Tests written: n total
- Test files: [list of test file paths]
- Coverage: [workflows/features covered]
- Test criteria met: [useful: yes/no, complete: yes/no, flexible: yes/no, automated: yes/no]

Files Generated:
- tests/functional/test_*.py (or equivalent for language)

Recommendation: [next action - usually "Run tests to verify they fail appropriately, then proceed with implementation"]
```

2. After writing the file, output this message to the user:

"Test writing complete. Summary available at:
.agent_planning/SUMMARY-functional-tester-<timestamp>.txt

Quick results:
- Tests written: n
- Test files: [list]
- Criteria: [status summary]
- Recommendation: [next step]"

Keep the console output under 8 lines. The file contains full details.
```

**Complexity**: Low - Template replacement following same pattern.

**Testing**: Run `/dev-loop:test-and-implement` (includes functional-tester), verify SUMMARY-functional-tester-*.txt exists.

---

#### Work Item 1.5: Update test-driven-implementer.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/test-driven-implementer.md`

**Location**: Lines 108-122 (existing "Final Summary (Required)" section)

**Changes**:
Replace existing section with:

```markdown
## Final Summary (Required)

At the end of your work:

1. Write summary to file: `.agent_planning/SUMMARY-test-driven-implementer-<YYYY-MM-DD-HHmmss>.txt`

Use this exact template:
```
Summary: [1-sentence description of implementation outcome]
Agent: test-driven-implementer
Timestamp: <YYYY-MM-DD HH:MM:SS>

Key Results:
- Tests now passing: n of m
- Implementation files: [list of modified/created files]
- Commits: n ([brief descriptions])
- Remaining failures: n ([brief list if any])

Files Generated/Modified:
- [list source files modified]

Recommendation: [All tests passing: Re-evaluate with /dev-loop:evaluate-and-plan | Tests still failing: Continue implementation]
```

2. After writing the file, output this message to the user:

"Implementation complete. Summary available at:
.agent_planning/SUMMARY-test-driven-implementer-<timestamp>.txt

Quick results:
- Tests passing: n of m
- Files modified: [count]
- Commits: n
- Recommendation: [next step]"

Keep the console output under 8 lines. The file contains full details.
```

**Complexity**: Low - Template replacement following same pattern.

**Testing**: Run `/dev-loop:test-and-implement` (includes test-driven-implementer), verify SUMMARY-test-driven-implementer-*.txt exists.

---

#### Work Item 1.6: Update iterative-implementer.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/iterative-implementer.md`

**Location**: Lines 76-90 (existing "Final Summary (Required)" section)

**Changes**:
Replace existing section with:

```markdown
## Final Summary (Required)

At the end of your work:

1. Write summary to file: `.agent_planning/SUMMARY-iterative-implementer-<YYYY-MM-DD-HHmmss>.txt`

Use this exact template:
```
Summary: [1-sentence description of implementation outcome]
Agent: iterative-implementer
Timestamp: <YYYY-MM-DD HH:MM:SS>

Key Results:
- Features implemented: [brief list]
- Implementation files: [list of modified/created files]
- Commits: n ([brief descriptions])
- Quality: [assessment - clean/needs-refactor/production-ready]

Files Generated/Modified:
- [list source files modified]

Recommendation: [next action - usually "Run work-evaluator to validate with runtime evidence"]
```

2. After writing the file, output this message to the user:

"Implementation complete. Summary available at:
.agent_planning/SUMMARY-iterative-implementer-<timestamp>.txt

Quick results:
- Features: [brief list]
- Files modified: [count]
- Commits: n
- Recommendation: [next step]"

Keep the console output under 8 lines. The file contains full details.
```

**Complexity**: Low - Template replacement following same pattern.

**Testing**: Run `/dev-loop:impl-and-iterate` (includes iterative-implementer), verify SUMMARY-iterative-implementer-*.txt exists.

---

#### Work Item 1.7: Update product-visionary.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/product-visionary.md`

**Location**: Lines 107-120 (existing "Final Summary (Required)" section)

**Changes**:
Replace existing section with:

```markdown
## Final Summary (Required)

At the end of your work:

1. Write summary to file: `.agent_planning/SUMMARY-product-visionary-<YYYY-MM-DD-HHmmss>.txt`

Use this exact template:
```
Summary: [1-sentence description of feature proposal outcome]
Agent: product-visionary
Timestamp: <YYYY-MM-DD HH:MM:SS>

Key Results:
- Features proposed: n
- Innovation level: [conservative/moderate/ambitious]
- Feasibility: [high/medium/low]
- User value: [high/medium/low]

Files Generated:
- FEATURE-PROPOSAL-<YYYY-MM-DD-HHmmss>.md

Recommendation: [next action - usually "Review proposal, then run /dev-loop:evaluate-and-plan to create implementation plan"]
```

2. After writing the file, output this message to the user:

"Feature proposal complete. Summary available at:
.agent_planning/SUMMARY-product-visionary-<timestamp>.txt

Quick results:
- Features proposed: n
- Innovation: [level]
- Feasibility: [assessment]
- Recommendation: [next step]"

Keep the console output under 8 lines. The file contains full details.
```

**Complexity**: Low - Template replacement following same pattern.

**Testing**: Run `/dev-loop:feature-proposal` (uses product-visionary), verify SUMMARY-product-visionary-*.txt exists.

---

### Phase 2: Command Visibility Enhancements (P0 - Critical)

**Goal**: Commands explicitly surface agent results to users through console messages that extract and display key metrics from generated files.

**Acceptance Criteria**:
- [ ] All 4 commands display progress updates after each agent completes
- [ ] Commands extract key metrics from generated files (STATUS, PLAN, etc.)
- [ ] Users see file paths for all generated artifacts
- [ ] Final aggregated summary displays after multi-agent commands complete
- [ ] Commands inform users of next recommended action

**Files to Modify**: 4 command files

#### Work Item 2.1: Update evaluate-and-plan.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/commands/evaluate-and-plan.md`

**Location**: Entire file (currently 17 lines)

**Changes**:
Replace content with enhanced version:

```markdown
---
argument-hint: [area of focus]
description: Evaluate the project and make an implementation plan.  Pass args to focus on something specific, or let Claude decide.  Designed to work with /dev-loop:test-and-implement
---

If specific areas of focus are defined below, focus entirely on those goals and architectural work to enable those goals.  If 'specific-areas-of-focus' is empty, use the PROJECT_SPEC.md file to evaluate the project as a whole.

Specific areas of focus:
<specific-areas-of-focus>
$ARGUMENTS
</specific-areas-of-focus>

**Step 1**: Use the dev-loop:project-evaluator agent to evaluate the current status of the project.

**Step 2**: After project-evaluator completes, display results to user:

Read the latest `.agent_planning/STATUS-*.md` file (highest timestamp) and extract:
- Overall completion percentage
- Top 3 critical gaps
- Status file path

Output to user:
"✅ Project evaluation complete

📊 Results:
- Completion: X% (n/m components)
- Critical gaps: [gap 1], [gap 2], [gap 3]
- STATUS file: .agent_planning/STATUS-<timestamp>.md
- Summary: .agent_planning/SUMMARY-project-evaluator-<timestamp>.txt

⏭️  Next: Running status-planner to create implementation backlog..."

**Step 3**: Only after project-evaluator has completed, use the dev-loop:status-planner agent to plan the remaining work for the project based on the output of Step 1.

**Step 4**: After status-planner completes, display results to user:

Read the latest `.agent_planning/PLAN-*.md` file (highest timestamp) and extract:
- Total work item count
- Priority breakdown (P0, P1, P2, P3 counts)
- Top priority item name
- PLAN file path

Output to user:
"✅ Planning complete

📋 Backlog:
- Work items: n total (P0: x, P1: y, P2: z, P3: w)
- Top priority: [item name]
- PLAN file: .agent_planning/PLAN-<timestamp>.md
- Summary: .agent_planning/SUMMARY-status-planner-<timestamp>.txt

🎯 Recommended next step:
- For TDD workflow: Run /dev-loop:test-and-implement
- For non-TDD workflow: Run /dev-loop:impl-and-iterate"

**Step 5**: Display final aggregated summary:

"
═══════════════════════════════════════════════════════════
Evaluation and Planning Complete
═══════════════════════════════════════════════════════════

📊 Project Status: X% complete (n/m components)
📋 Backlog: n work items (P0: x, P1: y)
🎯 Top Priority: [item name]

📁 Generated Files:
- .agent_planning/STATUS-<timestamp>.md
- .agent_planning/PLAN-<timestamp>.md
- .agent_planning/SUMMARY-project-evaluator-<timestamp>.txt
- .agent_planning/SUMMARY-status-planner-<timestamp>.txt

✨ Ready to implement! Choose your workflow:
- /dev-loop:test-and-implement (TDD - write tests first)
- /dev-loop:impl-and-iterate (Iterative - runtime validation)
═══════════════════════════════════════════════════════════
"
```

**Complexity**: Medium - Requires file reading and metric extraction logic.

**Testing**: Run `/dev-loop:evaluate-and-plan`, verify user sees all progress messages and final summary.

---

#### Work Item 2.2: Update test-and-implement.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/commands/test-and-implement.md`

**Location**: Entire file (TestLoop and ImplementLoop sections)

**Changes**:
Add progress messages after each agent invocation within loops:

1. After functional-tester in TestLoop:
   ```markdown
   After functional-tester completes:
   "✅ Tests written

   📝 Test Results:
   - Tests created: n
   - Test files: [list]
   - Summary: .agent_planning/SUMMARY-functional-tester-<timestamp>.txt

   ⏭️  Next: Evaluating tests against criteria..."
   ```

2. After project-evaluator in TestLoop:
   ```markdown
   After project-evaluator completes in TestLoop:
   "✅ Test evaluation complete

   📊 Criteria Check:
   - Useful: [yes/no]
   - Complete: [yes/no]
   - Flexible: [yes/no]
   - Automated: [yes/no]

   Decision: [CONTINUE TestLoop / EXIT TestLoop - criteria met]
   Reason: [brief explanation]"
   ```

3. After test-driven-implementer in ImplementLoop:
   ```markdown
   After test-driven-implementer completes:
   "✅ Implementation iteration complete

   🧪 Test Results:
   - Tests passing: n of m
   - Files modified: [count]
   - Commits: n
   - Summary: .agent_planning/SUMMARY-test-driven-implementer-<timestamp>.txt

   ⏭️  Next: Evaluating implementation quality..."
   ```

4. After project-evaluator in ImplementLoop:
   ```markdown
   After project-evaluator completes in ImplementLoop:
   "✅ Implementation evaluation complete

   📊 Quality Check:
   - Issues: n ([brief list])
   - Well-defined solutions: [yes/no for each issue]

   Decision: [CONTINUE ImplementLoop / EXIT ImplementLoop - no issues remain]
   Reason: [brief explanation]"
   ```

5. Final summary after all loops complete:
   ```markdown
   "
   ═══════════════════════════════════════════════════════════
   Test-Driven Implementation Complete
   ═══════════════════════════════════════════════════════════

   🧪 Tests: n written, all passing
   💻 Implementation: [files modified count] files
   📦 Commits: n total

   📁 Summary Files:
   - .agent_planning/SUMMARY-functional-tester-<timestamp>.txt
   - .agent_planning/SUMMARY-test-driven-implementer-<timestamp>.txt
   - .agent_planning/SUMMARY-project-evaluator-<timestamp>.txt (latest)

   ✨ Implementation complete and validated!
   🔄 Run /dev-loop:evaluate-and-plan to update project status
   ═══════════════════════════════════════════════════════════
   "
   ```

**Complexity**: Medium-High - Multiple loop iterations with conditional display logic.

**Testing**: Run `/dev-loop:test-and-implement`, verify progress messages appear throughout TestLoop and ImplementLoop.

---

#### Work Item 2.3: Update implement-and-iterate.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/commands/implement-and-iterate.md`

**Location**: Entire file (implementation/evaluation loop)

**Changes**:
Add progress messages after each agent invocation:

1. After iterative-implementer:
   ```markdown
   After iterative-implementer completes:
   "✅ Implementation iteration complete

   💻 Results:
   - Features: [brief list]
   - Files modified: [count]
   - Commits: n
   - Summary: .agent_planning/SUMMARY-iterative-implementer-<timestamp>.txt

   ⏭️  Next: Validating with runtime evidence..."
   ```

2. After work-evaluator:
   ```markdown
   After work-evaluator completes:
   "✅ Work evaluation complete

   📊 Validation Results:
   - Status: [COMPLETE/INCOMPLETE/BLOCKED]
   - Goals: n of m achieved
   - Evidence: [screenshot count, logs analyzed, etc.]
   - Issues: n ([brief list])
   - Summary: .agent_planning/SUMMARY-work-evaluator-<timestamp>.txt

   Decision: [CONTINUE loop / EXIT loop - work complete / BLOCKED - user input needed]
   Reason: [brief explanation]"
   ```

3. Final summary after loop completes:
   ```markdown
   "
   ═══════════════════════════════════════════════════════════
   Iterative Implementation Complete
   ═══════════════════════════════════════════════════════════

   Status: [COMPLETE/INCOMPLETE/BLOCKED]
   💻 Implementation: [iterations count] iterations
   📦 Commits: n total
   ✅ Goals: n of m achieved

   📁 Summary Files:
   - .agent_planning/SUMMARY-iterative-implementer-<timestamp>.txt (latest)
   - .agent_planning/SUMMARY-work-evaluator-<timestamp>.txt (latest)
   - .agent_planning/WORK-EVALUATION-<timestamp>.md

   [If COMPLETE]
   ✨ Implementation complete and validated!
   🔄 Run /dev-loop:evaluate-and-plan to update project status

   [If INCOMPLETE]
   ⚠️  Some goals not yet achieved. Review WORK-EVALUATION for details.
   Continue with another /dev-loop:impl-and-iterate cycle or adjust approach.

   [If BLOCKED]
   🛑 Implementation blocked. User guidance needed.
   Review WORK-EVALUATION for blocker details.
   ═══════════════════════════════════════════════════════════
   "
   ```

**Complexity**: Medium - Loop iterations with conditional display based on work-evaluator status.

**Testing**: Run `/dev-loop:impl-and-iterate`, verify progress messages and appropriate final summary.

---

#### Work Item 2.4: Update feature-proposal.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/commands/feature-proposal.md`

**Location**: Entire file

**Changes**:
Add progress message after product-visionary completes:

```markdown
After product-visionary completes:

"✅ Feature proposal complete

💡 Proposal:
- Features: n proposed
- Innovation: [conservative/moderate/ambitious]
- Feasibility: [high/medium/low]
- User value: [high/medium/low]

📁 Generated Files:
- .agent_planning/FEATURE-PROPOSAL-<timestamp>.md
- .agent_planning/SUMMARY-product-visionary-<timestamp>.txt

🎯 Next Steps:
1. Review the feature proposal
2. If approved, run /dev-loop:evaluate-and-plan to create implementation backlog
3. Proceed with /dev-loop:test-and-implement or /dev-loop:impl-and-iterate
"
```

**Complexity**: Low - Single agent invocation, straightforward display.

**Testing**: Run `/dev-loop:feature-proposal`, verify summary displays.

---

### Phase 3: Loop Progress Indicators (P1 - High Value)

**Goal**: Improve transparency for long-running loop-based commands by showing iteration counts and progress signals.

**Acceptance Criteria**:
- [ ] TestLoop shows iteration count (e.g., "TestLoop iteration 2/estimated 3")
- [ ] ImplementLoop shows iteration count and cumulative test pass count
- [ ] work-evaluator loop shows iteration count and goal progress
- [ ] Users understand why loops continue or exit
- [ ] Loop summaries show total iterations completed

**Files to Modify**: 2 command files (test-and-implement.md, implement-and-iterate.md)

#### Work Item 3.1: Add TestLoop iteration tracking to test-and-implement.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/commands/test-and-implement.md`

**Location**: TestLoop section

**Changes**:

1. Add iteration counter initialization before TestLoop:
   ```markdown
   Before entering TestLoop, initialize: testloop_iteration = 1
   ```

2. Modify TestLoop progress messages to include iteration:
   ```markdown
   "✅ Tests written (TestLoop iteration {testloop_iteration})

   📝 Test Results:
   - Tests created: n (cumulative: N total)
   - Test files: [list]
   - Summary: .agent_planning/SUMMARY-functional-tester-<timestamp>.txt

   ⏭️  Next: Evaluating tests against criteria..."
   ```

3. Increment counter at end of each TestLoop iteration:
   ```markdown
   At end of TestLoop iteration: testloop_iteration += 1
   ```

4. Include iteration summary in TestLoop exit message:
   ```markdown
   "✅ TestLoop complete after {testloop_iteration} iterations

   All test criteria met:
   ✓ Useful - validates real user workflows
   ✓ Complete - covers all acceptance criteria
   ✓ Flexible - allows implementation freedom
   ✓ Automated - runs without manual intervention

   ⏭️  Next: Beginning implementation to make tests pass..."
   ```

**Complexity**: Low-Medium - Requires counter management across loop iterations.

**Testing**: Run `/dev-loop:test-and-implement` with conditions requiring multiple TestLoop iterations, verify iteration counts display correctly.

---

#### Work Item 3.2: Add ImplementLoop iteration tracking to test-and-implement.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/commands/test-and-implement.md`

**Location**: ImplementLoop section

**Changes**:

1. Add iteration counter initialization before ImplementLoop:
   ```markdown
   Before entering ImplementLoop, initialize: implementloop_iteration = 1
   ```

2. Modify ImplementLoop progress messages to include iteration and cumulative progress:
   ```markdown
   "✅ Implementation iteration {implementloop_iteration} complete

   🧪 Test Results:
   - Tests passing: n of m (up from X in previous iteration)
   - Files modified: [count] (cumulative: N files)
   - Commits: n this iteration (cumulative: N commits)
   - Summary: .agent_planning/SUMMARY-test-driven-implementer-<timestamp>.txt

   ⏭️  Next: Evaluating implementation quality..."
   ```

3. Increment counter at end of each ImplementLoop iteration:
   ```markdown
   At end of ImplementLoop iteration: implementloop_iteration += 1
   ```

4. Include iteration summary in ImplementLoop exit message:
   ```markdown
   "✅ ImplementLoop complete after {implementloop_iteration} iterations

   🧪 All tests passing: n of n
   📦 Total commits: N
   💻 Files modified: N

   Implementation meets quality standards:
   ✓ All tests pass
   ✓ No outstanding issues with clear solutions
   ✓ Code ready for production

   ⏭️  Next: Re-evaluating project status..."
   ```

**Complexity**: Low-Medium - Requires counter management and cumulative metric tracking.

**Testing**: Run `/dev-loop:test-and-implement` with conditions requiring multiple ImplementLoop iterations, verify iteration counts and cumulative metrics.

---

#### Work Item 3.3: Add iteration tracking to implement-and-iterate.md

**File**: `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/commands/implement-and-iterate.md`

**Location**: Implementation/evaluation loop section

**Changes**:

1. Add iteration counter initialization before loop:
   ```markdown
   Before entering loop, initialize: iteration = 1
   ```

2. Modify progress messages to include iteration and goal progress:
   ```markdown
   After iterative-implementer:
   "✅ Implementation iteration {iteration} complete

   💻 Results:
   - Features: [brief list] (cumulative: N features)
   - Files modified: [count] (cumulative: N files)
   - Commits: n this iteration (cumulative: N commits)
   - Summary: .agent_planning/SUMMARY-iterative-implementer-<timestamp>.txt

   ⏭️  Next: Validating with runtime evidence..."

   After work-evaluator:
   "✅ Work evaluation iteration {iteration} complete

   📊 Validation Results:
   - Status: [COMPLETE/INCOMPLETE/BLOCKED]
   - Goals: n of m achieved (progress: X% → Y%)
   - Evidence: [screenshot count, logs analyzed, etc.]
   - Issues: n ([brief list])
   - Summary: .agent_planning/SUMMARY-work-evaluator-<timestamp>.txt

   Decision: [CONTINUE iteration {iteration + 1} / EXIT loop - work complete / BLOCKED - user input needed]
   Reason: [brief explanation]"
   ```

3. Increment counter at end of each loop iteration:
   ```markdown
   At end of loop iteration: iteration += 1
   ```

4. Include iteration summary in final exit message:
   ```markdown
   "
   ═══════════════════════════════════════════════════════════
   Iterative Implementation Complete
   ═══════════════════════════════════════════════════════════

   Status: [COMPLETE/INCOMPLETE/BLOCKED]
   🔄 Iterations: {iteration} cycles
   💻 Total commits: N
   ✅ Goals: n of m achieved

   📊 Progress:
   - Iteration 1: [goals achieved]
   - Iteration 2: [goals achieved]
   ...
   - Iteration {iteration}: [final status]

   [rest of final summary...]
   ═══════════════════════════════════════════════════════════
   "
   ```

**Complexity**: Medium - Requires iteration tracking and goal progress percentage calculation.

**Testing**: Run `/dev-loop:impl-and-iterate` with conditions requiring multiple iterations, verify progress percentages and iteration summaries.

---

## Dependency Graph

```
Phase 1 (File-Based Summaries)
├─ 1.1 project-evaluator.md      [Independent]
├─ 1.2 status-planner.md          [Independent]
├─ 1.3 work-evaluator.md          [Independent]
├─ 1.4 functional-tester.md       [Independent]
├─ 1.5 test-driven-implementer.md [Independent]
├─ 1.6 iterative-implementer.md   [Independent]
└─ 1.7 product-visionary.md       [Independent]

Phase 2 (Command Visibility)
├─ 2.1 evaluate-and-plan.md       [Depends on: 1.1, 1.2]
├─ 2.2 test-and-implement.md      [Depends on: 1.1, 1.4, 1.5]
├─ 2.3 implement-and-iterate.md   [Depends on: 1.3, 1.6]
└─ 2.4 feature-proposal.md        [Depends on: 1.7]

Phase 3 (Loop Progress)
├─ 3.1 TestLoop tracking          [Depends on: 2.2]
├─ 3.2 ImplementLoop tracking     [Depends on: 2.2]
└─ 3.3 iterate loop tracking      [Depends on: 2.3]
```

**Critical Path**: 1.1 → 1.2 → 2.1 (for evaluate-and-plan workflow)

---

## Recommended Implementation Order

### Sprint 1: Core Visibility (P0 - Days 1-3)
1. Work Item 1.1: project-evaluator.md
2. Work Item 1.2: status-planner.md
3. Work Item 2.1: evaluate-and-plan.md
4. **Test Milestone**: Run `/dev-loop:evaluate-and-plan`, verify full visibility

### Sprint 2: TDD Workflow Visibility (P0 - Days 4-6)
5. Work Item 1.4: functional-tester.md
6. Work Item 1.5: test-driven-implementer.md
7. Work Item 2.2: test-and-implement.md
8. **Test Milestone**: Run `/dev-loop:test-and-implement`, verify full visibility

### Sprint 3: Non-TDD Workflow Visibility (P0 - Days 7-9)
9. Work Item 1.3: work-evaluator.md
10. Work Item 1.6: iterative-implementer.md
11. Work Item 2.3: implement-and-iterate.md
12. **Test Milestone**: Run `/dev-loop:impl-and-iterate`, verify full visibility

### Sprint 4: Feature Proposal + Loop Enhancements (P1 - Days 10-11)
13. Work Item 1.7: product-visionary.md
14. Work Item 2.4: feature-proposal.md
15. Work Item 3.1: TestLoop iteration tracking
16. Work Item 3.2: ImplementLoop iteration tracking
17. Work Item 3.3: iterate loop tracking
18. **Final Test Milestone**: Run all commands, verify complete visibility

---

## Risk Assessment

### High-Risk Items

**None** - All changes are additive (new summary output) or display-only (command messages). No behavior changes to core agent logic.

### Medium-Risk Items

**Work Item 2.2, 2.3** (Loop visibility):
- **Risk**: Commands must extract metrics from generated files (STATUS, PLAN, etc.)
- **Mitigation**: File formats are well-defined. Use Read tool to extract specific sections.
- **Fallback**: If extraction fails, display generic message with file path only.

**Work Item 3.1, 3.2, 3.3** (Iteration tracking):
- **Risk**: Loop counter management across subagent invocations may be unreliable
- **Mitigation**: Test thoroughly with multi-iteration scenarios
- **Fallback**: Iteration count not critical to functionality - can be approximate or omitted if unreliable

### Low-Risk Items

**All Phase 1 items** (1.1-1.7):
- Simple template additions to existing summary sections
- File I/O operations that agents already perform
- No complex logic or dependencies

---

## Testing Strategy

### Unit Testing (Per Work Item)

After each work item completion:
1. Identify which slash command invokes the modified agent
2. Run that command with minimal input
3. Verify:
   - SUMMARY-*.txt file appears in `.agent_planning/`
   - Summary file contains all required template fields
   - Console message displays to user (visible without ctrl-o)
   - Console message contains correct file path

### Integration Testing (Per Sprint)

After each sprint completion:
1. Run the primary workflow command (e.g., `/dev-loop:evaluate-and-plan`)
2. Verify:
   - All agents produce summaries
   - Progress messages display after each agent
   - Final aggregated summary displays
   - All file paths are correct and files exist
   - User can navigate workflow without manual file inspection

### End-to-End Testing (After Phase 3)

Run complete workflows:
1. `/dev-loop:evaluate-and-plan` → verify two-agent visibility
2. `/dev-loop:test-and-implement` → verify loop visibility, iteration counts
3. `/dev-loop:impl-and-iterate` → verify loop visibility, goal progress
4. `/dev-loop:feature-proposal` → verify single-agent visibility

### Manual Validation Criteria

For each command, confirm:
- [ ] User sees agent completion without pressing ctrl-o
- [ ] User knows which files were generated
- [ ] User understands key results (metrics, gaps, recommendations)
- [ ] User knows what to do next
- [ ] Loop progress is transparent (for loop-based commands)

---

## Complexity Estimates

### Phase 1 (File-Based Summaries)
- **1.1-1.7**: Low complexity (x7 items)
- **Aggregate**: Medium complexity
- **Reasoning**: Repetitive template changes, low risk, straightforward file I/O

### Phase 2 (Command Visibility)
- **2.1**: Medium complexity (file extraction, aggregation)
- **2.2**: Medium-High complexity (multi-agent, multi-loop, conditionals)
- **2.3**: Medium complexity (loop with conditionals)
- **2.4**: Low complexity (single agent)
- **Aggregate**: High complexity
- **Reasoning**: Requires file reading, metric extraction, conditional logic, multi-agent coordination

### Phase 3 (Loop Progress)
- **3.1-3.3**: Low-Medium complexity (x3 items)
- **Aggregate**: Medium complexity
- **Reasoning**: Counter management, cumulative metrics, but straightforward logic

### Overall Project Complexity
**Medium-High** - Well-structured changes with clear patterns, but significant scope (12 files, multiple integration points).

---

## Quality Metrics

### Current State (Before Implementation)
- **User Visibility**: 0% - Summaries hidden without ctrl-o
- **File Discoverability**: 20% - Files exist but users unaware
- **Progress Transparency**: 10% - Agent invocation visible only
- **User Frustration**: HIGH - Disconnected from agent work
- **Workflow Clarity**: 30% - Users guess what happened

### Target State (After Phase 1)
- **User Visibility**: 60% - Summary files written, console messages displayed
- **File Discoverability**: 100% - All files announced to user
- **Progress Transparency**: 40% - Agent completion visible
- **User Frustration**: MEDIUM - Must read summary files
- **Workflow Clarity**: 60% - Key results visible

### Target State (After Phase 2)
- **User Visibility**: 95% - All key metrics displayed inline + files available
- **File Discoverability**: 100% - All files announced with context
- **Progress Transparency**: 80% - Multi-agent progress visible
- **User Frustration**: LOW - Immediate clarity on results
- **Workflow Clarity**: 90% - Clear progress and recommendations

### Target State (After Phase 3)
- **User Visibility**: 100% - Complete transparency
- **File Discoverability**: 100% - All files announced with context
- **Progress Transparency**: 95% - Loop iterations and decisions explained
- **User Frustration**: VERY LOW - Full understanding
- **Workflow Clarity**: 100% - Crystal clear progress and outcomes

---

## Architectural Considerations

### Why This Solution Respects Claude Code Architecture

**Claude Code Design**: Subagent isolation preserves main context, enables parallel execution, reduces noise.

**Our Approach**:
1. **Files**: Agents already write STATUS/PLAN files - adding SUMMARY files is consistent
2. **Console Messages**: Orchestrating commands (not subagents) display results - respects isolation
3. **No Hacks**: Uses existing tool capabilities (file I/O, message output) without workarounds

**Trade-offs**:
- Adds ~7 new SUMMARY-*.txt files to `.agent_planning/` (minimal disk impact)
- Commands become slightly longer with display logic (improves UX, worth complexity)
- Some duplication (summary in file + console) - necessary for both durability and immediacy

### File Retention Policy

SUMMARY files follow same retention as STATUS/PLAN:
- Max 4 SUMMARY-*.txt files per agent
- Delete oldest when creating new file
- Prevents directory bloat
- Consistent with existing cleanup patterns

**Implementation Note**: status-planner already implements cleanup logic - reuse pattern for SUMMARY files.

---

## Documentation Updates

After implementation, update these docs:

### plugins/dev-loop/CLAUDE.md

Add new section after "Command Reference":

```markdown
## Expected Output and Visibility

### What Users See During Command Execution

All dev-loop commands provide progressive visibility into subagent work:

**During Execution**:
1. Agent invocation message (e.g., "Using dev-loop:project-evaluator...")
2. Tool usage approvals (file reads/writes)
3. Progress messages after each agent completes
4. Final aggregated summary

**After Execution**:
1. Generated files in `.agent_planning/` directory
2. Summary files (SUMMARY-*.txt) for each agent
3. Status/Plan/Evaluation files with full details

### Summary Files

Each agent writes a SUMMARY-<agent-name>-<timestamp>.txt file containing:
- 1-sentence outcome summary
- Key metrics and results
- Generated file paths
- Recommended next action

**Example**: After running `/dev-loop:evaluate-and-plan`:
- `.agent_planning/SUMMARY-project-evaluator-2025-11-29-130400.txt`
- `.agent_planning/SUMMARY-status-planner-2025-11-29-130415.txt`

### Console Output Format

Commands display structured progress messages:

```
✅ [Agent] complete

📊 Results:
- [Key metric 1]
- [Key metric 2]
- [Key metric 3]

⏭️  Next: [What happens next]
```

Loop-based commands also show:
- Iteration count (e.g., "TestLoop iteration 2")
- Cumulative progress (e.g., "Tests passing: 5 of 8 (up from 3)")
- Loop exit decisions with reasoning

### Troubleshooting Visibility Issues

If you don't see agent summaries:

1. **Check summary files**: Look in `.agent_planning/SUMMARY-*.txt`
2. **Check command output**: Scroll up for progress messages
3. **Press ctrl-o**: Expands full message history including subagent context
4. **Verify command version**: Older commands may lack visibility enhancements
```

---

## Blockers and Questions

**None identified** - Implementation path is clear and well-defined based on STATUS report analysis.

---

## Files Requiring Modification (Summary)

**Phase 1** (7 files):
1. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/project-evaluator.md`
2. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/status-planner.md`
3. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/work-evaluator.md`
4. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/functional-tester.md`
5. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/test-driven-implementer.md`
6. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/iterative-implementer.md`
7. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/agents/product-visionary.md`

**Phase 2** (4 files):
8. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/commands/evaluate-and-plan.md`
9. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/commands/test-and-implement.md`
10. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/commands/implement-and-iterate.md`
11. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/commands/feature-proposal.md`

**Phase 3** (2 files - same as 9, 10):
- test-and-implement.md (additional modifications)
- implement-and-iterate.md (additional modifications)

**Documentation** (1 file):
12. `/Users/bmf/Library/Mobile Documents/com~apple~CloudDocs/_mine/icode/loom99-claude-marketplace/plugins/dev-loop/CLAUDE.md`

**Total**: 12 unique files requiring modification

---

**Summary:** Implementation plan created for subagent visibility problem - hybrid file-based + console echo solution across 3 phases
- Phases: P0 file summaries (7 agents), P0 command visibility (4 commands), P1 loop progress (2 commands)
- Work items: 17 total (7 agent updates, 4 command updates, 3 loop enhancements, 3 documentation)
- Complexity: Medium-High (well-structured patterns, significant scope)
- Testing: Unit tests per item, integration per sprint, E2E after Phase 3
- Risk: Low (additive changes, no behavior modifications, clear fallbacks)
