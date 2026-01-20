---
name: roadmap-skill
description: "Parse and manipulate ROADMAP.md files for hierarchical project planning with phases and topics. Entry point for /do:roadmap command."
context: fork
---

# Roadmap Skill

## Purpose

Parse, query, and update `.agent_planning/ROADMAP.md` files that define project phases and topics. Provides structured access to roadmap data for visualization and manipulation.

## When to Use

- Reading roadmap to display tree view
- Checking if a topic exists (similarity matching)
- Adding new topics to phases (single or batch)
- Updating topic states or metadata
- Generating topic status reports
- Migrating non-compliant roadmaps to schema format

**Multi-item support**: Input can contain multiple topics separated by newlines, semicolons, or as numbered/bulleted lists. Priority markers (P1, P2) auto-assign phases. File references are preserved as context.

## Entry Point

This skill serves as the implementation for `/do:roadmap`. The command invokes this skill with:

```
Skill("do:roadmap-skill") with:
  topic: "<topic-string>" | null
```

### Execute Command (Entry Point)

**Input**:
- `mode`: Either "view" (no arguments) or "add" (with topic argument)
- `topic`: Topic string to add (only used in "add" mode)

**Output**: Formatted text for display to user

**Flow**:

```python
def execute_command(mode: str, topic: str | None) -> str:
    """Entry point for /do:roadmap command"""

    # Handle migration request
    if mode == "view" and topic and "migrate" in topic.lower():
        return execute_migration()

    if mode == "view":
        # View mode: display roadmap tree
        if not file_exists(".agent_planning/ROADMAP.md"):
            return """No roadmap yet.

Run /do:roadmap <topic> to create your first roadmap with a topic.

Example: /do:roadmap user-authentication"""

        roadmap = parse_roadmap(".agent_planning/ROADMAP.md")
        return format_tree_view(roadmap)

    elif mode == "add":
        # Add mode: full add flow (handles single or batch input)
        return execute_add_flow(topic)

def execute_add_flow(topic_input: str) -> str:
    """Handle adding topic(s) to the roadmap (single or batch)"""

    # Step 1: Detect if input contains multiple topics
    topics = detect_multiple_topics(topic_input)

    if len(topics) > 1:
        # Batch mode: add multiple topics
        return execute_batch_add(topics)
    else:
        # Single mode: existing flow
        return execute_single_add(topic_input)

def execute_single_add(topic_input: str) -> str:
    """Handle adding a single topic to the roadmap"""

    # Step 1: Check/create ROADMAP.md
    if not file_exists(".agent_planning/ROADMAP.md"):
        roadmap = initialize_roadmap()
        # Skip similarity check - roadmap is empty
        selected_phase_num = 1
    else:
        roadmap = parse_roadmap(".agent_planning/ROADMAP.md")

        # Step 2: Similarity check (LLM-based)
        all_topics = list_all_topics(roadmap)
        similar = llm_check_similarity(topic_input, all_topics)

        if similar:
            # Step 3: Disambiguation (use do:prompt-questioning)
            choice = prompt_user_disambiguation(similar, topic_input)
            if choice == "view_status":
                return format_status_report(get_topic_status(similar["name"], roadmap))
            elif choice == "cancel":
                return "Cancelled."
            # else: continue to add as new topic

        # Step 4: Phase selection (use do:prompt-questioning)
        selected_phase_num = prompt_user_phase_selection(roadmap)

    # Step 5: Capture summary with context guidance
    topic_summary = prompt_user_for_summary(topic_input)

    # NEW: Step 5b: Validate context sufficiency
    is_sufficient, feedback = validate_context_sufficiency({"summary": topic_summary})
    if not is_sufficient:
        # Prompt for more context
        additional_context = prompt_for_additional_context(feedback)
        topic_summary = f"{topic_summary} | {additional_context}"

    # Step 6: Create beads epic
    topic_slug = to_kebab_case(topic_input)
    try:
        epic_id = create_beads_epic(topic_slug)
    except:
        epic_id = None  # Continue without epic

    # Step 7: Create topic directory
    mkdir(f".agent_planning/{topic_slug}/")

    # Step 8: Add to roadmap
    roadmap = add_topic_to_phase(
        topic_name=topic_slug,
        phase_num=selected_phase_num,
        roadmap=roadmap,
        summary=topic_summary,
        epic=epic_id
    )

    # Step 9: Write file
    content = write_roadmap(roadmap)
    write_file(".agent_planning/ROADMAP.md", content)

    # Step 10: Return confirmation
    phase = next(p for p in roadmap["phases"] if p["number"] == selected_phase_num)
    return f"""✓ Added topic to roadmap

Topic: {topic_slug}
Phase: Phase {selected_phase_num}: {phase['name']}
State: PROPOSED
Directory: .agent_planning/{topic_slug}/
Epic: {epic_id or "None (create with bd)"}

Next steps:
  1. Run /do:plan {topic_slug} to create a detailed plan
  2. Edit .agent_planning/ROADMAP.md to add dependencies or labels
  3. View roadmap: /do:roadmap"""
```

**User Interaction**: The add flow uses the `do:prompt-questioning` skill for:
- Disambiguation when similar topic found
- Phase selection
- Summary capture

