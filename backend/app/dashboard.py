from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.auth.dependencies import get_current_user
from app.models.models import User, Problem, UserProblemStatus
from app.utils import (
    determine_rank,
    get_progress_percentage,
    compute_streak,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


# --------------------------
# DB Session
# --------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------
# GET /dashboard/stats
# --------------------------
@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = current_user

    # ==============================================================
    # 1. XP, Rank, Progress
    # ==============================================================
    xp = user.xp
    rank = determine_rank(xp)
    progress = get_progress_percentage(xp)

    # ==============================================================
    # 2. Problems Solved Count
    # ==============================================================
    solved_count = (
        db.query(UserProblemStatus)
        .filter(
            UserProblemStatus.user_id == user.id,
            UserProblemStatus.status == "SOLVED",
        )
        .count()
    )

    # ==============================================================
    # 3. Topic-wise Statistics
    # ==============================================================
    problems = db.query(Problem).all()

    topic_map = {}
    for p in problems:
        topic = p.topic

        if topic not in topic_map:
            topic_map[topic] = {"solved": 0, "total": 0}

        topic_map[topic]["total"] += 1

        status_row = (
            db.query(UserProblemStatus)
            .filter(
                UserProblemStatus.user_id == user.id,
                UserProblemStatus.problem_id == p.id,
            )
            .first()
        )

        if status_row and status_row.status == "SOLVED":
            topic_map[topic]["solved"] += 1

    topic_stats = [
        {
            "topic": topic,
            "solved": data["solved"],
            "total": data["total"],
        }
        for topic, data in topic_map.items()
    ]

    # ==============================================================
    # 4. Streak Calculation
    # ==============================================================
    all_status_rows = (
        db.query(UserProblemStatus)
        .filter(UserProblemStatus.user_id == user.id)
        .order_by(UserProblemStatus.updated_at.asc())
        .all()
    )

    status_list = [row.status for row in all_status_rows]
    streak = compute_streak(status_list)

    # ==============================================================
    # FINAL RESPONSE
    # ==============================================================
    return {
        "xp": xp,
        "rank": rank,
        "progress_percentage": progress,
        "problems_solved": solved_count,
        "best_streak": streak,
        "topic_stats": topic_stats,
    }
