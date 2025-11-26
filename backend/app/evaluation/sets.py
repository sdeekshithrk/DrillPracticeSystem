def normalize_set_string(s: str):
    s = s.strip()

    if s.startswith("{") and s.endswith("}"):
        s = s[1:-1]

    parts = s.split(",")

    result = set()
    for part in parts:
        part = part.strip()
        if part == "":
            continue
        try:
            result.add(int(part))
        except:
            result.add(part)

    return result


def evaluate_finite_set(student: str, expected: str):
    try:
        s_set = normalize_set_string(student)
        e_set = normalize_set_string(expected)
    except:
        return {
            "correct": False,
            "feedback": "Invalid set format. Use {a,b,c} notation."
        }

    if s_set == e_set:
        return {
            "correct": True,
            "feedback": "Correct! Good job."
        }

    missing = e_set - s_set
    extra = s_set - e_set

    fb = []
    if missing:
        fb.append(f"Missing elements: {sorted(missing)}")
    if extra:
        fb.append(f"Extra elements: {sorted(extra)}")

    return {
        "correct": False,
        "feedback": "; ".join(fb)
    }