## Core Procedures

### Procedure 1: Parse ROADMAP.md

Reads `.agent_planning/ROADMAP.md` and returns structured data.

**Input**: Path to ROADMAP.md file (default: `.agent_planning/ROADMAP.md`)

**Output**: Structured roadmap data or empty structure if file doesn't exist

**Algorithm**:

```python
# Pseudocode for parsing

def parse_roadmap(path):
    if not file_exists(path):
        return {"version": "1.0", "phases": []}

    content = read_file(path)

    # Parse YAML frontmatter
    frontmatter = parse_yaml_frontmatter(content)
    version = frontmatter.get("version", "1.0")
    created = frontmatter.get("created", "")
    updated = frontmatter.get("updated", "")

    # Parse phases and topics
    phases = []
    current_phase = None
    current_topics = []

    for line in content.split("\n"):
        # Phase header: ## Phase N: Name
        if match := re.match(r"^##\s+Phase\s+(\d+):\s+(.+)$", line):
            if current_phase:
                current_phase["topics"] = current_topics
                phases.append(current_phase)

            current_phase = {
                "number": int(match.group(1)),
                "name": match.group(2).strip(),
                "topics": []
            }
            current_topics = []

        # Phase metadata: Goal: ...
        elif current_phase and line.startswith("Goal:"):
            current_phase["goal"] = line.split(":", 1)[1].strip()

        # Phase metadata: Status: ...
        elif current_phase and line.startswith("Status:"):
            current_phase["status"] = line.split(":", 1)[1].strip()

        # Topic line: - topic-slug [STATE]
        elif match := re.match(r"^-\s+([a-z0-9-]+)\s+\[([A-Z\s]+)\]", line):
            topic = {
                "name": match.group(1),
                "state": match.group(2).strip()
            }
            current_topics.append(topic)

        # Topic metadata: - Summary: ...
        elif current_topics and line.strip().startswith("- Summary:"):
            current_topics[-1]["summary"] = line.split(":", 1)[1].strip()

        # Topic metadata: - Epic: ...
        elif current_topics and line.strip().startswith("- Epic:"):
            current_topics[-1]["epic"] = line.split(":", 1)[1].strip()

        # Topic metadata: - Directory: ...
        elif current_topics and line.strip().startswith("- Directory:"):
            current_topics[-1]["directory"] = line.split(":", 1)[1].strip()

        # Topic metadata: - Dependencies: ...
        elif current_topics and line.strip().startswith("- Dependencies:"):
            deps = line.split(":", 1)[1].strip()
            current_topics[-1]["dependencies"] = [d.strip() for d in deps.split(",")]

        # Topic metadata: - Labels: ...
        elif current_topics and line.strip().startswith("- Labels:"):
            labels = line.split(":", 1)[1].strip()
            current_topics[-1]["labels"] = [l.strip() for l in labels.split(",")]

    # Add final phase
    if current_phase:
        current_phase["topics"] = current_topics
        phases.append(current_phase)

    return {
        "version": version,
        "created": created,
        "updated": updated,
        "phases": phases
    }
```

**Error Handling**:
- Missing file → Return empty structure
- Parse error → Return partial structure with warnings
- Unknown fields → Ignore (forward compatibility)
- Malformed lines → Skip and continue

### Procedure 1b: Migrate Non-Compliant ROADMAP Format

