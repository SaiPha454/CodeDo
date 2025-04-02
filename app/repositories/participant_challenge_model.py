from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.dbcon import Base
from repositories.user_model import User
from repositories.challenge_model import Challenge

class ParticipantChallenge(Base):
    __tablename__ = "participant_challenges"

    participant_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)
    challenge_id = Column(Integer, ForeignKey(Challenge.id), nullable=False, primary_key=True)
    join_date = Column(DateTime(timezone=True), server_default=func.now())

    participant = relationship("User", back_populates="participant_challenges")
    challenge = relationship("Challenge", back_populates="participant_challenges")
