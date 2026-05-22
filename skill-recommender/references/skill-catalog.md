# Skill Catalog — 117 Skills

Skills come from four sources:
- **[E]** = Engineering skills (skilbro — claude-skills-main/engineering)
- **[T]** = Engineering-Team skills (skilbro2 — claude-skills-main/engineering-team)
- **[W]** = Workflow/Superpowers skills (skilbro3 — superpowers-main)
- **[F]** = Indian Financial Planning skills (custom Indian financial planning skills)

---

## Table of Contents
1. [Multi-Agent & Parallel Work](#multi-agent--parallel-work)
2. [Workflow & Planning](#workflow--planning)
3. [Architecture & System Design](#architecture--system-design)
4. [Backend Development](#backend-development)
5. [Frontend Development](#frontend-development)
6. [Fullstack & Scaffolding](#fullstack--scaffolding)
7. [Cloud & Infrastructure](#cloud--infrastructure)
8. [DevOps & CI/CD](#devops--cicd)
9. [Containers & Kubernetes](#containers--kubernetes)
10. [Security](#security)
11. [Testing & Quality](#testing--quality)
12. [Data Engineering & Pipelines](#data-engineering--pipelines)
13. [ML & AI Engineering](#ml--ai-engineering)
14. [LLM & Prompt Engineering](#llm--prompt-engineering)
15. [Observability & Reliability](#observability--reliability)
16. [Databases](#databases)
17. [Incident Response](#incident-response)
18. [Productivity & Tooling](#productivity--tooling)
19. [Automation & Browser](#automation--browser)
20. [Communication & Human Touch](#communication--human-touch)
21. [Indian Financial Planning](#indian-financial-planning)

---

## Multi-Agent & Parallel Work

**`agenthub`** [E]
Spawns N parallel subagents competing on the same task via git worktree isolation. The best branch wins and gets merged.
_Use when:_ You want multiple approaches tried simultaneously — code optimization, content variation, research. Requires a git repo.

**`agent-designer`** [E]
Designs multi-agent systems: architectures, communication patterns, autonomous workflows.
_Use when:_ You need to design or build a multi-agent system.

**`agent-workflow-designer`** [E]
Designs production-grade multi-agent workflows with handoff contracts, failure handling, and cost controls.
_Use when:_ You need a production-ready multi-agent workflow with defined patterns.

**`init`** [E] _(AgentHub)_
Creates a new AgentHub session with task, agent count, and evaluation criteria.
_Use when:_ Starting a new AgentHub multi-agent competition session.

**`spawn`** [E] _(AgentHub)_
Launches N parallel subagents in isolated worktrees within an AgentHub session.
_Use when:_ Starting parallel competition in an AgentHub session.

**`eval`** [E] _(AgentHub)_
Evaluates and ranks agent results by metric or LLM judge.
_Use when:_ Comparing outputs from parallel agents in AgentHub.

**`merge`** [E] _(AgentHub)_
Merges the winning branch, archives losers, cleans up worktrees.
_Use when:_ An AgentHub competition is done and you need to merge the winner.

**`board`** [E] _(AgentHub)_
Reads/writes the AgentHub shared message board for agent coordination.
_Use when:_ Agents need to coordinate via a shared board in AgentHub.

**`dispatching-parallel-agents`** [W]
Guides dispatching multiple independent tasks to parallel subagents simultaneously.
_Use when:_ You have 2+ independent tasks that can run without shared state.

**`subagent-driven-development`** [W]
Guides executing implementation plans with independent tasks using subagents in the current session.
_Use when:_ Executing an implementation plan with independent parallelizable tasks.

---

## Workflow & Planning

**`brainstorming`** [W]
Explores intent, requirements, and design before any implementation. Turns vague ideas into concrete designs.
_Use when:_ Before any creative work — creating features, building components, adding functionality. Must run before implementation.

**`writing-plans`** [W]
Guides creation of a detailed step-by-step implementation plan from a spec or requirements.
_Use when:_ You have requirements for a multi-step task and need a plan before touching code.

**`executing-plans`** [W]
Guides faithful execution of a written implementation plan in a separate session with review checkpoints.
_Use when:_ You have a written plan ready to execute.

**`spec-driven-workflow`** [E]
Guides writing specs before code, defining acceptance criteria, planning features before implementation.
_Use when:_ You need to follow spec-first development — write specs, define acceptance criteria, then generate tests.

**`using-superpowers`** [W]
Establishes how to find and use skills, requiring Skill tool invocation before any response.
_Use when:_ Starting any conversation — sets up the rule that skills must be invoked first.

**`using-git-worktrees`** [W]
Ensures an isolated workspace via git worktrees before executing implementation plans.
_Use when:_ Starting feature work that needs isolation from the current workspace.

**`git-worktree-manager`** [E]
Runs parallel feature work safely with worktrees. Standardizes branch isolation, port allocation, env sync, and cleanup.
_Use when:_ Running parallel feature development using git worktrees.

**`writing-skills`** [W]
Guides creating new skills, editing existing skills, and verifying skills work before deployment.
_Use when:_ Creating or editing skills.

---

## Architecture & System Design

**`senior-architect`** [T]
Designs system architectures, evaluates microservices vs monolith, creates Mermaid/PlantUML/ASCII diagrams, generates ADRs, reviews system designs.
_Use when:_ Designing system architecture, evaluating microservices vs monolith, choosing a database, planning scalability.

**`migration-architect`** [E]
Plans, executes, and validates complex system migrations with minimal business impact.
_Use when:_ Planning or executing a complex migration between systems, databases, or infrastructure.

**`tech-stack-evaluator`** [T]
Evaluates and compares tech stacks with TCO analysis, security assessment, and ecosystem health scoring.
_Use when:_ Comparing frameworks, evaluating stacks, calculating TCO, or assessing migration paths.

**`engineering-skills`** [T]
A bundle of 23 engineering agent skills covering architecture, frontend, backend, QA, DevOps, security, AI/ML, Playwright, Stripe, AWS, MS365.
_Use when:_ You need a broad multi-domain engineering toolkit.

**`engineering-advanced-skills`** [E]
25 advanced engineering skills: agent design, RAG, MCP, CI/CD, database design, observability, security, release management.
_Use when:_ You need a broad advanced engineering toolkit.

---

## Backend Development

**`senior-backend`** [T]
Designs and implements REST APIs, microservices, DB architectures, auth flows, security hardening. Node.js/Express/Fastify, PostgreSQL, GraphQL.
_Use when:_ Designing REST APIs, optimizing DB queries, implementing auth, building microservices, reviewing backend code.

**`stripe-integration-expert`** [T]
Implements production Stripe integrations: subscriptions with trials/proration, usage-based billing, checkout, webhooks, customer portal. Next.js, Express, Django.
_Use when:_ Implementing or improving a Stripe payment integration.

**`email-template-builder`** [T]
Builds transactional email systems: React Email templates, provider integration (Resend, Postmark, SendGrid, AWS SES), dark mode, i18n, spam optimization.
_Use when:_ Building transactional email templates or a transactional email system.

---

## Frontend Development

**`senior-frontend`** [T]
React, Next.js, TypeScript, Tailwind. Builds components, optimizes performance, analyzes bundles, implements accessibility, reviews frontend code.
_Use when:_ Building React components, optimizing Next.js, analyzing bundles, implementing a11y, reviewing frontend code.

**`epic-design`** [T]
Builds immersive, cinematic 2.5D interactive websites using scroll storytelling, parallax depth, text animations, premium scroll effects.
_Use when:_ Any web design task requiring visual impact — landing pages, product sites, scroll-driven experiences.

---

## Fullstack & Scaffolding

**`senior-fullstack`** [T]
Project scaffolding for Next.js, FastAPI, MERN, Django. Code quality analysis, stack selection, project boilerplate generation.
_Use when:_ Scaffolding a new project, creating a Next.js app, setting up FastAPI with React, analyzing code quality, choosing a tech stack.

---

## Cloud & Infrastructure

**`aws-solution-architect`** [T]
Designs AWS serverless architectures. Lambda, API Gateway, DynamoDB, ECS, Aurora. CloudFormation templates, CI/CD pipelines, cost optimization.
_Use when:_ Designing serverless architecture on AWS, creating CloudFormation templates, optimizing AWS costs, migrating to AWS.

**`azure-cloud-architect`** [T]
Designs Azure architectures. Bicep/ARM templates, Azure DevOps, AKS, App Service, Azure Functions, Cosmos DB.
_Use when:_ Designing Azure infrastructure, creating Bicep/ARM templates, setting up Azure DevOps, migrating to Azure.

**`gcp-cloud-architect`** [T]
Designs GCP architectures. GKE, Cloud Run, BigQuery, Cloud Functions, Cloud SQL.
_Use when:_ Designing Google Cloud infrastructure, deploying to GKE or Cloud Run, BigQuery pipelines, migrating to GCP.

**`terraform-patterns`** [E]
Terraform modules, state backends, multi-region deployments, IaC security. Sentinel/OPA, CI/CD plan/apply workflows.
_Use when:_ Designing Terraform modules, managing state backends, reviewing Terraform security, IaC best practices.

**`ms365-tenant-manager`** [T]
Automates M365 tenant setup, Azure AD user management, Exchange Online, Teams admin, Conditional Access, PowerShell scripts.
_Use when:_ M365 tenant management, Office 365 admin, Azure AD user management, Microsoft 365 automation.

---

## DevOps & CI/CD

**`senior-devops`** [T]
Comprehensive DevOps: CI/CD, infra automation, containerization, AWS/GCP/Azure. Pipeline setup, IaC, deployment automation, monitoring.
_Use when:_ Setting up pipelines, deploying apps, managing infrastructure, implementing monitoring.

**`ci-cd-pipeline-builder`** [E]
Generates CI/CD pipelines from detected project stack signals. Fast baseline generation with repeatable checks and deployment stages.
_Use when:_ Setting up, generating, or improving CI/CD pipelines.

**`release-manager`** [E]
Plans releases, manages changelogs, coordinates deployments, creates release branches, automates versioning.
_Use when:_ Planning releases, managing changelogs, coordinating deployments.

**`changelog-generator`** [E]
Produces consistent release notes from Conventional Commits. Semantic bump logic and changelog rendering.
_Use when:_ Generating changelogs from git commits, automating release notes, managing semantic versioning.

---

## Containers & Kubernetes

**`docker-development`** [E]
Optimizes Dockerfiles, docker-compose, multi-stage builds, container security audits, image size reduction.
_Use when:_ Optimizing a Dockerfile, creating docker-compose configs, auditing container security, reducing image size.

**`kubernetes-operator`** [E]
Builds Kubernetes Operators — custom controllers reconciling CRD state. controller-runtime, kubebuilder, operator-sdk, metacontroller, KOPF.
_Use when:_ Building a Kubernetes Operator, designing CRDs, working on reconcile loops.

**`helm-chart-builder`** [E]
Creates/improves Helm charts, values.yaml, template helpers, RBAC/network policy audits, subchart management.
_Use when:_ Creating or improving Helm charts, auditing chart security, managing subcharts.

---

## Security

**`senior-security`** [T]
Threat modeling, vulnerability analysis, secure architecture, pen testing. STRIDE, OWASP, cryptography patterns, security scanning.
_Use when:_ Security reviews, threat analysis, vulnerability assessments, secure coding, CVE remediation.

**`senior-secops`** [T]
App security, vulnerability management, compliance. SAST/DAST, CVE remediation plans, dependency vuln checks, SOC2/PCI-DSS/HIPAA/GDPR compliance.
_Use when:_ Security review, responding to CVEs, hardening infra, enforcing security controls in CI/CD.

**`ai-security`** [T]
Assesses AI/ML systems for prompt injection, jailbreaks, model inversion, data poisoning, agent tool abuse. MITRE ATLAS mapping.
_Use when:_ Assessing AI/ML systems for prompt injection or jailbreak vulnerabilities.

**`cloud-security`** [T]
Assesses cloud infra for misconfigs, IAM privilege escalation, S3 exposure, open security groups, IaC gaps. AWS/Azure/GCP.
_Use when:_ Assessing cloud infrastructure for security misconfigurations or IAM privilege escalation.

**`security-pen-testing`** [T]
Security audits, pen testing, OWASP Top 10 checks, static analysis, dependency scanning, secret detection, API security, pen test reports.
_Use when:_ Security audits, penetration testing, vulnerability scanning, offensive security assessments.

**`red-team`** [T]
Authorized red team engagements, attack path analysis, MITRE ATT&CK kill-chain planning, OPSEC risk assessment.
_Use when:_ Planning or executing authorized red team engagements or attack simulations.

**`threat-detection`** [T]
Hunts threats in an environment, analyzes IOCs, detects behavioral anomalies. Hypothesis-driven hunting, z-score anomaly detection, MITRE ATT&CK mapping.
_Use when:_ Hunting for threats, analyzing IOCs, detecting behavioral anomalies in telemetry.

**`ship-gate`** [E]
Pre-production audit: security, DB, deployment, code quality, AI/LLM, dependency, frontend, observability issues. Blocks deploy until critical items pass.
_Use when:_ Deploying to production. Triggers: "am I ready to ship", "pre-launch audit", "can I deploy", "go live checklist".

**`skill-security-auditor`** [E]
Security audits AI agent skills. Detects malicious code, prompt injection in SKILL.md files, dangerous patterns, supply chain risks.
_Use when:_ Evaluating a skill from an untrusted source before installation.

**`env-secrets-manager`** [E]
Manages environment variable hygiene and secrets safety. Auditing, drift awareness, rotation readiness.
_Use when:_ Setting up secret management, auditing env vars, managing secret rotation.

**`secrets-vault-manager`** [E]
Sets up secret management infra: HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager. Secret rotation, access audits.
_Use when:_ Setting up vault infrastructure, implementing secret rotation, auditing secret access patterns.

---

## Testing & Quality

**`tdd-guide`** [T]
TDD workflow: writing tests, generating fixtures/mocks, analyzing coverage gaps, red-green-refactor. Jest, Pytest, JUnit, Vitest, Mocha.
_Use when:_ Writing tests, improving coverage, practicing TDD, generating mocks/stubs.

**`test-driven-development`** [W]
Guides the TDD workflow — writing tests before implementation code for any feature or bugfix.
_Use when:_ Implementing any feature or bugfix, before writing implementation code.

**`senior-qa`** [T]
Generates unit, integration, E2E tests for React/Next.js. Jest + RTL, Istanbul/LCOV coverage, Playwright, MSW mocks, test fixtures.
_Use when:_ Generating tests, analyzing coverage, scaffolding E2E tests, setting up Playwright/Jest.

**`api-test-suite-builder`** [E]
Generates API tests, integration test suites, REST endpoint tests, contract tests.
_Use when:_ Generating API tests, creating integration test suites, building contract tests.

**`code-reviewer`** [T]
Automated code review for TypeScript, JavaScript, Python, Go, Swift, Kotlin. SOLID violations, code smells, PR complexity analysis, review reports.
_Use when:_ Reviewing PRs, analyzing code quality, generating review checklists.

**`pr-review-expert`** [E]
Reviews PRs, analyzes code changes, checks security issues, assesses code quality of diffs.
_Use when:_ Reviewing pull requests, analyzing code changes, checking security in PRs.

**`adversarial-reviewer`** [T]
Adversarial code review that forces hostile reviewer personas to catch blind spots polite review misses.
_Use when:_ You want a genuinely critical review, or suspect Claude is being too agreeable about code quality.

**`karpathy-coder`** [E]
Enforces Karpathy's 4 coding principles: surface assumptions, keep it simple, surgical changes, verifiable goals.
_Use when:_ Writing, reviewing, or committing code to enforce coding discipline.

**`focused-fix`** [E]
Systematic deep-dive repair of a specific feature, module, or area across all files and dependencies.
_Use when:_ Fixing or making a specific feature/module work end-to-end. Not for quick single-bug fixes.

**`verification-before-completion`** [W]
Requires running verification commands before claiming work is complete or passing. Enforces evidence before assertions.
_Use when:_ About to claim work is complete, fixed, or passing; before committing or creating PRs.

**`requesting-code-review`** [W]
Guides when and how to request code review to verify work meets requirements.
_Use when:_ Completing tasks, implementing features, or before merging to verify requirements are met.

**`receiving-code-review`** [W]
Guides how to properly receive code review feedback with technical rigor rather than blind implementation.
_Use when:_ Receiving code review feedback, especially if it seems unclear or technically questionable.

**`finishing-a-development-branch`** [W]
Guides completion of development work — structured options for merge, PR, or cleanup once tests pass.
_Use when:_ Implementation is complete, tests pass, and you need to decide how to integrate the work.

**`self-eval`** [E]
Honestly evaluates AI work quality using a two-axis scoring system. Detects score inflation, forces devil's advocate reasoning.
_Use when:_ After completing a task to get an unbiased quality assessment.

---

## Data Engineering & Pipelines

**`senior-data-engineer`** [T]
Builds scalable data pipelines, ETL/ELT systems. Python, SQL, Spark, Airflow, dbt, Kafka, modern data stack.
_Use when:_ Designing data architectures, building pipelines, implementing data governance, troubleshooting data issues.

**`data-quality-auditor`** [E]
Audits datasets: completeness, consistency, accuracy, validity. Profiles distributions, detects anomalies, produces remediation plans.
_Use when:_ Full data audit, checking data quality before analysis or production use.

**`statistical-analyst`** [E]
Runs hypothesis tests, analyzes A/B results, calculates sample sizes, interprets statistical significance with effect sizes.
_Use when:_ Validating whether observed differences are real, sizing experiments, interpreting test results.

**`senior-data-scientist`** [T]
Statistical modeling, experiment design, causal inference, predictive analytics. A/B testing, DiD, feature engineering, AUC-ROC, SHAP, MLflow.
_Use when:_ Designing or analyzing controlled experiments, building ML models, causal analysis, feature engineering.

---

## ML & AI Engineering

**`senior-ml-engineer`** [T]
Productionizes ML models, builds MLOps pipelines. Model deployment, feature stores, drift monitoring, RAG, cost optimization. MLflow, Kubeflow, k8s, Docker.
_Use when:_ Deploying ML models, setting up MLOps, monitoring model drift, building RAG pipelines.

**`senior-computer-vision`** [T]
Object detection, image segmentation, visual AI. CNN/ViT architectures, YOLO/Faster R-CNN/DETR, Mask R-CNN/SAM, ONNX/TensorRT.
_Use when:_ Building detection pipelines, training custom vision models, optimizing inference, deploying vision systems.

**`autoresearch-agent`** [E]
Autonomous experiment loop that optimizes any file by a measurable metric. Edits, evaluates, commits improvements, discards failures, loops.
_Use when:_ Optimizing code speed, reducing bundle size, improving test pass rate, optimizing prompts, or any measurable improvement loop. Requires target file, eval command, git repo.

**`setup`** [E] _(autoresearch)_
Sets up a new autoresearch experiment interactively.
_Use when:_ Starting a new autoresearch experiment for the first time.

**`run`** [E] _(autoresearch)_
Runs a single autoresearch iteration — edits, evaluates, keeps or discards.
_Use when:_ Running one autoresearch iteration manually.

**`loop`** [E] _(autoresearch)_
Starts an autonomous experiment loop on a recurring schedule (10min, 1h, daily, weekly, monthly).
_Use when:_ Scheduling a recurring autoresearch loop.

**`resume`** [E] _(autoresearch)_
Resumes a paused autoresearch experiment.
_Use when:_ Resuming a previously paused autoresearch experiment.

**`status`** [E] _(autoresearch)_
Shows the autoresearch dashboard with results, active loops, and progress.
_Use when:_ Checking status of running/completed autoresearch experiments.

---

## LLM & Prompt Engineering

**`senior-prompt-engineer`** [T]
Optimizes prompts, designs templates, evaluates LLM outputs, builds agentic systems, implements RAG, creates few-shot examples, analyzes token usage.
_Use when:_ Optimizing prompts, designing prompt templates, evaluating LLM outputs, building AI workflows.

**`llm-cost-optimizer`** [E]
Optimizes LLM API costs: model selection, token usage reduction, prompt caching, per-feature cost logging, max_tokens config.
_Use when:_ LLM API costs are too high, optimizing token usage, choosing the right model.

**`rag-architect`** [E]
Designs RAG pipelines, optimizes retrieval, chooses embedding models, implements vector search, builds knowledge retrieval systems.
_Use when:_ Designing RAG pipelines, optimizing retrieval strategies, implementing vector search.

**`prompt-governance`** [E]
Manages prompts in production at scale: versioning, A/B tests, prompt registries, regression prevention, eval pipelines.
_Use when:_ Managing prompts in production — versioning, regression testing, A/B testing. Not for writing individual prompts.

**`llm-wiki`** [E]
Builds a persistent personal knowledge base in Obsidian where an LLM incrementally ingests sources and updates entity/concept pages.
_Use when:_ "Second brain", "Obsidian wiki", "ingest this paper/article", "build a research wiki", knowledge that should accumulate across sessions.

**`mcp-server-builder`** [E]
Builds MCP (Model Context Protocol) servers for extending AI agent capabilities with custom tools.
_Use when:_ Building or creating an MCP server.

---

## Observability & Reliability

**`observability-designer`** [E]
Creates production-ready observability strategies: metrics, logs, traces. SLI/SLO design, golden signals, alert optimization.
_Use when:_ Designing or improving observability for a production system.

**`slo-architect`** [E]
Defines, reviews, and operates SLOs/SLIs/error budgets. SLO designer, error-budget calculator, multi-window burn-rate thresholds.
_Use when:_ Defining, reviewing, or operating SLOs/SLIs/error budgets. This is specifically the SLO discipline.

**`chaos-engineering`** [E]
Plans, runs, and analyzes chaos experiments. Fault injection, gamedays, resilience tests, blast-radius calculator, steady-state hypothesis.
_Use when:_ Planning/running chaos experiments, fault injection, gamedays, resilience tests.

**`performance-profiler`** [E]
Profiles Node.js, Python, Go. CPU/memory/I/O bottlenecks, flamegraphs, bundle sizes, DB query optimization, memory leak detection, load tests.
_Use when:_ Profiling application performance, finding bottlenecks, optimizing queries, detecting memory leaks.

**`runbook-generator`** [E]
Generates operational runbooks for deployment, incident response, maintenance, and rollback workflows.
_Use when:_ Creating or generating operational runbooks for a service.

---

## Databases

**`database-designer`** [E]
Designs DB schemas, plans data migrations, optimizes queries, helps choose SQL vs NoSQL, models data relationships.
_Use when:_ Designing DB schemas, planning migrations, optimizing queries, choosing SQL vs NoSQL.

**`database-schema-designer`** [E]
Designs relational schemas from requirements. Generates migrations, TypeScript/Python types, seed data, RLS policies, indexes. Multi-tenancy, soft deletes, audit trails.
_Use when:_ Creating ERD diagrams, normalizing schemas, designing table relationships, planning schema migrations.

**`sql-database-assistant`** [E]
Writes SQL queries, optimizes DB performance, generates migrations, explores schemas, works with ORMs (Prisma, Drizzle, TypeORM, SQLAlchemy).
_Use when:_ Writing SQL queries, optimizing DB performance, generating migrations, working with ORMs.

---

## Incident Response

**`incident-commander`** [T]
Full incident response framework: detection through resolution and post-mortem. Severity classification, timeline reconstruction, post-incident analysis.
_Use when:_ Managing a live technology incident from detection through resolution.

**`incident-response`** [T]
Classifies, triages, escalates security incidents. SEV1-SEV4 classification, false positive filtering, forensic evidence collection, NIST SP 800-61.
_Use when:_ A security incident has been detected and needs classification, triage, and forensic collection.

**`systematic-debugging`** [W]
Structured process for debugging bugs, test failures, or unexpected behavior before proposing fixes.
_Use when:_ Any bug, test failure, or unexpected behavior — before proposing fixes.

---

## Productivity & Tooling

**`tc-tracker`** [E]
Tracks technical changes, creates change records, manages TC lifecycles, hands off work between AI sessions.
_Use when:_ Tracking technical changes, managing TC lifecycles, handing off work between sessions.

**`tech-debt-tracker`** [E]
Scans codebases for tech debt, scores severity, tracks trends, generates prioritized remediation plans.
_Use when:_ Assessing tech debt, refactoring priority, debt scoring, legacy code modernization.

**`feature-flags-architect`** [E]
Adds, retires, or audits feature flags. Flag debt scanner, rollout planner, kill-switch auditor. LaunchDarkly, GrowthBook, Statsig, Unleash, Flipt.
_Use when:_ Adding a feature flag, planning a rollout, cleaning up stale flags, implementing a kill switch.

**`dependency-auditor`** [E]
Analyzes dependencies across multi-language projects. Vulnerability identification, license compliance, dependency tree optimization, safe upgrades.
_Use when:_ Auditing dependencies for vulnerabilities, checking license compliance, planning upgrades.

**`monorepo-navigator`** [E]
Navigates and optimizes monorepos: Turborepo, Nx, pnpm workspaces, Lerna. Cross-package impact analysis, selective builds, remote caching.
_Use when:_ Navigating, managing, or optimizing a monorepo.

**`codebase-onboarding`** [E]
Analyzes a codebase and generates onboarding documentation for engineers, tech leads, and contractors.
_Use when:_ Engineers or contractors need to onboard to a new codebase quickly.

**`code-tour`** [E]
Creates CodeTour `.tour` files — step-by-step walkthroughs linking to real files/line numbers for onboarding, PR reviews, contributor guides.
_Use when:_ Creating a CodeTour file, onboarding tour, architecture tour, or PR review tour.

**`interview-system-designer`** [E]
Designs interview processes, hiring pipelines, generates questions, builds competency matrices, scoring rubrics, question banks.
_Use when:_ Designing interview processes, generating interview questions, building competency matrices.

**`skill-tester`** [E]
Tests AI agent skills for correctness, edge cases, and quality assurance before deployment.
_Use when:_ Testing a skill to verify it works before deployment.

---

## Automation & Browser

**`browser-automation`** [E]
Automates browser tasks, scrapes websites, fills forms, captures screenshots, extracts structured data, builds web automation workflows.
_Use when:_ Automating browser tasks, scraping, filling forms, extracting data. Not for testing (use Playwright for that).

**`full-page-screenshot`** [E]
Captures full-page screenshots of web pages. Handles SPA scroll containers, lazy-loaded images, very tall pages. Zero external dependencies.
_Use when:_ Capturing a full-page screenshot or complete page capture.

**`demo-video`** [E]
Creates demo videos, product walkthroughs, feature showcases, animated presentations, and GIFs. Uses playwright, ffmpeg, edge-tts.
_Use when:_ Creating a demo video, product walkthrough, feature showcase, marketing video, or GIF.

---

## Communication & Human Touch

**`behuman`** [E]
Makes AI responses more human-like — less robotic, less listy, more authentic and emotionally aware.
_Use when:_ Responses feel too robotic, or conversations are emotionally charged (grief, job loss, relationship advice). NOT for technical questions or code.

**`command-guide`** [E]
Helps choose the most appropriate Claude Code command, agent, or skill via a decision flowchart and cheat sheet.
_Use when:_ Unsure which command or tool to use; need to pick an agent/skill for a task.

---

## Indian Financial Planning

**`indian-tax-regime-optimizer`** [F]
Computes Indian income tax under both old and new regimes for FY 2025-26, enforces statutory deduction caps (80C ₹1.5L, 80CCD(1B) ₹50K, 80D age-based, 80TTB ₹50K senior-only), handles general/senior/super-senior slabs, applies Section 87A rebates, adds 4% cess, recommends optimal regime.
_Use when:_ Old vs new regime question, "which regime saves more", computing Indian income tax, 80C/80D/80TTB planning, Form 10-IEA, senior-citizen tax slabs. Verified May 2026 against Finance Act 2024/2025.

**`indian-real-estate-bhopal`** [F]
Indian real estate tax + transaction planning, MP-focused. MP stamp duty (10.5% total), capital gains grandfathering decision (Path A 12.5% no-index vs Path B 20%+indexation), Section 50C deemed value check, exemption recommender (54/54EC/54F/54B), REIT distribution classifier, Section 24 rental income, TDS calculations (194-IA, 194-IB, 194-I), Bhopal agricultural land Section 2(14)(iii) classification.
_Use when:_ Buying/selling/renting Indian property, stamp duty, capital gains on property, indexation, Section 54 exemptions, REIT tax, agricultural land, SAMPADA, MP-RERA. CII rates need annual June verification.

**`indian-mutual-fund-tax`** [F]
Indian MF tax calculator with Section 50AA debt-trap detector. Equity LTCG (12.5% above ₹1.25L), Section 50AA proactive warning for debt MFs/gold FoFs/intl FoFs purchased post April 2023, ELSS per-SIP lock-in tracking (36 months per installment), hybrid fund 65% equity threshold classification.
_Use when:_ MF tax planning, debt MF taxation, ELSS lock-in, hybrid fund classification, "Section 50AA" trap, gold MF vs gold ETF decision. Always trigger when user mentions debt MF purchased after April 2023.

**`senior-citizen-savings-scheme`** [F]
SCSS planner for retirees (60+). Quarterly cashflow at current 8.20% rate (Q1 FY 2026-27), TDS implications with ₹1L senior threshold from April 2025, 80TTB and 80C eligibility, premature withdrawal penalties (<1yr no interest, 1-2yr 1.5%, 2-5yr 1%), post-tax yield comparison vs FRSB/PO TD/bank FD.
_Use when:_ SCSS planning, safe income for parents/retirees, quarterly retirement income, Form 15H, 80TTB deduction. Re-verify rate quarterly (1 Apr / 1 Jul / 1 Oct / 1 Jan).

**`family-portfolio-aggregator`** [F]
Multi-member household portfolio rollup. Per-member totals, asset allocation breakdown (7 classes), drift detection vs age-based target allocations, concentration warnings for any single holding > 25% family NW, annual income projection per member.
_Use when:_ Family/household portfolio review, consolidated investment view, asset allocation drift, rebalancing, concentration risk across spouse/parents/children. Orchestrates other Indian-financial skills.

**`lrs-foreign-investment-tax`** [F]
LRS + foreign equity tax for Indian residents investing abroad. Three modules: TCS calculator (20% above ₹10L/FY, refundable), DTAA lookup for 8 countries + Form 67 foreign tax credit math (Rule 128), Section 112 foreign stock LTCG (12.5% after 24 months post Budget 2024). Includes Schedule FA mandatory disclosure reminder (₹10L penalty under Black Money Act).
_Use when:_ Investing in US/Japan/Singapore stocks from India, LRS, TCS, DTAA, Form 67, W-8BEN, foreign capital gains, Schedule FA. Always trigger when any non-Indian equity holding is mentioned.

---

*Total: 117 skills — 65 [E] Engineering + 32 [T] Engineering-Team + 14 [W] Workflow + 6 [F] Indian Financial Planning*
