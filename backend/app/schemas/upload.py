from typing import Dict, List, Any, Optional
from pydantic import BaseModel

class ColumnMappingRequest(BaseModel):
    mapping: Dict[str, str] # e.g. {"Item_Code": "product_id", "Sale_Date": "date", ...}

class ValidationIssue(BaseModel):
    issue_type: str
    description: str
    count: int

class ValidationResultResponse(BaseModel):
    total_rows: int
    valid_rows: int
    duplicate_rows: int
    invalid_rows: int
    products_found: int
    date_range_start: Optional[str] = None
    date_range_end: Optional[str] = None
    issues: List[ValidationIssue] = []
    is_valid: bool = True
