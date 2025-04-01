from sqlalchemy import Column, Integer, Text, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from config.dbcon import Base

class TestCase(Base):
    __tablename__ = "test_cases"
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    id = Column(Integer, nullable=False)
    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)

    problem = relationship("Problem", back_populates="test_cases")

    __table_args__ = (
        PrimaryKeyConstraint("problem_id", "id"),
    )