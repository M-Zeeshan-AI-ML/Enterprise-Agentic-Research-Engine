import uuid
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,Request
from fastapi.security import OAuth2PasswordRequestForm
from langgraph.types import Command
from app.api.deps import current_user
from app.database.session import SessionLocal
from app.models.schemas import *
from app.services.auth import authenticate,create_access_token
from app.services.persistence import *
from app.services.rate_limit import limiter
router=APIRouter()
@router.post("/auth/token",response_model=TokenResponse)
def token(form:Annotated[OAuth2PasswordRequestForm,Depends()]):
    if not authenticate(form.username,form.password): raise HTTPException(401,"Incorrect username or password")
    return TokenResponse(access_token=create_access_token(form.username))
@router.post("/research",response_model=ResearchResponse)
@limiter.limit("30/minute")
def research(payload:ResearchRequest,request:Request,user:str=Depends(current_user)):
    cid=str(uuid.uuid4()); rid=request.headers.get("X-Request-ID",str(uuid.uuid4())); db=SessionLocal()
    try:
        create_execution(db,cid,user,payload.question,rid); graph=request.app.state.graph; cfg={"configurable":{"thread_id":cid}}
        result=graph.invoke({"user_query":payload.question,"conversation_id":cid},config=cfg)
        if "__interrupt__" in result:
            update_execution(db,cid,status="awaiting_approval"); return ResearchResponse(conversation_id=cid,status="awaiting_approval",errors=[str(result["__interrupt__"][0].value)])
        status="completed" if not result.get("errors") else "guardrail_blocked"
        update_execution(db,cid,status=status,result={"answer":result.get("final_answer"),"citations":result.get("citations",[]),"verification_status":result.get("verification_status"),"tools_used":result.get("selected_tools",[]),"errors":result.get("errors",[])},tool_calls=len(result.get("tool_results",[])))
        return ResearchResponse(conversation_id=cid,status=status,answer=result.get("final_answer"),citations=result.get("citations",[]),verification_status=result.get("verification_status"),tools_used=result.get("selected_tools",[]),errors=result.get("errors",[]))
    except Exception as exc:
        update_execution(db,cid,status="failed",error=str(exc)); raise HTTPException(500,"Research execution failed") from exc
    finally: db.close()
@router.post("/approval",response_model=ResearchResponse)
def approval(payload:ApprovalRequest,request:Request,user:str=Depends(current_user)):
    db=SessionLocal()
    try:
        row=get_execution(db,payload.conversation_id)
        if not row: raise HTTPException(404,"Conversation not found")
        if row.user_id!=user: raise HTTPException(403,"Not authorized")
        result=request.app.state.graph.invoke(Command(resume={"approved":payload.approved}),config={"configurable":{"thread_id":payload.conversation_id}})
        if "__interrupt__" in result: return ResearchResponse(conversation_id=payload.conversation_id,status="awaiting_approval")
        status="completed" if not result.get("errors") else "guardrail_blocked"
        update_execution(db,payload.conversation_id,status=status,result={"answer":result.get("final_answer"),"citations":result.get("citations",[]),"verification_status":result.get("verification_status"),"tools_used":result.get("selected_tools",[]),"errors":result.get("errors",[])})
        return ResearchResponse(conversation_id=payload.conversation_id,status=status,answer=result.get("final_answer"),citations=result.get("citations",[]),verification_status=result.get("verification_status"),tools_used=result.get("selected_tools",[]),errors=result.get("errors",[]))
    finally: db.close()
@router.get("/research/{conversation_id}",response_model=ExecutionStatus)
def status(conversation_id:str,user:str=Depends(current_user)):
    db=SessionLocal()
    try:
        row=get_execution(db,conversation_id)
        if not row: raise HTTPException(404,"Conversation not found")
        if row.user_id!=user: raise HTTPException(403,"Not authorized")
        r=row.result or {}; return ExecutionStatus(conversation_id=row.conversation_id,status=row.status,answer=r.get("answer"),citations=r.get("citations",[]),verification_status=r.get("verification_status"),errors=r.get("errors",[]))
    finally: db.close()
