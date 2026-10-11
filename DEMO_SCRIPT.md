# AgentDoctor (AutoPatch AI) — Hackathon Demo Video Script & Submission Guide
> **Official Demo & Submission Companion for #neatHack (October 10–12, 2026)**

---

## ⏱️ Video Requirements Checklist (Strict Hackathon Rubric)
* **Maximum Duration**: **3 minutes or less** (Hard cutoff).
* **Mandatory Coverage**: Must explicitly cover **neatlogs**, **Entire**, and **cfo.ai** across 5 dimensions:
  1. **Architecture** (how it fits into the agent system)
  2. **Implementation** (code inspection)
  3. **Runtime** (live CLI/dashboard execution)
  4. **Reasoning** (how the agent interprets the feedback)
  5. **Result** (verified output and business impact)

---

## 🎬 3-Minute Timed Video Walkthrough Script

### [0:00 – 0:30] Hook & Problem Statement
* **Visual**: Show Web Dashboard at `http://localhost:5050` or CLI terminal.
* **Speaker**:
  > *"Every engineering team deploying microservices and AI agents faces the reliability crisis: subtle runtime bugs, rate limiter drifts, and silent tool failures take an average of 2.5 engineer hours to triage, costing over $230 per incident.*
  > *Meet **AgentDoctor** (AutoPatch AI): an autonomous software reliability doctor that detects failures, reproduces traces in **Neatlogs**, retrieves repository context via **Entire** checkpoints, self-heals across iterative testing, and models unit economics with **cfo.ai**."*

### [0:30 – 1:15] Sponsor 1: Neatlogs (Observability & Tracing)
* **Visual**: Show `agent.py` code where `tracker.start_llm_span` and `tracker.end_llm_span` are called, then hit **"⚡ Run Autonomous Repair"** on the dashboard. Point to the Pre-Fix vs Post-Fix comparison and the live span waterfall.
* **Speaker**:
  > *"First, **Neatlogs**. In our architecture, Neatlogs acts as the nervous system. At runtime, AgentDoctor automatically captures a baseline unpatched failure trace—here you can see the initial assertion failure on `test_burst_refill_and_continuity` with exit code 1.*
  > *Every tool call, test execution, and LLM reasoning turn is traced with latency, status, and token counts. Once repaired, AgentDoctor records the post-fix passing trace, allowing engineers to verify the before-and-after resolution in Neatlogs."*

### [1:15 – 2:00] Sponsor 2: Entire (Git Context, Checkpoints & AST Graph)
* **Visual**: Show `.entire/checkpoints/` in VS Code / terminal, and the Entire Checkpoints card on the dashboard with AST symbols.
* **Speaker**:
  > *"Second, **Entire**. Rather than sending entire repositories into LLM contexts and blowing token budgets, AgentDoctor integrates with **Entire**. Our `EntireGraph` parses Python AST locally to isolate `RateLimiter.allow_request` and its caller relationships with zero token overhead.*
  > *Furthermore, Entire's checkpoint manager records immutable snapshots in `.entire/checkpoints`: checkpoint 1 on incident ingestion, checkpoint 2 on initial patch refinement, and checkpoint 3 on verified resolution—all linked directly to Git commit lineage."*

### [2:00 – 2:30] Autonomous Self-Healing & Recovery Loop in Action
* **Visual**: Show the terminal / dashboard showing **Attempt #1 (Partial encounter)** -> **Recovery Triggered** -> **Attempt #2 (Resolved)**.
* **Speaker**:
  > *"Notice AgentDoctor's autonomous recovery loop in action. In Attempt #1, the agent generated an initial patch, but our regression suite detected a replenishment timing drift. Instead of quitting, AgentDoctor caught the error, analyzed the regression trace, and self-healed in Attempt #2 to produce the verified fix, achieving 100% green tests."*

### [2:30 – 3:00] Sponsor 3: cfo.ai (Unit Economics & Business Plan)
* **Visual**: Show `BUSINESS_PLAN.md` and the cfo.ai KPI card on the dashboard.
* **Speaker**:
  > *"Finally, **cfo.ai**. We planned AgentDoctor's business model directly using cfo.ai. With 8,800 tokens per patch on Groq Llama 3.3 70B and containerized test execution, our unit cost is just **$0.017 per patch**.*
  > *At 250 customers in our Growth tier ($1,499/mo), AgentDoctor generates **$374,750 MRR** at a **99.6% gross margin**, delivering customers a **39.6x ROI** by saving 625 engineering hours every month.*
  > *AgentDoctor: from failure to fix, verified and profitable. Thank you!"*

---

## 📢 Submission Tweet Template (For Quote Post on X)

When submissions open on Monday, Oct 12 at 7:00 PM IST, quote the official `@neatlogs` announcement post on X with:

```text
Excited to submit AgentDoctor (AutoPatch AI) for #neatHack by @neatlogs & @TheVibeFounder! 🚀

Autonomous bug triage, failure reproduction & self-healing agent platform:
🔍 Observability: @neatlogs comparative pre/post traces & span waterfall
🌿 Git Context: @entire_io AST code graphs & checkpoint lineage
💼 Economics: @cfo_ai unit economics ($0.017/patch, 99.6% margin, 39.6x ROI)

👥 Team: Team Antigravity
📦 Repo: <YOUR_PUBLIC_GITHUB_REPO_URL>
🎥 Demo Video (3m): <YOUR_YOUTUBE_OR_LOOM_LINK>
📄 Business Plan: <LINK_TO_BUSINESS_PLAN.md>

#AI #AIagents #Observability #OpenSource
```

---

## 🛠️ Step-by-Step Recording Instructions
1. Open terminal 1 and start the web dashboard:
   ```bash
   ./run.sh
   # Or: python AgentDoctor/server.py
   ```
2. Open Chrome to `http://localhost:5050`.
3. Open terminal 2 or VS Code with `.entire/` and `BUSINESS_PLAN.md` visible.
4. Record screen using Loom / OBS / QuickTime with system audio + microphone.
5. Keep within **2 minutes 45 seconds** to ensure safety margin under the 3:00 limit.
