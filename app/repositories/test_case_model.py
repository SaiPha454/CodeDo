from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from config.dbcon import Base

class TestCase(Base):
    __tablename__ = "test_cases"

    problem_id = Column(Integer, ForeignKey("problems.id"), primary_key=True)
    id = Column(Integer, primary_key=True)
    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)

    # Define the relationship back to Problem
    problem = relationship("Problem", back_populates="test_cases")