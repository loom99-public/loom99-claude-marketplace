---
name: init-project
description: Initialize a new project or major architectural component. Use when user wants to start a new project, make architectural changes, or create a new subsystem.
---

# Initialize Project

Transform user intent into concrete project foundation.

## Process

Use do3:project-architect agent to:

1. **Classify scenario**: New project, architectural change, greenfield addition, migration, or feature design
2. **Adaptive interview**: 15-25 relevant questions with options and tradeoffs
3. **Generate**: PROJECT_SPEC.md with 7 sections (Overview, Architecture, Tech Stack, Workflow, ADRs, Roadmap, Future)
4. **Scaffold** (if new): Directory structure, skeleton files, package setup

## Output

Display summary:
```
═══════════════════════════════════════
Project Initialized
  Spec: .agent_planning/PROJECT_SPEC.md
  Type: [new project | architectural change | ...]
Next: /do3:plan to start implementation planning
═══════════════════════════════════════
```
