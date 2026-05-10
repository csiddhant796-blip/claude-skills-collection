---
name: skill-recommender
description: >
  Recommends the right skill for any task and tells you exactly how to use it.
  Use this skill whenever the user asks "what skill should I use for X", "which skill handles Y",
  "recommend a skill for Z", "is there a skill that does...", "what's the best skill to...",
  "I want to do X — which skill?", or describes a task and seems unsure which tool or approach
  to apply. Also trigger when the user is browsing skills, asking about available skills, or wants
  to understand what capabilities exist. Even trigger when the user just says things like
  "help me pick a skill", "what can I use for this?", "which one do I need?",
  or "is there something for [task]?"
---

# Skill Recommender

You help users find exactly the right skill for their task and show them how to invoke it.

## Step 1: Read the catalog first

**Before recommending anything**, read `references/skill-catalog.md`. It contains all 111 available skills organized by domain — with what each one does and when to use it.

## Step 2: Understand the task

Read the user's request carefully. If it's genuinely ambiguous (you can't tell if they want, say, security testing vs. architecture design), ask **one** focused question to clarify. If the intent is reasonably clear, go straight to recommendations — don't over-ask.

## Step 3: Match and recommend

Find 1–3 skills that best fit the task. For each recommendation, present it like this:

---

**🎯 `skill-name`**
**What it does:** One clear sentence.
**Why it fits your task:** Explain specifically how this skill addresses what they described.
**How to invoke it:** Give an exact phrase they can say or type, e.g.:
> "Use the `skill-name` skill to [accomplish their specific goal]"

---

If multiple skills could work, rank them clearly — primary recommendation first — and explain the tradeoff in one sentence (e.g., "Use X for the full workflow, Y if you only need the testing part").

If nothing in the catalog fits well, say so honestly. Don't stretch a bad match. Instead suggest the closest option and note what it doesn't cover.

## Routing logic

Use these signals to guide your matching:

| Task type | Lean toward |
|-----------|-------------|
| Vague idea, need to think it through first | `brainstorming` |
| Writing a plan before coding | `writing-plans` |
| Debugging a bug or test failure | `systematic-debugging` |
| Building a new feature end-to-end | `spec-driven-workflow` → `writing-plans` → senior role skill |
| Need to work in parallel / split tasks | `dispatching-parallel-agents` |
| Backend API, auth, DB work | `senior-backend` |
| Frontend / React / Next.js | `senior-frontend` |
| Full project scaffold | `senior-fullstack` |
| Cloud infra on AWS | `aws-solution-architect` |
| Cloud infra on Azure | `azure-cloud-architect` |
| Cloud infra on GCP | `gcp-cloud-architect` |
| Security audit / pen test | `senior-secops` or `security-pen-testing` |
| ML models / MLOps | `senior-ml-engineer` |
| Data pipelines / ETL | `senior-data-engineer` |
| Statistics / A/B tests | `statistical-analyst` |
| Writing tests / TDD | `tdd-guide` or `test-driven-development` |
| Code review | `code-reviewer` or `pr-review-expert` |
| Docker / containers | `docker-development` |
| Kubernetes / Helm | `kubernetes-operator` or `helm-chart-builder` |
| CI/CD pipelines | `ci-cd-pipeline-builder` or `senior-devops` |
| Observability / SLOs | `observability-designer` or `slo-architect` |
| Incident / outage | `incident-commander` |
| Multi-agent competition | `agenthub` |
| Optimize code by a metric automatically | `autoresearch-agent` |
| Creating a new skill | `writing-skills` |
| Ready to deploy / go live | `ship-gate` |
| Responses feel robotic | `behuman` |

## Tone

Be direct and concrete. Users want to know *exactly what to do* — give them an actionable answer, not a list of caveats. The best response is one where they can immediately copy the "How to invoke" phrase and get started.
