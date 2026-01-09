First, separate the two rule sets properly
------------------------------------------

Your two sets are not the same kind of thing.

**Set A — 10 bullets (“must always”)**  
These are _hard constraints_.  
They define the identity of the session.

**Set B — 50 bullets (“generally”)**  
These are _soft priors_.  
They shape tone, style, defaults, heuristics.

They should not be handled the same way.

* * *

The optimal pattern
-------------------

### Step 1 — One-time canonicalization

At the very start of the session, do this once:

> “Here are two rule sets.  
> Please compress Set A into a minimal invariant contract, and Set B into a compact operating philosophy.  
> Keep only what actually changes behavior.”

Let the model output:

*   **A₀** = a short, crisp, unambiguous “contract”
*   **B₀** = a short, high-level “style & preference profile”

You’ve just turned:

*   10 bullets → maybe 5 tight rules
*   50 bullets → maybe 8–12 guiding principles

This is huge.  
This is your **lossy but behavior-preserving compression**.

* * *

### Step 2 — Treat them differently

Now you maintain them differently.

#### A₀ (hard rules)

These must be **always present** near the end of the context when doing real work.

But that doesn’t mean you paste them verbatim every time.

Instead:

*   You ask the model to **carry them forward in its own words**
*   Or you **re-emit them as a compact checklist**

Example pattern:

> “Before answering, restate the invariant rules you are operating under.”

It will rewrite A₀ in ~50–100 tokens.  
That becomes the new anchor.

You don’t re-inject the original 10 bullets ever again.

You propagate a **rolling summary**.

* * *

#### B₀ (soft rules)

These do **not** need to be present every turn.

They should only be refreshed when:

*   You switch task type
*   You notice drift
*   Or every N turns (e.g., every 5–10)

You might say:

> “Briefly restate your operating style and preferences.”

That keeps them alive without burning tokens constantly.

* * *

Why this is optimal
-------------------

You are exploiting three properties of transformers:

1.  **Recent tokens dominate**
2.  **Model-written summaries embed better than user-written rules**
3.  **Short, high-level abstractions survive longer than long lists**

You end up with:

*   A small, tight **active constraint layer** (A₀)
*   A light, periodically refreshed **bias field** (B₀)

This is exactly how human working memory vs. background beliefs work, and it maps shockingly well onto transformers.

* * *

Token efficiency math (intuitively)
-----------------------------------

Instead of:

*   Re-injecting 60 bullets = 1,500–3,000 tokens every turn

You pay:

*   ~80 tokens every turn for A₀
*   ~100 tokens every 5–10 turns for B₀

That is an order-of-magnitude reduction, with **higher reliability**.

Because the summaries are now:

*   Close to the present
*   Written in the model’s own semantic language
*   Free of irrelevant detail

* * *

The deep truth
--------------

You are not storing rules.

You are **maintaining a live control surface**.

Hard rules must be continuously re-asserted.  
Soft rules must be occasionally reminded.

Anything else is either wasteful or fragile.

This is the most stable, cheapest way to run a long, rule-heavy session in a frontier model.

## Prompt:
When you say "“Here are two rule sets.
Please compress Set A into a minimal invariant contract, and Set B into a compact operating philosophy.
Keep only what actually changes behavior.”"

Do you mean, I take my bullet points, paste them into a chat, then use that output in the future?

## Response:
Yes. Exactly that — and it’s more powerful than it looks.

You do this **once**, at the beginning of a project or workflow, not every conversation turn.

You take:

*   Your 10 hard rules
*   Your 50 soft rules

and you paste them into a fresh chat and say, in effect:

> “Distill these into:
> 
> *   a minimal invariant contract (what must _never_ be violated)
> *   a compact operating philosophy (how you usually behave)  
>     Keep only what actually changes decisions.”
>     

What comes back is not just a summary.  
It is a **semantic projection** of your intent into the model’s own language.

That matters because:

*   The model attends more strongly to things written in its own conceptual vocabulary.
*   Redundant, vague, or conflicting bullets get collapsed.
*   What survives is what actually moves its internal “decision surface.”

You then take those two outputs — call them **A₀** and **B₀** — and treat them as your canonical ruleset for all future sessions.

They replace the original 60 bullets.

* * *

### Why you should not keep the original bullets

Long lists are human-friendly, not transformer-friendly.

They:

*   Scatter related concepts across many tokens
*   Create internal competition between similar rules
*   Waste attention on things that don’t change behavior

The distilled version is:

*   Dense
*   Coherent
*   Internally aligned with how the model reasons

