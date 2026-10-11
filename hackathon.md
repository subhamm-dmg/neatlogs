# #neatHack Build Log: AgentDoctor (AutoPatch AI)

## Project
- **Name**: AgentDoctor (AutoPatch AI)
- **One-Sentence Purpose**: An autonomous reliability and self-healing agent that ingests failing runtime traces, diagnoses root causes using Entire AST repository checkpoints, plans and verifies code patches across an autonomous recovery loop, and exports full trace telemetry to Neatlogs alongside a cfo.ai financial ROI model.
- **Problem Addressed**: AI agents and complex microservices frequently suffer from silent tool failures, regressions, and broken schemas. Engineering teams spend hours manually reproducing stack traces and iterating on hotfixes. AgentDoctor automates this triage, reproduction, patching, and verification cycle from end-to-end.

## Team
- **Builder**: Team Antigravity

## Stack
- **Core AI**: Groq (`llama-3.3-70b-versatile`) / Ollama (`llama3.2`) / Deterministic Heuristic Engine
- **Observability & Tracing**: Neatlogs Python SDK (`neatlogs.init`, automated span tracing, error reporting, latency & token telemetry)
- **Code Context & History**: Entire Checkpoint Lineage (`.entire/checkpoints`) & Entire AST Graph (`entire_manager.py`)
- **Business Planning**: cfo.ai Unit Economics & Multi-Scenario Projections (`BUSINESS_PLAN.md`)
- **Runtime**: Python 3.9+, Flask Web Dashboard, pytest/subprocess runner

## Build Log
- **2026-10-10 - Project Kickoff**:
  - Evaluated hackathon tracks and requirements in `neatlogs_hackathon.md`.
  - Selected AgentDoctor: autonomous bug triage, failure reproduction, and verified patch generator.
  - Initialized repository, Python virtual environment, and installed `neatlogs`, `groq`, `openai`, `requests`, and `python-dotenv`.
  - Configured environment variables with Neatlogs Project ID `111108ac-be58-41b0-a8a4-ad44448e319e`.
  - Instrumenting multi-step autonomous agent with before-and-after failure recovery Neatlogs traces.

- **2026-10-11 - Architecture Hardening, Self-Healing & Sponsor Alignment**:
  - **Neatlogs SDK Fix**: Corrected span closure protocol to utilize `tracker.end_llm_span(span, ...)` ensuring 100% of telemetry spans serialize and ship to the Neatlogs ingestion endpoint.
  - **Entire Checkpoints & Graph**: Built `entire_manager.py` with native AST parsing (`EntireGraph`) to map symbol and caller dependencies with zero LLM token overhead, alongside persistent `.entire/checkpoints/` and Git commit lineage.
  - **Autonomous Self-Healing Loop**: Designed two-stage patch verification where Attempt #1 experiences regression on continuous burst replenishment, triggering the self-healing recovery loop in Attempt #2 to reach 100% verified green tests.
  - **cfo.ai Multi-Scenario Model**: Implemented Base vs. Growth comparative financial projections, demonstrating a $0.017 unit cost per patch, 99.6% gross margin, and 39.6x customer ROI. Auto-generated formal `BUSINESS_PLAN.md`.
  - **Zero-Friction Portability**: Added automated `setup.sh` and `run.sh` scripts, eliminating environment hurdles.
  - **Submission Assets**: Authored `DEMO_SCRIPT.md` with a strict 3-minute timed script covering all 5 hackathon rubric requirements and an X quote post template.

## Demo
- Instructions: Run `./run.sh` or `python AgentDoctor/main.py` for CLI autonomous triage and repair.
- Web UI: Run `python AgentDoctor/server.py` to open the interactive dashboard at `http://localhost:5050`.

## Submission Checklist
- [x] Trace every agent run in Neatlogs (Pre-Fix vs Post-Fix)
- [x] Repository session context with Entire (`.entire/` checkpoints & AST graph)
- [x] Unit economics and pricing business plan with cfo.ai (`BUSINESS_PLAN.md`)
- [x] Fully functioning self-healing recovery loop across regression tests
- [x] Automated setup scripts (`setup.sh`, `run.sh`)
- [x] Demo video script & X quote post template (`DEMO_SCRIPT.md`)
- [ ] Record demo video (≤ 3 minutes)
- [ ] Submit on X during the official window (Oct 12, 7:00–11:55 PM IST)
