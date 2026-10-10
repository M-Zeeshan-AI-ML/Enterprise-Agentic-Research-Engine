# AWS deployment: ECS/Fargate + RDS

This is an AWS-ready procedure, not proof of an already completed deployment.

1. Create an ECR repository: `aws ecr create-repository --repository-name enterprise-research-agent`.
2. Build and push the image using `aws ecr get-login-password`, `docker build`, `docker tag`, and `docker push`.
3. Create RDS PostgreSQL in the same VPC/private subnets as ECS. Enable pgvector where supported by the chosen RDS configuration.
4. Store the configured provider key (`GOOGLE_API_KEY` when `LLM_PROVIDER=google`, or `OPENAI_API_KEY` when `LLM_PROVIDER=openai`), `JWT_SECRET_KEY`, database credentials, and optional LangSmith credentials in AWS Secrets Manager.
5. Create ECS Fargate cluster/task definition with port 8000 and the ECR image.
6. Put an ALB in front of ECS and configure the target health check to `/health`.
7. Inject `DATABASE_URL` and `LANGGRAPH_DATABASE_URL` into the task.
8. Verify `/health` and `/ready` from the public service.

Only after the service is actually reachable and verified should AWS deployment be claimed on a CV.
