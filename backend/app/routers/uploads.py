import json
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.shop import Shop
from app.schemas.upload import ColumnMappingRequest, ValidationResultResponse
from app.services.csv_service import CSVService
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/shops/{shop_id}/uploads", tags=["CSV Uploads & Validation"])

def check_shop_access(shop_id: int, current_user: User, db: Session) -> Shop:
    shop = db.query(Shop).filter(Shop.shop_id == shop_id, Shop.user_id == current_user.user_id).first()
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found or access denied.")
    return shop

@router.post("/preview")
async def preview_csv_upload(
    shop_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_shop_access(shop_id, current_user, db)
    contents = await file.read()
    try:
        res = CSVService.preview_csv(contents, file.filename)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate", response_model=ValidationResultResponse)
async def validate_csv_mapping(
    shop_id: int,
    file: UploadFile = File(...),
    mapping_str: str = Form(...), # JSON string of mapping
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_shop_access(shop_id, current_user, db)
    contents = await file.read()
    try:
        mapping = json.loads(mapping_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid mapping JSON string.")

    try:
        _, summary = CSVService.validate_and_clean(contents, mapping)
        return summary
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/process")
async def process_and_save_csv(
    shop_id: int,
    file: UploadFile = File(...),
    mapping_str: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shop = check_shop_access(shop_id, current_user, db)
    contents = await file.read()
    try:
        mapping = json.loads(mapping_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid mapping JSON string.")

    try:
        cleaned_df, summary = CSVService.validate_and_clean(contents, mapping)
        upload = CSVService.process_and_save(db, shop_id, file.filename, cleaned_df, summary)
        return {
            "message": "CSV data cleaned and imported successfully.",
            "upload_id": upload.upload_id,
            "summary": summary
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
