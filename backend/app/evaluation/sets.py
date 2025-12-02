import re

TUPLE_PATTERN = re.compile(r"\(\s*([^,]+?)\s*,\s*([^,]+?)\s*\)")

def parse_element(token: str):
    token = token.strip()

    # Try number
    try:
        return int(token)
    except:
        pass

    # Try quoted string
    token = token.strip("'\"")
    return token


def normalize_set_string(s: str):
    """
    Parses a string like:
        "{(1, x), (2, y), a, 3}"
    into:
        { (1, 'x'), (2, 'y'), 'a', 3 }
    """

    s = s.strip()

    if not (s.startswith("{") and s.endswith("}")):
        raise ValueError("Set must be enclosed in { }")

    inside = s[1:-1].strip()

    result = set()

    idx = 0
    while idx < len(inside):
        if inside[idx] == "(":
            # Tuple detected
            match = TUPLE_PATTERN.match(inside, idx)
            if not match:
                raise ValueError("Invalid tuple syntax. Use (a, b).")

            left, right = match.groups()
            left = parse_element(left)
            right = parse_element(right)

            result.add((left, right))
            idx = match.end() + 1  # skip comma
        else:
            # Single element
            elem = []
            while idx < len(inside) and inside[idx] != ",":
                elem.append(inside[idx])
                idx += 1

            token = "".join(elem).strip()
            if token:
                result.add(parse_element(token))

            idx += 1  # skip comma

    return result


def evaluate_finite_set(student: str, expected: str):
    try:
        print("evaluate_finite_set")
        print(student)
        print(expected)
        s_set = normalize_set_string(student)
        e_set = normalize_set_string(expected)
        print(s_set)
        print(e_set)
    except Exception as e:
        return {
            "correct": False,
            "feedback": f"Invalid set format: {str(e)}. Use {{(a,b), c, d}} notation."
        }

    if s_set == e_set:
        print("comparing")
        return {
            "correct": True,
            "feedback": "Correct! Well done."
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
