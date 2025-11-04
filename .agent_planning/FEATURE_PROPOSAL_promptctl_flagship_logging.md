# PromptCtl Flagship Logging System - Feature Proposal

## Executive Summary

This proposal introduces **LogFlow**, a premium logging system for PromptCtl that transforms debugging from a necessary evil into a delightful experience. LogFlow combines zero-configuration simplicity with infinite customizability, delivering instant insights through beautiful visualizations and intelligent filtering.

The system captures every aspect of hook processing with microsecond precision, stores it efficiently in a hybrid format optimized for both human and machine consumption, and presents it through multiple interfaces that adapt to the user's workflow. Most importantly, it "just works" out of the box while scaling to enterprise-grade requirements.

## Brainstormed Ideas (Initial Exploration)

### The Many Ideas Considered

1. **Time-Travel Debugging**: Record complete state snapshots at each event, allowing users to replay entire sessions and step through hook processing frame-by-frame

2. **AI-Powered Log Analysis**: Use Claude to automatically identify patterns, anomalies, and suggest optimizations based on log data

3. **Distributed Tracing**: OpenTelemetry-style distributed tracing across Claude Code sessions, tracking causality chains

4. **Visual Hook Flow Diagrams**: Real-time SVG/Mermaid diagrams showing hook execution flow with timing data

5. **Log Streaming to External Services**: Stream logs to DataDog, Splunk, CloudWatch, etc. for centralized monitoring

6. **Smart Log Compression**: Context-aware compression that keeps important data uncompressed while aggressively compressing repetitive patterns

7. **Semantic Log Levels**: Beyond ERROR/WARN/INFO - domain-specific levels like HOOK_MATCH, ACTION_EXECUTE, TEMPLATE_RENDER

8. **Interactive Terminal UI**: Rich TUI (like htop/k9s) for real-time log monitoring and filtering

9. **Git-Style Log Branching**: Create "branches" of logs for different experiments, merge insights back

10. **Performance Profiling Integration**: Automatic performance bottleneck detection with flame graphs

11. **Privacy-Aware Logging**: Automatic PII detection and redaction with configurable sensitivity levels

12. **Log-Driven Testing**: Generate test cases from actual log patterns

## Filtering Rationale

### Why Most Ideas Were Rejected

- **Time-Travel Debugging**: Too complex for MVP, requires significant memory overhead
- **AI-Powered Analysis**: Requires external dependencies, adds latency, not core functionality
- **Distributed Tracing**: Over-engineered for a local tool, OpenTelemetry is heavyweight
- **Visual Flow Diagrams**: Nice-to-have but not essential, better as a separate tool
- **External Streaming**: Adds complexity and dependencies, not needed for local development
- **Git-Style Branching**: Conceptually interesting but practically confusing
- **Performance Profiling**: Should be a separate feature, not mixed with logging
- **Log-Driven Testing**: Too magical, users want explicit control over tests

### Why The Selected Ideas Win

The winning combination focuses on:

1. **Smart Compression + Semantic Levels**: Provides massive storage efficiency while maintaining human readability
2. **Interactive Terminal UI + Privacy-Aware Logging**: Delivers immediate value with security built-in
3. **Hybrid Storage Format**: Enables both real-time streaming and historical analysis

These features solve real, painful problems (log volume, finding relevant info, privacy concerns) while being implementable with Python's standard library plus minimal dependencies.

## The LogFlow System - Detailed Specification

### Core Architecture

#### 1. Three-Layer Logging Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Capture   │ --> │   Process    │ --> │    Store    │
│   Layer     │     │   Layer      │     │    Layer    │
└─────────────┘     └──────────────┘     └─────────────┘
      ↓                    ↓                     ↓
  Zero-overhead      Smart filtering      Hybrid format
  async capture      & enrichment          (JSONL + DB)
```

**Capture Layer**:
- Async, non-blocking log emission at every critical point
- Structured logging with rich context
- Automatic correlation IDs for request tracing

**Process Layer**:
- Semantic level assignment
- Privacy scanning and redaction
- Context enrichment (git info, system state)
- Smart aggregation of repetitive events

**Store Layer**:
- Dual storage: JSONL files for streaming, SQLite for queries
- Automatic rotation and archival
- Configurable retention policies

#### 2. Semantic Log Levels

Beyond traditional levels, we introduce domain-specific semantics:

```python
class LogLevel:
    # Traditional (for compatibility)
    ERROR = 50
    WARNING = 40
    INFO = 30
    DEBUG = 20

    # Hook-specific
    HOOK_RECEIVED = 35      # Hook event arrived
    HOOK_MATCHED = 33       # Handler matched
    HOOK_EXECUTED = 31      # Handler completed

    # Action-specific
    ACTION_START = 25       # Action beginning
    ACTION_RESULT = 23      # Action outcome

    # Template/Context
    CONTEXT_RENDER = 15     # Template rendering
    STATE_CHANGE = 13       # State mutations
