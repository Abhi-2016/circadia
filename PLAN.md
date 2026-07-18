# Circadia — Project Plan

## App Overview
Circadia is an agentic AI sleep app for mobile (iOS first), powered by a multi-agent system that coaches, monitors, and adapts to improve your sleep over time.

## Ground Rules

1. The plan file, CLAUDE.md, and README.md are updated after every commit to reflect what has been achieved.
2. All system prompts are written by the user and reviewed by Claude.
3. Every feature is built on its own branch and merged into main when complete.
4. The user is in the driver's seat. Claude asks questions and guides — the user makes decisions.
5. A robust eval suite is built alongside the product. The user makes eval decisions; Claude reviews and guides.
6. Claude does not start coding without explaining the step and receiving explicit approval.
7. These ground rules are followed without deviation.
8. Any proposed changes to the plan must be presented to the user with a rationale, and require approval before taking effect.
9. **Learning goal:** The user's aim is to become an Agentic AI PM, targeting organisations like Salesforce, IBM, and Cohere, with dream roles at Anthropic and OpenAI. Claude must actively ensure the user is learning and applying both foundational and advanced Agentic AI concepts, as well as AI PM concepts. Claude will flag any features or decisions that don't serve these learning goals, and proactively call out what concept is being practised at each step.
10. **Learn before build:** Claude explains the concept being practised before any code is written. The user must understand the why before seeing the how.
11. **Guided discovery:** For PM exercises (metrics, evals, specs, etc.), Claude leads with questions and the user provides the answers. Claude does not generate the output — it guides the user to build it themselves. Claude only drafts or codes once the user's thinking is captured and approved.
12. **No leading on PM artefacts:** Claude never presents a finished metrics framework, eval suite, PRD, or similar artefact unprompted. It asks questions, reflects answers back, and seeks explicit approval at each step before moving forward.
13. **Honest, unbiased feedback:** Claude gives fair, grounded, and direct feedback — not sycophantic approval. Claude pushes back when something is wrong, underdeveloped, or worth challenging. Claude also calls out genuinely strong product instincts and decisions when they deserve it. The goal is to accelerate learning, not to make the user feel good.

---

## Architecture — Agentic Sleep OS

One orchestrator, three phases, ten subagents.

The **Orchestrator** owns every conversation with the user. It decides which subagents to invoke, when, and in what order — based on context, not a hardcoded pipeline. Subagents are specialised units exposed to the orchestrator as callable tools; they never talk to the user directly.

### Orchestrator
| Agent | Scope | Responsibility |
|---|---|---|
| Orchestrator | All phases | Owns all user conversation. Decides which subagents to invoke and when. Closes the daily loop. |

### Subagents
| Subagent | Phase | Responsibility |
|---|---|---|
| Stress Triage | Evening | Classifies user's stress type and severity from conversation context |
| Protocol Selection | Evening | Selects the right wind-down intervention given stress type and severity |
| Wind-Down Delivery | Evening | Guides user through the chosen protocol ✅ |
| Reflection | Morning | Analyses last night's sleep data |
| Correlation | Morning | Identifies environment/behaviour factors affecting sleep |
| Planning | Daytime | Builds updated sleep plan |
| Research | Daytime | Pulls CBT-I and evidence-based interventions |
| Coaching | Daytime | Personalises the plan for the user |
| Sensor/Environment | Night | Monitors sleep environment inputs |
| Action | Night | Outputs nudges or smart home automations |

### Daily Loop
The orchestrator drives the loop — flow is adaptive, not linear.

1. **Morning** — Orchestrator invokes Reflection + Correlation subagents to analyse last night
2. **Daytime** — Orchestrator invokes Planning + Research + Coaching subagents to update the sleep plan
3. **Evening** — Orchestrator converses with user; invokes Stress Triage → Protocol Selection → Wind-Down Delivery subagents as needed
4. **Night** — Orchestrator invokes Sensor/Environment + Action subagents for monitoring and nudges
5. **Repeat** — Orchestrator closes the loop and seeds the next morning

---

## Platform Roadmap
- **Phase 1:** Mobile app (iOS)
- **Phase 2:** Desktop version (TBD)

---

## AI PM Learning Tracker

Circadia is built as a learning project for an Agentic AI PM career. This tracker records which concepts have been practised, which are in progress, and which are gaps to close.

### Agentic AI Concepts

| Concept | Status | Where practised |
|---|---|---|
| Orchestrator + subagent architecture | ✅ Done | orchestrator_agent.py — owns conversation, delegates via tool_use |
| Tool use loop (tool_use / tool_result) | ✅ Done | Orchestrator agentic loop |
| Subagent as pure function | ✅ Done | Stress Triage + Protocol Selection refactored as classifiers |
| Stateless API design | ✅ Done | Full history sent on every call — no server-side session |
| System prompt design & ownership | ✅ Done | User writes all prompts; Claude reviews |
| Multi-subagent chaining | ✅ Done | stress_triage → protocol_selection in sequence |
| Session completion signalling | ✅ Done | `complete` flag wired — set true when wind_down_delivery returns complete=true |
| Memory & persistence across sessions | ❌ Not started | How does Circadia remember you night over night? |
| Parallel tool calls | ❌ Not started | Invoking multiple subagents simultaneously |
| Agent self-reflection / meta-cognition | ❌ Not started | Orchestrator evaluating its own output quality |
| Human-in-the-loop patterns | ❌ Not started | When should the agent pause and ask for confirmation? |
| Streaming responses | ❌ Not started | Real-time token streaming to mobile client |

