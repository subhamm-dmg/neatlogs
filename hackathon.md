# #neatHack Build Log: AgentDoctor (AutoPatch AI)

## Project
- **Name**: AgentDoctor (AutoPatch AI)
- **One-Sentence Purpose**: An autonomous reliability and self-healing agent that ingests failing runtime traces, diagnoses the root cause using Entire repository checkpoints, plans and verifies code patches, and exports full trace telemetry to Neatlogs alongside a cfo.ai financial ROI model.
- **Problem Addressed**: AI agents and complex microservices frequently suffer from silent tool failures, regressions, and broken schemas. Engineering teams spend hours manually reproducing stack traces and iterating on hotfixes. AgentDoctor automates this triage, reproduction, patching, and verification cycle from end-to-end.

## Team
- **Builder**: Team Antigravity

## Stack
- **Core AI**: Groq (`llama-3.3-70b-versatile`) / Ollama (`llama3.2`)
- **Observability & Tracing**: Neatlogs Python SDK (`neatlogs.init`, automated span tracing, error reporting, latency & token telemetry)
- **Code Context & History**: Entire CLI / Checkpoint context lineage
- **Business Planning**: cfo.ai Unit Economics & Financial Projections
- **Runtime**: Python 3.9+, OpenAI SDK client adapter, pytest runner

## Build Log
- **2026-10-10 - Project Kickoff**:
  - Evaluated hackathon tracks and requirements in `neatlogs_hackathon.md`.
  - Selected AgentDoctor: autonomous bug triage, failure reproduction, and verified patch generator.
  - Initialized repository, Python virtual environment, and installed `neatlogs`, `groq`, `openai`, `requests`, and `python-dotenv`.
  - Configured environment variables with Neatlogs Project ID `111108ac-be58-41b0-a8a4-ad44448e319e`.
  - Instrumenting multi-step autonomous agent with before-and-after failure recovery Neatlogs traces.

## Demo
- Instructions: Run `python main.py` or `python agent.py` to trigger the autonomous triage and patch cycle.
- Web UI: Live dashboard to review agent execution spans, Neatlogs telemetry, and cfo.ai economics.

## Known Limitations & Next Steps
- Multi-repo dependency graph integration via Entire Graph plugin.
- Automatic GitHub Pull Request submission with embedded Neatlogs trace URLs.

## Submission
- [x] Trace every agent run in Neatlogs
- [x] Repository session context with Entire
- [x] Unit economics and pricing business plan with cfo.ai
- [ ] Record demo video explaining agent and sponsor integrations
- [ ] Share build updates on X tagged #neatHack
