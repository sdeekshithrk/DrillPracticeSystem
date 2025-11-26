from itertools import product
from typing import Dict, List
from app.ast_models import LogicNode, LogicVar, LogicNot, LogicBinary


# Evaluate a logic AST node with a variable assignment
def eval_logic(node: LogicNode, env: Dict[str, bool]) -> bool:
    if node.type == "VAR":
        return env[node.name]

    if node.type == "NOT":
        return not eval_logic(node.child, env)

    if node.type == "AND":
        return eval_logic(node.left, env) and eval_logic(node.right, env)

    if node.type == "OR":
        return eval_logic(node.left, env) or eval_logic(node.right, env)

    if node.type == "IMPLIES":
        left = eval_logic(node.left, env)
        right = eval_logic(node.right, env)
        return (not left) or right

    if node.type == "IFF":
        left = eval_logic(node.left, env)
        right = eval_logic(node.right, env)
        return left == right

    raise ValueError(f"Unknown logic node type: {node.type}")


# Extract variables recursively
def extract_vars(node: LogicNode) -> List[str]:
    if node.type == "VAR":
        return [node.name]

    if node.type == "NOT":
        return extract_vars(node.child)

    if node.type in ["AND", "OR", "IMPLIES", "IFF"]:
        return list(set(extract_vars(node.left) + extract_vars(node.right)))

    return []


# Main equivalence evaluator
def evaluate_logic_ast(student: LogicNode, expected: LogicNode):
    vars_list = sorted(set(extract_vars(student) + extract_vars(expected)))

    # Truth table comparison
    for values in product([False, True], repeat=len(vars_list)):
        env = dict(zip(vars_list, values))

        s_val = eval_logic(student, env)
        e_val = eval_logic(expected, env)

        if s_val != e_val:
            return {
                "correct": False,
                "feedback": f"Not equivalent for assignment {env}"
            }

    return {
        "correct": True,
        "feedback": "Correct (logically equivalent)."
    }
