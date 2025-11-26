from app.evaluation.set_builder import evaluate_set_builder


def test_set_builder_equivalent():
    result = evaluate_set_builder(
        "{ x ∈ ℤ | x even ∧ x > 10 ∧ x ≤ 20 }",
        "{ x ∈ ℤ | 10 < x ≤ 20 ∧ x even }"
    )
    assert result["correct"] is True


def test_set_builder_missing_condition():
    result = evaluate_set_builder(
        "{ x ∈ ℤ | x > 10 }",
        "{ x ∈ ℤ | 10 < x ≤ 20 ∧ x even }"
    )
    assert result["correct"] is False
    assert "Missing conditions" in result["feedback"]
