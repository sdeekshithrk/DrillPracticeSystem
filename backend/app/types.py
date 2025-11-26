from enum import Enum

class AnswerType(str, Enum):
    FINITE_SET = "FINITE_SET"
    LOGIC_EXPR = "LOGIC_EXPR"
    SET_BUILDER = "SET_BUILDER"
    NUMERIC = "NUMERIC"
    BOOLEAN = "BOOLEAN"
    STRUCTURED = "STRUCTURED"
