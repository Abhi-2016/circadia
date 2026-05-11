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
