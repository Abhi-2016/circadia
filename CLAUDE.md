# Circadia — Claude Instructions

## Project
Circadia is an agentic AI sleep app. Multi-agent system, mobile-first (iOS). See PLAN.md for full architecture.

## Working Agreement
- The user drives all decisions. Claude guides, explains, and asks questions — never assumes.
- Do not start coding without explaining the step and getting explicit user approval.
- All system prompts are written by the user and reviewed by Claude.
- Every feature lives on its own branch before merging to main.
- Update PLAN.md, CLAUDE.md, and README.md after every commit.
- Any proposed plan changes must be presented with a rationale and require user approval.
- The eval suite is built alongside the product — never as an afterthought.

## Architecture
See PLAN.md for the full agent map and daily loop.

## Key Decisions Made
- App name: Circadia
- Platform: Mobile first (iOS), desktop on roadmap
- Agent architecture: Orchestrator + subagent pattern. One orchestrator owns all user conversation and decides which subagents to invoke. Subagents are specialised units (Stress Triage, Protocol Selection, Wind-Down Delivery, etc.) exposed to the orchestrator as callable tools — never a hardcoded linear pipeline.
- Stateless backend: mobile sends full conversation history on every API call; no server-side session state

## Build Status
| Subagent | Status |
|---|---|
| Stress Triage | ✅ Complete |
| Protocol Selection | 🔜 Next |
| Wind-Down Delivery | 🔜 Pending |
| All others | 🔜 Pending |
| Orchestrator | 🔜 Pending (builds after evening subagents complete) |
