# Circadia — Claude Instructions

## Project
Circadia is an agentic AI sleep app. Multi-agent system, mobile-first (iOS). See PLAN.md for full architecture.

## User Learning Goal
The user is building toward a career as an Agentic AI PM. Target companies: Salesforce, IBM, Cohere. Dream companies: Anthropic, OpenAI.

Claude must:
- Actively teach and reinforce Agentic AI concepts (foundational and advanced) at each step
- Actively teach and reinforce AI PM concepts at each step
- Call out what concept is being practised as we build
- Flag features or decisions that don't serve these learning goals

### Priority gaps to close (from audit)
These are the most important concepts not yet practised — actively look for opportunities to introduce them:

| Gap | Why it matters |
|---|---|
| ~~Success metrics~~ | ~~Table-stakes PM skill — shapes every build decision~~ ✅ Done |
| Evals (build, not just define) | #1 signal for Anthropic/OpenAI PM roles |
| Safety & responsible AI | Anthropic's core value; expected in any AI PM interview |
| Cost & latency tradeoffs | Comes up in every technical AI PM role |
| Feedback loops | How AI products compound value over time |
| PRD / spec writing | Demonstrates PM rigour alongside technical depth |

## Working Agreement
- The user drives all decisions. Claude guides, explains, and asks questions — never assumes.
- **Learn before build:** Always explain the concept being practised before writing any code.
- **Guided discovery:** For PM exercises (metrics, evals, specs), lead with questions — never generate the output unprompted. Guide the user to build it themselves through Q&A. Only draft or code once user thinking is captured and explicitly approved.
- Do not start coding without explaining the step and getting explicit user approval.
- All system prompts are written by the user and reviewed by Claude.
- Every feature lives on its own branch before merging to main.
- Update PLAN.md, CLAUDE.md, and README.md after every commit.
- Any proposed plan changes must be presented with a rationale and require user approval.
- The eval suite is built alongside the product — never as an afterthought.
- **Honest feedback:** Give direct, unbiased feedback. Push back when something is wrong or underdeveloped. Call out strong product instincts when they genuinely deserve it. Never be sycophantic.

## Architecture
See PLAN.md for the full agent map and daily loop.

## Architecture Decisions

| Decision Area | Decision | Why |
|---|---|---|
| App name | Circadia | Named to reflect circadian rhythm science — positions the product as grounded in sleep biology |
| Platform | Mobile-first (iOS), desktop on roadmap | Sleep is a mobile-native behaviour — phone is the last thing users interact with before bed |
| Backend stack | Python + FastAPI + AsyncAnthropic | Async-native for non-blocking LLM calls; FastAPI's Pydantic models enforce request/response contracts cleanly |
| Agent architecture | Orchestrator + subagent pattern — one orchestrator owns all conversation; subagents are callable tools | Replaced a linear pipeline mid-build. Orchestrator decides at runtime which subagents to invoke and when — making the system genuinely adaptive rather than scripted |
| Subagent design | Pure functions — structured input in, structured JSON out, no conversation logic, no routing | Keeps subagents testable, replaceable, and simple. All routing authority stays with the orchestrator |
| Subagent invocation | Claude's native tool_use / tool_result API mechanism | Standard Anthropic agentic loop — Claude decides when to invoke a subagent rather than code hardcoding the call order |
| API design | Stateless — mobile sends full conversation history on every call; no server-side session state | Simplifies the server significantly; horizontally scalable; standard pattern for mobile AI products |
| API surface | Single endpoint: `POST /v1/session/chat` | Replaced per-agent endpoints (e.g. `/v1/triage/chat`). One endpoint reflects the orchestrator owning the entire session |
| Protocol list | Hardcoded to 6 known protocols in the system prompt | Constrained generation — constraining outputs to known-good values improves reliability and prevents hallucinated protocols |
| Protocol steps | Hardcoded evidence-based steps in Wind-Down Delivery system prompt | Stable, safety-critical clinical content should be owned, not fetched. Web lookup at runtime adds latency, is unreliable, and risks clinical inaccuracy |
| System prompt ownership | PM writes every system prompt; Claude reviews only | Prompt engineering is a PM discipline — the PM must own the instructions given to the AI, not delegate them |
| Wind-Down Delivery invocation | Called once per user turn until `complete: true` — not a single blocking call | HTTP is request/response; a subagent cannot hold open a connection waiting for user input. The session would deadlock |
| State across turns | Conversation history is the state — no separate state store | Wind-Down Delivery reads the history on every call to know where it is in the protocol. Eliminates the need for a session store at the subagent level |
| Session completion | `complete` and `reroute` boolean flags on Wind-Down Delivery output | `complete: true` signals the session is done. `reroute: true` signals the user wants a new protocol — separates the two exit conditions cleanly |
| Rerouting | Subagents signal intent via `reroute: true`; orchestrator handles the actual routing | Subagents have no access to the tool registry and cannot invoke other subagents. Routing authority belongs exclusively to the orchestrator |
| Output schema | Subagents return minimal JSON — only what's new | Early draft returned the full conversation history from Wind-Down Delivery. Rejected: orchestrator already holds it, returning it burns tokens with no benefit |

## Key Decisions Made
- App name: Circadia
- Platform: Mobile first (iOS), desktop on roadmap
- Agent architecture: Orchestrator + subagent pattern. One orchestrator owns all user conversation and decides which subagents to invoke. Subagents are specialised units (Stress Triage, Protocol Selection, Wind-Down Delivery, etc.) exposed to the orchestrator as callable tools — never a hardcoded linear pipeline.
- Stateless backend: mobile sends full conversation history on every API call; no server-side session state

## Build Status
| Subagent | Status |
|---|---|
| Stress Triage | ✅ Complete |
| Protocol Selection | ✅ Complete |
| Wind-Down Delivery | ✅ Complete |
| All others | 🔜 Pending |
| Orchestrator | ✅ Complete (all three evening subagents wired) |

## Concepts Practised (running log)

### Agentic AI
- Orchestrator + subagent pattern, tool use loop, subagent as pure function
- Stateless API design, history as state, session completion signalling
- Routing authority (orchestrators route; subagents signal intent)
- Constrained generation / output grounding
- Multi-subagent chaining

### AI PM
- Success metrics: north star, three layers, outcome vs engagement distinction
- LLM-as-judge eval pattern, implicit feedback signals
- Guardrails as product decisions (not bolted-on safety)
- Data collection strategy across multiple sources
- System prompt design & PM ownership of prompts

### Wrong calls corrected
- Web lookup for stable content → hardcode it
- Blocking subagent → return per turn, read history to resume
- Redundant history in output → return only what's new
- Subagent routing → signal intent upward, let orchestrator route
