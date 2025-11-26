import re

def clean(expr: str):
    expr = expr.strip().lower()

    replacements = {
        '∈': ' in ',
        'ℤ': ' z ',
        'ℕ': ' n ',
        '∧': ' and ',
        '∨': ' or ',
        '≥': '>=',
        '≤': '<=',
        '≠': '!=',
        '⇒': '->',
        '|': ' | ',
        '\\mid': '|',
    }
    for old, new in replacements.items():
        expr = expr.replace(old, new)

    expr = re.sub(r'\s+', ' ', expr)
    return expr


def extract_predicates(expr: str):
    preds = set()

    # Detect domain
    if "x in z" in expr:
        preds.add("domain_Z")
    if "x in n" in expr:
        preds.add("domain_N")

    # Even / odd
    if "even" in expr:
        preds.add("even")
    if "odd" in expr:
        preds.add("odd")

    # Inequalities (canonical form)
    inequalities = re.findall(r'(x\s*[<>]=?\s*\d+|\d+\s*[<>]=?\s*x)', expr)
    for i in inequalities:
        normalized = i.replace(" ", "")
        preds.add(normalized)

    return preds


def evaluate_set_builder(student: str, expected: str):
    s_clean = clean(student)
    e_clean = clean(expected)

    s_preds = extract_predicates(s_clean)
    e_preds = extract_predicates(e_clean)

    missing = e_preds - s_preds
    extra = s_preds - e_preds

    if not missing and not extra:
        return {"correct": True, "feedback": "Correct set-builder structure!"}

    fb = []
    if missing:
        fb.append(f"Missing conditions: {list(missing)}")
    if extra:
        fb.append(f"Extra conditions: {list(extra)}")

    return {"correct": False, "feedback": "; ".join(fb)}
