import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User
from app.models.calculation import Calculation, OperationType
from app.factory.calculation_factory import CalculationFactory

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost:5432/calcdb"
)

@pytest.fixture(scope="session")
def engine():
    eng = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=eng)
    yield eng
    Base.metadata.drop_all(bind=eng)

@pytest.fixture()
def db(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

def _insert_calc(db, a, b, op_type, user_id=None):
    result = CalculationFactory.compute(op_type, a, b)
    calc = Calculation(a=a, b=b, type=op_type, result=result, user_id=user_id)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc

class TestCalculationIntegration:
    def test_insert_add(self, db):
        calc = _insert_calc(db, 3, 4, OperationType.ADD)
        assert calc.id is not None and calc.result == 7.0

    def test_insert_sub(self, db):
        assert _insert_calc(db, 10, 3, OperationType.SUB).result == 7.0

    def test_insert_multiply(self, db):
        assert _insert_calc(db, 6, 7, OperationType.MULTIPLY).result == 42.0

    def test_insert_divide(self, db):
        assert _insert_calc(db, 20, 4, OperationType.DIVIDE).result == 5.0

    def test_db_stores_correct_operands(self, db):
        calc = _insert_calc(db, 11, 22, OperationType.ADD)
        fetched = db.query(Calculation).filter_by(id=calc.id).first()
        assert fetched.a == 11.0 and fetched.b == 22.0

    def test_divide_by_zero_blocked(self, db):
        with pytest.raises(ValueError, match="zero"):
            _insert_calc(db, 5, 0, OperationType.DIVIDE)

    def test_null_result_allowed(self, db):
        calc = Calculation(a=1, b=2, type=OperationType.ADD, result=None)
        db.add(calc)
        db.commit()
        db.refresh(calc)
        assert calc.result is None

    def test_compute_on_demand(self, db):
        calc = Calculation(a=9, b=3, type=OperationType.DIVIDE, result=None)
        db.add(calc)
        db.commit()
        db.refresh(calc)
        assert calc.compute() == 3.0

    def test_query_by_type(self, db):
        _insert_calc(db, 1, 1, OperationType.ADD)
        adds = db.query(Calculation).filter_by(type=OperationType.ADD).all()
        assert all(c.type == OperationType.ADD for c in adds)

    def test_invalid_type_raises_at_factory(self):
        with pytest.raises((ValueError, KeyError)):
            CalculationFactory.get_operation("Modulo")
