---
argument-hint: [topic to add to roadmap]
description: View roadmap tree or add topic. No args = show tree view. With args = add to roadmap.
---

# Roadmap Command

Hierarchical project planning with phases and topics.

## Usage

- `/lp:roadmap` - Display roadmap tree view
- `/lp:roadmap <topic>` - Add topic to roadmap (with disambiguation if similar exists)

## Implementation

### Step 1: Check Arguments

Determine mode based on arguments:

```python
if ARGUMENTS.strip():
    mode = "add"
    topic_input = ARGUMENTS.strip()
else:
    mode = "view"
```

---

### Step 2: View Mode (No Arguments)

Display the roadmap as a formatted tree view.

#### Step 2a: Check if ROADMAP.md Exists

```bash
ls .agent_planning/ROADMAP.md
```

**If doesn't exist:**

Display message:
```
No roadmap yet.

Run /lp:roadmap <topic> to create your first roadmap with a topic.

Example: /lp:roadmap user-authentication
```

**Stop here.**

#### Step 2b: Parse and Display Tree View

Use the `lp:roadmap` skill to parse and format the tree:

```python
# Parse roadmap using skill procedures
roadmap = parse_roadmap(".agent_planning/ROADMAP.md")

# Format tree view using skill
tree = format_tree_view(roadmap)

# Display
print(tree)
```

**Example output:**
```
Project Roadmap
Last updated: 2025-12-18-143000

🟢 Phase 1: MVP [ACTIVE] (1/3 completed)
  Goal: Deliver core functionality
  ├─ ✅ user-authentication [COMPLETED]
  │   Epic: USER-AUTHENTICATION-1 (3/3 issues closed)
  ├─ 🔄 payment-processing [IN PROGRESS]
  │   Epic: PAYMENT-PROCESSING-1 (2/5 issues closed)
  └─ 💡 dashboard-ui [PROPOSED]

⏸️ Phase 2: Growth [QUEUED] (0/2 completed)
  Goal: Scale and optimize
  ├─ 💡 performance-optimization [PROPOSED]
  └─ 💡 analytics-dashboard [PROPOSED]
```

**Stop here.**

---

### Step 3: Add Mode (With Arguments)

Add a topic to the roadmap with disambiguation.

#### Step 3a: Check if ROADMAP.md Exists

```bash
ls .agent_planning/ROADMAP.md
```

**If doesn't exist:**

Create initial roadmap using skill:

```python
roadmap = initialize_roadmap()  # Creates Phase 1: MVP
```

Proceed to Step 3d (skip similarity check since roadmap is empty).

#### Step 3b: Parse Existing Roadmap

```python
roadmap = parse_roadmap(".agent_planning/ROADMAP.md")
```

#### Step 3c: Similarity Check

Convert topic input to kebab-case and check for similar topics:

```python
# Convert to slug
topic_slug = to_kebab_case(topic_input)  # "User Authentication" → "user-authentication"

# List all topics for LLM comparison
all_topics = list_all_topics(roadmap)
```

**LLM Task**: Check if any existing topics are similar to `topic_input`.

Present the list of existing topics to the LLM with this prompt:

```
Existing topics in roadmap:
{list all_topics with: name, state, phase}

User wants to add: "{topic_input}"

Are any of these topics similar to what the user wants to add?
- If yes: Return the most similar topic name
- If no: Return "NO_MATCH"

Consider:
- Synonyms (e.g., "auth" vs "authentication")
- Abbreviations (e.g., "db" vs "database")
- Related concepts (e.g., "login" vs "user-authentication")
```

**If LLM returns a matching topic name** → Go to Step 3c-1 (Disambiguation)

**If LLM returns "NO_MATCH"** → Go to Step 3d (Select Phase)

##### Step 3c-1: Disambiguation Flow

Found a similar topic. Present options to user using `lp:prompt-questioning` skill:

```python
# Get detailed status of similar topic
similar_topic = find_topic(matching_topic_name, roadmap)
status = get_topic_status(matching_topic_name, roadmap)

# Format status report
status_report = format_status_report(status)
```

Present to user:

```
┌─ Similar Topic Found ────────────────────────────────┐
│                                                      │
│ Found similar topic: {similar_topic.name}            │
│ Phase: {similar_topic.phase}                         │
│ State: {similar_topic.state}                         │
│                                                      │
│ {status_report (truncated - key info only)}          │
│                                                      │
│ Did you mean:                                        │
│ 1. View full status of '{similar_topic.name}'       │
│ 2. Add '{topic_slug}' as a NEW topic                │
│ 3. Cancel                                            │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**User selects option:**

**Option 1**: Display full status report and stop:
```python
print(format_status_report(status))
```
**Stop here.**

**Option 2**: Continue to Step 3d (add as new topic)

**Option 3**: Cancel and stop
**Stop here.**

#### Step 3d: Select Phase

Ask user which phase to add the topic to:

```python
# List active and queued phases
available_phases = [p for p in roadmap["phases"] if p["status"] in ["active", "queued"]]
```

Present to user using `lp:prompt-questioning`:

```
┌─ Add Topic: {topic_slug} ────────────────────────────┐
│                                                      │
│ Which phase should this topic be added to?          │
│                                                      │
│ {for each phase in available_phases:}               │
│ {phase.number}. Phase {phase.number}: {phase.name}   │
│     Status: {phase.status}                           │
│     Goal: {phase.goal}                               │
│     Topics: {len(phase.topics)}                      │
│                                                      │
│ {len(available_phases)+1}. Create new phase          │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**If user selects existing phase:**
- Use that phase number
- Go to Step 3e