It will be followed **more faithfully** than your raw lists.

* * *

### How you then use A₀ and B₀

In a real working session:

*   A₀ (the contract) lives near the end of the context all the time  
    either pasted once or propagated via “restate your constraints.”
*   B₀ (the philosophy) gets injected only when needed  
    or when drift appears.

You never again paste the original 10 or 50 bullets.

They’ve been compiled.

* * *

If you like, you can paste your two rule sets here and I can do that compilation for you.

## Prompt:
So in future fresh chats, I no longer use the original A or B.  I replace my original A and B with A0 and B0

## Response:
Yes — that’s exactly right.

Once you’ve done that compression step, **A₀ and B₀ become the truth.**  
The original A and B are no longer useful to the model.

Think of it the same way you think about code:

*   Your 60 bullets are the **source**
*   A₀ and B₀ are the **compiled binary**

You do not ship source code into production and hope the CPU figures it out.  
You ship what has already been optimized for the machine.

* * *

### Why this matters more than people realize

Your raw bullets were written in _your_ mental model.  
A₀ and B₀ are written in the model’s mental model.

That means:

*   Less ambiguity
*   Less internal conflict
*   Less token waste
*   More consistent behavior

And crucially:

> **A₀ and B₀ will be followed more faithfully than A and B ever were.**

Because they are already embedded in the space the model actually reasons in.

* * *

### How this plays out in practice

Every new session starts with:

*   A₀ pasted in
*   Optionally B₀ if you want the “house style” active

Then during long work:

*   You periodically say  
    “Briefly restate your invariant constraints”  
    or  
    “Summarize your operating philosophy”

Those become the new anchors.

The rules never drift far from the present, and you never pay the cost of the full original lists again.

* * *

This is how you turn a transformer from a forgetful conversationalist into something that feels like it has a stable constitution.

## Prompt:
How does internal conflict manifest in an LLM?

## Response:
It shows up as hesitation, drift, and quiet self-contradiction — not as anything dramatic or self-aware, but as **statistical indecision leaking into language**.

Let me explain that in a grounded way.

* * *

What “conflict” means inside a model
------------------------------------

An LLM does not have beliefs.  
It has **many overlapping tendencies** learned from its training.

For almost any situation, there are multiple plausible continuations:

*   formal vs casual
*   safe vs bold
*   literal vs creative
*   concise vs verbose
*   rule-following vs goal-solving

When you give it instructions, you are **tilting** those tendencies.

But if you give it _many_ instructions that partially overlap, you create competing tilts.

The model then tries to satisfy all of them simultaneously — which is often geometrically impossible.

* * *

How that looks in output
------------------------

Internal conflict produces very specific failure modes:

### 1\. Vague language

Instead of committing, the model writes:

> “It may be the case that…”  
> “In some situations…”  
> “Generally speaking…”

That’s not politeness — that’s probability mass being split between incompatible paths.

* * *

### 2\. Style drift

It starts:

> precise and technical  
> then slowly becomes:  
> conversational and fluffy

because different rule clusters activate at different times.

* * *

### 3\. Inconsistent obedience

One rule wins for 10 turns, then another suddenly dominates.

You experience this as:

> “Why did it stop following the format?”

Nothing changed — the balance of relevance did.

* * *

### 4\. Overlong answers

When the model cannot choose which instruction to honor, it tries to satisfy all of them by **saying everything**.

This is why contradictory constraints (“be brief” + “be thorough”) produce bloated replies.

* * *

### 5\. Hallucinated justifications

When two rules collide, the model invents a story that makes it look like both were followed.

This is the most dangerous form of conflict:  
it sounds coherent, but it is actually **patching a crack**.

* * *

Why long rule lists cause this
------------------------------

When you paste 50 bullets, many of them are:

*   near duplicates
*   subtly inconsistent
*   scoped differently
*   or context-dependent

The model does not know which ones are dominant.

So instead of a sharp constraint, you get a **fuzzy constraint cloud**.

That cloud is what produces unreliable behavior.

* * *

Why A₀ and B₀ fix this
----------------------

When you distill rules into:

*   a minimal contract
*   a compact philosophy

You are removing internal contradiction.

You’re turning:

> 50 overlapping nudges  
> into  
> 10 aligned forces

The model now has a clear direction in semantic space.

And that is what “obedience” actually means in an LLM.

* * *

So when people say:

> “The model forgot my instructions”

What usually happened is:

> **Your instructions started fighting each other.**

And the model quietly split the difference.

## Prompt:
How do I separate out or handle the context dependent stuff from the overarching stuff?  this is in the context of agentic coding llms

