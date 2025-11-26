CREATE TABLE problems (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    title TEXT NOT NULL,
    description TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    topic TEXT NOT NULL,

    answer_type TEXT NOT NULL CHECK (
        answer_type IN (
            'LOGIC_EXPR',
            'SET_BUILDER',
            'FINITE_SET',
            'NUMERIC',
            'BOOLEAN'
        )
    ),

    expected_ast JSONB,    -- For logic + set-builder
    expected_value JSONB,  -- For numeric, boolean, finite-set

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  first_name VARCHAR NOT NULL,
  last_name VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_problem_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    problem_id UUID REFERENCES problems(id) ON DELETE CASCADE,
    status VARCHAR NOT NULL DEFAULT 'UNATTEMPTED',
    last_answer TEXT,
    last_correct_answer TEXT,
    is_correct BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMPTZ DEFAULT now()
);


