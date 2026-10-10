# CV bullets — use only after verifying your own run/deployment

- Built a LangGraph-based enterprise research agent with explicit state, conditional routing, typed tool calling, RAG retrieval, source verification, output guardrails, and human approval for external research.
- Developed a FastAPI/PostgreSQL service with JWT authentication, persistent execution records, LangGraph PostgreSQL checkpoints, Docker packaging, health/readiness checks, rate limiting, and automated pytest coverage.
- Created a 30-question evaluation dataset and reproducible evaluation runner covering answer relevance, grounding, context relevance/recall, citation quality, and tool-call correctness, with optional LangSmith tracing.

## AWS wording
Do not add “deployed to AWS” until you have actually deployed and verified ECS/Fargate + RDS. Then revise the second bullet to name the services you actually used.
