import os
from app.config.settings import get_settings
def configure_tracing():
    s=get_settings()
    if s.langsmith_tracing and s.langsmith_api_key:
        os.environ.setdefault("LANGSMITH_TRACING","true"); os.environ.setdefault("LANGSMITH_API_KEY",s.langsmith_api_key); os.environ.setdefault("LANGSMITH_PROJECT",s.langsmith_project); os.environ.setdefault("LANGSMITH_ENDPOINT",s.langsmith_endpoint)
    if s.langchain_tracing_v2 and s.langchain_api_key:
        os.environ.setdefault("LANGCHAIN_TRACING_V2","true"); os.environ.setdefault("LANGCHAIN_API_KEY",s.langchain_api_key); os.environ.setdefault("LANGCHAIN_PROJECT",s.langchain_project); os.environ.setdefault("LANGCHAIN_ENDPOINT",s.langchain_endpoint)
