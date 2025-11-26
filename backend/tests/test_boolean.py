from app.evaluation.boolean import evaluate_boolean_expression


def test_boolean_yes():
    result = evaluate_boolean_expression("Yes", "yes")
    assert result["correct"] is True


def test_boolean_no():
    result = evaluate_boolean_expression("no", "no")
    assert result["correct"] is True


def test_boolean_wrong():
    result = evaluate_boolean_expression("yes", "no")
    assert result["correct"] is False
