from pydantic import BaseModel
from typing import Optional
from .types import AnswerType

class ProblemBase(BaseModel):
    title: str
    topic: str
    difficulty: str
    content: str
    answer_type: AnswerType
    expected_answer: str
    alternate_answers: Optional[str] = None

class ProblemCreate(ProblemBase):
    pass

class ProblemRead(ProblemBase):
    id: int

    class Config:
        from_attributes = True
