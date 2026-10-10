from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "enterprise-research-agent"
    environment: str = "development"
    log_level: str = "INFO"
    api_prefix: str = "/api/v1"
    llm_provider: str = "google"
    google_api_key: str | None = None
    google_model: str = "gemini-3.5-flash-lite"
    google_embedding_model: str = "gemini-embedding-2"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/research_agent"
    langgraph_database_url: str = "postgresql://postgres:postgres@localhost:5432/research_agent"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    demo_username: str = "demo"
    demo_password: str = "change-me"
    search_max_results: int = 5
    allowed_search_domains: str = "arxiv.org,paperswithcode.com,developers.google.com,aws.amazon.com,nist.gov,nih.gov,who.int,scikit-learn.org,pytorch.org,tensorflow.org"
    chroma_dir: str = "./.chroma"
    rag_collection: str = "research_documents"
    rag_top_k: int = 5
    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    langsmith_project: str = "enterprise-research-agent"
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    langchain_tracing_v2: bool = False
    langchain_api_key: str | None = None
    langchain_project: str = "enterprise-research-agent"
    langchain_endpoint: str = "https://api.smith.langchain.com"
    max_query_length: int = 4000
    rate_limit: str = "30/minute"
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")
    @property
    def search_domains(self):
        return [x.strip() for x in self.allowed_search_domains.split(",") if x.strip()]

@lru_cache
def get_settings():
    return Settings()
