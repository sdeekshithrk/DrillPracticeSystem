from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db import crud
from app.types import AnswerType  # (you can remove if truly unused)

from app.evaluation.sets import evaluate_finite_set
from app.evaluation.logic_parser import parse_logic
from app.ast_models import LogicVar, LogicNot, LogicBinary
from app.evaluation.logic_ast_eval import evaluate_logic_ast
from app.evaluation.set_builder import evaluate_set_builder
from app.evaluation.numeric import evaluate_numeric_expression
from app.evaluation.boolean import evaluate_boolean_expression

from app.auth.dependencies import get_current_user  # NEW
from app.models.models import User  # for typing (optional)

router = APIRouter(prefix="/evaluate", tags=["evaluation"])


class EvalRequest(BaseModel):
    problem_id: str
    student_answer: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def load_logic_ast(json_obj):
    """
    Converts stored JSONB AST into the correct Pydantic model.
    """
    if not isinstance(json_obj, dict) or "type" not in json_obj:
        raise ValueError("Invalid AST JSON structure")

    t = json_obj["type"]

    if t == "VAR":
        return LogicVar.model_validate(json_obj)

    if t == "NOT":
        return LogicNot.model_validate(json_obj)

    if t in ["AND", "OR", "IMPLIES", "IFF"]:
        return LogicBinary.model_validate(json_obj)

    raise ValueError(f"Unknown AST node type: {t}")


@router.post("/")
def evaluate(
    req: EvalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Fetch problem from DB
    problem = crud.get_problem(db, req.problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    student = req.student_answer
    answer_type = problem.answer_type
    expected = problem.expected_value or problem.expected_ast

    result = None

    # 2. Dispatch by problem type
    if answer_type == "FINITE_SET":
        result = evaluate_finite_set(student, expected)

    elif answer_type == "LOGIC_EXPR":
        student_ast = parse_logic(student)      # convert input string → Logic AST
        expected_ast = load_logic_ast(expected) # JSONB stored AST → AST models
        result = evaluate_logic_ast(student_ast, expected_ast)

    elif answer_type == "SET_BUILDER":
        result = evaluate_set_builder(student, expected)

    elif answer_type == "NUMERIC":
        result = evaluate_numeric_expression(student, expected)

    elif answer_type == "BOOLEAN":
        result = evaluate_boolean_expression(student, expected)

    else:
        raise HTTPException(status_code=400, detail="Unsupported question type")

    # 3. Save user progress
    crud.upsert_user_problem_status(
        db=db,
        user_id=current_user.id,
        problem_id=problem.id,
        student_answer=student,
        is_correct=bool(result.get("correct")),
    )

    return result
