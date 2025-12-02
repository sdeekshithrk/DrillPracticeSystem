# app/utils.py

# ==========================================================
#  XP SYSTEM
# ==========================================================

XP_REWARD = {
    "Easy": 10,
    "Medium": 20,
    "Hard": 40,
}

def calculate_xp_gain(difficulty: str) -> int:
    """
    Return XP awarded for a problem based on difficulty.
    """
    return XP_REWARD.get(difficulty.capitalize(), 10)


# ==========================================================
#  RANK SYSTEM
# ==========================================================

# XP thresholds for ranks (lower bound of XP)
RANK_THRESHOLDS = [
    ("Beginner", 0),
    ("Learner", 50),
    ("Intermediate", 150),
    ("Advanced", 350),
    ("Professional", 600),
    ("Master", 1000),
]

RANK_ORDER = [r[0] for r in RANK_THRESHOLDS]  # list of rank names


def determine_rank(xp: int) -> str:
    """
    Determine the user's rank from total XP.
    """
    current_rank = "Beginner"

    for rank_name, threshold in RANK_THRESHOLDS:
        if xp >= threshold:
            current_rank = rank_name
    
    return current_rank


def get_rank_threshold(rank: str) -> int:
    """
    Return the XP threshold for the given rank.
    """
    for r, threshold in RANK_THRESHOLDS:
        if r == rank:
            return threshold
    return 0


def next_rank(rank: str) -> str | None:
    """
    Returns the next rank after the current rank.
    If at highest rank, returns None.
    """
    if rank not in RANK_ORDER or rank == "Master":
        return None

    idx = RANK_ORDER.index(rank)
    return RANK_ORDER[idx + 1]


# ==========================================================
#  PROGRESS CALCULATION
# ==========================================================

def get_progress_percentage(xp: int) -> float:
    """
    Percentage progress toward the next rank.
    If Master, returns 100%.
    """
    rank = determine_rank(xp)
    nr = next_rank(rank)

    if nr is None:
        return 100.0  # Master rank capped

    lower = get_rank_threshold(rank)
    upper = get_rank_threshold(nr)

    pct = 100 * (xp - lower) / (upper - lower)
    return round(max(0, min(pct, 100)), 2)


# ==========================================================
#  STREAK SYSTEM (simple version)
# ===========================================================
# You can extend this later (e.g., based on timestamps)
# For now we compute the streak based on consecutive SOLVED entries.

def compute_streak(status_records: list) -> int:
    """
    Compute streak as consecutive 'SOLVED' problems from the latest attempts.
    Input: list of status strings in order (e.g., from DB)
    """
    streak = 0
    for status in reversed(status_records):
        if status == "SOLVED":
            streak += 1
        else:
            break
    return streak
