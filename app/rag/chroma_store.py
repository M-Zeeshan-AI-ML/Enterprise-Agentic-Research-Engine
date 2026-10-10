from pathlib import Path
from app.config.settings import get_settings
from app.agents.llm import get_embeddings
class ChromaRAG:
    def __init__(self):
        s=get_settings(); self.dir=Path(s.chroma_dir); self.collection=s.rag_collection; self.store=None
    def _get(self):
        if self.store is None:
            from langchain_chroma import Chroma
            self.store=Chroma(collection_name=self.collection,persist_directory=str(self.dir),embedding_function=get_embeddings())
        return self.store
    def add_documents(self,items):
        from langchain_core.documents import Document
        docs=[Document(page_content=x["text"],metadata={"title":x.get("title","Untitled"),"source":x.get("source",""),"source_type":x.get("source_type","document")}) for x in items]
        if docs: self._get().add_documents(docs)
        return len(docs)
    def search(self,query,top_k=5):
        return [{"text":d.page_content,"title":d.metadata.get("title","Untitled"),"url":d.metadata.get("source",""),"source_type":d.metadata.get("source_type","document")} for d in self._get().similarity_search(query,k=top_k)]
