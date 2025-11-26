from app.evaluation.sets import evaluate_finite_set


def test_correct_set():
    result = evaluate_finite_set("{1,2,3,4}", "{4,3,2,1}")
    assert result["correct"] is True


def test_missing_elements():
    result = evaluate_finite_set("{1,2}", "{1,2,3}")
    assert result["correct"] is False
    assert "Missing elements" in result["feedback"]


def test_extra_elements():
    result = evaluate_finite_set("{1,2,3,4}", "{1,2,3}")
    assert result["correct"] is False
    assert "Extra elements" in result["feedback"]
