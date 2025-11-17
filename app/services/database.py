from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

DATABASE_URL = "sqlite:///./automation_agent.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TaskResult(Base):
    __tablename__ = "task_results"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    status = Column(String)
    category = Column(String, nullable=True)
    reasoning = Column(Text, nullable=True)
    action_taken = Column(String, nullable=True)
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_task_result(task_id: str, status: str, category: str = None, 
                     reasoning: str = None, action_taken: str = None, result: dict = None):
    db = SessionLocal()
    try:
        task = db.query(TaskResult).filter(TaskResult.task_id == task_id).first()
        if task:
            task.status = status
            task.category = category
            task.reasoning = reasoning
            task.action_taken = action_taken
            task.result = json.dumps(result) if result else None
            task.updated_at = datetime.utcnow()
        else:
            task = TaskResult(
                task_id=task_id,
                status=status,
                category=category,
                reasoning=reasoning,
                action_taken=action_taken,
                result=json.dumps(result) if result else None
            )
            db.add(task)
        db.commit()
        db.refresh(task)
        return task
    finally:
        db.close()

def get_task_result(task_id: str):
    db = SessionLocal()
    try:
        task = db.query(TaskResult).filter(TaskResult.task_id == task_id).first()
        if task and task.result:
            task_dict = {
                "id": task.id,
                "task_id": task.task_id,
                "status": task.status,
                "category": task.category,
                "reasoning": task.reasoning,
                "action_taken": task.action_taken,
                "result": json.loads(task.result),
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            return task_dict
        return None
    finally:
        db.close()