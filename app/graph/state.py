from typing import Any,TypedDict
class AgentState(TypedDict,total=False):
    user_query:str; conversation_id:str; research_plan:dict[str,Any]; selected_tools:list[str]
    retrieved_documents:list[dict]; tool_results:list[dict]; intermediate_findings:list[dict]
    verification_results:list[dict]; final_answer:str; citations:list[dict]; errors:list[str]
    execution_metadata:dict[str,Any]; approval_required:bool; approval_reason:str; approved:bool; verification_status:str
