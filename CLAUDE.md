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
| Success metrics | Table-stakes PM skill — shapes every build decision |
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
| Protocol Selection | ✅ Complete |
| Wind-Down Delivery | 🔜 Next |
| All others | 🔜 Pending |
| Orchestrator | ✅ In progress (stress triage + protocol selection wired) |
