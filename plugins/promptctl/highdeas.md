
Got it — low-frequency, sometimes-synchronous, function-call style events. Here’s a tight, practical set of patterns and concrete decisions tuned to that workload (no fluff).

Top-line architecture
•	API gateway (gRPC or HTTP/JSON with HTTP/2) that accepts requests, enforces auth/quotas, and forwards to a stateless worker pool. Use unary RPC for function-call semantics and built-in deadlines.
•	Stateless service instances (async event loop or lightweight thread-per-request) that run rules synchronously and return a value. Scale by instance count — you don’t need heavy brokering for 0.03–1 req/s.
•	Durable audit store (append-only table or lightweight event log) for every incoming request + decision + output for replay/debugging.

Request flow (recommended)
1.	Ingress → validate schema → assign request_id/correlation id.
2.	Persist incoming request record (minimal) synchronously (or at least in the same DB transaction as the decision if you require durability).
3.	Execute rule evaluation in-process with a strict deadline (e.g., RPC deadline minus safety margin).
4.	Persist decision/result and any outbound side effects (use transactional outbox).
5.	Return response (or an immediate token + async result if you must offload long work).

Rule-engine choices (for low QPS & sync response)
•	Compiled rules / functions: rules expressed as code or compiled DSL → load into process. Fast, deterministic, easy to profile. Use when rules are moderate in number and performance matters.
•	Decision tables + engine: if non-devs must author rules, use decision tables (CSV/Excel → engine) or a safe sandbox (WASM). Evaluate with a fast interpreter.
•	WASM sandbox: safe, hot-reloadable, good for per-tenant custom logic while keeping main process stable.
•	Avoid heavy Rete or CEP unless you need complex, stateful pattern matching over many events.

State & persistence
•	Primary DB: single ACID DB (Postgres) is fine — low throughput, simple transactions, rich indexing.
•	Audit/event log: append-only table (or a small Kafka if you want replay later), with snapshots for stateful rules.
•	Transactional outbox for side-effects (so responses are durable and no lost calls).
•	Local cache (in-memory LRU) for read-heavy lookups if rules need reference data.

Concurrency, deadlines, and reliability
•	Use async handler model (goroutines / async/await) to avoid blocking threads on IO.
•	Enforce per-request deadlines and circuit breakers on downstream calls. Return deterministic error codes for timeouts.
•	Idempotency keys for retries: accept idempotency_key and dedupe using DB constraint or small cache.
•	Retries: local retry for transient failures with exponential backoff; never retry silently across business-logic boundaries.

Observability & governance
•	Structured logs with request_id, trace ids; always persist request + decision.
•	Distributed tracing even at low QPS — it catches latent bugs.
•	Per-rule metrics: invocation count, avg latency, error rate, last-change timestamp.
•	Rule change governance: git-backed rule bundles, automated tests, canary rollout, and immediate rollback hooks.

Security & operational controls
•	Auth via mTLS or JWT; RBAC for rule changes.
•	Sandboxing of user-supplied logic (WASM or separate process) with CPU/memory caps.
•	PII redaction in logs and encrypt-at-rest for the event store.

Practical combos (pick one)
•	Simple/fast: gRPC unary → Go async handlers → Postgres for audit + outbox → compiled rules (Go functions).
•	Non-dev rule authors: HTTP JSON → Python/Go service → decision-table engine or WASM for rule logic → Postgres.
•	Per-tenant custom logic: WASM sandbox per-tenant, rules deployed as WASM bundles, executed in-process with limits.

Edge-case patterns
•	If a rule needs to call remote services but must still reply synchronously: return a short-circuit deterministic value if downstream unavailable (circuit open) or return an encoded “deferred result” token and perform async execution with callback/webhook.
•	For reproducibility: store inputs, code version, and deterministic random seeds with each decision so you can replay exactly.

You can implement a robust, simple, auditable, low-latency decision service with these choices and avoid heavyweight stream infra without sacrificing correctness or observability.

This design will give you predictable synchronous responses, durable audits, and safe rule evolution.
