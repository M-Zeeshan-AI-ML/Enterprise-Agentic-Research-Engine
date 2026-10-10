from langchain_core.tools import StructuredTool
from pydantic import BaseModel,Field
from app.rag.chroma_store import ChromaRAG
class RetrievalInput(BaseModel): query:str=Field(min_length=3,max_length=1000); top_k:int=Field(default=5,ge=1,le=10)
_rag=ChromaRAG()
def retrieve_documents(query,top_k=5): return _rag.search(query,top_k)
retrieval_tool=StructuredTool.from_function(func=retrieve_documents,name="document_retrieval",description="Semantic search over indexed local documents",args_schema=RetrievalInput)
