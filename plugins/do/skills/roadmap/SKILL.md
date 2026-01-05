---
name: roadmap
description: Parse and manipulate ROADMAP.md files for hierarchical project planning with phases and topics.
---

# Roadmap Skill

## Purpose

Parse, query, and update `.agent_planning/ROADMAP.md` files that define project phases and topics. Provides structured access to roadmap data for visualization and manipulation.

## When to Use

- Reading roadmap to display tree view
- Checking if a topic exists (similarity matching)
- Adding new topics to phases
- Updating topic states or metadata
- Generating topic status reports

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

**Input**: Topic name, phase number, optional metadata (epic, dependencies, labels)

**Output**: Updated roadmap data

**Algorithm**:

```python
def add_topic_to_phase(topic_name, phase_num, roadmap, epic=None, deps=None, labels=None):
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

## See Also

- `SCHEMA.md` - Full schema documentation
- `.agent_planning/ROADMAP.md.example` - Example file
- `/do:roadmap` command - Main user interface
