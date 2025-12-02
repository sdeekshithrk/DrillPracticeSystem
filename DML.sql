INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_ast)
VALUES (
  'Negate Implication',
  'Negate the proposition: P → Q.',
  'Easy',
  'Logic',
  'LOGIC_EXPR',
  '{
     "type":"AND",
     "left":{"type":"VAR","name":"P"},
     "right":{"type":"NOT","child":{"type":"VAR","name":"Q"}}
   }'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_ast)
VALUES (
  'Simplify Negation',
  'Simplify the expression ¬(¬P ∨ Q).',
  'Medium',
  'Logic',
  'LOGIC_EXPR',
  '{
     "type":"AND",
     "left":{"type":"VAR","name":"P"},
     "right":{"type":"NOT","child":{"type":"VAR","name":"Q"}}
   }'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_ast)
VALUES (
  'Remove Implication',
  'Rewrite P → (Q ∧ R) using only ¬, ∧, ∨.',
  'Medium',
  'Logic',
  'LOGIC_EXPR',
  '{
    "type":"OR",
    "left":{"type":"NOT","child":{"type":"VAR","name":"P"}},
    "right":{
      "type":"AND",
      "left":{"type":"VAR","name":"Q"},
      "right":{"type":"VAR","name":"R"}
    }
  }'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_ast)
VALUES (
  'Contrapositive',
  'Write the contrapositive of P → Q.',
  'Easy',
  'Logic',
  'LOGIC_EXPR',
  '{
     "type":"IMPLIES",
     "left":{"type":"NOT","child":{"type":"VAR","name":"Q"}},
     "right":{"type":"NOT","child":{"type":"VAR","name":"P"}}
   }'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_ast)
VALUES (
  'Negate Conjunction',
  'Negate the proposition P ∧ Q.',
  'Easy',
  'Logic',
  'LOGIC_EXPR',
  '{
     "type":"OR",
     "left":{"type":"NOT","child":{"type":"VAR","name":"P"}},
     "right":{"type":"NOT","child":{"type":"VAR","name":"Q"}}
   }'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_ast)
VALUES (
  'Rewrite Biconditional',
  'Rewrite the biconditional P ↔ Q using only implication.',
  'Medium',
  'Logic',
  'LOGIC_EXPR',
  '{
     "type":"AND",
     "left":{
       "type":"IMPLIES",
       "left":{"type":"VAR","name":"P"},
       "right":{"type":"VAR","name":"Q"}
     },
     "right":{
       "type":"IMPLIES",
       "left":{"type":"VAR","name":"Q"},
       "right":{"type":"VAR","name":"P"}
     }
   }'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_ast)
VALUES (
  'XOR Expression',
  'Write the XOR of P and Q using AND, OR, and NOT.',
  'Medium',
  'Logic',
  'LOGIC_EXPR',
  '{
     "type":"OR",
     "left":{
       "type":"AND",
       "left":{"type":"VAR","name":"P"},
       "right":{"type":"NOT","child":{"type":"VAR","name":"Q"}}
     },
     "right":{
       "type":"AND",
       "left":{"type":"NOT","child":{"type":"VAR","name":"P"}},
       "right":{"type":"VAR","name":"Q"}
     }
   }'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_ast)
VALUES (
  'CNF Conversion',
  'Convert ¬(P ∨ Q) ∨ R into CNF.',
  'Hard',
  'Logic',
  'LOGIC_EXPR',
  '{
     "type":"AND",
     "left":{
       "type":"OR",
       "left":{"type":"NOT","child":{"type":"VAR","name":"P"}},
       "right":{"type":"VAR","name":"R"}
     },
     "right":{
       "type":"OR",
       "left":{"type":"NOT","child":{"type":"VAR","name":"Q"}},
       "right":{"type":"VAR","name":"R"}
     }
   }'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Symmetric Difference',
  'Compute A △ B for A={1,2,3,4} and B={3,4,5,6}.',
  'Hard',
  'Set Theory',
  'FINITE_SET',
  '{1,2,5,6}'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Intersection Count',
  'Let A={1,2,3,4,5} and B={2,4,6,8}. What is |A ∩ B|?',
  'Hard',
  'Set Theory',
  'NUMERIC',
  '2'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_ast)
VALUES (
  'Apply De Morgan’s Law',
  'Rewrite ¬(P ∧ Q) using De Morgan’s law.',
  'Easy',
  'Logic',
  'LOGIC_EXPR',
  '{
     "type":"OR",
     "left":{"type":"NOT","child":{"type":"VAR","name":"P"}},
     "right":{"type":"NOT","child":{"type":"VAR","name":"Q"}}
   }'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_ast)
VALUES (
  'OR Distribution',
  'Rewrite P ∨ (Q ∧ R) using distribution.',
  'Medium',
  'Logic',
  'LOGIC_EXPR',
  '{
    "type":"AND",
    "left":{
      "type":"OR",
      "left":{"type":"VAR","name":"P"},
      "right":{"type":"VAR","name":"Q"}
    },
    "right":{
      "type":"OR",
      "left":{"type":"VAR","name":"P"},
      "right":{"type":"VAR","name":"R"}
    }
  }'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_ast)
