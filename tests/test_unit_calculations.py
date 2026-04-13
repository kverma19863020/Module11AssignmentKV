import pytest
from pydantic import ValidationError
from app.models.calculation import OperationType
from app.schemas.calculation import CalculationCreate, CalculationRead
from app.factory.calculation_factory import (
    CalculationFactory, AddOperation, SubOperation,
    MultiplyOperation, DivideOperation,
)

class TestCalculationFactory:
    def test_get_add_operation(self):
        assert isinstance(CalculationFactory.get_operation(OperationType.ADD), AddOperation)

    def test_get_sub_operation(self):
        assert isinstance(CalculationFactory.get_operation(OperationType.SUB), SubOperation)

    def test_get_multiply_operation(self):
        assert isinstance(CalculationFactory.get_operation(OperationType.MULTIPLY), MultiplyOperation)

    def test_get_divide_operation(self):
        assert isinstance(CalculationFactory.get_operation(OperationType.DIVIDE), DivideOperation)

    def test_add(self):
        assert CalculationFactory.compute(OperationType.ADD, 3, 4) == 7

    def test_sub(self):
        assert CalculationFactory.compute(OperationType.SUB, 10, 3) == 7

    def test_multiply(self):
        assert CalculationFactory.compute(OperationType.MULTIPLY, 3, 4) == 12

    def test_divide(self):
        assert CalculationFactory.compute(OperationType.DIVIDE, 12, 4) == 3.0

    def test_divide_by_zero_raises(self):
        with pytest.raises(ValueError, match="zero"):
            CalculationFactory.compute(OperationType.DIVIDE, 5, 0)

    def test_add_negative_numbers(self):
        assert CalculationFactory.compute(OperationType.ADD, -3, -4) == -7

    def test_multiply_by_zero(self):
        assert CalculationFactory.compute(OperationType.MULTIPLY, 100, 0) == 0

    def test_sub_float(self):
        assert abs(CalculationFactory.compute(OperationType.SUB, 1.5, 0.5) - 1.0) < 1e-9

class TestCalculationCreateSchema:
    def test_valid_add(self):
        schema = CalculationCreate(a=1, b=2, type="Add")
        assert schema.type == OperationType.ADD

    def test_valid_divide(self):
        schema = CalculationCreate(a=10, b=2, type="Divide")
        assert schema.type == OperationType.DIVIDE

    def test_invalid_type_string(self):
        with pytest.raises(ValidationError):
            CalculationCreate(a=1, b=2, type="Modulo")

    def test_divide_by_zero_rejected(self):
        with pytest.raises(ValidationError, match="zero"):
            CalculationCreate(a=5, b=0, type="Divide")

    def test_missing_a_raises(self):
        with pytest.raises(ValidationError):
            CalculationCreate(b=2, type="Add")

    def test_optional_user_id_defaults_none(self):
        schema = CalculationCreate(a=1, b=2, type="Add")
        assert schema.user_id is None

class TestCalculationReadSchema:
    def test_serializes_correctly(self):
        data = {"id": 1, "a": 3.0, "b": 4.0, "type": "Add", "result": 7.0}
        schema = CalculationRead(**data)
        assert schema.result == 7.0

    def test_result_optional(self):
        data = {"id": 2, "a": 3.0, "b": 4.0, "type": "Sub"}
        schema = CalculationRead(**data)
        assert schema.result is None
