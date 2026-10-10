from typing import Literal
from pydantic import BaseModel, Field, ConfigDict
class ResearchRequest(BaseModel):
    question: str = Field(min_length=10,max_length=4000)
    top_k: int = Field(default=5,ge=1,le=10)
class Citation(BaseModel):
    title: str; url: str; source_type: Literal["web","document"]
class ResearchResponse(BaseModel):
    model_config=ConfigDict(extra="forbid")
    conversation_id: str; status: str; answer: str|None=None; citations:list[Citation]=[]; verification_status:str|None=None; tools_used:list[str]=[]; errors:list[str]=[]
class ApprovalRequest(BaseModel):
    conversation_id: str = Field(min_length=1,max_length=255); approved: bool
class TokenResponse(BaseModel): access_token:str; token_type:str="bearer"
class ExecutionStatus(BaseModel):
    conversation_id:str; status:str; answer:str|None=None; citations:list[Citation]=[]; verification_status:str|None=None; errors:list[str]=[]
