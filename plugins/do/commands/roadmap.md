---
argument-hint: [topic to add to roadmap]
description: "View roadmap tree or add topic. No args = show tree view. With args = add to roadmap."
---

Skill("roadmap-skill") with:
  mode: "add" ? $ARGUMENTS == "" : "view"
  topic: topic

