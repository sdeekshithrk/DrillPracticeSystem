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

