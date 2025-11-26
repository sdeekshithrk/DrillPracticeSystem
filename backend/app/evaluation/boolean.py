def normalize_bool(s: str):
    s = s.strip().lower()
    if s in ["yes", "y", "true", "t", "1"]:
        return True
    if s in ["no", "n", "false", "f", "0"]:
        return False
    return None


def evaluate_boolean_expression(student: str, expected: str):
    s_val = normalize_bool(student)
    e_val = normalize_bool(expected)

    if s_val is None:
        return {
            "correct": False,
            "feedback": "Invalid boolean response. Use Yes/No."
        }

    if s_val == e_val:
        return {
            "correct": True,
            "feedback": "Correct."
        }

    return {
        "correct": False,
        "feedback": f"Incorrect. Expected '{expected}'."
    }
