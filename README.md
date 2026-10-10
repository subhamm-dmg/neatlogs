# AgentDoctor · Autonomous Bug Triage & Self-Healing Agent
> **#neatHack Hackathon Project** (October 10–12, 2026)

Build agents you’d trust to run without you watching.

**AgentDoctor** is an autonomous reliability agent that observes runtime exceptions, correlates stack traces with repository context, formulates targeted patches, verifies them against test suites with auto-recovery, and records full telemetry traces in **Neatlogs** alongside **Entire** checkpoints and a **cfo.ai** unit economics model.

---

## 🌟 Hackathon Integrations & Evidence

| Requirement | Implementation | Evidence in Project |
| :--- | :--- | :--- |
| **Neatlogs Tracing (25%)** | Auto-instruments every tool span, LLM reasoning call, duration, latency, and error state. | Comparative traces logged before and after self-healing. |
| **Entire Context (25%)** | Captures commit history, turn boundaries, and checkpoint metadata (`entire_graph_nodes`). | Tracked via `EntireCheckpointManager` & session lineage. |
| **cfo.ai Business Plan (25%)** | Full unit economics: $0.017 cost per patch, 99.4% gross margin, $74.9k MRR, and 39.6x customer ROI. | Realized in `cfo_model.py` and displayed on dashboard. |
| **Agent Autonomy (30%)** | Start-to-finish execution: Planning $\to$ Reproduction $\to$ Root Cause $\to$ Patch $\to$ Auto-Recovery $\to$ Verification. | `agent.py` state machine with self-healing loop. |

---

## 🚀 Quickstart

### 1. Setup Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your keys:
```env
NEATLOGS_API_KEY=<your-neatlogs-project-api-key>
NEATLOGS_PROJECT_ID=111108ac-be58-41b0-a8a4-ad44448e319e
GROQ_API_KEY=<your-groq-api-key>
```
*(If keys are not supplied, AgentDoctor runs in simulation mode so the full autonomous loop and telemetry tree can still be demonstrated.)*

### 3. Run the CLI
```bash
# Run the complete autonomous self-healing cycle
python main.py --run

# Reset the target code to its buggy baseline
python main.py --reset

# Display the cfo.ai unit economics
python main.py --economics
```

### 4. Launch the Interactive Web Dashboard
```bash
python server.py
```
Open **[http://localhost:5050](http://localhost:5050)** to explore:
- Live pre-fix vs post-fix test output comparisons
- Real-time Neatlogs span waterfall
- Entire checkpoint timeline
- cfo.ai financial ROI projections

---

## 📂 Project Architecture

```
neatlogs/
├── agent.py                 # Core autonomous triage & self-healing agent
├── cfo_model.py             # cfo.ai unit economics & runway financial model
├── server.py                # Live web dashboard backend (Flask)
├── main.py                  # CLI runner and reset utility
├── hackathon.md             # Official #neatHack build log companion
├── requirements.txt         # Project dependencies
├── templates/
│   └── index.html           # Modern interactive UI for demo video
└── sample_target_repo/
    ├── service.py           # Target token-bucket microservice with race/drift bug
    └── test_service.py      # Regression test suite
```
