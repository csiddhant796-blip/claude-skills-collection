# Claude Skills Collection

A curated collection of 111+ Claude agent skills organized for use with [Claude Code](https://claude.ai/code) and Cowork. These skills extend Claude's capabilities across engineering, DevOps, security, ML, databases, productivity, and more.

**Maintainer:** [csiddhant796-blip](https://github.com/csiddhant796-blip) · csiddhant796@gmail.com

---

## What are Claude Skills?

Skills are Markdown-based prompt packages (`.skill` files or folders with a `SKILL.md`) that give Claude specialized knowledge and workflows for specific domains. Install them once, invoke them naturally in conversation.

---

## Skill Categories

| # | Category | Count | Skills |
|---|----------|-------|--------|
| 1 | Multi-Agent & Parallel Work | 10 | `agenthub`, `agent-designer`, `agent-workflow-designer`, `init`, `spawn`, `eval`, `merge`, `board`, `dispatching-parallel-agents`, `subagent-driven-development` |
| 2 | Workflow & Planning | 8 | `brainstorming`, `writing-plans`, `executing-plans`, `spec-driven-workflow`, `using-superpowers`, `using-git-worktrees`, `git-worktree-manager`, `writing-skills` |
| 3 | Architecture & System Design | 5 | `senior-architect`, `migration-architect`, `tech-stack-evaluator`, `engineering-skills`, `engineering-advanced-skills` |
| 4 | Backend Development | 3 | `senior-backend`, `stripe-integration-expert`, `email-template-builder` |
| 5 | Frontend Development | 2 | `senior-frontend`, `epic-design` |
| 6 | Fullstack & Scaffolding | 1 | `senior-fullstack` |
| 7 | Cloud & Infrastructure | 5 | `aws-solution-architect`, `azure-cloud-architect`, `gcp-cloud-architect`, `terraform-patterns`, `ms365-tenant-manager` |
| 8 | DevOps & CI/CD | 4 | `senior-devops`, `ci-cd-pipeline-builder`, `release-manager`, `changelog-generator` |
| 9 | Containers & Kubernetes | 3 | `docker-development`, `kubernetes-operator`, `helm-chart-builder` |
| 10 | Security | 9 | `senior-security`, `senior-secops`, `ai-security`, `cloud-security`, `security-pen-testing`, `red-team`, `threat-detection`, `ship-gate`, `skill-security-auditor`, `env-secrets-manager`, `secrets-vault-manager` |
| 11 | Testing & Quality | 12 | `tdd-guide`, `test-driven-development`, `senior-qa`, `api-test-suite-builder`, `code-reviewer`, `pr-review-expert`, `adversarial-reviewer`, `karpathy-coder`, `focused-fix`, `verification-before-completion`, `requesting-code-review`, `receiving-code-review`, `finishing-a-development-branch`, `self-eval` |
| 12 | Data Engineering | 4 | `senior-data-engineer`, `data-quality-auditor`, `statistical-analyst`, `senior-data-scientist` |
| 13 | ML & AI Engineering | 7 | `senior-ml-engineer`, `senior-computer-vision`, `autoresearch-agent`, `setup`, `run`, `loop`, `resume`, `status` |
| 14 | LLM & Prompt Engineering | 6 | `senior-prompt-engineer`, `llm-cost-optimizer`, `rag-architect`, `prompt-governance`, `llm-wiki`, `mcp-server-builder` |
| 15 | Observability & Reliability | 5 | `observability-designer`, `slo-architect`, `chaos-engineering`, `performance-profiler`, `runbook-generator` |
| 16 | Databases | 3 | `database-designer`, `database-schema-designer`, `sql-database-assistant` |
| 17 | Incident Response | 3 | `incident-commander`, `incident-response`, `systematic-debugging` |
| 18 | Productivity & Tooling | 10 | `tc-tracker`, `tech-debt-tracker`, `feature-flags-architect`, `dependency-auditor`, `monorepo-navigator`, `codebase-onboarding`, `code-tour`, `interview-system-designer`, `skill-tester`, `skill-recommender` |
| 19 | Automation & Browser | 3 | `browser-automation`, `full-page-screenshot`, `demo-video` |
| 20 | Communication | 2 | `behuman`, `command-guide` |

---

## Installation

Double-click any `.skill` file to install, or copy the folder into your Claude skills directory.

To use a skill, invoke it naturally:
> *"Use the `database-schema-designer` skill to design a schema for my SaaS app"*

Or just describe your task — the `skill-recommender` skill (included) will suggest the right one.

---

## Source Attribution & Credits

This collection was assembled from multiple open-source skill repositories. Below is a mapping of which skills came from which upstream source, along with the original contributor credits.

> ⚠️ **Note:** Not all original skill repos were fully downloaded locally. The source mapping below is based on available download metadata, folder origins (`skilbro` / `skilbro2` / `skilbro3`), skill naming conventions, and the contributor credits table. Some attributions are best-effort assessments.

### Source Folders

| Folder | Source Repo | Skills Tagged |
|--------|-------------|---------------|
| `skilbro` (engineering) | Various (see table below) | `[E]` — 65 skills |
| `skilbro2` (engineering-team) | Various (see table below) | `[T]` — 32 skills |
| `skilbro3` (superpowers-main) | [obra/superpowers](https://github.com/obra/superpowers) | `[W]` — 14 skills |

### Skills from `obra/superpowers` [W]

All 14 workflow skills originate from [obra/superpowers](https://github.com/obra/superpowers), a 5-phase workflow system (Clarify → Design → Plan → Code → Verify) for complex architecture and development tasks:

`dispatching-parallel-agents` · `subagent-driven-development` · `brainstorming` · `writing-plans` · `executing-plans` · `using-superpowers` · `using-git-worktrees` · `writing-skills` · `test-driven-development` · `verification-before-completion` · `requesting-code-review` · `receiving-code-review` · `finishing-a-development-branch` · `systematic-debugging`

### Skills by Upstream Contributor

| Category | Skill Name(s) | Source Repo | Notes |
|----------|--------------|-------------|-------|
| Data Science / Spreadsheets | `xlsx` | [anthropics/xlsx](https://github.com/anthropics/xlsx) | Automates data cleaning, formula generation, EDA within spreadsheets |
| Skill Meta / Creation | `skill-creator`, `skill-recommender`, `skill-tester`, `skill-security-auditor` | [anthropics/skill-creator](https://github.com/anthropics/skill-creator) | Standardizes creation of other skills, best practices in prompt engineering |
| MCP / Cloud Integration | `mcp-builder`, `mcp-server-builder` | [anthropics/mcp-builder](https://github.com/anthropics/mcp-builder) | Automates creation of MCP servers to integrate APIs and cloud services |
| Documents & Reporting | `docx`, `pdf`, `pptx`, `internal-comms` | [anthropics/skills/docx](https://github.com/anthropics/skills) · [anthropics/internal-comms](https://github.com/anthropics/internal-comms) | Document formatting, citations, business reporting, status updates, FAQ generation |
| Web / API Testing | `api-test-suite-builder`, `browser-automation` | [anthropics/webapp-testing](https://github.com/anthropics/webapp-testing) · [mendableai/firecrawl](https://github.com/mendableai/firecrawl) | Playwright-based web app testing; Firecrawl for web scraping and structured data extraction |
| Cybersecurity / Pen Testing | `security-pen-testing`, `red-team`, `threat-detection`, `senior-security`, `senior-secops` | [trailofbits/security-skills](https://github.com/trailofbits/security-skills) | Developed by Trail of Bits for vulnerability scanning, automated threat modeling, pen testing |
| ML / MLOps | `senior-ml-engineer`, `senior-data-scientist`, `senior-computer-vision` | [ComposioHQ/skills](https://github.com/ComposioHQ/skills) | Connects Claude to ML pipelines for model evaluation and structured experimentation |
| SQL / Databases | `sql-database-assistant`, `database-designer`, `database-schema-designer` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Generates optimized queries, maps database schemas for data engineers |
| DevOps / Git / CI-CD | `ci-cd-pipeline-builder`, `changelog-generator`, `git-worktree-manager`, `release-manager` | [kbdhunga/claude-skills](https://github.com/kbdhunga/claude-skills) | Automates Git repo management, CI/CD setup, semantic versioning |
| Autonomous Agents / Research | `autoresearch-agent`, `setup`, `run`, `loop`, `resume`, `status` | [sickn33/antigravity](https://github.com/sickn33/antigravity) | Specialized for autonomous planning logic, experiment loops, and agent-driven iteration |
| Financial Analysis | `statistical-analyst`, `senior-data-engineer` | [anthropic-cookbooks](https://github.com/anthropics/anthropic-cookbook) | Includes ratio calculators and full suites for specialized financial analysis |

### Skills with Unclear / Blended Origin

The following skills appeared in `skilbro` or `skilbro2` but could not be definitively traced to a single upstream repo. They are likely original Anthropic team skills or composites from multiple sources:

`senior-architect` · `senior-backend` · `senior-frontend` · `senior-fullstack` · `senior-devops` · `senior-prompt-engineer` · `senior-qa` · `senior-secops` · `aws-solution-architect` · `azure-cloud-architect` · `gcp-cloud-architect` · `ms365-tenant-manager` · `kubernetes-operator` · `helm-chart-builder` · `docker-development` · `chaos-engineering` · `observability-designer` · `slo-architect` · `rag-architect` · `llm-cost-optimizer` · `llm-wiki` · `performance-profiler` · `incident-commander` · `incident-response` · `codebase-onboarding` · `code-tour` · `code-reviewer` · `adversarial-reviewer` · `tdd-guide` · `senior-qa` · `epic-design` · `stripe-integration-expert` · `email-template-builder` · `ai-security` · `cloud-security` · `behuman` · `karpathy-coder` · `monorepo-navigator` · `tech-debt-tracker` · `tc-tracker` · `feature-flags-architect` · `dependency-auditor` · `demo-video` · `full-page-screenshot`

---

## Highlighted Skills

### `skill-recommender` ⭐ (built in this repo)
Takes any task description and recommends which skill to use plus exactly how to invoke it. Uses the full catalog as a reference.

> *"What skill should I use to debug my slow React app?"*
> → Recommends `performance-profiler` with exact invocation phrase

### `agenthub`
Spawns N parallel Claude agents competing on the same task. Best branch wins and merges. Requires a git repo.

### `autoresearch-agent`
Autonomous improvement loop — edits, evaluates, commits improvements, discards failures, repeats.

### `systematic-debugging`
Structured debugging before proposing fixes. Forces hypothesis-driven analysis.

---

## Contributing

Pull requests welcome. To add a new skill:
1. Create a folder with a `SKILL.md` (YAML frontmatter: `name`, `description`)
2. Add references or scripts if needed
3. Submit a PR with the skill's category and source attribution

---

## License

Individual skills may carry licenses from their upstream repositories. Where not specified, skills are shared under MIT. See individual skill folders for details.

---

*Assembled by [csiddhant796-blip](https://github.com/csiddhant796-blip) using Claude Cowork mode.*