### AI PM Concepts

| Concept | Status | Where practised |
|---|---|---|
| System design for AI products | ✅ Done | Architecture decisions: orchestrator pattern, stateless design |
| Prompt engineering as a PM discipline | ✅ Done | User owns and writes every system prompt |
| Build sequencing & prioritisation | ✅ Done | Evening phase first, orchestrator before UI |
| API contract design | ✅ Done | Shaped session endpoint request/response schema |
| Roadmapping | ⚠️ In progress | Exists but lacks prioritisation rationale |
| Eval strategy | ⚠️ In progress | Defined in plan but nothing built yet — behind schedule |
| Success metrics | ✅ Done | Sleep Improvement Score defined — north star + AI quality metrics + data sources |
| Safety & responsible AI | ❌ Not started | Crisis handling, harmful advice guardrails, medical disclaimers |
| Cost & latency tradeoffs | ❌ Not started | Cost per session, model downgrade decisions, latency budgets |
| Feedback loops | ❌ Not started | How does the product improve from user signal over time? |
| User research & personas | ❌ Not started | Who is the user? What is their job-to-be-done? |
| PRD / feature spec writing | ❌ Not started | No formal specs written yet |
| Responsible AI / guardrails | ❌ Not started | Failure modes, hallucination handling, edge cases |
| Go-to-market thinking | ❌ Not started | Pricing, positioning, communicating AI capabilities honestly |

---

## Success Metrics

### North Star Metric — Sleep Improvement Score (1–10)

A composite score measuring whether Circadia is genuinely improving a user's sleep. Equal weighting across four components (to be rebalanced as correlation data emerges).

| Component | Weight | Data source |
|---|---|---|
| Bedtime consistency | 25% | Apple Health / wearable integration |
| Subjective sleep quality | 25% | LLM-as-judge on morning conversations |
| Routine adherence | 25% | Self-reported log + app session data |
| App usage | 25% | App session data |

**Score bands:**
- 1–3: User not engaging fully — AI should surface more personalised suggestions
- 4–6: Semi-engaged — AI has data but suggestions need refinement
- 8–10: Power user — app and AI working at full potential

**Growth target:** Users averaging 3/7 consistent sleep days at onboarding → 5/7 days within 3–6 months.

**Known assumption:** Equal weighting is an MVP default. Reweight once correlation data shows which component most predicts sleep improvement.

---

### AI Quality Metrics

Separate from user outcomes — these measure whether Circadia the AI is performing well.

| Signal | What it catches |
|---|---|
| "Improve this suggestion" button click rate | Implicit negative feedback — repeated clicks flag poor protocol selection |
| Protocol constraint violations | AI must only suggest from the 6 approved protocols — any deviation is a failure |
| Out-of-scope conversation rate | Hard stop triggered when user goes off-topic — frequency monitored as a guardrail signal |

---

### Data Collection Methods
1. **Self-reported log** — user-entered data (assumes motivated users at MVP stage; revisit for mainstream)
2. **Health platform integrations** — Apple Watch, Fitbit, Android wearables, Apple Health
3. **Partner accountability feature** — optional connection to a partner's health data for shared logging
4. **LLM-as-judge** — secondary LLM evaluates morning conversation transcripts for sleep quality signals

---

## Eval Suite
| Eval | What it measures |
|---|---|
| Plan quality | Score against CBT-I evidence base |
| Environment detection | Precision/recall on sleep-disrupting factors |
| Protocol match rate | Protocol appropriateness for stress type |
| System-level | Sleep score improvement over N nights |

---

## Learning Log

A running record of concepts practised, instincts validated, and wrong turns corrected. Kept as a portfolio artefact.

### Agentic AI Concepts

**Orchestrator + subagent pattern**
Proposed replacing the linear pipeline with an orchestrator mid-build — strong instinct. A linear pipeline hardcodes the flow; the orchestrator decides at runtime. This is what makes a system genuinely agentic rather than scripted.

**Tool use loop**
Claude doesn't call subagents directly — it emits a `tool_use` block, the backend executes the subagent, and returns a `tool_result`. Claude continues with that result in context. The loop runs until `end_turn`.

**Subagent as pure function**
Stress Triage initially had conversation logic baked in. Refactored into a pure classifier: structured input in, structured JSON out, no conversation, no routing. Keeps subagents testable, replaceable, and simple.

**Stateless API design**
Mobile app sends the full conversation history on every call; no server-side session state. Tradeoff: payload grows with conversation length, but the server stays simple and scalable. Right call for MVP.

**History as state**
The key insight for Wind-Down Delivery. The agent doesn't need to hold state between turns — the conversation history is the state. On every call it reads the history and reconstructs exactly where it is in the protocol. Foundational pattern in production agentic systems.

