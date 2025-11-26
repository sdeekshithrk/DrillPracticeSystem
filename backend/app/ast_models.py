from pydantic import BaseModel
from typing import List, Optional, Literal, Union


# ==========================================
# LOGIC AST MODELS
# ==========================================

class LogicVar(BaseModel):
    type: Literal["VAR"]
    name: str


class LogicNot(BaseModel):
    type: Literal["NOT"]
    child: "LogicNode"


class LogicBinary(BaseModel):
    type: Literal["AND", "OR", "IMPLIES", "IFF"]
    left: "LogicNode"
    right: "LogicNode"


LogicNode = Union[LogicVar, LogicNot, LogicBinary]
LogicNot.update_forward_refs()
LogicBinary.update_forward_refs()


# ==========================================
# SET BUILDER AST MODELS
# ==========================================

class SBConstant(BaseModel):
    kind: Literal["CONST"]
    value: int


class SBVar(BaseModel):
    kind: Literal["VAR"]
    name: str


class SBInequality(BaseModel):
    kind: Literal["INEQUALITY"]
    left: Union[SBVar, SBConstant]
    op: Literal["<", "<=", ">", ">=", "=="]
    right: Union[SBVar, SBConstant]


class SBParity(BaseModel):
    kind: Literal["PARITY"]
    var: str
    value: Literal["EVEN", "ODD"]


class SetBuilderAST(BaseModel):
    type: Literal["SET_BUILDER"]
    var: str
    domain: Literal["Z", "N"]
    constraints: List[Union[SBInequality, SBParity]]


# ==========================================
# FINITE SET AST
# ==========================================
class FiniteSetAST(BaseModel):
    type: Literal["FINITE_SET"]
    elements: List[int]


# ==========================================
# BOOLEAN / NUMERIC
# ==========================================
class BooleanAST(BaseModel):
    type: Literal["BOOLEAN"]
    value: bool


class NumericAST(BaseModel):
    type: Literal["NUMERIC"]
    value: float
