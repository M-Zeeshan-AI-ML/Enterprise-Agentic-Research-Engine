from urllib.parse import urlparse
from langchain_core.tools import StructuredTool
from pydantic import BaseModel,Field
from app.config.settings import get_settings
class SearchInput(BaseModel): query:str=Field(min_length=3,max_length=500); max_results:int=Field(default=5,ge=1,le=10)
def allowed(url):
    host=(urlparse(url).hostname or "").lower(); return any(host==d or host.endswith("."+d) for d in get_settings().search_domains)
def web_search(query,max_results=5):
    from duckduckgo_search import DDGS
    out=[]
    with DDGS() as ddgs:
        for item in ddgs.text(query,max_results=max_results):
            url=item.get("href") or item.get("url")
            if url and allowed(url): out.append({"title":item.get("title",""),"url":url,"snippet":item.get("body","") ,"source_type":"web"})
    return out
web_search_tool=StructuredTool.from_function(func=web_search,name="web_search",description="Search approved public web domains",args_schema=SearchInput)
