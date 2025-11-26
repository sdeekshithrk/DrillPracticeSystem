from app.evaluation.numeric import evaluate_numeric_expression


def test_numeric_correct():
    result = evaluate_numeric_expression("10", "10")
    assert result["correct"] is True


def test_numeric_incorrect():
    result = evaluate_numeric_expression("5", "10")
    assert result["correct"] is False
