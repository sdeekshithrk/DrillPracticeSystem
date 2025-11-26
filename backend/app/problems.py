from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db import crud
from app.auth.dependencies import get_current_user
from app.models.models import User
from app.models.models import UserProblemStatus

router = APIRouter(prefix="/problems", tags=["problems"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.get_all_problems(db)


@router.get("/with-status")
def get_all_with_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns all problems with per-user status:
    UNATTEMPTED / ATTEMPTED / SOLVED
    """
    return crud.get_problems_with_status_for_user(db, current_user.id)



@router.get("/{problem_id}")
def get_one(
    problem_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    problem = crud.get_problem(db, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Fetch user-specific status
    status_row = crud.get_user_problem_status(
        db=db,
        user_id=current_user.id,
        problem_id=problem_id
    )

    # Prepare response
    return {
        "id": str(problem.id),
        "title": problem.title,
        "description": problem.description,
        "topic": problem.topic,
        "difficulty": problem.difficulty,
        "answer_type": problem.answer_type,
        "expected_ast": problem.expected_ast,
        "expected_value": problem.expected_value,

        "status": status_row.status if status_row else "UNATTEMPTED",
        "last_answer": status_row.last_answer if status_row else None,
        "last_correct_answer": status_row.last_correct_answer if status_row else None,
    }