VALUES (
  'Remove Biconditional',
  'Rewrite P ↔ (Q ∧ R) using implications.',
  'Hard',
  'Logic',
  'LOGIC_EXPR',
  '{
    "type":"AND",
    "left":{
      "type":"IMPLIES",
      "left":{"type":"VAR","name":"P"},
      "right":{
        "type":"AND",
        "left":{"type":"VAR","name":"Q"},
        "right":{"type":"VAR","name":"R"}
      }
    },
    "right":{
      "type":"IMPLIES",
      "left":{
        "type":"AND",
        "left":{"type":"VAR","name":"Q"},
        "right":{"type":"VAR","name":"R"}
      },
      "right":{"type":"VAR","name":"P"}
    }
  }'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_ast)
VALUES (
  'Negate Nested Expression',
  'Negate the expression ¬(P → (Q ∨ R)).',
  'Medium',
  'Logic',
  'LOGIC_EXPR',
  '{
     "type":"AND",
     "left":{"type":"VAR","name":"P"},
     "right":{
       "type":"AND",
       "left":{"type":"NOT","child":{"type":"VAR","name":"Q"}},
       "right":{"type":"NOT","child":{"type":"VAR","name":"R"}}
     }
   }'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_ast)
VALUES (
  'Expand Implication',
  'Rewrite (P → Q) → R using only ¬, ∧, ∨.',
  'Hard',
  'Logic',
  'LOGIC_EXPR',
  '{
    "type":"OR",
    "left":{
      "type":"AND",
      "left":{"type":"VAR","name":"P"},
      "right":{"type":"NOT","child":{"type":"VAR","name":"Q"}}
    },
    "right":{"type":"VAR","name":"R"}
  }'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Set Difference',
  'Compute A - B for A={1,2,3,4,5} and B={2,5}.',
  'Easy',
  'Set Theory',
  'FINITE_SET',
  '{1,3,4}'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Union of Sets',
  'Compute A ∪ B for A={a,b,c} and B={b,c,d}.',
  'Easy',
  'Set Theory',
  'FINITE_SET',
  '{a,b,c,d}'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Intersection',
  'Compute A ∩ B for A={2,4,6,8} and B={1,2,3,4,5}.',
  'Easy',
  'Set Theory',
  'FINITE_SET',
  '{2,4}'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Cartesian Product Small',
  'Compute A × B for A={1,2} and B={x,y}.',
  'Medium',
  'Set Theory',
  'FINITE_SET',
  '{(1,x),(1,y),(2,x),(2,y)}'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Three-Set Difference',
  'Compute A - (B ∪ C) for A={1,2,3,4}, B={2}, C={3,5}.',
  'Medium',
  'Set Theory',
  'FINITE_SET',
  '{1,4}'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Set Complement',
  'Given U={1,2,3,4,5,6} and A={2,4,6}, compute Aᶜ.',
  'Medium',
  'Set Theory',
  'FINITE_SET',
  '{1,3,5}'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Large Cartesian Product',
  'Compute |A × B| for A={1,2,3} and B={a,b,c,d}. (Numeric answer)',
  'Hard',
  'Set Theory',
  'NUMERIC',
  '12'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Union Cardinality',
  'Let A={1,2,3,4} and B={3,4,5}. Compute |A ∪ B|.',
  'Easy',
  'Set Theory',
  'NUMERIC',
  '5'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Set Difference Size',
  'Let A={1,2,3,4,5} and B={2,5}. Compute |A - B|.',
  'Easy',
  'Set Theory',
  'NUMERIC',
  '3'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Truth Table Rows',
  'How many rows does a truth table for 4 variables have?',
  'Easy',
  'Logic',
  'NUMERIC',
  '16'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Power Set Cardinality',
  'What is |P(A)| if |A| = 6?',
  'Medium',
  'Logic',
  'NUMERIC',
  '64'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Boolean Functions Count',
  'How many Boolean functions exist on 3 variables?',
  'Hard',
  'Logic',
  'NUMERIC',
  '256'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Union Cardinality Formula',
  'Given |A|=10, |B|=15 and |A ∩ B|=5, compute |A ∪ B|.',
  'Medium',
  'Set Theory',
  'NUMERIC',
  '20'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Cartesian Count',
  'Let |A|=5 and |B|=7. Compute |A × B|.',
  'Medium',
  'Set Theory',
  'NUMERIC',
  '35'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Hard Power Set Question',
  'If |A|=8, what is |P(P(A))|?',
  'Hard',
  'Logic',
  'NUMERIC',
  '65536'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Triple Cartesian Product',
  'Let |A|=2, |B|=3, and |C|=4. Compute |A × B × C|.',
  'Medium',
  'Set Theory',
  'NUMERIC',
  '24'
);

INSERT INTO problems (title, description, difficulty, topic, answer_type, expected_value)
VALUES (
  'Size of Complex Set Expression',
  'Let A={1,2,3,4,5}, B={3,4}, C={4,5,6}. Compute |(A-B) ∪ (B ∩ C)|.',
  'Hard',
  'Set Theory',
  'NUMERIC',
  '4'
);
