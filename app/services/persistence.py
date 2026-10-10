from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.database.models import ResearchExecution

def create_execution(db, conversation_id, user_id, question, request_id):
    row = ResearchExecution(conversation_id=conversation_id,user_id=user_id,question=question,request_id=request_id,status="running")
    db.add(row); db.commit(); db.refresh(row); return row

def update_execution(db: Session, conversation_id: str, **values):
    row = db.query(ResearchExecution).filter_by(conversation_id=conversation_id).order_by(ResearchExecution.created_at.desc()).first()
    if not row: return
    for k,v in values.items(): setattr(row,k,v)
    row.updated_at=datetime.now(timezone.utc); db.commit()

def get_execution(db, conversation_id):
    return db.query(ResearchExecution).filter_by(conversation_id=conversation_id).order_by(ResearchExecution.created_at.desc()).first()