**If user selects "Create new phase":**

Ask for phase details:
```
┌─ Create New Phase ───────────────────────────────────┐
│                                                      │
│ Phase name: [user input]                            │
│ Phase goal: [user input]                            │
│                                                      │
│ Phase number will be: {max_phase_num + 1}           │
│ Phase status will be: queued                        │
│                                                      │
└──────────────────────────────────────────────────────┘
```

Create new phase:
```python
new_phase_num = max(p["number"] for p in roadmap["phases"]) + 1
new_phase = {
    "number": new_phase_num,
    "name": phase_name,
    "goal": phase_goal,
    "status": "queued",
    "topics": []
}
roadmap["phases"].append(new_phase)
selected_phase_num = new_phase_num
```

Go to Step 3e.

#### Step 3e: Create Beads Epic

Auto-create beads epic for the new topic:

```python
try:
    epic_id = create_beads_epic(topic_slug)
    print(f"Created beads epic: {epic_id}")
except Exception as e:
    print(f"Warning: Could not create beads epic: {e}")
    print("You can create it manually later with: bd create epic {topic_slug.upper()}")
    epic_id = None
```

**If beads not available** (no `.beads/` directory):
- Set `epic_id = None`
- Display warning
- Continue (epic can be added manually later)

#### Step 3f: Create Topic Directory

```bash
mkdir -p .agent_planning/{topic_slug}/
```

#### Step 3g: Add Topic to Roadmap

```python
# Determine initial state
if os.path.exists(f".agent_planning/{topic_slug}/STATUS-*.md"):
    initial_state = "PLANNING"
elif os.path.exists(f".agent_planning/{topic_slug}/PLAN-*.md"):
    initial_state = "PLANNING"
else:
    initial_state = "PROPOSED"

# Add topic using skill
roadmap = add_topic_to_phase(
    topic_name=topic_slug,
    phase_num=selected_phase_num,
    roadmap=roadmap,
    epic=epic_id,
    deps=None,  # Can be added manually later
    labels=None  # Can be added manually later
)
```

#### Step 3h: Write Updated Roadmap

```python
# Serialize roadmap back to file
content = write_roadmap(roadmap)

# Write to file
with open(".agent_planning/ROADMAP.md", "w") as f:
    f.write(content)
```

#### Step 3i: Confirm Addition

Display confirmation:

```
✓ Added topic to roadmap

Topic: {topic_slug}
Phase: Phase {selected_phase_num}: {phase_name}
State: {initial_state}
Directory: .agent_planning/{topic_slug}/
Epic: {epic_id or "None (create with bd)"}

Next steps:
  1. Run /lp:plan {topic_slug} to create a detailed plan
  2. Edit .agent_planning/ROADMAP.md to add dependencies or labels
  3. View roadmap: /lp:roadmap
```

**Stop here.**

---

## Key Principles

**View mode (no args):**
- Fast, read-only operation
- Show project structure at a glance
- Include completion metrics from beads

**Add mode (with args):**
- Intelligent disambiguation (LLM-based similarity)
- Always show status of similar items before offering to create new
- Auto-create beads epic for full integration
- Create topic directory immediately
- User chooses phase (don't assume)

**Similarity matching:**
- Use LLM to compare user input against existing topics
- Consider synonyms, abbreviations, related concepts
- Show status report to help user decide
- Let user override if LLM got it wrong

**Beads integration:**
- Auto-create epic when adding new topic
- Graceful degradation if beads unavailable
- Show epic status in tree view
- Use epic completion % in phase metrics

**Error handling:**
- Missing ROADMAP.md in view mode → Helpful message
- Missing ROADMAP.md in add mode → Auto-create with Phase 1
- Beads unavailable → Continue without epic, warn user
- Invalid phase selection → Ask again

## Integration with Other Commands

**After adding topic:**
- Suggest `/lp:plan {topic}` to create planning files
- Mention that planning files update topic state automatically

**Relationship to /lp:plan:**
- Roadmap provides high-level organization
- Plan provides detailed implementation breakdown
- Both can be used independently or together

**Topic state sync:**
- PROPOSED → no planning files
- PLANNING → STATUS/PLAN/DOD exist, no implementation
- IN PROGRESS → implementation started
- COMPLETED → all acceptance criteria met
- ARCHIVED → no longer maintained

States updated by:
- `PROPOSED` - Default when adding to roadmap
- `PLANNING` - Auto-detected when STATUS/PLAN files exist
- `IN PROGRESS` - Updated by implementer agents
- `COMPLETED` - Updated by work-evaluator (all DoD met)
- `ARCHIVED` - Manual update in ROADMAP.md

## Customization via CLAUDE.md

Users can customize behavior by adding to their CLAUDE.md:

```markdown
## lp:roadmap preferences

- Auto-select similar topics without asking (I'll review before confirming)
- Always add new topics to Phase 1 unless I specify
- Skip beads epic creation (I'll create manually)
```

These preferences override the default prompting behavior.

## See Also

- `skills/roadmap/SKILL.md` - Parsing and manipulation procedures
- `skills/roadmap/SCHEMA.md` - ROADMAP.md format specification
- `.agent_planning/ROADMAP.md.example` - Example file
