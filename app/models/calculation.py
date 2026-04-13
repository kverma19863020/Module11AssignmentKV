from sqlalchemy import Column, Integer, Float, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class OperationType(str, enum.Enum):
    ADD = "Add"
    SUB = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"

class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(SAEnum(OperationType), nullable=False)
    result = Column(Float, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="calculations")

    def compute(self) -> float:
        if self.type == OperationType.ADD:
            return self.a + self.b
        elif self.type == OperationType.SUB:
            return self.a - self.b
        elif self.type == OperationType.MULTIPLY:
            return self.a * self.b
        elif self.type == OperationType.DIVIDE:
            if self.b == 0:
                raise ValueError("Division by zero is not allowed.")
            return self.a / self.b
        raise ValueError(f"Unknown operation type: {self.type}")
