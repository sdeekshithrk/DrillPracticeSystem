from sqlalchemy.orm import Session
from app.models.models import Problem, UserProblemStatus
from app.models.models import User, Problem
from app.utils import calculate_xp_gain

def get_all_problems(db: Session):
    return db.query(Problem).all()

def get_problem(db: Session, problem_id: str):
    return db.query(Problem).filter(Problem.id == problem_id).first()


# ---------- NEW: status helpers ----------

def get_user_problem_status(db: Session, user_id, problem_id):
    return (
        db.query(UserProblemStatus)
        .filter(
            UserProblemStatus.user_id == user_id,
            UserProblemStatus.problem_id == problem_id,
        )
        .first()
    )


def upsert_user_problem_status(
    db: Session,
    user_id,
    problem_id,
    student_answer: str,
    is_correct: bool,
):
    

    record = get_user_problem_status(db, user_id, problem_id)

    if record is None:
        record = UserProblemStatus(
            user_id=user_id,
            problem_id=problem_id,
        )
        db.add(record)

    record.last_answer = student_answer
    record.is_correct = is_correct

    # Fetch user + problem
    user = db.query(User).filter(User.id == user_id).first()
    problem = db.query(Problem).filter(Problem.id == problem_id).first()

    if is_correct:
        # Update status
        record.status = "SOLVED"
        record.last_correct_answer = student_answer

        # Add XP only once per problem
        if not getattr(record, "xp_awarded", False):
            gain = calculate_xp_gain(problem.difficulty)
            user.xp += gain
            record.xp_awarded = True  # prevents XP farming
    else:
        if record.status != "SOLVED":
            record.status = "ATTEMPTED"

    db.commit()
    db.refresh(record)
    return record


def get_problems_with_status_for_user(db: Session, user_id):
    problems = db.query(Problem).all()
    result = []

    for p in problems:
        status_row = (
            db.query(UserProblemStatus)
            .filter(
                UserProblemStatus.user_id == user_id,
                UserProblemStatus.problem_id == p.id,
            )
            .first()
        )

        status = status_row.status if status_row else "UNATTEMPTED"

        result.append(
            {
                "id": str(p.id),
                "title": p.title,
                "description": p.description,
                "topic": p.topic,
                "difficulty": p.difficulty,
                "answer_type": p.answer_type,
                "status": status,
            }
        )

    return result
