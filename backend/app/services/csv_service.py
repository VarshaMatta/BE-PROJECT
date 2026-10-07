import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Tuple
from sqlalchemy.orm import Session
from app.models.upload import CSVUpload
from app.models.product import Product
from app.models.sales import SalesRecord
from app.models.constraint import ProductConstraint
from app.services.product_analysis_service import ProductAnalysisService

class CSVService:
    REQUIRED_FIELDS = ["product_id", "date", "quantity_sold", "selling_price"]
    
    @staticmethod
    def preview_csv(file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """
        Reads raw CSV, extracts headers and first 5 preview rows.
        """
        if not filename.lower().endswith(".csv"):
            raise ValueError("Unsupported file type. Please upload a .csv file.")
        
        if len(file_bytes) > 50 * 1024 * 1024:
            raise ValueError("File size exceeds maximum limit of 50 MB.")

        try:
            df = pd.read_csv(pd.io.common.BytesIO(file_bytes), nrows=10)
        except Exception as e:
            raise ValueError(f"Failed to parse CSV file: {str(e)}")
        
        if df.empty:
            raise ValueError("The uploaded CSV file is empty.")

        columns = list(df.columns)
        # Suggest auto-mapping based on column name heuristics
        suggested_mapping = {}
        for col in columns:
            col_clean = str(col).strip().lower().replace("_", "").replace(" ", "")
            if col_clean in ["productid", "itemcode", "sku", "productcode", "itemid", "code"]:
                suggested_mapping[col] = "product_id"
            elif col_clean in ["date", "saledate", "txndate", "transactiondate", "time"]:
                suggested_mapping[col] = "date"
            elif col_clean in ["quantity", "quantitysold", "units", "qty", "unitssold", "volume"]:
                suggested_mapping[col] = "quantity_sold"
            elif col_clean in ["price", "sellingprice", "rate", "unitprice", "amount"]:
                suggested_mapping[col] = "selling_price"
            elif col_clean in ["category", "dept", "department", "group"]:
                suggested_mapping[col] = "category"
            elif col_clean in ["promo", "promotion", "discountflag", "offer"]:
                suggested_mapping[col] = "promotion"

        preview_data = df.head(5).to_dict(orient="records")
        return {
            "filename": filename,
            "total_columns": len(columns),
            "columns": columns,
            "suggested_mapping": suggested_mapping,
            "preview": preview_data
        }

    @staticmethod
    def validate_and_clean(file_bytes: bytes, mapping: Dict[str, str]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Applies mapping, validates data types and ranges, identifies duplicates, 
        cleans dataset, and returns cleaned DataFrame and detailed metrics.
        """
        # Ensure all required target fields are mapped
        mapped_targets = list(mapping.values())
        for req in CSVService.REQUIRED_FIELDS:
            if req not in mapped_targets:
                raise ValueError(f"Required field '{req}' is not mapped to any column.")

        df = pd.read_csv(pd.io.common.BytesIO(file_bytes))
        total_rows = len(df)

        if total_rows == 0:
            raise ValueError("CSV contains 0 rows of data.")

        # Invert mapping: source_column -> target_field
        target_to_source = {v: k for k, v in mapping.items() if v != "ignore"}
        
        # Rename columns according to mapping
        rename_dict = {source: target for target, source in target_to_source.items()}
        df = df.rename(columns=rename_dict)
        
        # Keep only mapped columns
        df = df[[c for c in CSVService.REQUIRED_FIELDS + ["category", "promotion"] if c in df.columns]]

        # Set defaults for optional columns
        if "category" not in df.columns:
            df["category"] = "General"
        else:
            df["category"] = df["category"].fillna("General").astype(str)

        if "promotion" not in df.columns:
            df["promotion"] = "None"
        else:
            df["promotion"] = df["promotion"].fillna("None").astype(str)

        issues = []

        # Check missing selling price / invalid selling price
        missing_price_count = df["selling_price"].isna().sum()
        df["selling_price"] = pd.to_numeric(df["selling_price"], errors="coerce")
        invalid_price_count = (df["selling_price"] <= 0).sum() + df["selling_price"].isna().sum() - missing_price_count
        
        if missing_price_count > 0:
            issues.append({"issue_type": "Missing Selling Price", "description": "rows contain missing selling price", "count": int(missing_price_count)})
        if invalid_price_count > 0:
            issues.append({"issue_type": "Invalid Selling Price", "description": "rows contain selling price <= 0", "count": int(invalid_price_count)})

        # Check quantity sold
        missing_qty_count = df["quantity_sold"].isna().sum()
        df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce")
        invalid_qty_count = (df["quantity_sold"] < 0).sum() + df["quantity_sold"].isna().sum() - missing_qty_count
        
        if missing_qty_count > 0 or invalid_qty_count > 0:
            issues.append({"issue_type": "Invalid Quantity", "description": "rows contain invalid or negative quantities", "count": int(missing_qty_count + invalid_qty_count)})

        # Parse date
        df["parsed_date"] = pd.to_datetime(df["date"], errors="coerce")
        invalid_date_count = df["parsed_date"].isna().sum()
        if invalid_date_count > 0:
            issues.append({"issue_type": "Invalid Date", "description": "rows contain unparseable dates", "count": int(invalid_date_count)})

        # Check product_id
        df["product_id_str"] = df["product_id"].astype(str).str.strip()
        invalid_product_count = (df["product_id_str"].isin(["", "nan", "None", "null"])).sum()
        if invalid_product_count > 0:
            issues.append({"issue_type": "Invalid Product ID", "description": "rows contain missing product identifiers", "count": int(invalid_product_count)})

        # Identify invalid rows condition
        invalid_mask = (
            df["selling_price"].isna() | (df["selling_price"] <= 0) |
            df["quantity_sold"].isna() | (df["quantity_sold"] < 0) |
            df["parsed_date"].isna() |
            df["product_id_str"].isin(["", "nan", "None", "null"])
        )

        invalid_rows_count = int(invalid_mask.sum())
        
        # Filter out invalid rows for clean dataset
        valid_df = df[~invalid_mask].copy()

        # Duplicate detection (same product, date, price, quantity)
        dup_mask = valid_df.duplicated(subset=["product_id_str", "parsed_date", "selling_price", "quantity_sold"])
        duplicate_rows_count = int(dup_mask.sum())
        if duplicate_rows_count > 0:
            issues.append({"issue_type": "Duplicate Rows", "description": "duplicate transaction rows detected", "count": duplicate_rows_count})

        # Deduplicate
        cleaned_df = valid_df[~dup_mask].copy()
        valid_rows_count = len(cleaned_df)

        products_found = int(cleaned_df["product_id_str"].nunique()) if not cleaned_df.empty else 0

        date_range_start = None
        date_range_end = None
        if not cleaned_df.empty:
            min_date = cleaned_df["parsed_date"].min()
            max_date = cleaned_df["parsed_date"].max()
            date_range_start = min_date.strftime("%d %b %Y")
            date_range_end = max_date.strftime("%d %b %Y")

        summary = {
            "total_rows": total_rows,
            "valid_rows": valid_rows_count,
            "duplicate_rows": duplicate_rows_count,
            "invalid_rows": invalid_rows_count,
            "products_found": products_found,
            "date_range_start": date_range_start,
            "date_range_end": date_range_end,
            "issues": issues,
            "is_valid": valid_rows_count > 0
        }

        return cleaned_df, summary

    @staticmethod
    def process_and_save(db: Session, shop_id: int, filename: str, cleaned_df: pd.DataFrame, summary: Dict[str, Any]) -> CSVUpload:
        # Create CSVUpload record
        upload = CSVUpload(
            shop_id=shop_id,
            filename=filename,
            total_rows=summary["total_rows"],
            valid_rows=summary["valid_rows"],
            duplicate_rows=summary["duplicate_rows"],
            invalid_rows=summary["invalid_rows"],
        )
        db.add(upload)
        db.flush()

        product_cache: Dict[str, Product] = {}

        # Fetch existing products for shop
        existing_products = db.query(Product).filter(Product.shop_id == shop_id).all()
        for p in existing_products:
            product_cache[p.external_code] = p

        sales_to_insert = []
        products_to_update = set()

        for idx, row in cleaned_df.iterrows():
            ext_code = str(row["product_id_str"]).strip()
            cat = str(row["category"]).strip()
            price = float(row["selling_price"])

            if ext_code not in product_cache:
                new_p = Product(
                    shop_id=shop_id,
                    external_code=ext_code,
                    product_name=f"Product {ext_code}",
                    category=cat if cat != "nan" else "General",
                    current_price=price,
                    data_sufficiency_status="COLD START"
                )
                db.add(new_p)
                db.flush()
                product_cache[ext_code] = new_p

                # Add default constraint for new product
                default_constraint = ProductConstraint(
                    product_id=new_p.product_id,
                    cost_price=round(price * 0.75, 2), # 25% margin default estimate
                    mrp=round(price * 1.15, 2),        # 15% above selling price
                    max_discount_pct=15.0,
                    min_margin_pct=10.0,
                    available_stock=100
                )
                db.add(default_constraint)

            product = product_cache[ext_code]
            products_to_update.add(product.product_id)

            sales_record = SalesRecord(
                product_id=product.product_id,
                upload_id=upload.upload_id,
                sale_date=row["parsed_date"].date(),
                selling_price=price,
                quantity_sold=int(row["quantity_sold"]),
                promotion=str(row["promotion"])
            )
            sales_to_insert.append(sales_record)

        db.bulk_save_objects(sales_to_insert)
        db.commit()

        # Update stats and data sufficiency status for all affected products
        for pid in products_to_update:
            ProductAnalysisService.update_product_stats(db, pid)

        return upload
