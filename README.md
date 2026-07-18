# Circadia

> Your agentic sleep coach. Built on science, powered by AI.

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Claude](https://img.shields.io/badge/Claude-Sonnet%204.6-D97706?logo=anthropic&logoColor=white)](https://anthropic.com)
[![Status](https://img.shields.io/badge/Status-Early%20Development-orange)](https://github.com/Abhi-2016/circadia)

Circadia is a mobile-first AI sleep app that uses a multi-agent system to coach, monitor, and adapt to improve your sleep — every single night.

## What it does

- **Morning:** Reflects on last night's sleep and identifies what helped or hurt
- **Daytime:** Builds a personalised sleep plan grounded in CBT-I research
- **Evening:** Assesses your stress and guides you through a tailored wind-down
- **Night:** Monitors your sleep environment and nudges you toward better rest

## How it works

Circadia is built on an **orchestrator + subagent architecture**. A single orchestrator agent owns every conversation with the user and decides — in real time — which specialised subagents to invoke and when. There is no fixed script or linear pipeline: the orchestrator adapts based on what you say.

Subagents handle specific tasks (stress classification, protocol selection, wind-down delivery, sleep analysis, and more) and report back to the orchestrator, which weaves the results into a coherent, natural conversation.

## Status
Early development. Evening phase in progress.

| Component | Status |
|---|---|
| Orchestrator | ✅ In progress |
| Stress Triage subagent | ✅ Complete |
| Protocol Selection subagent | ✅ Complete |
| Wind-Down Delivery subagent | ✅ Complete |
| Mobile app (iOS) | 🔜 Pending |

## Success Metrics

Circadia measures success at two layers:

**North star — Sleep Improvement Score (1–10)**

| Component | Weight |
|---|---|
| Bedtime consistency | 25% |
| Subjective sleep quality (LLM-as-judge) | 25% |
| Routine adherence | 25% |
| App usage | 25% |

Target: users averaging 3/7 consistent sleep nights at onboarding → 5/7 within 3–6 months.

**AI quality signals:** protocol suggestion feedback rate, constraint violation monitoring, out-of-scope guardrail triggers.

## Roadmap
- [x] Evening phase (Stress Triage → Protocol Selection → Wind-Down Delivery)
- [ ] Eval suite
- [ ] Morning + Daytime phases
- [ ] Mobile app (iOS)
- [ ] Desktop version

## Built for learning

Circadia is a portfolio project documenting a learning journey toward an **Agentic AI PM** career. Every architectural decision, subagent, and PM artefact is chosen to practise a specific concept in building, evaluating, and shipping production agentic systems.

### Agentic AI concepts

| Concept | Where practised |
|---|---|
| Orchestrator + subagent architecture | `brain/app/agents/orchestrator_agent.py` |
| Tool use loop (tool_use / tool_result) | Orchestrator agentic loop |
| Subagent as pure function | Stress Triage, Protocol Selection |
| Stateless API design | `POST /v1/session/chat` — full history on every call |
| History as state | Wind-Down Delivery reads history to know its position in the protocol |
| Session completion signalling | `complete` + `reroute` flags wired end-to-end |
| Routing authority | Only the orchestrator routes — subagents signal intent |
| Constrained generation | Protocol outputs hardcoded to 6 known protocols |
| Multi-subagent chaining | Stress Triage → Protocol Selection → Wind-Down Delivery |
| System prompt design & ownership | PM writes every prompt; Claude reviews |

### AI PM concepts

| Concept | Where practised |
|---|---|
| Success metrics | Sleep Improvement Score — north star, AI quality signals, data sources |
| Three layers of metrics | Usage → AI quality → real-world impact |
| Outcome vs engagement metrics | Corrected early draft that measured app usage instead of sleep outcomes |
| LLM-as-judge | Subjective sleep quality evaluated by a secondary LLM |
| Implicit feedback signals | "Improve this suggestion" button as a negative feedback loop |
| Guardrails as responsible AI | Scope hard-stops and output constraints built as product decisions |
| Data collection strategy | Self-report, health integrations, partner feature, LLM-as-judge |
| System design for AI products | Orchestrator pattern, stateless API, subagent contracts |

### Key wrong calls (and corrections)

| Wrong call | Correction |
|---|---|
| Fetch protocol steps from web at runtime | Hardcode stable clinical content — never fetch safety-critical data at runtime |
| Subagent blocks until protocol is complete | HTTP is request/response; agents return per turn and read history to resume |
| Return full conversation history from subagent | Return only what's new — orchestrator already holds the history |
| Subagent routes to another subagent directly | Subagents signal intent (`reroute: true`); orchestrator does the routing |
