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
| Wind-Down Delivery | Evening | Guides user through the chosen protocol |
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
| Session completion signalling | 🔜 Next | `complete` flag — wire up when Wind-Down Delivery is built |
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