```

#### 3. Log Entry Schema

```python
class LogEntry:
    # Core fields (always present)
    timestamp: float        # Microsecond precision
    level: str             # Semantic level
    event: str             # Event type (hook.received, action.execute, etc.)
    session_id: str        # Claude session correlation
    correlation_id: str    # Request correlation

    # Context fields (enriched)
    hook_name: Optional[str]
    handler_name: Optional[str]
    tool_name: Optional[str]
    file_path: Optional[str]

    # Performance fields
    duration_ms: Optional[float]
    memory_delta: Optional[int]

    # Payload (smart storage)
    data: Dict[str, Any]   # Actual data (redacted if needed)
    data_hash: str         # For deduplication

    # Metadata
    git_commit: Optional[str]
    git_branch: Optional[str]
    python_version: str
    promptctl_version: str
```

### Configuration Interface

#### Zero-Config Defaults

Out of the box, LogFlow works perfectly with these defaults:

```yaml
# Implicit defaults (no config needed)
logging:
  enabled: true
  level: INFO  # Shows hook matches and executions
  storage:
    type: hybrid  # Both JSONL and SQLite
    location: ~/.promptctl/logs/
    rotation: daily
    retention_days: 30
  privacy:
    enabled: true
    sensitivity: medium  # Redacts obvious PII
  output:
    console: auto  # Shows warnings/errors to stderr
    format: pretty  # Human-readable with colors
```

#### Power User Configuration

For those who want control:

```yaml
# promptctl.yaml - Advanced logging configuration
logging:
  enabled: true
  level: DEBUG  # Or use semantic: "CONTEXT_RENDER"

  # Capture configuration
  capture:
    include_payload: true
    include_environment: false
    stack_traces: on_error  # always | on_error | never
    performance_tracking: true
    memory_tracking: false

  # Processing configuration
  processing:
    privacy:
      enabled: true
      sensitivity: high  # low | medium | high | custom
      custom_patterns:  # Only if sensitivity: custom
        - pattern: 'api[_-]?key'
          replacement: '[API_KEY]'
        - pattern: '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
          replacement: '[EMAIL]'

    aggregation:
      enabled: true
      window_ms: 100  # Aggregate similar events within window

    enrichment:
      git_info: true
      system_info: true

  # Storage configuration
  storage:
    type: hybrid  # jsonl | sqlite | hybrid
    location: ~/.promptctl/logs/

    # File storage options
    jsonl:
      compress: true  # gzip compression
      rotation: size  # daily | size | never
      max_size_mb: 100
      max_files: 10

    # Database options
    sqlite:
      enabled: true
      path: ~/.promptctl/logs/events.db
      wal_mode: true  # Write-ahead logging for performance
      indexes:
        - session_id
        - correlation_id
        - timestamp
        - hook_name

    # Retention
    retention:
      days: 30
      archive: true  # Move to .tar.gz after retention
      archive_location: ~/.promptctl/archives/

  # Output configuration
  output:
    console:
      enabled: auto  # true | false | auto (errors/warnings only)
      format: pretty  # pretty | json | compact
      colors: true
      timestamp_format: relative  # iso | unix | relative | human

    # Structured output for other tools
    structured:
      enabled: false
      format: json
      destination: stdout  # stdout | stderr | file:<path>

  # Filtering rules
  filters:
    include:
      - event: hook.*  # Include all hook events
      - level: ">=WARNING"  # Include warnings and above
    exclude:
      - event: context.render  # Too noisy
      - handler: test_*  # Exclude test handlers

  # Performance limits
  limits:
    max_payload_size: 10240  # Truncate large payloads
    max_entries_per_second: 1000  # Rate limiting
    buffer_size: 10000  # In-memory buffer before flush
```

### Output & Formatting

#### 1. Pretty Console Output (Default)

```
[13:42:15.234] 🎯 HOOK_MATCHED PreToolUse → auto-test (priority: 10)
               Session: abc123... | Tool: Edit | File: server.py

[13:42:15.267] ⚡ ACTION_START command: "pytest server.py"
               Handler: auto-test | Correlation: xyz789...

[13:42:16.891] ✅ ACTION_RESULT command completed (1624ms)
               Output: 42 tests passed
               Memory: +2.3MB | CPU: 78ms

[13:42:16.905] 🏁 HOOK_EXECUTED PreToolUse → auto-test
               Total duration: 1671ms | Actions: 1 | Status: success
