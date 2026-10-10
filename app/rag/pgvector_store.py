from sqlalchemy import create_engine,text
from app.config.settings import get_settings
class PgVectorStore:
    """Minimal real pgvector adapter for production embeddings."""
    def __init__(self,dimension=1536): self.engine=create_engine(get_settings().database_url,pool_pre_ping=True); self.dimension=dimension
    def ensure_schema(self):
        with self.engine.begin() as c:
            c.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
            c.execute(text(f'''CREATE TABLE IF NOT EXISTS research_documents (id BIGSERIAL PRIMARY KEY,content TEXT NOT NULL,title TEXT,source TEXT,source_type TEXT,embedding vector({self.dimension}))'''))
    def similarity_search(self,embedding,top_k=5):
        with self.engine.begin() as c:
            rows=c.execute(text('SELECT content,title,source,source_type FROM research_documents ORDER BY embedding <=> CAST(:embedding AS vector) LIMIT :limit'),{'embedding':str(embedding),'limit':top_k}).mappings().all()
        return [dict(x) for x in rows]
