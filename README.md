# Circadia

> Your agentic sleep coach. Built on science, powered by AI.

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
Early development. Evening phase subagents in progress.

| Component | Status |
|---|---|
| Stress Triage subagent | ✅ Complete |
| Protocol Selection subagent | 🔜 In progress |
| Wind-Down Delivery subagent | 🔜 Pending |
| Orchestrator | 🔜 Pending |
| Mobile app (iOS) | 🔜 Pending |

## Roadmap
- [ ] Evening phase (Stress Triage → Protocol Selection → Wind-Down Delivery)
- [ ] Orchestrator
- [ ] Morning + Daytime phases
- [ ] Mobile app (iOS)
- [ ] Eval suite
- [ ] Desktop version
