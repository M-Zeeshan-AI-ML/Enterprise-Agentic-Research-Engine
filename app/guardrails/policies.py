import re
from pydantic import BaseModel,Field
from app.config.settings import get_settings
INJECTION_PATTERNS=[r"ignore\s+(all|any|previous|prior)\s+instructions",r"system\s+prompt",r"reveal\s+(your|the)\s+(prompt|instructions)",r"developer\s+message",r"jailbreak",r"disable\s+(the\s+)?guardrails"]
UNSUPPORTED_PATTERNS=[r"execute\s+arbitrary\s+python",r"run\s+shell\s+command",r"steal\s+(credentials|passwords|tokens)"]
class GuardrailResult(BaseModel): allowed:bool; reasons:list[str]=Field(default_factory=list)
class OutputGuardrailResult(BaseModel): grounded:bool; has_citations:bool; safe:bool; reasons:list[str]=Field(default_factory=list)
def validate_input(question):
    reasons=[]; q=question.strip(); s=get_settings()
    if len(q)>s.max_query_length: reasons.append("Question exceeds configured length limit")
    if any(re.search(p,q,re.I) for p in INJECTION_PATTERNS): reasons.append("Potential prompt-injection instruction detected")
    if any(re.search(p,q,re.I) for p in UNSUPPORTED_PATTERNS): reasons.append("Unsupported or unsafe execution request detected")
    return GuardrailResult(allowed=not reasons,reasons=reasons)
def validate_tool_name(name,allowed):
    if name not in allowed: raise ValueError(f"Unauthorized tool: {name}")
def validate_final_output(answer,citations,findings):
    reasons=[]; has_citations=bool(citations) and any(c.get("url") for c in citations); grounded=bool(findings)
    if not has_citations: reasons.append("Final answer has no usable citations")
    if not grounded: reasons.append("No source-backed findings were produced")
    safe=re.search(r"(api[_ -]?key|password|secret|private[_ -]?key)\s*[:=]\s*\S+",answer,re.I) is None
    if not safe: reasons.append("Potential secret disclosure detected")
    return OutputGuardrailResult(grounded=grounded,has_citations=has_citations,safe=safe,reasons=reasons)
