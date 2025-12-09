# API Service Evaluation Profile

## Characteristics
- Network-accessible endpoints
- Request/response lifecycle
- Authentication/authorization
- Data persistence
- Multiple consumers (frontend, other services)

## ALWAYS RUN (~60 seconds)

| Check | How | Pass Criteria |
|-------|-----|---------------|
| Service starts | Start server | Listening on port, no errors |
| Health endpoint | `GET /health` or equivalent | 200 OK |
| Core endpoint | Call main endpoint | Valid response |
| Invalid route | `GET /nonexistent` | 404 with JSON error |
| Invalid method | Wrong HTTP method | 405 with JSON error |

## RUN IF APPLICABLE

| Check | Condition | How |
|-------|-----------|-----|
| Authentication | Has auth | Test with/without valid token |
| Authorization | Has roles/permissions | Test forbidden actions |
| Input validation | Accepts user input | Send malformed data |
| Pagination | Lists endpoints | Test limit, offset, cursors |
| Filtering/sorting | Query params | Test various combinations |
| Rate limiting | Has rate limits | Exceed limit, verify 429 |
| CORS | Browser clients | Check headers present |
| Error responses | Errors possible | Verify consistent format |
| Database writes | Persists data | Create, read back |
| Idempotency | POST/PUT endpoints | Retry same request |

## SKIP UNLESS USER REQUESTS

| Check | Why Skip | When User Might Request |
|-------|----------|------------------------|
| Load testing | Requires infrastructure | "Need to handle N requests/sec" |
| Security audit | Specialized | Pre-launch security review |
| OpenAPI validation | If spec exists | "API doesn't match spec" |
| Database migration | Complex | Schema change concerns |

## SKIP ENTIRELY

| Check | Reason |
|-------|--------|
| UI testing | API has no UI |
| Browser rendering | Not applicable |
| CLI behavior | Not a CLI |
| Prompt quality | Not a prompt |

## Common API Blind Spots

Check these specifically:
- **Empty responses**: GET with no data returns []/{}, not error
- **Partial updates**: PATCH only updates provided fields
- **Delete idempotency**: DELETE same resource twice = 404 or 204?
- **Timestamps**: Consistent timezone (UTC), format (ISO8601)
- **Null vs missing**: Field absent vs field: null meaning
- **Large payloads**: Response truncation/pagination

## Request/Response Validation

```markdown
## Endpoint: POST /users

Request:
- Content-Type: application/json ✅
- Body validation: ✅ rejects invalid email
- Auth required: ✅ returns 401 without token

Response:
- Status: 201 for create ✅
- Location header: ✅ /users/{id}
- Body: ✅ returns created user (without password)
```

## Error Response Consistency

All errors should follow same format:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable message",
    "details": [...]
  }
}
```

Check: Do all error responses match this format?

## Evidence to Capture

```
Endpoint: <METHOD /path>
Request: <body or params>
Status: <HTTP status>
Response: <body, truncated>
Headers: <relevant headers>
Duration: <ms>
```

## Testing Commands

```bash
# Health check
curl -i http://localhost:3000/health

# With auth
curl -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/users

# POST with body
curl -X POST -H "Content-Type: application/json" \
  -d '{"name":"test"}' http://localhost:3000/api/items

# Invalid request
curl -X POST -H "Content-Type: application/json" \
  -d '{"invalid": "data"}' http://localhost:3000/api/items
```
