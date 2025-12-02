import uuid

from sqlalchemy import Column, String, Text, JSON, Enum, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import text, func
from app.db.database import Base
from app.types import AnswerType
from sqlalchemy.orm import relationship


# ==========================================
# PROBLEMS TABLE
# ==========================================
class Problem(Base):
    __tablename__ = "problems"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String, nullable=False)
    topic = Column(String, nullable=False)

    answer_type = Column(String, nullable=False)

    expected_ast = Column(JSONB, nullable=True)
    expected_value = Column(JSONB, nullable=True)
    user_status = relationship("UserProblemStatus", back_populates="problem")


# ==========================================
# USERS TABLE
# ==========================================
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    xp = Column(Integer, default=0)   
    rank = Column(String, default="Beginner")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    progress = relationship("UserProblemStatus", back_populates="user")


class UserProblemStatus(Base):
    __tablename__ = "user_problem_status"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    problem_id = Column(
        UUID(as_uuid=True), ForeignKey("problems.id", ondelete="CASCADE"), nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="UNATTEMPTED"  # Allowed: UNATTEMPTED, ATTEMPTED, SOLVED
    )

    last_answer = Column(Text, nullable=True)
    last_correct_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, default=False)

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    xp_awarded = Column(Boolean, default=False)

    # Relationships
    user = relationship("User")
    problem = relationship("Problem")
