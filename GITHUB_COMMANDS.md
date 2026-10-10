# GitHub upload

```bash
git init
git add .
git commit -m "Build enterprise research decision agent"
git branch -M main
git remote add origin https://github.com/<USERNAME>/enterprise-research-agent.git
git push -u origin main
```

Before the first commit:

```bash
copy .env.example .env
```

Keep `.env` untracked. Never commit API keys, database passwords, or LangSmith keys.
