from sqlalchemy.orm import Session
from app.models.models import Problem, UserProblemStatus

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

    # Update status fields
    record.last_answer = student_answer
    record.is_correct = is_correct

    if is_correct:
        record.status = "SOLVED"
        record.last_correct_answer = student_answer
    else:
        # Only mark as ATTEMPTED if not already SOLVED
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