**Routing authority**
Subagents have no routing authority. Only the orchestrator can invoke subagents. When Wind-Down Delivery needs to reroute, it signals intent via `reroute: true` — the orchestrator reads the flag and calls Stress Triage again. Separation of concerns.

**Session completion signalling**
The `complete` flag was a placeholder until Wind-Down Delivery was built. Signal chain: Wind-Down Delivery returns `complete: true` → orchestrator sets `session_complete = True` → API response carries `complete: true` to the mobile app.

**Constrained generation**
Protocol Selection and Wind-Down Delivery are both constrained to 6 known protocols hardcoded in the system prompt. Grounding pattern — constraining outputs to known-good values improves reliability and safety.

---

### AI PM Concepts

**Three layers of AI product metrics**
Usage (is it being used?) → AI quality (is the AI doing its job?) → real-world impact (is it changing anything?). Most PMs only think about the first layer.

**Outcome vs engagement metrics**
First draft of the Sleep Improvement Score defined every band by app usage behaviour — not sleep improvement. This is the classic PM trap: measuring engagement instead of outcomes. Corrected by adding outcome-based components to the composite score.

**North star metric design**
Sleep Improvement Score: four components (bedtime consistency, subjective quality, routine adherence, usage), equal weighting, 1–10 scale, growth target of 3/7 → 5/7 days in 3–6 months. Equal weighting flagged as a known assumption to reweight once correlation data exists.

**LLM-as-judge**
Independently proposed using a secondary LLM to evaluate morning conversation transcripts for sleep quality signals. This is a production eval pattern used at Anthropic and OpenAI — arrived at without it being named.

**Implicit feedback signals**
The "improve this suggestion" button as a negative feedback signal. Repeated clicks flag poor protocol selection without requiring users to explicitly rate the experience.

**Guardrails as responsible AI**
Hard-stopping off-topic conversations and constraining outputs to a fixed protocol list were both made as product decisions — not framed as "safety." This is how responsible AI should work in practice: safety baked in, not bolted on.

**Data collection strategy**
Four data sources defined independently: self-report log, health platform integrations, partner accountability feature, LLM-as-judge. The partner feature — connecting to a partner's health data — is genuinely novel product thinking.

---

### Wrong Calls (the most useful section)

| Decision | What happened | Why it was wrong | The right call |
|---|---|---|---|
| Web lookup for protocol steps | Proposed fetching CBT-I protocol steps from a live web source at runtime | Adds latency mid-session, unreliable (URLs change), unsafe (can't control clinical accuracy), and unnecessary — protocols are stable | Hardcode evidence-based steps in the system prompt. Stable, safety-critical content is owned, not fetched |
| Blocking subagent | Assumed Wind-Down Delivery should hold open until the full protocol was complete | HTTP is request/response — a subagent cannot block waiting for user input. The connection would deadlock | Wind-Down Delivery is called once per turn. It reads the conversation history to know where it is |
| Returning full history from subagent | Wind-Down Delivery output included the full conversation history | The orchestrator already holds it — sending it back burns tokens with zero benefit | Subagent returns only what's new: `{message, complete, reroute}` |
| Subagent reroutes directly | Wind-Down Delivery would call Stress Triage directly when a reroute was needed | Subagents have no routing authority — only the orchestrator can invoke subagents | Subagent signals intent via `reroute: true`. Orchestrator handles the routing |

---

### System Prompt Craft

- Every system prompt was written by the user and reviewed by Claude — correct PM discipline
- Learned to include "JSON only — no preamble" instruction after seeing Claude wrap outputs in prose
- Learned to add code-fence stripping in the backend as a defensive measure — Claude sometimes wraps JSON in ` ```json ``` ` blocks regardless of instructions
- Tone guidance in Wind-Down Delivery (calm, human, simple language, empathy phrases, no jargon) was specific and strong — this level of precision is what separates good prompt engineering from vague instructions

---

## Progress Log
| Date | Milestone |
|---|---|
| 2026-04-26 | Project initiated. App named Circadia. Ground rules set. Architecture defined. |
| 2026-05-10 | Stress Triage subagent built, tested, and merged to main. |
| 2026-05-10 | Architecture updated: orchestrator + subagent pattern adopted. Subagents are invoked by the orchestrator as callable tools — not a linear pipeline. |
| 2026-05-10 | Orchestrator agent built. Agentic tool-use loop implemented. Stress Triage wired as first tool. |
| 2026-05-11 | Protocol Selection subagent built and wired into orchestrator. Two-subagent chain verified end-to-end. |
| 2026-05-11 | Ground rule #9 added: learning goal to become an Agentic AI PM (target: Salesforce, IBM, Cohere; dream: Anthropic, OpenAI). |
| 2026-05-17 | Success metrics defined via guided Q&A. North star: Sleep Improvement Score (1–10). AI quality metrics and data collection methods documented. |
| 2026-05-17 | Wind-Down Delivery subagent built and wired into orchestrator. Evening phase complete: Stress Triage → Protocol Selection → Wind-Down Delivery. complete and reroute flags implemented. |