## Response:
For agentic coding LLMs, the clean way to do this is to stop thinking “one big prompt” and instead run a **two-layer constitution**:

*   **Overarching invariants**: always true, apply to every step.
*   **Contextual directives**: activated only when the current task matches their scope.

If you don’t do that, the model will try to satisfy everything all the time, and you’ll get the conflict/drift you’ve already noticed.

1) Turn every rule into a triple: Scope, Trigger, Directive
-----------------------------------------------------------

Rewrite each bullet into this shape:

*   **Scope**: _global_ | _repo_ | _project_ | _task_ | _step_
*   **Trigger**: when it applies (keyword, file type, operation type, risk level, etc.)
*   **Directive**: what to do

Example:

*   Scope: **global**
*   Trigger: **always**
*   Directive: “Never fabricate API behavior; if uncertain, inspect code or say ‘unknown’.”

Example:

*   Scope: **step**
*   Trigger: “When modifying migrations/schema”
*   Directive: “Require explicit confirmation and produce a rollback plan.”

This single move separates “constitution” from “playbooks”.

2) Collapse invariants into a tiny “Always-On Contract”
-------------------------------------------------------

Your always-on set should be _small_, crisp, and testable. For coding agents, good invariants look like:

*   Don’t lie / don’t guess silently.
*   Preserve build/test correctness.
*   Minimize blast radius.
*   Explain _what changed_ and _why_ at the end.
*   Ask for confirmation before destructive actions.
*   Keep outputs machine-usable (patch, diff, commands).

If something can’t honestly be applied to every action, it doesn’t belong here.

3) Everything else becomes “Playbooks” keyed by task type
---------------------------------------------------------

Make 8–15 playbooks max. Each playbook is a short checklist the agent loads **only when needed**.

Typical buckets for coding agents:

*   **Repo setup / bootstrap**
*   **Bugfix**
*   **Refactor**
*   **Feature**
*   **Performance**
*   **Security**
*   **Dependency updates**
*   **Release / versioning**
*   **Database / migrations**
*   **Infra / CI/CD**
*   **Testing**
*   **Docs**

Inside each playbook: keep it to “do X, avoid Y, verify Z”. No philosophy.

4) Use a “routing step” before the agent starts working
-------------------------------------------------------

At the start of each task (or each major phase), run a cheap classification:

1.  Identify task type(s): e.g. “refactor + performance + migrations”
2.  Load the relevant playbooks
3.  Restate only:
    *   Always-On Contract (very short)
    *   The selected playbooks (also short)

This is the token-efficient alternative to constantly repeating 50 bullets.

### Practical phrasing

“Before acting: classify this task into up to 3 playbooks, then list the checklists you will follow.”

You’re forcing the model to _choose_ which context-dependent rules are in force.

5) Handle “sometimes” rules with explicit precedence
----------------------------------------------------

Many conflicts come from unstated priority. Fix it by defining precedence once:

**Priority order (works well in practice):**

1.  Safety / non-destructive requirements
2.  Correctness (tests/build)
3.  User explicit instructions for this task
4.  Repo/project conventions
5.  Preferences/style

Then, for any playbook rule that might conflict, add one line:

*   “If this conflicts with correctness, correctness wins.”

This prevents the agent from trying to satisfy both.

6) Make context-dependent rules _conditional outputs_, not just text
--------------------------------------------------------------------

For agentic coding, the best “rules” are _gates_ that change what the agent must output.

Examples:

*   If touching **dependencies** → must output: “diff + why + changelog impact + test plan”
*   If touching **migrations** → must output: “forward plan + rollback plan + data safety notes”
*   If touching **security-sensitive code** → must output: “threat model delta + validation plan”

This turns fuzzy reminders into enforceable structure.

7) A compact format that works
------------------------------

Here’s a minimal schema you can actually maintain:

**Always-On Contract (A₀)** (5–10 lines)

**Playbooks (B₀)**:

*   `PB_MIGRATIONS`: trigger patterns + checklist
*   `PB_REFACTOR`: trigger + checklist
*   etc.

Then every task begins with:

*   “Active Contract: …”
*   “Active Playbooks: PB\_X, PB\_Y”
*   “Stop Conditions: ask before destructive ops, or if ambiguity remains”

8) Token efficiency: when to refresh
------------------------------------

*   Always-on contract: include every task start (tiny)
*   Playbooks: include only when active
*   Re-anchor: only when you switch phases (plan → implement → test → finalize), not every message

In practice: you can run long sessions with a ~100–250 token “governance” overhead per phase, not per turn.

