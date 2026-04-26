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

---

## Architecture — Agentic Sleep OS

Three phases, one orchestrator:

### Agents
| Agent | Phase | Responsibility |
|---|---|---|
| Orchestrator | All | Routes tasks across agents, manages the daily loop |
| Reflection Agent | Morning | Analyzes last night's sleep data |
| Correlation Agent | Morning | Identifies environment/behaviour factors affecting sleep |
| Planning Agent | Daytime | Builds updated sleep plan |
| Research Agent | Daytime | Pulls CBT-I and evidence-based interventions |
| Coaching Agent | Daytime | Personalises the plan for the user |
| Stress Triage Agent | Evening | Assesses current stress/state via journaling prompt |
| Protocol Selection Agent | Evening | Picks the right wind-down intervention |
| Wind-Down Delivery Agent | Evening | Guides user through the chosen protocol |
| Sensor/Environment Agent | Night | Monitors sleep environment inputs |
| Action Agent | Night | Outputs nudges or smart home automations |

### Daily Loop
1. **Morning** — Reflection + Correlation agents analyse last night
2. **Daytime** — Planning + Research + Coaching agents update the sleep plan
3. **Evening** — Stress Triage → Protocol Selection → Wind-Down Delivery
4. **Night** — Environment monitoring and nudges
5. **Repeat** — Orchestrator closes the loop

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
