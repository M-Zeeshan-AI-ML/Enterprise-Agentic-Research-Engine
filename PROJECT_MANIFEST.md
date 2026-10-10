# Project manifest

## Core runtime
- `app/main.py` — FastAPI application lifecycle, PostgreSQL checkpoint setup, health/readiness, demo route.
- `app/api/routes.py` — authentication, research, approval/resume, and status endpoints.
- `app/api/deps.py` — bearer-token dependency.
- `app/api/demo.py` — deliberately minimal HTML demo.
- `app/graph/state.py` — explicit LangGraph state contract.
- `app/graph/nodes.py` — validation, planning, tool selection, approval, research, analysis, verification, guardrails.
- `app/graph/builder.py` — graph topology and conditional edges.
- `app/graph/checkpoint.py` — PostgreSQL LangGraph checkpointer.

## Tools and RAG
- `app/tools/search.py` — allow-listed web search.
- `app/tools/retrieval.py` — typed RAG retrieval tool.
- `app/tools/calculator.py` — restricted arithmetic evaluator.
- `app/tools/verification.py` — allow-listed source verification.
- `app/tools/registry.py` — explicit tool authorization registry.
- `app/rag/chroma_store.py` — local Chroma semantic store.
- `app/rag/pgvector_store.py` — production PostgreSQL/pgvector adapter.
- `app/rag/ingest.py` — sample corpus ingestion.

## Persistence/security/observability
- `app/database/*` — SQLAlchemy/PostgreSQL application persistence.
- `app/services/auth.py` — JWT authentication.
- `app/services/persistence.py` — execution records.
- `app/services/rate_limit.py` — request rate limiting.
- `app/services/tracing.py` — optional LangSmith/LangChain tracing environment setup.
- `app/guardrails/policies.py` — input, tool, and output controls.
- `alembic/*` — database migration setup and initial migration.

## Evaluation and quality
- `evals/dataset.jsonl` — 30 realistic questions.
- `evals/run_evaluation.py` — reproducible local evaluation runner; no fabricated scores.
- `tests/*` — guardrails, calculator, graph routing, tools, API health, dataset, approval routing.

## Deployment/docs
- `Dockerfile` — non-root container.
- `docker-compose.yml` — API + pgvector PostgreSQL.
- `docs/aws-deployment.md` — ECS/Fargate + RDS deployment procedure.
- `docs/architecture.md` — architecture rationale.
- `README.md` — setup, API, evaluation, security, deployment, interview explanation.
