# Claude Skills Collection

A curated collection of 117+ Claude agent skills organized for use with [Claude Code](https://claude.ai/code) and Cowork. These skills extend Claude's capabilities across engineering, DevOps, security, ML, databases, productivity, Indian financial planning, and more.

**Maintainer:** [csiddhant796-blip](https://github.com/csiddhant796-blip) · csiddhant796@gmail.com

---

## What are Claude Skills?

Skills are Markdown-based prompt packages (`.skill` files or folders with a `SKILL.md`) that give Claude specialized knowledge and workflows for specific domains. Install them once, invoke them naturally in conversation.

```
skill-name/
├── SKILL.md          ← required: YAML frontmatter + instructions
└── references/       ← optional: docs, templates, schemas
└── scripts/          ← optional: executable helpers
└── assets/           ← optional: fonts, icons, templates
```

---

## Quick Start

**Install:** Double-click any `.skill` file, or copy the skill folder into your Claude skills directory.

**Invoke naturally:**
> *"Use the `database-schema-designer` skill to design a schema for my SaaS app"*

Or just describe your task — the `skill-recommender` skill (included) will suggest the right one.

---

## Full Skill Catalog

### 1. Multi-Agent & Parallel Work (10 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `agenthub` | Spawns N parallel Claude agents competing on the same task; best branch wins and merges | You want multiple approaches tried simultaneously on a hard problem |
| `agent-designer` | Designs multi-agent system architectures with roles, communication flows, and orchestration | Planning an agentic system with specialized sub-agents |
| `agent-workflow-designer` | Creates detailed workflow specs for multi-step agent pipelines | Mapping out a complex automated workflow before building it |
| `init` | Initializes a new multi-agent workspace with shared context and task queues | Starting a fresh parallel-agent project |
| `spawn` | Spawns a new sub-agent with a specific role and instructions | Delegating a subtask to a specialized agent mid-workflow |
| `eval` | Evaluates agent outputs and selects the best result across parallel runs | Grading competing agent outputs objectively |
| `merge` | Merges outputs from parallel agents into a coherent final result | Combining results from multiple agents working in parallel |
| `board` | Displays a live board of running agents, their status, and outputs | Monitoring a parallel multi-agent run |
| `dispatching-parallel-agents` | Pattern for dispatching independent subtasks to parallel Claude agents | Breaking a large task into parallelizable chunks |
| `subagent-driven-development` | Full workflow for developing software using coordinated sub-agents | Complex software projects where different agents own different concerns |

### 2. Workflow & Planning (8 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `brainstorming` | Structured brainstorming workflow — diverge, converge, prioritize | Exploring a problem space before committing to a direction |
| `writing-plans` | Writes detailed step-by-step implementation plans from a goal | You have a goal and need a concrete plan before coding |
| `executing-plans` | Executes a written plan step by step, tracking progress | Following through on a previously written plan |
| `spec-driven-workflow` | Drives development from a spec: clarify → design → plan → code → verify | Building features with strict spec adherence |
| `using-superpowers` | Meta-skill: teaches Claude to use the full superpowers workflow effectively | Onboarding to the obra/superpowers system |
| `using-git-worktrees` | Pattern for using git worktrees to parallelize development branches | Working on multiple features simultaneously without conflicts |
| `git-worktree-manager` | Manages git worktrees: create, switch, delete, merge | Hands-on worktree management in a project |
| `writing-skills` | Teaches how to write good Claude skills — format, structure, best practices | Creating new skills or improving existing ones |

### 3. Architecture & System Design (5 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `senior-architect` | Senior software architect persona — ADRs, trade-off analysis, system design | Designing systems, reviewing architecture, making tech decisions |
| `migration-architect` | Plans and executes large-scale system migrations (DB, cloud, framework) | Migrating from a legacy system or platform |
| `tech-stack-evaluator` | Evaluates and compares technology stacks for a given use case | Choosing between frameworks, databases, or cloud providers |
| `engineering-skills` | Core engineering skill set: code quality, patterns, code review | General software engineering tasks |
| `engineering-advanced-skills` | Advanced engineering: distributed systems, performance, scalability | Tackling hard engineering problems at scale |

### 4. Backend Development (3 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `senior-backend` | Senior backend engineer persona — APIs, services, data modeling | Building or reviewing backend systems |
| `stripe-integration-expert` | Implements Stripe payments: subscriptions, webhooks, checkout | Adding payment processing to an application |
| `email-template-builder` | Builds responsive HTML email templates with inline CSS | Creating email campaigns or transactional email templates |

### 5. Frontend Development (2 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `senior-frontend` | Senior frontend engineer persona — React, TypeScript, performance, accessibility | Building or reviewing frontend applications |
| `epic-design` | Creates polished, production-quality UI designs and components | When you want genuinely beautiful, thoughtful UI |

### 6. Fullstack & Scaffolding (1 skill)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `senior-fullstack` | Full-stack engineer persona — end-to-end feature development across stack | Building complete features that span frontend and backend |

### 7. Cloud & Infrastructure (5 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `aws-solution-architect` | AWS architecture — EC2, S3, Lambda, RDS, VPC, IAM, cost optimization | Designing or reviewing AWS infrastructure |
| `azure-cloud-architect` | Azure architecture — App Service, AKS, Cosmos DB, AD, networking | Designing or reviewing Azure infrastructure |
| `gcp-cloud-architect` | GCP architecture — GKE, BigQuery, Cloud Run, Pub/Sub, IAM | Designing or reviewing Google Cloud infrastructure |
| `terraform-patterns` | Terraform best practices — modules, state management, workspaces | Writing or reviewing infrastructure as code |
| `ms365-tenant-manager` | Microsoft 365 tenant configuration — users, groups, policies, licensing | Managing an M365 tenant or Azure AD |

### 8. DevOps & CI/CD (4 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `senior-devops` | Senior DevOps engineer persona — CI/CD, IaC, monitoring, incident response | DevOps tasks, pipeline design, platform engineering |
| `ci-cd-pipeline-builder` | Builds GitHub Actions, GitLab CI, or Jenkins pipelines from scratch | Setting up automated build/test/deploy pipelines |
| `release-manager` | Manages releases — changelogs, versioning, tagging, release notes | Cutting a release or setting up a release process |
| `changelog-generator` | Generates changelogs from git history using conventional commits | Automating release documentation |

### 9. Containers & Kubernetes (3 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `docker-development` | Docker best practices — multi-stage builds, compose, optimization | Writing Dockerfiles or Docker Compose configurations |
| `kubernetes-operator` | Kubernetes expertise — deployments, services, ingress, RBAC, operators | Managing or debugging Kubernetes workloads |
| `helm-chart-builder` | Builds Helm charts for Kubernetes applications | Packaging a Kubernetes application for distribution |

### 10. Security (11 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `senior-security` | Senior security engineer persona — threat modeling, secure design, code review | Security architecture and secure development practices |
| `senior-secops` | Security operations persona — SIEM, incident detection, response playbooks | Security monitoring and incident response operations |
| `ai-security` | AI/ML-specific security — prompt injection, model theft, data poisoning | Securing AI systems and LLM applications |
| `cloud-security` | Cloud security posture — IAM hardening, network security, compliance | Auditing or improving cloud security configuration |
| `security-pen-testing` | Penetration testing methodology and tooling guidance | Authorized pen testing and vulnerability assessment |
| `red-team` | Red team operations — adversarial simulation, attack path analysis | Red team exercises and adversarial testing |
| `threat-detection` | Threat detection rules, SIEM queries, anomaly detection patterns | Building or tuning detection capabilities |
| `ship-gate` | Security gate before shipping — checks for secrets, vulnerabilities, bad patterns | Final security check before deploying code |
| `skill-security-auditor` | Audits Claude skills for security issues and malicious content | Reviewing skills before installing them |
| `env-secrets-manager` | Manages environment variables and secrets safely | Handling credentials, API keys, and environment config |
| `secrets-vault-manager` | Integrates with secrets vaults (Vault, AWS Secrets Manager, etc.) | Setting up proper secrets management infrastructure |

### 11. Testing & Quality (14 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `tdd-guide` | Test-driven development guidance — red/green/refactor cycle | Learning or applying TDD methodology |
| `test-driven-development` | Full TDD workflow: write tests first, then implementation | Practicing strict TDD on a feature |
| `senior-qa` | QA engineer persona — test plans, test cases, quality metrics | Comprehensive QA planning and execution |
| `api-test-suite-builder` | Builds API test suites with Playwright, Supertest, or Postman | Creating automated API tests |
| `code-reviewer` | Thorough code review — correctness, security, performance, style | Reviewing a PR or code change |
| `pr-review-expert` | PR review specialist with structured feedback format | Reviewing pull requests systematically |
| `adversarial-reviewer` | Adversarial code review — deliberately finds problems and edge cases | Getting a tough second opinion on code |
| `karpathy-coder` | Andrej Karpathy-inspired coding style — careful, minimal, correct | Writing clean, careful, well-reasoned code |
| `focused-fix` | Fixes one specific bug or issue without changing anything else | Surgical bug fixes |
| `verification-before-completion` | Verifies work is complete and correct before declaring done | Final check before marking a task complete |
| `requesting-code-review` | Prepares a PR for review — summary, context, what to focus on | Requesting a code review from a teammate |
| `receiving-code-review` | Processes code review feedback constructively | Responding to and implementing review feedback |
| `finishing-a-development-branch` | Wraps up a branch — cleanup, tests, docs, PR prep | Finishing a feature branch before merging |
| `self-eval` | Self-evaluation of outputs against requirements | Checking your own work before submitting |

### 12. Data Engineering (4 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `senior-data-engineer` | Senior data engineer persona — pipelines, ETL, data modeling, warehousing | Data pipeline design and implementation |
| `data-quality-auditor` | Audits datasets for completeness, accuracy, consistency, validity | Profiling a dataset for quality issues |
| `statistical-analyst` | Statistical analysis — distributions, hypothesis testing, regression | Running statistical analyses and interpreting results |
| `senior-data-scientist` | Data science persona — ML experimentation, feature engineering, model evaluation | Data science projects end to end |

### 13. ML & AI Engineering (8 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `senior-ml-engineer` | ML engineering persona — model training, deployment, MLOps | Building production ML systems |
| `senior-computer-vision` | Computer vision expertise — CNN architectures, object detection, segmentation | Computer vision model development |
| `autoresearch-agent` | Autonomous improvement loop — edits, evaluates, commits, repeats | Self-improving code or model experiments |
| `setup` | Sets up an autonomous research run environment | Initializing an autoresearch-agent run |
| `run` | Executes one iteration of an autonomous research loop | Running a single research iteration |
| `loop` | Runs the full autonomous research loop until convergence | Fully automated iterative improvement |
| `resume` | Resumes a paused autonomous research run | Continuing an interrupted autoresearch run |
| `status` | Reports the status of a running autonomous research loop | Checking progress of an ongoing run |

### 14. LLM & Prompt Engineering (6 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `senior-prompt-engineer` | Expert prompt engineering — system prompts, few-shot, chain-of-thought | Writing or improving prompts for any LLM |
| `llm-cost-optimizer` | Optimizes LLM usage costs — prompt compression, model selection, caching | Reducing API costs for LLM-powered applications |
| `rag-architect` | RAG system design — chunking, embedding, retrieval, reranking | Building retrieval-augmented generation systems |
| `prompt-governance` | Prompt versioning, testing, and governance workflows | Managing prompts in production at scale |
| `llm-wiki` | Reference knowledge base for LLM concepts, models, and capabilities | Quick lookups on LLM internals and best practices |
| `mcp-server-builder` | Builds MCP (Model Context Protocol) servers to connect Claude to external APIs | Creating custom Claude tools and integrations |

### 15. Observability & Reliability (5 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `observability-designer` | Designs observability stacks — metrics, logs, traces, dashboards | Setting up monitoring for a service or system |
| `slo-architect` | Defines SLOs, SLIs, error budgets, and alerting policies | Establishing reliability targets and on-call policies |
| `chaos-engineering` | Chaos engineering experiments — failure injection, resilience testing | Testing system resilience through controlled failures |
| `performance-profiler` | Performance analysis — profiling, bottleneck identification, optimization | Diagnosing and fixing performance problems |
| `runbook-generator` | Generates operational runbooks for recurring procedures | Creating on-call documentation |

### 16. Databases (3 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `database-designer` | Database design — normalization, indexing, query optimization | Designing a new database schema |
| `database-schema-designer` | Generates detailed schema DDL with constraints, indexes, relationships | Writing the actual SQL for a schema |
| `sql-database-assistant` | SQL query writing, optimization, and debugging | Writing complex queries or fixing slow SQL |

### 17. Incident Response (3 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `incident-commander` | Incident command — triage, coordination, communication, postmortem | Running a production incident end to end |
| `incident-response` | Incident response playbooks and step-by-step procedures | Following a structured response to an incident |
| `systematic-debugging` | Hypothesis-driven debugging before proposing fixes | Diagnosing a hard bug methodically |

### 18. Productivity & Tooling (10 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `tc-tracker` | Tracks technical changes across sessions — init, update, resume, close | Handoffs between AI sessions on long-running code changes |
| `tech-debt-tracker` | Scans codebases for technical debt, scores severity, generates remediation plans | Technical debt audits and cleanup sprints |
| `feature-flags-architect` | Designs feature flag systems — rollouts, targeting, flag lifecycle | Building or improving feature flag infrastructure |
| `dependency-auditor` | Audits project dependencies for outdated, vulnerable, or unused packages | Keeping dependencies healthy and secure |
| `monorepo-navigator` | Navigates and works effectively within monorepo structures | Working in large monorepos with multiple packages |
| `codebase-onboarding` | Generates a guided onboarding tour of an unfamiliar codebase | Getting up to speed on a new codebase quickly |
| `code-tour` | Creates interactive code tours highlighting key areas | Sharing knowledge about a codebase with teammates |
| `interview-system-designer` | Designs technical interview questions and evaluation rubrics | Preparing or running technical interviews |
| `skill-tester` | Tests Claude skills by running them against sample prompts | Verifying a skill works before deploying it |
| `skill-recommender` | Given any task, recommends the right skill and exact invocation phrase | When you're not sure which skill to use |

### 19. Automation & Browser (3 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `browser-automation` | Playwright-based browser automation — navigation, form filling, scraping | Automating web interactions or scraping web data |
| `full-page-screenshot` | Takes full-page screenshots of websites | Capturing web pages for documentation or review |
| `demo-video` | Creates demo video scripts and guides for recording | Preparing a product demo or tutorial recording |

### 20. Communication (2 skills)

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `behuman` | Rewrites AI-sounding text to sound genuinely human | Polishing AI-generated copy to be less robotic |
| `command-guide` | Generates clear CLI command reference guides | Documenting command-line tools |

### 21. Indian Financial Planning (6 skills) `[F]`

Skills purpose-built for Indian tax law, investment instruments, and the regulatory framework governing NRI/LRS transactions. All calculations are current for FY2025-26.

| Skill | What It Does | Use When |
|-------|-------------|----------|
| `indian-tax-regime-optimizer` | Compares old vs. new tax regime side-by-side for FY2025-26; calculates breakeven deduction threshold; recommends the better regime with exact tax savings | Deciding which regime to file under, or advising a family member |
| `indian-real-estate-bhopal` | Handles MP stamp duty (10.5%), Circle Rate lookups, Section 54/54B/54EC/54F capital gains exemptions, TDS 194-IA (1% buyer deduction), and sale-vs-hold NPV analysis | Buying, selling, or inheriting agricultural/residential property in Madhya Pradesh |
| `indian-mutual-fund-tax` | Calculates STCG/LTCG across equity, debt, and hybrid funds post-Finance Act 2023; flags the Section 50AA "debt-trap" on market-linked debentures; models SWP tax efficiency | Tax planning for a mutual fund portfolio, especially debt or hybrid funds |
| `senior-citizen-savings-scheme` | Models SCSS at 8.20% (Q1 FY2026-27) with quarterly payouts, TDS 194A thresholds, Form 15H filing, 80C deduction, and premature closure penalties; compares against FD and RBI bonds | Senior citizens or their children planning safe, government-backed income |
| `family-portfolio-aggregator` | Aggregates 7 asset classes (equity MF, debt MF, PPF, SCSS, real estate, gold, NPS) across multiple family members; checks age-based allocation targets; detects drift and suggests rebalancing | Reviewing or rebalancing a multi-member family investment portfolio |
| `lrs-foreign-investment-tax` | Handles TCS 206C(1G) at 20% on LRS remittances above ₹7L, DTAA offset guidance for 8 countries, FEMA compliance, Form 67 for claiming foreign tax credits, and Section 112 LTCG 12.5% on foreign assets | Indian residents investing abroad, NRIs, or anyone remitting funds overseas |

---

## Installation

**Option A — Skill file:**
Double-click any `.skill` file to install it directly into Claude Code or Cowork.

**Option B — Manual:**
Copy the skill folder into your Claude skills directory:
- **Mac/Linux:** `~/.claude/skills/`
- **Windows:** `%APPDATA%\Claude\skills\`

Then invoke naturally:
> *"Use the `senior-architect` skill to review my system design"*

Or just describe your task — the `skill-recommender` will suggest the right skill and tell you exactly how to invoke it.

---

## Source Attribution & Credits

This collection was assembled from multiple open-source skill repositories. Below is the full source mapping with upstream credits.

> ⚠️ **Attribution note:** Not all original skill repos were fully downloaded locally during assembly. The mappings below are based on available download metadata, folder origins (`skilbro` / `skilbro2` / `skilbro3`), skill naming conventions, and the contributor credits table provided. Some attributions are best-effort assessments. Upstream license terms apply to their respective skills.

### Source Folder Tags

| Tag | Folder | Source | Approx. Count |
|-----|--------|--------|---------------|
| `[E]` | `skilbro` (engineering) | Various — see table below | ~65 skills |
| `[T]` | `skilbro2` (engineering-team) | Various — see table below | ~32 skills |
| `[W]` | `skilbro3` (superpowers-main) | [obra/superpowers](https://github.com/obra/superpowers) | 14 skills |
| `[F]` | `indian-financial-planning` | Original — custom Indian financial planning skills | 6 skills |

---

### Skills from `obra/superpowers` `[W]`

All 14 workflow skills originate from [obra/superpowers](https://github.com/obra/superpowers), a 5-phase workflow system (Clarify → Design → Plan → Code → Verify) for complex architecture and development tasks:

`dispatching-parallel-agents` · `subagent-driven-development` · `brainstorming` · `writing-plans` · `executing-plans` · `using-superpowers` · `using-git-worktrees` · `writing-skills` · `test-driven-development` · `verification-before-completion` · `requesting-code-review` · `receiving-code-review` · `finishing-a-development-branch` · `systematic-debugging`

---

### Skills by Upstream Contributor

| Category | Skills | Source Repo | Notes |
|----------|--------|-------------|-------|
| Excel / Spreadsheets | `xlsx` | [anthropics/xlsx](https://github.com/anthropics/xlsx) | Automates data cleaning, formula generation, EDA within spreadsheets |
| Skill Meta / Creation | `skill-creator`, `skill-recommender`, `skill-tester`, `skill-security-auditor` | [anthropics/skill-creator](https://github.com/anthropics/skill-creator) | Standardizes skill creation, prompt engineering best practices |
| MCP / Cloud Integration | `mcp-builder`, `mcp-server-builder` | [anthropics/mcp-builder](https://github.com/anthropics/mcp-builder) | Automates creation of MCP servers to integrate APIs and cloud services |
| Documents & Reporting | `docx`, `pdf`, `pptx` | [anthropics/skills](https://github.com/anthropics/skills) | Word/PDF/PowerPoint generation with formatting and citations |
| Internal Communications | `internal-comms` | [anthropics/internal-comms](https://github.com/anthropics/internal-comms) | Status reports, newsletters, FAQs, incident reports, team updates |
| Web / API Testing | `api-test-suite-builder`, `browser-automation` | [anthropics/webapp-testing](https://github.com/anthropics/webapp-testing) · [mendableai/firecrawl](https://github.com/mendableai/firecrawl) | Playwright-based testing; Firecrawl for scraping and structured extraction |
| Cybersecurity / Pen Testing | `security-pen-testing`, `red-team`, `threat-detection`, `senior-security`, `senior-secops` | [trailofbits/security-skills](https://github.com/trailofbits/security-skills) | Trail of Bits — vulnerability scanning, threat modeling, pen testing |
| ML / MLOps | `senior-ml-engineer`, `senior-data-scientist`, `senior-computer-vision` | [ComposioHQ/skills](https://github.com/ComposioHQ/skills) | Connects Claude to ML pipelines for model evaluation and experimentation |
| SQL / Databases | `sql-database-assistant`, `database-designer`, `database-schema-designer` | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Optimized queries, schema mapping for data engineers |
| DevOps / Git / CI-CD | `ci-cd-pipeline-builder`, `changelog-generator`, `git-worktree-manager`, `release-manager` | [kbdhunga/claude-skills](https://github.com/kbdhunga/claude-skills) | Git automation, CI/CD setup, semantic versioning, releases |
| Autonomous Research | `autoresearch-agent`, `setup`, `run`, `loop`, `resume`, `status` | [sickn33/antigravity](https://github.com/sickn33/antigravity) | Autonomous planning logic, experiment loops, agent-driven iteration |
| Financial Analysis | `statistical-analyst`, `senior-data-engineer` | [anthropic-cookbooks](https://github.com/anthropics/anthropic-cookbook) | Ratio calculators, financial analysis suites |
| Workflow System | All `[W]` skills (14 total) | [obra/superpowers](https://github.com/obra/superpowers) | 5-phase development workflow (Clarify → Design → Plan → Code → Verify) |
| Indian Financial Planning | `indian-tax-regime-optimizer`, `indian-real-estate-bhopal`, `indian-mutual-fund-tax`, `senior-citizen-savings-scheme`, `family-portfolio-aggregator`, `lrs-foreign-investment-tax` | Original `[F]` — custom Indian financial planning skills | FY2025-26 tax law, MP stamp duty, SCSS, LRS/TCS, DTAA; includes stdlib-only Python calculators |

---

### Skills with Blended / Unconfirmed Origin

The following skills appeared in `skilbro` or `skilbro2` but could not be definitively traced to a single upstream source. They are likely original Anthropic-adjacent team skills or composites from multiple repositories:

`senior-architect` · `senior-backend` · `senior-frontend` · `senior-fullstack` · `senior-devops` · `senior-prompt-engineer` · `senior-qa` · `senior-secops` · `aws-solution-architect` · `azure-cloud-architect` · `gcp-cloud-architect` · `ms365-tenant-manager` · `kubernetes-operator` · `helm-chart-builder` · `docker-development` · `chaos-engineering` · `observability-designer` · `slo-architect` · `rag-architect` · `llm-cost-optimizer` · `llm-wiki` · `performance-profiler` · `incident-commander` · `incident-response` · `codebase-onboarding` · `code-tour` · `code-reviewer` · `adversarial-reviewer` · `tdd-guide` · `epic-design` · `stripe-integration-expert` · `email-template-builder` · `ai-security` · `cloud-security` · `behuman` · `karpathy-coder` · `monorepo-navigator` · `tech-debt-tracker` · `tc-tracker` · `feature-flags-architect` · `dependency-auditor` · `demo-video` · `full-page-screenshot` · `agenthub` · `agent-designer` · `agent-workflow-designer` · `init` · `spawn` · `eval` · `merge` · `board` · `spec-driven-workflow` · `tech-stack-evaluator` · `engineering-skills` · `engineering-advanced-skills` · `prompt-governance` · `runbook-generator` · `interview-system-designer` · `self-eval` · `focused-fix` · `ship-gate` · `env-secrets-manager` · `secrets-vault-manager` · `terraform-patterns` · `command-guide`

---

## Highlighted Skills

### `skill-recommender` ⭐
Takes any task description and recommends which skill to use, with the exact invocation phrase. Built specifically for this collection — use it whenever you're unsure which skill fits your task.

> *"What skill should I use to debug my slow React app?"*
> → Recommends `performance-profiler` with exact invocation phrase

### `agenthub`
Spawns N parallel Claude agents competing on the same task. Best branch wins and merges. Requires a git repo. Great for hard problems where you want multiple approaches explored simultaneously.

### `autoresearch-agent`
Autonomous improvement loop — edits, evaluates, commits improvements, discards failures, repeats until convergence. Pairs with `setup`, `run`, `loop`, `resume`, and `status`.

### `systematic-debugging`
Structured, hypothesis-driven debugging before proposing fixes. From the obra/superpowers workflow — forces you to understand the problem before jumping to a solution.

### `senior-architect`
Full senior software architect persona with deep knowledge of ADRs, trade-off analysis, distributed systems design, and technology selection.

### Indian Financial Planning Skills `[F]` *(new in v1.1)*
Six original skills covering the full Indian financial planning stack — tax regime comparison, Madhya Pradesh real estate (stamp duty + capital gains exemptions), mutual fund taxation, SCSS for senior citizens, multi-member family portfolio aggregation, and LRS/TCS for foreign investments. All calculations are current for FY2025-26 and include stdlib-only Python calculators with no external dependencies.

> *"Use the `family-portfolio-aggregator` skill to review our family's investments across equity, debt, real estate and gold"*

---

## Contributing

Pull requests welcome. To add a new skill:

1. Create a folder with a `SKILL.md` (YAML frontmatter: `name`, `description`)
2. Add `references/`, `scripts/`, or `assets/` subdirectories if needed
3. Submit a PR with the skill's category and source attribution

---

## License

Individual skills carry licenses from their upstream repositories. Where not specified, skills are shared under MIT. Attribution to upstream contributors is listed in the table above.

---

*Assembled by [csiddhant796-blip](https://github.com/csiddhant796-blip) using Claude Cowork mode.*
