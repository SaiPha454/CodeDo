from sqlalchemy import Column, Integer, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.dbcon import Base
import enum

class SubmissionStatus(enum.Enum):
    Pass = "Pass"
    Fail = "Fail"

class UserSubmission(Base):
    __tablename__ = "participant_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=True)
    code = Column(Text, nullable=False)
    status = Column(Enum(SubmissionStatus), nullable=False)
    total_test_cases = Column(Integer, nullable=False)
    passed_test_cases = Column(Integer, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")
    challenge = relationship("Challenge", back_populates="submissions")