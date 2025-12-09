# Web Application Evaluation Profile

## Characteristics
- Multi-user, concurrent access
- Stateful (sessions, databases)
- UI interactions (forms, navigation)
- Network requests (API calls)
- Browser-based rendering

## ALWAYS RUN (~60 seconds)

| Check | How | Pass Criteria |
|-------|-----|---------------|
| App starts | `npm run dev` or equivalent | No errors, server listening |
| Home page loads | Navigate to root URL | Page renders, no console errors |
| Basic navigation | Click 2-3 main nav links | Pages load without error |
| Form submission | Submit a simple form | Form processes, feedback shown |
| Error page | Navigate to /nonexistent | 404 page, not crash |

## RUN IF APPLICABLE

| Check | Condition | How |
|-------|-----------|-----|
| Authentication | App has login | Login, logout, protected routes |
| Data persistence | App saves user data | Create item, refresh, verify exists |
| Responsive design | Mobile users expected | Resize to mobile width |
| Loading states | Async data fetching | Verify spinners/skeletons shown |
| Form validation | Forms have constraints | Submit invalid data |
| Pagination | Lists > 10 items | Navigate pages, verify correct items |
| Search/filter | Search feature exists | Test with matches, no matches |

## SKIP UNLESS USER REQUESTS

| Check | Why Skip | When User Might Request |
|-------|----------|------------------------|
| Cross-browser testing | Time-consuming | "Works in Chrome but not Safari" |
| Performance audits | Lighthouse takes time | "Page feels slow" |
| Accessibility audit | Comprehensive a11y is lengthy | "Need WCAG compliance" |
| Security testing | Specialized skill | Pre-launch security review |
| Load testing | Requires infrastructure | "Expecting high traffic" |

## SKIP ENTIRELY

| Check | Reason |
|-------|--------|
| Exit codes | Not applicable |
| CLI argument parsing | Not a CLI |
| Stdin/stdout testing | Not applicable |

## Common Web App Blind Spots

Check these specifically:
- **Empty states**: What shows with no data?
- **Long content**: Text overflow, truncation
- **Rapid clicks**: Double-submit protection
- **Back button**: State preserved correctly?
- **Refresh**: Form data lost? Appropriate warning?
- **Network failure**: Graceful error handling?

## Evidence to Capture

Use chrome-devtools MCP when available:
```
URL: <page URL>
Screenshot: <path to screenshot>
Console errors: <any errors>
Network failures: <any failed requests>
Visible text: <key content>
```

Without chrome-devtools:
```
URL tested: <url>
Server logs: <relevant entries>
Database state: <if applicable>
Error output: <any errors>
```
