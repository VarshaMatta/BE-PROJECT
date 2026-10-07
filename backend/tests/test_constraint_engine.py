import pytest
from app.schemas.constraint import ConstraintInput
from app.constraint_engine.evaluator import ConstraintEngine

def test_valid_price_range():
    # Cost = 52, MRP = 68, Max Disc = 15% (Min price disc = 68 * 0.85 = 57.80)
    # Min Margin = 10% (Min price margin = 52 / 0.9 = 57.77)
    # Effective range: 57.80 to 68.00
    inp = ConstraintInput(
        cost_price=52.0,
        mrp=68.0,
        max_discount_pct=15.0,
        min_margin_pct=10.0,
        available_stock=120
    )
    res = ConstraintEngine.evaluate(inp)
    assert res.is_valid is True
    assert res.min_allowed_price == 57.80
    assert res.max_allowed_price == 68.00
    assert res.status_title == "VALID PRICE RANGE"

def test_margin_conflict():
    # Cost = 60, MRP = 68, Min Margin = 20% -> P >= 60 / 0.8 = 75 (exceeds MRP 68)
    inp = ConstraintInput(
        cost_price=60.0,
        mrp=68.0,
        max_discount_pct=10.0,
        min_margin_pct=20.0,
        available_stock=50
    )
    res = ConstraintEngine.evaluate(inp)
    assert res.is_valid is False
    assert res.status_title == "NO VALID PRICE RANGE"
    assert any("exceeds MRP" in r for r in res.conflict_reasons)

def test_mrp_lower_than_cost():
    inp = ConstraintInput(
        cost_price=100.0,
        mrp=80.0,
        max_discount_pct=5.0,
        min_margin_pct=5.0,
        available_stock=10
    )
    res = ConstraintEngine.evaluate(inp)
    assert res.is_valid is False
    assert any("cannot exceed MRP" in r for r in res.conflict_reasons)

def test_boundary_values():
    # Cost = 50, MRP = 50, Max Disc = 0%, Min Margin = 0% -> P = 50
    inp = ConstraintInput(
        cost_price=50.0,
        mrp=50.0,
        max_discount_pct=0.0,
        min_margin_pct=0.0,
        available_stock=0
    )
    res = ConstraintEngine.evaluate(inp)
    assert res.is_valid is True
    assert res.min_allowed_price == 50.0
    assert res.max_allowed_price == 50.0
