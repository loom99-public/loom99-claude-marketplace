---
argument-hint: [code|planning|security|competitive|tests|everything]
description: Comprehensive audit across code quality, planning, security, competitive, and test coverage dimensions. Invoke audit-master skill.
---

Comprehensive audit command. Routes to `audit-master` skill.

<user-input>$ARGUMENTS</user-input>
<current-command>audit</current-command>

## Subcommand Detection

**Quick check**: Does `$ARGUMENTS` contain `/do:` patterns (other than the current command)?

- **If NO** → `main_instructions = $ARGUMENTS`, proceed
- **If YES** → Invoke `do:route-subcommands` skill, then proceed with returned `main_instructions`

---

## Main Workflow

**Use the Skill tool** to invoke `audit-master` skill with `main_instructions` as context.

The skill will:
1. Detect which dimensions to audit based on `main_instructions`
2. Prompt user if no dimensions specified
3. Run selected audit dimensions
4. Output combined audit report

---

## Post-Commands

If subcommands were detected and `post_commands` is non-empty, execute them now.
