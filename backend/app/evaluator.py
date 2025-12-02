from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db import crud
from app.types import AnswerType

from app.evaluation.sets import evaluate_finite_set
from app.evaluation.logic_parser import parse_logic
from app.evaluation.logic_ast_eval import evaluate_logic_ast
from app.evaluation.set_builder import evaluate_set_builder
from app.evaluation.numeric import evaluate_numeric_expression
from app.evaluation.boolean import evaluate_boolean_expression

from app.ast_models import LogicVar, LogicNot, LogicBinary

from app.auth.dependencies import get_current_user
from app.models.models import User

from app.ai.feedback import generate_feedback
from app.utils import calculate_xp_gain, determine_rank

router = APIRouter(prefix="/evaluate", tags=["evaluation"])


# -----------------------------
# Request Model
# -----------------------------
class EvalRequest(BaseModel):
    problem_id: str
    student_answer: str


# -----------------------------
# DB Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# AST Loader (from JSONB)
# -----------------------------
def load_logic_ast(json_obj):
    """Convert JSON stored AST into pydantic AST model."""
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


# -----------------------------
# MAIN EVALUATION ENDPOINT
# -----------------------------
@router.post("/")
async def evaluate(
    req: EvalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Fetch the problem
    problem = crud.get_problem(db, req.problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    student = req.student_answer.strip()
    answer_type = problem.answer_type
    expected = problem.expected_value or problem.expected_ast

    result = None

    # -----------------------------------------------------
    # 2. Evaluate by problem type
    # -----------------------------------------------------
    try:
        print(answer_type)
        if answer_type == "FINITE_SET":
            print("entered")
            result = evaluate_finite_set(student, expected)

        elif answer_type == "LOGIC_EXPR":
            student_ast = parse_logic(student)
            expected_ast = load_logic_ast(expected)
            result = evaluate_logic_ast(student_ast, expected_ast)

        elif answer_type == "SET_BUILDER":
            result = evaluate_set_builder(student, expected)

        elif answer_type == "NUMERIC":
            result = evaluate_numeric_expression(student, expected)

        elif answer_type == "BOOLEAN":
            result = evaluate_boolean_expression(student, expected)

        else:
            raise HTTPException(400, "Unsupported question type")

    except Exception as e:
        # If parsing fails or student enters invalid syntax
        return {
            "correct": False,
            "feedback": f"Your expression could not be parsed. Error: {str(e)}"
        }

    # Extract correctness
    is_correct = bool(result.get("correct"))

    # -----------------------------------------------------
    # 3. Save user's attempt in progress table
    # -----------------------------------------------------
    status_row = crud.upsert_user_problem_status(
        db=db,
        user_id=current_user.id,
        problem_id=problem.id,
        student_answer=student,
        is_correct=is_correct,
    )

    # -----------------------------------------------------
    # 4. Handle XP / Rank update ONLY IF FIRST TIME SOLVED
    # -----------------------------------------------------
    existing_status = status_row.status  # After update

    if is_correct:

        # If first time solving correctly → award XP
        if existing_status == "SOLVED" and status_row.last_correct_answer == student:
            gained = calculate_xp_gain(problem.difficulty)
            current_user.xp += gained
            current_user.rank = determine_rank(current_user.xp)
            db.commit()

            return {
                "correct": True,
                "feedback": f"Great job! You solved it correctly. (+{gained} XP)",
                "xp": current_user.xp,
                "rank": current_user.rank,
            }

        # If user already solved earlier → no XP
        return {
            "correct": True,
            "feedback": "Correct! You already solved this problem earlier — no XP gained.",
            "xp": current_user.xp,
            "rank": current_user.rank,
        }

    # -----------------------------------------------------
    # 5. Incorrect → Generate AI feedback
    # -----------------------------------------------------
    ai_feedback = await generate_feedback(
        answer_type=answer_type,
        problem_text=problem.description,
        expected=str(expected),
        student=student
    )

    return {
        "correct": False,
        "feedback": ai_feedback,
        "xp": current_user.xp,
        "rank": current_user.rank,
    }
