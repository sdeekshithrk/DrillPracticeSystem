from app.ast_models import LogicVar, LogicNot, LogicBinary
from app.evaluation.logic_ast_eval import evaluate_logic_ast


def build_expr_P_and_not_Q():
    return LogicBinary(
        type="AND",
        left=LogicVar(type="VAR", name="P"),
        right=LogicNot(
            type="NOT",
            child=LogicVar(type="VAR", name="Q")
        )
    )


def build_expr_not_notP_or_Q():
    return LogicNot(
        type="NOT",
        child=LogicBinary(
            type="OR",
            left=LogicNot(
                type="NOT",
                child=LogicVar(type="VAR", name="P")
            ),
            right=LogicVar(type="VAR", name="Q")
        )
    )


def test_equivalent_expressions_ast():
    expr1 = build_expr_P_and_not_Q()
    expr2 = build_expr_not_notP_or_Q()

    result = evaluate_logic_ast(expr1, expr2)
    assert result["correct"] is True


def test_non_equivalent_expressions_ast():
    expr1 = LogicBinary(
        type="AND",
        left=LogicVar(type="VAR", name="P"),
        right=LogicVar(type="VAR", name="Q")
    )

    expr2 = LogicBinary(
        type="OR",
        left=LogicVar(type="VAR", name="P"),
        right=LogicVar(type="VAR", name="Q")
    )

    result = evaluate_logic_ast(expr1, expr2)
    assert result["correct"] is False

def test_equiv_P_and_not_Q():
    expr1 = LogicBinary(
        type="AND",
        left=LogicVar(type="VAR", name="P"),
        right=LogicNot(type="NOT", child=LogicVar(type="VAR", name="Q"))
    )

    expr2 = LogicNot(
        type="NOT",
        child=LogicBinary(
            type="OR",
            left=LogicNot(type="NOT", child=LogicVar(type="VAR", name="P")),
            right=LogicVar(type="VAR", name="Q")
        )
    )

    assert evaluate_logic_ast(expr1, expr2)["correct"] is True

# (P OR Q) == (Q OR P) (commutativity)
def test_or_commutativity():
    expr1 = LogicBinary(
        type="OR",
        left=LogicVar(type="VAR", name="P"),
        right=LogicVar(type="VAR", name="Q")
    )
    expr2 = LogicBinary(
        type="OR",
        left=LogicVar(type="VAR", name="Q"),
        right=LogicVar(type="VAR", name="P")
    )
    assert evaluate_logic_ast(expr1, expr2)["correct"] is True

# NOT(NOT(P)) == P (double negation)
def test_double_negation():
    expr1 = LogicNot(
        type="NOT",
        child=LogicNot(type="NOT", child=LogicVar(type="VAR", name="P"))
    )
    expr2 = LogicVar(type="VAR", name="P")
    assert evaluate_logic_ast(expr1, expr2)["correct"] is True


#P AND Q != P OR Q
def test_P_and_Q_vs_P_or_Q():
    expr1 = LogicBinary(
        type="AND",
        left=LogicVar(type="VAR", name="P"),
        right=LogicVar(type="VAR", name="Q")
    )
    expr2 = LogicBinary(
        type="OR",
        left=LogicVar(type="VAR", name="P"),
        right=LogicVar(type="VAR", name="Q")
    )
    assert evaluate_logic_ast(expr1, expr2)["correct"] is False

#(P -> Q) == (NOT P OR Q)
def test_implication_identity():
    expr1 = LogicBinary(
        type="IMPLIES",
        left=LogicVar(type="VAR", name="P"),
        right=LogicVar(type="VAR", name="Q")
    )
    expr2 = LogicBinary(
        type="OR",
        left=LogicNot(type="NOT", child=LogicVar(type="VAR", name="P")),
        right=LogicVar(type="VAR", name="Q")
    )
    assert evaluate_logic_ast(expr1, expr2)["correct"] is True

# (P ↔ Q) == (P->Q AND Q->P)   
def test_biconditional_identity():
    expr1 = LogicBinary(
        type="IFF",
        left=LogicVar(type="VAR", name="P"),
        right=LogicVar(type="VAR", name="Q")
    )
    expr2 = LogicBinary(
        type="AND",
        left=LogicBinary(
            type="IMPLIES",
            left=LogicVar(type="VAR", name="P"),
            right=LogicVar(type="VAR", name="Q")
        ),
        right=LogicBinary(
            type="IMPLIES",
            left=LogicVar(type="VAR", name="Q"),
            right=LogicVar(type="VAR", name="P")
        )
    )
    assert evaluate_logic_ast(expr1, expr2)["correct"] is True

#(P AND (Q AND R)) == ((P AND Q) AND R)
def test_and_associativity():
    expr1 = LogicBinary(
        type="AND",
        left=LogicVar(type="VAR", name="P"),
        right=LogicBinary(
            type="AND",
            left=LogicVar(type="VAR", name="Q"),
            right=LogicVar(type="VAR", name="R")
        )
    )

    expr2 = LogicBinary(
        type="AND",
        left=LogicBinary(
            type="AND",
            left=LogicVar(type="VAR", name="P"),
            right=LogicVar(type="VAR", name="Q")
        ),
        right=LogicVar(type="VAR", name="R")
    )

    assert evaluate_logic_ast(expr1, expr2)["correct"] is True

#NOT(P AND Q) == (NOT P OR NOT Q)
def test_de_morgan_1():
    expr1 = LogicNot(
        type="NOT",
        child=LogicBinary(
            type="AND",
            left=LogicVar(type="VAR", name="P"),
            right=LogicVar(type="VAR", name="Q")
        )
    )

    expr2 = LogicBinary(
        type="OR",
        left=LogicNot(type="NOT", child=LogicVar(type="VAR", name="P")),
        right=LogicNot(type="NOT", child=LogicVar(type="VAR", name="Q"))
    )

    assert evaluate_logic_ast(expr1, expr2)["correct"] is True

#2: NOT(P OR Q) == (NOT P AND NOT Q)
def test_de_morgan_2():
    expr1 = LogicNot(
        type="NOT",
        child=LogicBinary(
            type="OR",
            left=LogicVar(type="VAR", name="P"),
            right=LogicVar(type="VAR", name="Q")
        )
    )

    expr2 = LogicBinary(
        type="AND",
        left=LogicNot(type="NOT", child=LogicVar(type="VAR", name="P")),
        right=LogicNot(type="NOT", child=LogicVar(type="VAR", name="Q"))
    )

    assert evaluate_logic_ast(expr1, expr2)["correct"] is True

# (P AND (Q OR R)) == ((P AND Q) OR (P AND R)) (distributive law)
def test_distributive_law():
    expr1 = LogicBinary(
        type="AND",
        left=LogicVar(type="VAR", name="P"),
        right=LogicBinary(
            type="OR",
            left=LogicVar(type="VAR", name="Q"),
            right=LogicVar(type="VAR", name="R")
        )
    )

    expr2 = LogicBinary(
        type="OR",
        left=LogicBinary(
            type="AND",
            left=LogicVar(type="VAR", name="P"),
            right=LogicVar(type="VAR", name="Q")
        ),
        right=LogicBinary(
            type="AND",
            left=LogicVar(type="VAR", name="P"),
            right=LogicVar(type="VAR", name="R")
        )
    )

    assert evaluate_logic_ast(expr1, expr2)["correct"] is True
