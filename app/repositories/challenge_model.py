from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from config.dbcon import Base
from repositories.problem_model import Problem

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Add cascade delete for associated problems
    problems = relationship("Problem", back_populates="challenge", cascade="all, delete-orphan")
    participant_challenges = relationship("ParticipantChallenge", back_populates="challenge")