Detects and migrates non-schema-compliant roadmaps (like cherry-chrome-mcp's narrative format) to expected schema.

**Input**: Path to ROADMAP.md file (default: `.agent_planning/ROADMAP.md`)

**Output**: Migrated roadmap structure ready for write_roadmap(), or error message

**Detection heuristics**:

```python
def detect_migration_needed(path: str) -> tuple[bool, str]:
    """Check if file needs migration. Returns (needs_migration, reason)"""
    if not file_exists(path):
        return False, "File does not exist"

    content = read_file(path)

    # Missing YAML frontmatter → non-compliant
    if not content.strip().startswith("---"):
        return True, "Missing YAML frontmatter"

    # Uses H4 headers (####) for topics → non-compliant
    if "####" in content:
        return True, "Uses H4 headers instead of list items for topics"

    # Has custom fields (Description, Tools, Pain point) → may need migration
    if any(field in content for field in ["**Description**", "**Tools", "**Pain point"]):
        return True, "Contains custom narrative fields"

    # Already compliant (has valid frontmatter and list-based topics)
    return False, "Already compliant with schema"
```

**Migration algorithm** (for cherry-chrome-mcp format):

```python
def migrate_roadmap_format(path: str) -> dict:
    """Detect and migrate non-schema-compliant roadmaps to expected format"""

    content = read_file(path)

    # Initialize structure
    roadmap = {
        "version": "1.0",
        "created": current_timestamp(),
        "updated": current_timestamp(),
        "phases": []
    }

    current_phase = None
    current_topic = None
    phase_number = 0

    for line in content.split("\n"):
        # Phase headers: ## Phase N: Name or similar patterns
        if match := re.match(r"^##\s+Phase\s+(\d+):\s+(.+?)(?:\s+\[([A-Z]+)\])?$", line):
            # Save previous topic and phase
            if current_topic and current_phase:
                # Compile topic summary from collected parts
                if "summary_parts" in current_topic:
                    current_topic["summary"] = " | ".join(current_topic["summary_parts"])
                    del current_topic["summary_parts"]
                current_phase["topics"].append(current_topic)
                current_topic = None

            if current_phase:
                roadmap["phases"].append(current_phase)

            # Create new phase
            phase_number = int(match.group(1))
            status = match.group(3).lower() if match.group(3) else ("active" if phase_number == 1 else "queued")

            current_phase = {
                "number": phase_number,
                "name": match.group(2).strip(),
                "status": status,
                "topics": []
            }

        # Phase metadata: Goal: ...
        elif current_phase and line.strip().startswith("Goal:"):
            current_phase["goal"] = line.split(":", 1)[1].strip()

        # Phase metadata: Status: ...
        elif current_phase and line.strip().startswith("Status:"):
            current_phase["status"] = line.split(":", 1)[1].strip().lower()

        # Topic headers: #### topic-slug [STATE] or similar
        elif match := re.match(r"^####\s+([a-z0-9-]+)(?:\s+\[([A-Z\s]+)\])?", line):
            # Save previous topic
            if current_topic and current_phase:
                if "summary_parts" in current_topic:
                    current_topic["summary"] = " | ".join(current_topic["summary_parts"])
                    del current_topic["summary_parts"]
                current_phase["topics"].append(current_topic)

            # Create new topic
            current_topic = {
                "name": match.group(1),
                "state": match.group(2).strip() if match.group(2) else "PROPOSED",
                "directory": f".agent_planning/{match.group(1)}/",
                "summary_parts": []
            }

        # Extract context from custom fields
        elif current_topic:
            if line.strip().startswith("**Description**:"):
                desc = line.split(":", 1)[1].strip()
                if desc:
                    current_topic["summary_parts"].append(desc)
            elif line.strip().startswith("**Tools to implement**:"):
                # Mark section start, collect subsequent items
                current_topic["summary_parts"].append("Tools: " + line.split(":", 1)[1].strip() if line.split(":", 1)[1].strip() else "")
            elif line.strip().startswith("**Pain point**:"):
                pain = line.split(":", 1)[1].strip()
                if pain:
                    current_topic["summary_parts"].append("Pain: " + pain)
            elif line.strip().startswith("**Directory**:"):
                current_topic["directory"] = line.split(":", 1)[1].strip()
            elif line.strip().startswith("**Improvements**:"):
                current_topic["summary_parts"].append("Improvements: " + line.split(":", 1)[1].strip() if line.split(":", 1)[1].strip() else "")
            # Collect bullet points and content lines that look like details
            elif line.strip().startswith("-") and current_topic:
                # Collect as part of summary/description
                detail = line.strip()[1:].strip()
                if detail and not detail.startswith("Summary:") and not detail.startswith("Epic:"):
                    current_topic["summary_parts"].append(detail)

    # Finalize last topic and phase
    if current_topic and current_phase:
        if "summary_parts" in current_topic:
            current_topic["summary"] = " | ".join(current_topic["summary_parts"])
            del current_topic["summary_parts"]
        current_phase["topics"].append(current_topic)

    if current_phase:
        roadmap["phases"].append(current_phase)

    return roadmap
```

**Migration execution**:

```python
def execute_migration() -> str:
    """Migrate non-compliant ROADMAP.md to schema format"""

    path = ".agent_planning/ROADMAP.md"

    if not file_exists(path):
        return "No ROADMAP.md found to migrate."

    # Check if migration needed
    needs_migration, reason = detect_migration_needed(path)
    if not needs_migration:
        return f"✓ ROADMAP.md already compliant with schema.\n\nReason: {reason}\n\nNo migration needed."

    # Backup original
    timestamp = current_timestamp()
    backup_path = f".agent_planning/ROADMAP.md.backup-{timestamp}"
    copy_file(path, backup_path)

    # Attempt migration
    try:
        roadmap = migrate_roadmap_format(path)

        # Validate migration result
        if not roadmap.get("phases"):
            return f"""✗ Migration failed: No phases found after migration.

Check file format and try manual migration.
Backup saved: {backup_path}
See SCHEMA.md for expected format."""

        # Write migrated roadmap
        content = write_roadmap(roadmap)
        write_file(path, content)

        # Count migrated items
        total_topics = sum(len(p["topics"]) for p in roadmap["phases"])

        return f"""✓ Migrated ROADMAP.md to schema format

Backup saved: {backup_path}

Migration summary:
- Phases migrated: {len(roadmap['phases'])}
- Topics migrated: {total_topics}
- Format: H4 headers → list items
- Metadata: Custom fields → Summary field
- YAML frontmatter: Added with timestamps

Changes:
- Topics now use list format: - topic-slug [STATE]
- Context extracted to Summary field
- State values standardized to uppercase
- Directory paths preserved
- All content preserved (nothing lost)

Next steps:
  1. Review migrated roadmap: /do:roadmap
  2. Add Epic IDs if using beads
  3. Organize into phases as needed
  4. Use /do:roadmap <topic> to continue adding

If issues found, restore backup:
  mv {backup_path} {path}"""

    except Exception as e:
        return f"""✗ Migration failed: {str(e)}

Original file unchanged.
Backup available at: {backup_path}
Review format and try manual migration.
See SCHEMA.md for expected format."""
```

### Procedure 2: Find Topic

Searches for a topic by name (exact or similarity match).

**Input**: Topic name or slug, parsed roadmap data

**Output**: Topic object with phase context, or None

**Algorithm**:

```python
def find_topic(topic_name, roadmap):
    # Normalize to slug format
    slug = to_kebab_case(topic_name)

    # Exact match
    for phase in roadmap["phases"]:
        for topic in phase["topics"]:
            if topic["name"] == slug:
                return {
                    "topic": topic,
                    "phase": phase,
                    "match_type": "exact"
                }

    # Similarity match (for user disambiguation)
    # Return all topics for LLM to decide similarity
    return None

def list_all_topics(roadmap):
    """Returns flat list of all topics with phase context"""
    topics = []
    for phase in roadmap["phases"]:
        for topic in phase["topics"]:
            topics.append({
                "name": topic["name"],
                "state": topic["state"],
                "phase": f"Phase {phase['number']}: {phase['name']}",
                "directory": topic.get("directory", ""),
                "epic": topic.get("epic", "")
            })
    return topics
```

### Procedure 3: Add Topic to Phase

Adds a new topic to a specified phase and updates the file.

**Input**: Topic name, phase number, optional metadata (summary, epic, dependencies, labels)

**Output**: Updated roadmap data

**Algorithm**:

```python
def add_topic_to_phase(topic_name, phase_num, roadmap, summary=None, epic=None, deps=None, labels=None):
    # Find target phase
    phase = next((p for p in roadmap["phases"] if p["number"] == phase_num), None)
    if not phase:
        raise ValueError(f"Phase {phase_num} not found")

    # Create topic slug
    slug = to_kebab_case(topic_name)

    # Build topic object
    topic = {
        "name": slug,
        "state": "PLANNING" if has_planning_files(slug) else "PROPOSED"
    }

    # Add summary (captured from conversation - context for /do:plan)
    if summary:
        topic["summary"] = summary

    # Add directory
    topic["directory"] = f".agent_planning/{slug}/"

    # Add optional metadata
    if epic:
        topic["epic"] = epic
    if deps:
        topic["dependencies"] = deps
    if labels:
        topic["labels"] = labels

    # Add to phase
    phase["topics"].append(topic)

    # Update timestamp
    roadmap["updated"] = current_timestamp()

    return roadmap

def to_kebab_case(text):
    """Convert text to kebab-case slug"""
    import re
    # Lowercase and replace spaces/underscores with hyphens
    text = text.lower().replace("_", "-").replace(" ", "-")
    # Remove non-alphanumeric except hyphens
    text = re.sub(r"[^a-z0-9-]", "", text)
    # Collapse multiple hyphens
    text = re.sub(r"-+", "-", text)
    # Strip leading/trailing hyphens
    return text.strip("-")
```

### Procedure 4: Write ROADMAP.md

Serializes roadmap data back to ROADMAP.md format.

**Input**: Roadmap data structure

**Output**: Formatted ROADMAP.md file content

**Algorithm**:

```python
def write_roadmap(roadmap):
    lines = []

    # Write YAML frontmatter
    lines.append("---")
    lines.append(f"version: \"{roadmap['version']}\"")
    lines.append(f"created: {roadmap['created']}")
    lines.append(f"updated: {roadmap['updated']}")
    lines.append("---")
    lines.append("")
    lines.append("# Project Roadmap")
    lines.append("")

    # Write phases
    for phase in roadmap["phases"]:
        lines.append(f"## Phase {phase['number']}: {phase['name']}")
        lines.append("")

        if "goal" in phase:
            lines.append(f"Goal: {phase['goal']}")
        if "status" in phase:
            lines.append(f"Status: {phase['status']}")
        lines.append("")

        lines.append("### Topics")
        lines.append("")

        # Write topics
        for topic in phase["topics"]:
            lines.append(f"- {topic['name']} [{topic['state']}]")

            # Write topic metadata (indented)
            # Summary first - it's the key context for understanding the topic
            if "summary" in topic:
                lines.append(f"  - Summary: {topic['summary']}")
            if "epic" in topic:
                lines.append(f"  - Epic: {topic['epic']}")
            if "directory" in topic:
                lines.append(f"  - Directory: {topic['directory']}")
            if "dependencies" in topic and topic["dependencies"]:
                deps = ", ".join(topic["dependencies"])
                lines.append(f"  - Dependencies: {deps}")
            if "labels" in topic and topic["labels"]:
                labels = ", ".join(topic["labels"])
                lines.append(f"  - Labels: {labels}")

            lines.append("")

    return "\n".join(lines)
```

### Procedure 5: Get Topic Status

Gathers comprehensive status information for a topic.

**Input**: Topic name, parsed roadmap

**Output**: Status report object

**Algorithm**:

```python
def get_topic_status(topic_name, roadmap):
    # Find topic
    result = find_topic(topic_name, roadmap)
    if not result:
        return None

    topic = result["topic"]
    phase = result["phase"]

    # Build status object
    status = {
        "name": topic["name"],
        "phase": f"Phase {phase['number']}: {phase['name']}",
        "state": topic["state"],
        "directory": topic.get("directory", ""),
        "epic": topic.get("epic", ""),
        "dependencies": topic.get("dependencies", []),
        "labels": topic.get("labels", [])
    }

    # Get planning files
    if status["directory"]:
        status["planning_files"] = list_planning_files(status["directory"])

    # Get beads epic info (if epic exists)
    if status["epic"]:
        status["beads_info"] = get_beads_epic_info(status["epic"])

    return status

def list_planning_files(directory):
    """List STATUS, PLAN, DOD files with timestamps"""
    import os
    import glob

    files = []
    patterns = ["EVALUATION-*.md", "PLAN-*.md", "DOD-*.md", "USER-RESPONSE-*.md"]

    for pattern in patterns:
        matches = glob.glob(os.path.join(directory, pattern))
        for path in matches:
            stat = os.stat(path)
            files.append({
                "name": os.path.basename(path),
                "modified": stat.st_mtime
            })

    return sorted(files, key=lambda f: f["modified"], reverse=True)

def get_beads_epic_info(epic_id):
    """Get beads epic information using bd CLI"""
    import subprocess
    import json

    try:
        # Get epic details
        result = subprocess.run(
            ["bd", "show", epic_id, "--json"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {"error": "Epic not found"}

        epic_data = json.loads(result.stdout)

        # Get issues for epic
        result = subprocess.run(
            ["bd", "list", "--epic", epic_id, "--json"],
            capture_output=True,
            text=True
        )
        issues_data = json.loads(result.stdout) if result.returncode == 0 else []

        # Calculate completion
        total = len(issues_data)
        closed = sum(1 for issue in issues_data if issue.get("state") == "closed")

        return {
            "epic_id": epic_id,
            "title": epic_data.get("title", ""),
            "total_issues": total,
            "closed_issues": closed,
            "completion_pct": round(closed / total * 100) if total > 0 else 0,
            "issues": issues_data
        }

    except Exception as e:
        return {"error": str(e)}
```

## Practical Examples

### Example 1: Display Roadmap Tree View

```bash
# Command context: /do:roadmap (no args)

# Step 1: Parse roadmap
roadmap = parse_roadmap(".agent_planning/ROADMAP.md")

# Step 2: Format tree view (see Procedure 6 below)
tree = format_tree_view(roadmap)

# Step 3: Display
print(tree)
```

### Example 2: Add New Topic with Disambiguation

```bash
# Command context: /do:roadmap "user authentication"

# Step 1: Parse roadmap
roadmap = parse_roadmap(".agent_planning/ROADMAP.md")

# Step 2: List all topics for LLM similarity check
topics = list_all_topics(roadmap)

# Step 3: LLM checks for similarity
# Present topics list to LLM: "Are any of these similar to 'user authentication'?"
# LLM response: "Yes, 'auth' is similar" OR "No similar topics found"

# Step 4a: If similar found - Ask user
"""
Found similar item 'auth' in Phase 1: MVP [IN PROGRESS]
Did you mean:
1. View status of 'auth'
2. Add 'user-authentication' as new topic
"""

# Step 4b: If no similar - Ask which phase
"""
Add 'user-authentication' to which phase?
1. Phase 1: MVP (active)
2. Phase 2: Growth (queued)
3. Create new phase
"""

# Step 5: Add to roadmap
roadmap = add_topic_to_phase("user-authentication", 1, roadmap)

# Step 6: Create beads epic
epic_id = create_beads_epic("user-authentication")
roadmap["phases"][0]["topics"][-1]["epic"] = epic_id

# Step 7: Write back to file
content = write_roadmap(roadmap)
write_file(".agent_planning/ROADMAP.md", content)

# Step 8: Create topic directory
mkdir(".agent_planning/user-authentication/")
```

### Example 3: Display Topic Status

```bash
# Command context: User chose "View status of 'auth'"

# Step 1: Get topic status
status = get_topic_status("auth", roadmap)

# Step 2: Format status report (see Procedure 7 below)
report = format_status_report(status)

# Step 3: Display
print(report)
```

## Additional Procedures

### Procedure 6: Format Tree View

Creates visual tree representation of roadmap.

```python
def format_tree_view(roadmap):
    if not roadmap["phases"]:
        return "No roadmap yet. Run /do:roadmap <topic> to create one."

    lines = []
    lines.append("Project Roadmap")
    lines.append(f"Last updated: {roadmap['updated']}")
    lines.append("")

    for phase in roadmap["phases"]:
        # Phase icon
        if phase["status"] == "active":
            icon = "🟢"
        elif phase["status"] == "completed":
            icon = "✅"
        else:
            icon = "⏸️"

        # Phase completion
        total = len(phase["topics"])
        completed = sum(1 for t in phase["topics"] if t["state"] == "COMPLETED")
        pct = f"({completed}/{total} completed)"

        lines.append(f"{icon} Phase {phase['number']}: {phase['name']} [{phase['status'].upper()}] {pct}")
        lines.append(f"  Goal: {phase.get('goal', 'N/A')}")

        # Topics
        for i, topic in enumerate(phase["topics"]):
            is_last = i == len(phase["topics"]) - 1
            prefix = "└─" if is_last else "├─"

            # Topic icon
            if topic["state"] == "COMPLETED":
                topic_icon = "✅"
            elif topic["state"] == "IN PROGRESS":
                topic_icon = "🔄"
            elif topic["state"] == "PLANNING":
                topic_icon = "📋"
            elif topic["state"] == "ARCHIVED":
                topic_icon = "📦"
            else:  # PROPOSED
                topic_icon = "💡"

            lines.append(f"  {prefix} {topic_icon} {topic['name']} [{topic['state']}]")

            # Topic metadata (indented further)
            indent = "  │   " if not is_last else "      "

            if "epic" in topic:
                epic_info = ""
                if "beads_info" in topic:
                    bi = topic["beads_info"]
                    epic_info = f" ({bi['closed_issues']}/{bi['total_issues']} issues closed)"
                lines.append(f"{indent}Epic: {topic['epic']}{epic_info}")

        lines.append("")

    return "\n".join(lines)
```

### Procedure 7: Format Status Report

Creates detailed status report for a topic.

```python
def format_status_report(status):
    lines = []
    lines.append("═" * 60)
    lines.append(f"Topic Status: {status['name']}")
    lines.append("═" * 60)
    lines.append("")
    lines.append(f"Location: {status['phase']}")
    lines.append(f"State: {status['state']}")
    lines.append(f"Directory: {status['directory']}")
    lines.append("")

    # Planning artifacts
    if status.get("planning_files"):
        lines.append("Planning Artifacts:")
        for f in status["planning_files"]:
            lines.append(f"  {f['name']}")
        lines.append("")
    else:
        lines.append("Planning Artifacts: None")
        lines.append("")

    # Beads epic
    if status.get("beads_info"):
        bi = status["beads_info"]
        if "error" not in bi:
            lines.append(f"Beads Epic: {bi['epic_id']}")
            lines.append(f"  Title: {bi['title']}")
            lines.append(f"  Issues: {bi['total_issues']} total, {bi['closed_issues']} closed, {bi['total_issues'] - bi['closed_issues']} open")
            lines.append(f"  Completion: {bi['completion_pct']}%")
            lines.append("")

            if bi["issues"]:
                lines.append("Issues:")
                for issue in bi["issues"]:
                    icon = "✅" if issue["state"] == "closed" else "🔄" if issue.get("in_progress") else "📋"
                    lines.append(f"  {icon} {issue['key']}: {issue['summary']} [{issue['state']}]")
                lines.append("")
    elif status.get("epic"):
        lines.append(f"Beads Epic: {status['epic']} (not found or error)")
        lines.append("")
    else:
        lines.append("Beads Epic: None (run /do:roadmap to create)")
        lines.append("")

    # Dependencies
    if status.get("dependencies"):
        lines.append(f"Dependencies: {', '.join(status['dependencies'])}")
        lines.append("")

    # Labels
    if status.get("labels"):
        lines.append(f"Labels: {', '.join(status['labels'])}")
        lines.append("")

    lines.append("═" * 60)

    return "\n".join(lines)
```

### Procedure 8: Create Beads Epic

Auto-creates a beads epic for a new topic.

```python
def create_beads_epic(topic_name):
    """Create beads epic using bd CLI"""
    import subprocess
    import re

    # Convert topic-slug to TOPIC-SLUG format for epic key
    epic_key = topic_name.upper()

    # Create title from slug
    title = topic_name.replace("-", " ").title()

    # Create epic
    result = subprocess.run(
        ["bd", "create", "epic", epic_key, "--title", title],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"Failed to create epic: {result.stderr}")

    # Extract epic ID from output
    match = re.search(r"Created epic: ([A-Z-]+-\d+)", result.stdout)
    if match:
        return match.group(1)

    # Fallback: assume format TOPIC-SLUG-1
    return f"{epic_key}-1"
```

### Procedure 9: Initialize Empty Roadmap

Creates a new ROADMAP.md with default structure.

```python
def initialize_roadmap():
    """Create initial ROADMAP.md with Phase 1: MVP"""
    timestamp = current_timestamp()

    roadmap = {
        "version": "1.0",
        "created": timestamp,
        "updated": timestamp,
        "phases": [
            {
                "number": 1,
                "name": "MVP",
                "goal": "Deliver core functionality",
                "status": "active",
                "topics": []
            }
        ]
    }

    return roadmap

def current_timestamp():
    """Returns timestamp in YYYY-MM-DD-HHmmss format"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d-%H%M%S")
```

## Error Handling

**File not found**:
- Return empty structure: `{"version": "1.0", "phases": []}`
- Allow creation of new roadmap

**Parse errors**:
- Log warning with line number
- Continue parsing (partial structure better than nothing)
- Return accumulated data + error list

**Invalid topic name**:
- Sanitize to kebab-case
- Warn if significantly changed from input

**Beads not available**:
- Continue without epic creation
- Warn user that epic will need manual creation
- Add placeholder epic field for later

**Phase not found**:
- Suggest creating new phase
- List available phases

## Integration Points

**Beads CLI**:
- `bd create epic <key> --title <title>` - Create epic
- `bd show <epic-id> --json` - Get epic details
- `bd list --epic <epic-id> --json` - Get issues
- `bd blocked --json` - Get blocked issues
- `bd ready --json` - Get ready issues

**File System**:
- `.agent_planning/ROADMAP.md` - Main roadmap file
- `.agent_planning/<topic>/` - Topic directories
- Planning files: `EVALUATION-*.md`, `PLAN-*.md`, `DOD-*.md`

**Commands**:
- `/do:roadmap` - Main command using this skill
- `/do:plan <topic>` - Creates planning files (updates topic state)

## Best Practices

**Parsing**:
- Always handle missing files gracefully
- Ignore unknown fields (forward compatibility)
- Validate critical fields, warn on invalid values

**Writing**:
- Update `updated` timestamp on every write
- Preserve unknown fields when round-tripping
- Validate before writing (prevent corruption)

**Performance**:
- Parse once, cache result in command context
- Only write if data actually changed
- Use file modification time for cache invalidation

**Error Messages**:
- Be specific: "Topic 'user-auth' not found in roadmap"
- Suggest fixes: "Run /do:roadmap user-auth to add it"
- Include context: phase, state, directory path

### Procedure 10: Detect Multiple Topics

Detects if input contains multiple topics using light heuristics.

**Input**: Topic input string (possibly containing multiple items)

**Output**: List of topic strings (single item if no pattern detected)

**Algorithm**:

```python
def detect_multiple_topics(input_text: str) -> list[str]:
    """
    Detect if input contains multiple topics. Light heuristics:
    - Newline-separated lines that look like topics
    - Semicolon-separated items
    - Numbered list (1., 2., etc.)
    - Bullet list (-, *, •)

    Returns list of topic strings. Single item if no pattern detected.
    """

    input_text = input_text.strip()

    # File reference (don't treat as batch)
    if input_text.endswith(".md"):
        return [input_text]

    # Semicolon delimiter (2+ items)
    if ";" in input_text:
        items = [t.strip() for t in input_text.split(";") if t.strip()]
        if len(items) >= 2:
            return items

    # Newline-separated (3+ lines that look like topics - short, descriptive)
    lines = [line.strip() for line in input_text.split("\n") if line.strip()]
    if len(lines) >= 3:
        # Heuristic: Are lines topic-like? (short lines < 100 chars, no periods)
        topic_like = all(len(line) < 100 and not line.endswith(".") for line in lines)
        if topic_like:
            return lines

    # Numbered list (1. item, 2. item, etc.)
    numbered = re.findall(r"^\d+\.\s+(.+)$", input_text, re.MULTILINE)
    if len(numbered) >= 2:
        return numbered

    # Bullet list (-, *, •)
    bullets = re.findall(r"^[-*•]\s+(.+)$", input_text, re.MULTILINE)
    if len(bullets) >= 2:
        return bullets

    # Default: Single topic
    return [input_text]
```

### Procedure 11: Batch Add Multiple Topics

Adds multiple topics in batch mode with smart priority-to-phase mapping.

**Input**: List of topic strings

**Output**: Confirmation message with count of added items

**Algorithm**:

```python
def execute_batch_add(topics: list[str]) -> str:
    """
    Add multiple topics in batch mode.

    Strategy:
    1. Detect priority markers (P1, P2, P3) to infer phase
    2. Parse topic name and description
    3. Validate context for each topic
    4. Add all with consistent metadata
    """

    # Load roadmap
    if not file_exists(".agent_planning/ROADMAP.md"):
        roadmap = initialize_roadmap()
        default_phase = 1
    else:
        roadmap = parse_roadmap(".agent_planning/ROADMAP.md")
        default_phase = next(
            (p["number"] for p in roadmap["phases"] if p.get("status") == "active"),
            1
        )

    # Parse topics and extract metadata
    parsed_topics = []
    for topic_input in topics:
        # Extract priority marker if present (P1, P2, P3)
        priority = None
        if match := re.search(r"\bP(\d)\b", topic_input, re.IGNORECASE):
            priority = int(match.group(1))

        # Extract name and description
        # Patterns: "Name - Description" or "Name: Description"
        if " - " in topic_input:
            name, desc = topic_input.split(" - ", 1)
        elif ": " in topic_input:
            name, desc = topic_input.split(": ", 1)
        else:
            name = topic_input
            desc = ""

        # Determine phase from priority
        phase_num = priority if priority and priority <= len(roadmap["phases"]) else default_phase

        parsed_topics.append({
            "input": topic_input,
            "name": name.strip(),
            "description": desc.strip(),
            "priority": priority,
            "phase": phase_num
        })

    # Add all topics
    added_count = 0
    skipped_count = 0

    for topic_data in parsed_topics:
        slug = to_kebab_case(topic_data["name"])

        # Skip duplicates
        if find_topic(slug, roadmap):
            skipped_count += 1
            continue

        # Create directory
        mkdir(f".agent_planning/{slug}/")

        # Add to roadmap
        roadmap = add_topic_to_phase(
            topic_name=slug,
            phase_num=topic_data["phase"],
            roadmap=roadmap,
            summary=topic_data["description"],
            epic=None  # Batch mode skips epic creation
        )
        added_count += 1

    # Write file
    if added_count > 0:
        content = write_roadmap(roadmap)
        write_file(".agent_planning/ROADMAP.md", content)

    # Build confirmation
    msg = f"""✓ Batch add complete

Added: {added_count} topic(s)
Skipped: {skipped_count} duplicate(s)
Total processed: {len(parsed_topics)}

Phase assignments:
"""
    # Show phase distribution
    phase_counts = {}
    for topic_data in parsed_topics:
        phase_num = topic_data["phase"]
        phase_counts[phase_num] = phase_counts.get(phase_num, 0) + 1

    for phase_num in sorted(phase_counts.keys()):
        phase = next((p for p in roadmap["phases"] if p["number"] == phase_num), None)
        if phase:
            msg += f"  Phase {phase_num}: {phase['name']} - {phase_counts[phase_num]} items\n"

    msg += f"""
Next steps:
  1. Review roadmap: /do:roadmap
  2. Create plans: /do:plan <topic>
  3. Add Epic IDs: Edit .agent_planning/ROADMAP.md"""

    return msg
```

### Procedure 12: Validate Context Sufficiency

Checks if topic has enough planning context (problem + outcome + areas).

**Input**: Topic data dict with summary field

**Output**: Tuple of (is_sufficient: bool, feedback: str)

**Algorithm**:

```python
def validate_context_sufficiency(topic_data: dict) -> tuple[bool, str]:
    """
    Check if topic has enough context for planning.

    Requirements:
    - Problem statement (what issue exists)
    - Intended outcome (what we want to achieve)
    - Relevant project areas (conceptual, not file paths)

    Returns: (is_sufficient: bool, feedback: str)
    """

    summary = topic_data.get("summary", "").strip()

    # Minimum length check
    if len(summary) < 20:
        return False, "Summary too brief. Need at least: problem + intended outcome + affected areas."

    # Check for problem indicator words
    problem_words = ["fix", "bug", "issue", "error", "problem", "broken", "fails",
                     "correct", "improve", "resolve", "handle"]
    has_problem = any(word in summary.lower() for word in problem_words)

    # Check for outcome indicator words
    outcome_words = ["add", "implement", "create", "enable", "support", "improve",
                    "refactor", "enhance", "consolidate", "centralize"]
    has_outcome = any(word in summary.lower() for word in outcome_words)

    # Check for project area mentions (conceptual, not paths)
    area_patterns = ["tool", "module", "component", "system", "handler", "manager",
                    "service", "layer", "interface", "bridge", "adapter", "endpoint"]
    has_area = any(pattern in summary.lower() for pattern in area_patterns)

    # Sufficient if 2+ indicators present
    indicators_count = sum([has_problem, has_outcome, has_area])
    if indicators_count >= 2:
        return True, ""

    # Build feedback
    missing = []
    if not has_problem and not has_outcome:
        missing.append("what problem exists or what outcome is desired")
    if not has_area:
        missing.append("which project areas are affected (e.g., 'tool routing', 'error handling')")

    feedback = f"Context insufficient. Add: {', '.join(missing)}."
    return False, feedback

def prompt_for_additional_context(feedback: str) -> str:
    """Prompt user for additional context with guidance"""
    guidance = f"""
{feedback}

Please add context about:
- What's the problem or goal?
- Which project areas does this affect?

Example: "Consolidate error handling across 17 tools to enforce single-point error formatting at MCP boundary"
"""
    return do_prompt_questioning({
        "question": "Additional context needed:",
        "guidance": guidance
    })

def prompt_user_for_summary(topic_name: str) -> str:
    """Prompt user for topic summary with context guidance"""
    guidance = """Summary for planning context.

Include:
- Problem statement or intended outcome
- Relevant project areas (e.g., "tool routing", not file paths)

Example: "Centralize error formatting in MCP boundary to eliminate duplicate error handling across all tools"
"""
    return do_prompt_questioning({
        "question": f"Summary for '{topic_name}':",
        "guidance": guidance
    })
```

### Procedure 13: Missing has_planning_files() Function

Checks if topic has planning files (indicates topic state).

**Input**: Topic slug name

**Output**: True if planning files exist, False otherwise

**Algorithm**:

```python
def has_planning_files(topic_slug: str) -> bool:
    """
    Check if planning files exist for a topic.

    Detection criteria:
    - Directory .agent_planning/<slug>/ exists
    - Contains at least one of: PLAN-*.md, EVALUATION-*.md, DOD-*.md, STATUS-*.md

    Returns: True if planning has started (state should be PLANNING or later)
    """

    directory = f".agent_planning/{topic_slug}/"
    if not dir_exists(directory):
        return False

    # Check for planning file patterns
    import os
    import glob

    files = []
    try:
        files = os.listdir(directory)
    except:
        return False

    planning_patterns = ["PLAN-", "EVALUATION-", "DOD-", "STATUS-"]

    return any(
        any(pattern in filename for pattern in planning_patterns)
        for filename in files
    )
```

## See Also

- `SCHEMA.md` - Full schema documentation
- `.agent_planning/ROADMAP.md.example` - Example file
- `/do:roadmap` command - Main user interface
