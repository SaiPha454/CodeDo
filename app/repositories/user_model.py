from sqlalchemy import Column, Integer, String, Enum
import enum
from config.dbcon import Base
from sqlalchemy.orm import relationship
# from repositories.participant_challenge_model import ParticipantChallenge

class UserRole(enum.Enum):
    participant = "participant"
    questioner = "questioner"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    participant_challenges = relationship("ParticipantChallenge", back_populates="participant")
    submissions = relationship("UserSubmission", back_populates="user")
