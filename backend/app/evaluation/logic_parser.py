# app/evaluation/logic_parser.py

from app.ast_models import LogicVar, LogicNot, LogicBinary, LogicNode


# ------------------------------------------
# TOKENIZER (NO SYMBOLS — ENGLISH ONLY)
# ------------------------------------------

def tokenize(expr: str):
    expr = expr.upper()

    # Ensure parentheses spaced
    expr = expr.replace("(", " ( ").replace(")", " ) ")

    return expr.split()


# ------------------------------------------
# PARSER (Operator Precedence)
# ------------------------------------------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def eat(self, tok=None):
        curr = self.peek()
        if tok and curr != tok:
            raise ValueError(f"Expected {tok}, got {curr}")
        self.i += 1
        return curr

    def parse(self):
        return self.parse_iff()

    def parse_iff(self):
        node = self.parse_implies()
        while self.peek() == "IFF":
            self.eat("IFF")
            right = self.parse_implies()
            node = LogicBinary(type="IFF", left=node, right=right)
        return node

    def parse_implies(self):
        node = self.parse_or()
        while self.peek() == "IMPLIES":
            self.eat("IMPLIES")
            right = self.parse_or()
            node = LogicBinary(type="IMPLIES", left=node, right=right)
        return node

    def parse_or(self):
        node = self.parse_and()
        while self.peek() == "OR":
            self.eat("OR")
            right = self.parse_and()
            node = LogicBinary(type="OR", left=node, right=right)
        return node

    def parse_and(self):
        node = self.parse_not()
        while self.peek() == "AND":
            self.eat("AND")
            right = self.parse_not()
            node = LogicBinary(type="AND", left=node, right=right)
        return node

    def parse_not(self):
        if self.peek() == "NOT":
            self.eat("NOT")
            return LogicNot(type="NOT", child=self.parse_not())
        return self.parse_atom()

    def parse_atom(self):
        tok = self.peek()

        if tok is None:
            raise ValueError("Unexpected end of input")

        if tok.isalpha():   # variable
            self.eat()
            return LogicVar(type="VAR", name=tok)

        if tok == "(":
            self.eat("(")
            node = self.parse_iff()
            self.eat(")")
            return node

        raise ValueError(f"Unexpected token: {tok}")


# ------------------------------------------
# PUBLIC API
# ------------------------------------------

def parse_logic(expr: str) -> LogicNode:
    tokens = tokenize(expr)
    parser = Parser(tokens)
    return parser.parse()
