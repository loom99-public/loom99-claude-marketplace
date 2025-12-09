# CLI Tool Evaluation Profile

## Characteristics
- Single-user execution
- Typically stateless between runs
- Input via arguments, flags, stdin
- Output via stdout, stderr, exit codes
- May read/write files

## ALWAYS RUN (~30 seconds)

| Check | How | Pass Criteria |
|-------|-----|---------------|
| Help flag works | `<cmd> --help` | Exits 0, shows usage |
| Version flag works | `<cmd> --version` | Shows version string |
| No args behavior | `<cmd>` | Helpful error or default action |
| Invalid args | `<cmd> --invalid-flag` | Non-zero exit, error message |
| Exit codes | Run with valid/invalid input | Correct exit codes (0=success, non-zero=error) |

## RUN IF APPLICABLE

| Check | Condition | How |
|-------|-----------|-----|
| File input | Tool accepts file paths | Test with existing file, non-existent file, empty file |
| Stdin input | Tool reads stdin | `echo "input" \| <cmd>` |
| Output format | Tool has --json/--csv flags | Verify parseable output |
| Quiet mode | Tool has -q/--quiet flag | Verify suppresses non-essential output |
| Verbose mode | Tool has -v/--verbose flag | Verify additional output |
| Config file | Tool reads config | Test with valid config, missing config, invalid config |

## SKIP UNLESS USER REQUESTS

| Check | Why Skip | When User Might Request |
|-------|----------|------------------------|
| Performance benchmarks | Time-consuming, rarely blocking | "Tool feels slow" |
| Large file handling | Requires test data generation | "Need to process big files" |
| Shell integration | Complex environment setup | "Tab completion not working" |

## SKIP ENTIRELY

| Check | Reason |
|-------|--------|
| Pagination | CLI tools don't paginate |
| Concurrent access | Single-user tool |
| Session management | Stateless |
| Browser testing | No UI |
| Memory profiling | Overkill for CLIs |

## Common CLI Blind Spots

Check these specifically:
- **Path handling**: Spaces in paths, relative vs absolute, ~ expansion
- **Unicode**: Non-ASCII filenames, content with emoji
- **Empty input**: Zero bytes, empty lines
- **Pipe behavior**: Works in pipeline (`cat file \| cmd \| other`)
- **TTY detection**: Different behavior for interactive vs piped

## Evidence to Capture

```
Command: <exact command run>
Exit code: <n>
Stdout (truncated): <first 500 chars>
Stderr: <if any>
Files created/modified: <list>
```
