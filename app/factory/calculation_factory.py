from abc import ABC, abstractmethod
from app.models.calculation import OperationType

class Operation(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass

class AddOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b

class SubOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a - b

class MultiplyOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a * b

class DivideOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b

class CalculationFactory:
    _registry: dict = {
        OperationType.ADD: AddOperation,
        OperationType.SUB: SubOperation,
        OperationType.MULTIPLY: MultiplyOperation,
        OperationType.DIVIDE: DivideOperation,
    }

    @classmethod
    def get_operation(cls, op_type: OperationType) -> Operation:
        klass = cls._registry.get(op_type)
        if klass is None:
            raise ValueError(f"Unsupported operation type: {op_type}")
        return klass()

    @classmethod
    def compute(cls, op_type: OperationType, a: float, b: float) -> float:
        return cls.get_operation(op_type).execute(a, b)
