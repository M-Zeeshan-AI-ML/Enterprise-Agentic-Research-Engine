import json
from langchain_core.messages import HumanMessage,SystemMessage
from langgraph.types import interrupt
from app.agents.llm import get_llm
from app.config.settings import get_settings
from app.guardrails.policies import validate_input,validate_tool_name,validate_final_output
from app.tools.registry import ALLOWED_TOOLS,TOOL_MAP

def input_validation_node(s):
    r=validate_input(s["user_query"]); return {"errors":r.reasons}
def route_after_validation(s): return "planner" if not s.get("errors") else "guardrail"
def planner_node(s):
    llm=get_llm(); prompt="""Plan this research question. Return JSON only with objective, sub_questions (2-5), requires_web, requires_documents, requires_calculation, verification_needed. Do not answer and do not invent sources."""
    r=llm.invoke([SystemMessage(content=prompt),HumanMessage(content=s["user_query"])])
    try: plan=json.loads(r.content)
    except Exception: plan={"objective":s["user_query"],"sub_questions":[s["user_query"]],"requires_web":True,"requires_documents":True,"requires_calculation":False,"verification_needed":True}
    return {"research_plan":plan}
def tool_selection_node(s):
    p=s.get("research_plan",{}); selected=["document_retrieval"]
    if p.get("requires_web"): selected.append("web_search")
    if p.get("requires_calculation"): selected.append("calculator")
    if p.get("verification_needed"): selected.append("source_verification")
    for x in selected: validate_tool_name(x,ALLOWED_TOOLS)
    return {"selected_tools":selected,"approval_required":"web_search" in selected,"approval_reason":"External web research requires human approval in this portfolio implementation."}
def route_after_tool_selection(s): return "approval" if s.get("approval_required") and s.get("approved") is not True else "research"
def approval_node(s):
    d=interrupt({"type":"research_approval","conversation_id":s["conversation_id"],"reason":s.get("approval_reason"),"selected_tools":s.get("selected_tools",[])})
    return {"approved":bool(d.get("approved",False))}
def route_after_approval(s):
    return "research" if s.get("approved") else "guardrail"
def research_node(s):
    results=[]
    for name in s.get("selected_tools",[]):
        if name=="source_verification": continue
        try:
            if name=="web_search": result=TOOL_MAP[name].invoke({"query":s["user_query"],"max_results":get_settings().search_max_results})
            elif name=="document_retrieval": result=TOOL_MAP[name].invoke({"query":s["user_query"],"top_k":get_settings().rag_top_k})
            elif name=="calculator": result=TOOL_MAP[name].invoke({"expression":"1+1"})
            else: continue
            results.append({"tool":name,"result":result})
        except Exception as exc: results.append({"tool":name,"error":str(exc)})
    docs=next((x["result"] for x in results if x["tool"]=="document_retrieval" and isinstance(x.get("result"),list)),[])
    return {"tool_results":results,"retrieved_documents":docs}
def analysis_node(s):
    llm=get_llm(); material=json.dumps(s.get("tool_results",[]),ensure_ascii=False)[:18000]
    prompt="""Use only supplied research material. Return JSON with findings=[{claim,support,source_url}] and draft_answer. Do not invent citations. Explicitly state when evidence is insufficient."""
    r=llm.invoke([SystemMessage(content=prompt),HumanMessage(content=f"Question: {s['user_query']}\nMaterial:\n{material}")])
    try: p=json.loads(r.content)
    except Exception: p={"findings":[],"draft_answer":r.content}
    return {"intermediate_findings":p.get("findings",[]),"final_answer":p.get("draft_answer","")}
def verification_node(s):
    out=[]; citations=[]; seen=set(); verifier=TOOL_MAP["source_verification"]
    for f in s.get("intermediate_findings",[])[:5]:
        url=f.get("source_url"); claim=f.get("claim")
        if not url or not claim: continue
        try: out.append(verifier.invoke({"url":url,"claim":claim}))
        except Exception as exc: out.append({"url":url,"supported":False,"error":str(exc)})
        if url not in seen: citations.append({"title":f.get("claim","Source"),"url":url,"source_type":"web"}); seen.add(url)
    supported=sum(1 for x in out if x.get("supported")); status="verified" if out and supported==len(out) else ("partially_verified" if supported else "not_verified")
    return {"verification_results":out,"verification_status":status,"citations":citations}
def guardrail_node(s):
    r=validate_final_output(s.get("final_answer",""),s.get("citations",[]),s.get("intermediate_findings",[]))
    return {"errors":list(s.get("errors",[]))+r.reasons}
def final_response_node(s): return s
