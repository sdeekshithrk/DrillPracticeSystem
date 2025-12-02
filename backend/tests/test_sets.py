import pytest
from app.evaluation.sets import evaluate_finite_set


# -------------------------------------------------------------
# BASIC CORRECTNESS TESTS
# -------------------------------------------------------------

def test_correct_unordered_set():
    result = evaluate_finite_set("{1,2,3,4}", "{4,3,2,1}")
    assert result["correct"] is True


def test_correct_with_spaces():
    result = evaluate_finite_set("{ 1 ,  2 , 3 }", "{3,2,1}")
    assert result["correct"] is True


def test_correct_string_elements():
    result = evaluate_finite_set("{a, b, c}", "{c, b, a}")
    assert result["correct"] is True


def test_correct_mixed_types():
    result = evaluate_finite_set("{1, x, 2, y}", "{y,2,x,1}")
    assert result["correct"] is True


# -------------------------------------------------------------
# INCORRECT SET — MISSING ELEMENTS
# -------------------------------------------------------------

def test_missing_elements():
    result = evaluate_finite_set("{1,2}", "{1,2,3}")
    assert result["correct"] is False
    assert "Missing elements" in result["feedback"]


# -------------------------------------------------------------
# INCORRECT SET — EXTRA ELEMENTS
# -------------------------------------------------------------

def test_extra_elements():
    result = evaluate_finite_set("{1,2,3,4}", "{1,2,3}")
    assert result["correct"] is False
    assert "Extra elements" in result["feedback"]


# -------------------------------------------------------------
# DUPLICATE HANDLING
# -------------------------------------------------------------

def test_duplicate_elements_ignored():
    result = evaluate_finite_set("{1,1,1,2}", "{1,2}")
    assert result["correct"] is True


# -------------------------------------------------------------
# INVALID FORMAT TESTS
# -------------------------------------------------------------

def test_invalid_brackets_list_style():
    result = evaluate_finite_set("[1,2,3]", "{1,2,3}")
    assert result["correct"] is False
    assert "Invalid set format" in result["feedback"]


def test_invalid_semicolon_separators():
    result = evaluate_finite_set("{1;2;3}", "{1,2,3}")
    assert result["correct"] is False
    assert "Invalid set format" in result["feedback"] or "Missing elements" in result["feedback"]


def test_invalid_characters():
    result = evaluate_finite_set("{1,2,!!}", "{1,2}")
    assert result["correct"] is False


# -------------------------------------------------------------
# EMPTY SET TESTS
# -------------------------------------------------------------

def test_empty_set_correct():
    result = evaluate_finite_set("{}", "{}")
    assert result["correct"] is True


def test_empty_set_missing_elements():
    result = evaluate_finite_set("{}", "{1}")
    assert result["correct"] is False
    assert "Missing elements" in result["feedback"]


# -------------------------------------------------------------
# TUPLE ELEMENT TESTS
# -------------------------------------------------------------

def test_correct_tuple_elements():
    result = evaluate_finite_set("{(1,2), (3,4)}", "{(3,4), (1,2)}")
    assert result["correct"] is True


def test_incorrect_tuple_elements():
    result = evaluate_finite_set("{(1,2)}", "{(1,2), (3,4)}")
    assert result["correct"] is False
    assert "Missing elements" in result["feedback"]


def test_malformed_tuple_missing_comma():
    result = evaluate_finite_set("{(1 2)}", "{(1,2)}")
    assert result["correct"] is False


def test_malformed_tuple_wrong_format():
    result = evaluate_finite_set("{(1,2,3)}", "{(1,2)}")
    assert result["correct"] is False


def test_nested_tuple_error():
    result = evaluate_finite_set("{((1,2))}", "{(1,2)}")
    assert result["correct"] is False


# -------------------------------------------------------------
# COMPLETELY INVALID INPUT
# -------------------------------------------------------------

def test_completely_invalid_input():
    result = evaluate_finite_set("this is wrong", "{1,2,3}")
    assert result["correct"] is False
    assert "Invalid set format" in result["feedback"]
