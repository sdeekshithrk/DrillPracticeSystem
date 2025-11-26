def evaluate_numeric_expression(student: str, expected: str):
    student = student.strip()
    expected = expected.strip()

    try:
        s_val = float(student)
        e_val = float(expected)

        if s_val == e_val:
            return {
                "correct": True,
                "feedback": "Correct numeric answer."
            }

        return {
            "correct": False,
            "feedback": f"Incorrect. Expected {expected}."
        }

    except:
        return {
            "correct": False,
            "feedback": "Invalid numeric format."
        }
