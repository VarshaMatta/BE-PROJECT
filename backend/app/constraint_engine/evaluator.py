import math
from typing import Dict, Any, List
from app.schemas.constraint import ConstraintInput, ConstraintEvaluationResponse, ConstraintCheckItem

class ConstraintEngine:
    """
    PriceWise Backend Constraint Engine.
    Enforces business rules on product pricing:
    1. Selling Price >= Cost Price
    2. Selling Price <= MRP
    3. Selling Price >= MRP * (1 - Max Discount %)
    4. Selling Price >= Cost Price / (1 - Min Margin %)
    """

    @staticmethod
    def evaluate(inputs: ConstraintInput) -> ConstraintEvaluationResponse:
        cost = inputs.cost_price
        mrp = inputs.mrp
        max_disc = inputs.max_discount_pct
        min_margin = inputs.min_margin_pct

        conflict_reasons: List[str] = []
        checks: List[ConstraintCheckItem] = []

        # 1. Base validation
        if cost <= 0:
            conflict_reasons.append("Cost price must be greater than 0.")
        if mrp <= 0:
            conflict_reasons.append("MRP must be greater than 0.")
        if cost > mrp:
            conflict_reasons.append(f"Cost price (₹{cost:.2f}) cannot exceed MRP (₹{mrp:.2f}).")

        # 2. Lower bound calculations
        # Bound A: Cost Price
        bound_cost = cost

        # Bound B: Max Discount Limit (P >= MRP * (1 - D_max/100))
        bound_disc = mrp * (1.0 - (max_disc / 100.0))

        # Bound C: Min Margin Limit (P >= Cost / (1 - M_min/100))
        if min_margin >= 100.0:
            conflict_reasons.append("Minimum margin percentage must be less than 100%.")
            bound_margin = float('inf')
        else:
            bound_margin = cost / (1.0 - (min_margin / 100.0))

        # Effective Lower Bound is the maximum of all lower bounds
        min_allowed_price = max(bound_cost, bound_disc, bound_margin)
        max_allowed_price = mrp

        # 3. Check items logic for visual checklist
        checks.append(ConstraintCheckItem(
            label="Above cost price",
            passed=min_allowed_price >= cost,
            detail=f"Minimum price (₹{min_allowed_price:.2f}) >= Cost (₹{cost:.2f})"
        ))

        checks.append(ConstraintCheckItem(
            label="Below MRP",
            passed=min_allowed_price <= mrp,
            detail=f"Minimum price (₹{min_allowed_price:.2f}) <= MRP (₹{mrp:.2f})"
        ))

        checks.append(ConstraintCheckItem(
            label="Discount limit respected",
            passed=(mrp - min_allowed_price) / mrp * 100.0 <= max_disc + 0.001 if mrp > 0 else False,
            detail=f"Effective discount at min price is {((mrp - min_allowed_price) / mrp * 100.0):.1f}% (Max: {max_disc:.1f}%)"
        ))

        margin_at_min = ((min_allowed_price - cost) / min_allowed_price * 100.0) if min_allowed_price > 0 else 0.0
        checks.append(ConstraintCheckItem(
            label="Margin requirement respected",
            passed=margin_at_min >= min_margin - 0.001,
            detail=f"Margin at min price is {margin_at_min:.1f}% (Min required: {min_margin:.1f}%)"
        ))

        # 4. Feasibility Check
        if min_allowed_price > max_allowed_price:
            if bound_margin > mrp:
                conflict_reasons.append(
                    f"Minimum required price for {min_margin}% margin is ₹{bound_margin:.2f}, which exceeds MRP of ₹{mrp:.2f}."
                )
            if bound_disc > mrp:
                conflict_reasons.append("Max discount calculation error.")
            
            return ConstraintEvaluationResponse(
                is_valid=False,
                min_allowed_price=round(min_allowed_price, 2),
                max_allowed_price=round(max_allowed_price, 2),
                status_title="NO VALID PRICE RANGE",
                status_description="Your selected constraints conflict. Please modify your constraints.",
                checks=checks,
                conflict_reasons=conflict_reasons
            )

        if conflict_reasons:
            return ConstraintEvaluationResponse(
                is_valid=False,
                min_allowed_price=None,
                max_allowed_price=None,
                status_title="NO VALID PRICE RANGE",
                status_description="Invalid constraint inputs detected.",
                checks=checks,
                conflict_reasons=conflict_reasons
            )

        return ConstraintEvaluationResponse(
            is_valid=True,
            min_allowed_price=round(min_allowed_price, 2),
            max_allowed_price=round(max_allowed_price, 2),
            status_title="VALID PRICE RANGE",
            status_description="Based on your constraints.",
            checks=checks,
            conflict_reasons=[]
        )