```

#### 2. Compact Output (High-Volume)

```
13:42:15 MATCH PreToolUse>auto-test tool=Edit file=server.py
13:42:15 EXEC  cmd="pytest server.py"
13:42:16 OK    cmd 1624ms tests=42
13:42:16 DONE  PreToolUse>auto-test 1671ms
```

#### 3. JSON Output (Machine-Readable)

```json
{
  "timestamp": 1701439335.234567,
  "level": "HOOK_MATCHED",
  "event": "hook.matched",
  "session_id": "abc123...",
  "correlation_id": "xyz789...",
  "hook_name": "PreToolUse",
  "handler_name": "auto-test",
  "data": {
    "tool_name": "Edit",
    "file_path": "server.py",
    "priority": 10
  }
}
```

### Query & Analysis Interface

#### 1. CLI Query Tool

```bash
# Basic queries
promptctl logs                    # Show recent logs (tail -f style)
promptctl logs --follow          # Real-time streaming
promptctl logs --last 1h         # Last hour
promptctl logs --session abc123  # Specific session

# Semantic queries
promptctl logs --hooks           # Only hook events
promptctl logs --errors          # Only errors
promptctl logs --slow            # Operations > 1s

# Advanced filtering
promptctl logs --filter "tool_name='Edit' AND duration_ms > 100"
promptctl logs --grep "pytest"   # Text search
promptctl logs --json            # JSON output

# Analysis commands
promptctl logs stats             # Statistics summary
promptctl logs timeline          # Visual timeline
promptctl logs bottlenecks       # Performance analysis
```

#### 2. Interactive TUI (Terminal UI)

```
┌─[PromptCtl LogFlow]──────────────────────────────────────┐
│ 📊 Dashboard                        [F1:Help] [Q:Quit]   │
├───────────────────────────────────────────────────────────┤
│ Session: abc123-def456-789012 | Uptime: 2h 15m          │
│ Events: 1,247 | Handlers: 12 | Errors: 0 | Warnings: 3  │
├───────────────────────────────────────────────────────────┤
│ [FILTERS]                                                │
│ Level: ≥INFO  Hook: ALL  Handler: ALL  Tool: ALL       │
├───────────────────────────────────────────────────────────┤
│ 13:42:15 🎯 PreToolUse → auto-test [Edit:server.py]     │
│ 13:42:15 ⚡ Running: pytest server.py                    │
│ 13:42:16 ✅ Success: 42 tests passed (1.6s)             │
│ 13:42:17 🎯 PostToolUse → review-changes                │
│ 13:42:17 📝 Prompt: "Review the test results"           │
│ >>> ▌                                                    │
├───────────────────────────────────────────────────────────┤
│ [/] Search  [F] Filter  [S] Stats  [E] Export           │
└───────────────────────────────────────────────────────────┘
```

Key features:
- Real-time updates with color coding
- Keyboard navigation (j/k, arrow keys)
- Quick filters (press 'h' for hooks only, 'e' for errors)
- Inline search with highlighting
- Export current view to file

#### 3. MCP Tool Integration

```python
@mcp.tool()
def promptctl_logs(
    query: str = "recent",
    limit: int = 100,
    format: str = "pretty"
) -> str:
    """
    Query PromptCtl logs from within Claude.

    Examples:
    - promptctl_logs("errors")
    - promptctl_logs("session:current", limit=50)
    - promptctl_logs("hook:PreToolUse AND tool:Edit")
    """
    # Implementation queries the log store and returns formatted results
    pass
```

### Integration Points

#### 1. Hooks That Log Their Own Execution

```yaml
handlers:
  debug-logger:
    enabled: true
    hook: PostToolUse
    actions:
      - action: log
        level: DEBUG
        message: "Tool {tool_name} completed in {duration_ms}ms"
        data:
          custom_metric: "{state.my_value}"
```

#### 2. Log-Based Triggers

```yaml
handlers:
  error-notifier:
    enabled: true
    hook: LogEvent  # Special hook triggered by log events
    match:
      level: ERROR
    actions:
      - action: notification
        message: "Error detected: {log.message}"
```

#### 3. Export Capabilities

```python
# Export to various formats
promptctl logs export --format csv --output report.csv
promptctl logs export --format json --compress --output logs.json.gz
promptctl logs export --format markdown --session current --output session.md

# Stream to external services (via plugins)
promptctl logs stream --destination datadog --api-key $DD_KEY
```

### Performance Optimizations

#### 1. Async Write-Behind Buffer

```python
class LogBuffer:
    def __init__(self, size: int = 10000):
        self.buffer = deque(maxlen=size)
        self.flush_task = None

    async def write(self, entry: LogEntry):
        self.buffer.append(entry)
        if len(self.buffer) > self.size * 0.8:
            await self.flush()

    async def flush(self):
        # Batch write to both JSONL and SQLite
        entries = list(self.buffer)
        self.buffer.clear()

        # Parallel writes
        await asyncio.gather(
            self._write_jsonl(entries),
            self._write_sqlite(entries)
        )
