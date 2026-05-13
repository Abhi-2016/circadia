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
| Success metrics | ❌ Not started | What does "Circadia is working" look like? |
| Safety & responsible AI | ❌ Not started | Crisis handling, harmful advice guardrails, medical disclaimers |
| Cost & latency tradeoffs | ❌ Not started | Cost per session, model downgrade decisions, latency budgets |
| Feedback loops | ❌ Not started | How does the product improve from user signal over time? |
| User research & personas | ❌ Not started | Who is the user? What is their job-to-be-done? |
| PRD / feature spec writing | ❌ Not started | No formal specs written yet |
| Responsible AI / guardrails | ❌ Not started | Failure modes, hallucination handling, edge cases |
| Go-to-market thinking | ❌ Not started | Pricing, positioning, communicating AI capabilities honestly |

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
