# Route Subcommands Examples

Detailed examples of parsing and routing `/do:*` commands.

## Example 1: Pre and Post Commands

**Input**: `/do:it /do:explore understand auth, then /do:plan. Fix the login bug. /do:chores cleanup temp files`

**Analysis**:
- Pre-commands: `/do:explore understand auth`, `/do:plan`
- Main instructions: `Fix the login bug.`
- Post-commands: `/do:chores cleanup temp files`

**Execution Order**:
1. `/do:explore understand auth Fix the login bug.`
2. `/do:plan Fix the login bug.`
3. Main `/do:it` workflow with "Fix the login bug."
4. `/do:chores cleanup temp files Fix the login bug.`

---

## Example 2: Only Pre-Commands

**Input**: `/do:it First /do:plan, then implement the auth system`

**Analysis**:
- Pre-commands: `/do:plan`
- Main instructions: `implement the auth system`
- Post-commands: none

**Execution**:
1. `/do:plan implement the auth system`
2. Main `/do:it` workflow with "implement the auth system"

---

## Example 3: Only Post-Commands

**Input**: `/do:it Fix the bug, then /do:chores`

**Analysis**:
- Pre-commands: none
- Main instructions: `Fix the bug`
- Post-commands: `/do:chores`

**Execution**:
1. Main `/do:it` workflow with "Fix the bug"
2. `/do:chores Fix the bug`

---

## Example 4: No Subcommands

**Input**: `/do:it Fix the login bug`

**Analysis**:
- Pre-commands: none
- Main instructions: `Fix the login bug`
- Post-commands: none

Skill returns immediately, no SlashCommand calls needed.

---

## Example 5: Multiple Pre-Commands in Sequence

**Input**: `/do:it /do:explore auth, /do:research JWT, /do:plan. Build login system`

**Analysis**:
- Pre-commands: `/do:explore auth`, `/do:research JWT`, `/do:plan`
- Main instructions: `Build login system`
- Post-commands: none

**Execution**:
1. `/do:explore auth Build login system`
2. `/do:research JWT Build login system`
3. `/do:plan Build login system`
4. Main `/do:it` workflow

---

## Example 6: Complex Chain with Documentation

**Input**: `/do:it First /do:plan, implement feature, then /do:docs readme and /do:chores`

**Analysis**:
- Pre-commands: `/do:plan`
- Main instructions: `implement feature`
- Post-commands: `/do:docs readme`, `/do:chores`

**Execution**:
1. `/do:plan implement feature`
2. Main `/do:it` workflow
3. `/do:docs readme implement feature`
4. `/do:chores implement feature`
