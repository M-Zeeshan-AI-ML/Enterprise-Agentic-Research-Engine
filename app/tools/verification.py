import httpx
from bs4 import BeautifulSoup
from langchain_core.tools import StructuredTool
from pydantic import BaseModel,Field
from app.tools.search import allowed
class VerificationInput(BaseModel): url:str=Field(min_length=10,max_length=2000); claim:str=Field(min_length=3,max_length=1000)
def verify_source(url,claim):
    if not allowed(url): return {"url":url,"claim":claim,"supported":False,"checked":False,"error":"URL is outside the approved source allow-list"}
    try:
        r=httpx.get(url,timeout=8,follow_redirects=True,headers={"User-Agent":"EnterpriseResearchAgent/1.0"}); r.raise_for_status()
        text=" ".join(BeautifulSoup(r.text,"html.parser").stripped_strings).lower(); words=[w for w in claim.lower().split() if len(w)>3][:12]
        ratio=sum(w in text for w in words)/max(len(words),1)
        return {"url":url,"claim":claim,"supported":ratio>=.35,"overlap_ratio":round(ratio,3),"checked":True}
    except Exception as exc: return {"url":url,"claim":claim,"supported":False,"checked":False,"error":str(exc)}
verification_tool=StructuredTool.from_function(func=verify_source,name="source_verification",description="Fetch a source URL and heuristically check textual support for a claim",args_schema=VerificationInput)
