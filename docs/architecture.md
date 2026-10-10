# Architecture notes

The graph is explicit: input validation → planner → tool selection → optional approval → research → analysis → verification → output guardrail → response.

Application metadata is persisted with SQLAlchemy/PostgreSQL. LangGraph checkpoints use the PostgreSQL checkpointer when the application can connect to PostgreSQL; the builder's in-memory fallback exists only for local isolated tests.

No node accepts arbitrary Python or shell commands. Tool interfaces are typed with Pydantic and the calculator uses a restricted AST evaluator.