```

#### 2. Smart Compression

```python
class SmartCompressor:
    def compress_entry(self, entry: LogEntry) -> bytes:
        # Keep important fields uncompressed for quick access
        header = {
            'timestamp': entry.timestamp,
            'level': entry.level,
            'event': entry.event
        }

        # Compress payload with zstd (better for JSON)
        compressed_data = zstd.compress(
            json.dumps(entry.data).encode(),
            level=3  # Fast compression
        )

        # Check for deduplication opportunity
        if entry.data_hash in self.recent_hashes:
            return self._create_reference(entry.data_hash)

        return self._pack(header, compressed_data)
```

#### 3. Lazy Loading & Pagination

```python
class LogReader:
    def query(self, filter: LogFilter) -> LogIterator:
        # Returns iterator that loads chunks on demand
        return LogIterator(
            source=self.storage,
            filter=filter,
            chunk_size=1000
        )

class LogIterator:
    def __iter__(self):
        while True:
            chunk = self._load_next_chunk()
            if not chunk:
                break
            for entry in chunk:
                if self.filter.matches(entry):
                    yield entry
```

### Implementation Phases

#### Phase 1: Core Logging (Week 1)
- Basic capture layer with async writes
- JSONL file storage with rotation
- Simple console output with colors
- Configuration system

#### Phase 2: Smart Features (Week 2)
- Privacy scanning and redaction
- Semantic log levels
- SQLite hybrid storage
- Basic CLI query tool

#### Phase 3: Interactive Experience (Week 3)
- Terminal UI with real-time updates
- MCP tool integration
- Performance optimizations
- Smart compression

#### Phase 4: Advanced Capabilities (Week 4)
- Export capabilities
- Log-based triggers
- External streaming plugins
- Performance profiling integration

### Success Metrics

1. **Performance Impact**: < 1% overhead on hook processing
2. **Storage Efficiency**: 10x compression for typical workloads
3. **Query Speed**: < 100ms for common queries on 1M entries
4. **User Delight**: "It just works" - zero configuration needed
5. **Power User Satisfaction**: Every aspect customizable
6. **Privacy Compliance**: Zero PII leakage in default configuration
7. **Debugging Time**: 50% reduction in time to find issues

### Example Usage Scenarios

#### Scenario 1: New User Experience

```bash
# User installs promptctl, no configuration
$ claude "Please help me refactor this code"

# Logs automatically captured, user sees nothing unless error
# Later, user wants to see what happened
$ promptctl logs
[Beautiful, colored output showing the hook flow]
```

#### Scenario 2: Debugging Complex Handler

```bash
# User has a handler that's not working
$ promptctl logs --handler my-handler --level DEBUG

# See detailed execution flow with template rendering
13:42:15.234 CONTEXT_RENDER template="{tool_name}" result="Edit"
13:42:15.235 STATE_CHANGE key="last_tool" value="Edit"
13:42:15.236 HOOK_MATCHED conditions_met=true priority=10

# User realizes template variable was wrong
```

#### Scenario 3: Performance Investigation

```bash
# User notices Claude is slow
$ promptctl logs bottlenecks

Top slowest operations:
1. Handler: code-review (avg: 3.2s, called: 45 times)
   - Action: command "npm test" (avg: 2.8s)
2. Handler: git-commit (avg: 1.1s, called: 23 times)
   - Action: git "add -A" (avg: 0.7s)

$ promptctl logs timeline --session current
[Visual ASCII timeline showing where time was spent]
```

#### Scenario 4: Privacy-Conscious Enterprise User

```yaml
# strictest privacy settings
logging:
  processing:
    privacy:
      enabled: true
      sensitivity: paranoid  # Custom level
      redact_all_strings: true  # Replace all string values
      hash_identifiers: true    # Hash all IDs
  storage:
    encryption: true
    encryption_key: ${PROMPTCTL_LOG_KEY}
```

### What Makes This Flagship

1. **Zero to Hero**: Works perfectly out-of-box, scales to enterprise
2. **Beautiful by Default**: Logs you actually want to read
3. **Fast as Lightning**: Async everything, smart buffering
4. **Privacy First**: PII protection built into the core
5. **Infinitely Flexible**: Every single aspect can be customized
6. **Developer Joy**: The debugging experience becomes enjoyable
7. **Future Proof**: Extensible architecture for new features

This isn't just logging - it's a debugging transformation that makes users wonder how they ever lived without it. The combination of zero-configuration simplicity with infinite customization creates a tool that grows with the user, from their first handler to production deployment.

## Next Steps

1. Review and approve the specification
2. Begin Phase 1 implementation (core logging)
3. Create test harness for performance validation
4. Document migration path for existing users
5. Design plugin architecture for external integrations

The LogFlow system will become the gold standard for developer tool logging, setting a new bar for what "good logging" means in the CLI tool ecosystem.