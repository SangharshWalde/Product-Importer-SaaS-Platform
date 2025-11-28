import pandas as pd
import os
from celery_app import celery_app
from database import SessionLocal
from models import Product
from utils import ProgressTracker, validate_sku, validate_price, validate_quantity
from sqlalchemy import func
from tasks.webhook_sender import send_webhook_notification


@celery_app.task(bind=True)
def process_csv_file(self, file_path: str, task_id: str):
    """
    Process CSV file and import products into database
    
    Args:
        file_path: Path to the CSV file
        task_id: Unique task identifier for progress tracking
    """
    db = SessionLocal()
    tracker = ProgressTracker()
    
    try:
        # Update initial status
        tracker.set_progress(task_id, 0, "Reading CSV file...", 100)
        
        # Read CSV file
        df = pd.read_csv(file_path)
        total_rows = len(df)
        
        if total_rows == 0:
            tracker.set_error(task_id, "CSV file is empty")
            return {"status": "error", "message": "CSV file is empty"}
        
        # Normalize column names
        df.columns = df.columns.str.lower().str.strip()
        
        # Validate required columns
        required_columns = {'sku', 'name', 'price'}
        if not required_columns.issubset(set(df.columns)):
            missing = required_columns - set(df.columns)
            error_msg = f"Missing required columns: {', '.join(missing)}"
            tracker.set_error(task_id, error_msg)
            return {"status": "error", "message": error_msg}
        
        # Process in chunks
        chunk_size = 1000
        processed = 0
        created_count = 0
        updated_count = 0
        error_count = 0
        
        tracker.set_progress(task_id, 0, f"Processing {total_rows} products...", total_rows)
        
        for start_idx in range(0, total_rows, chunk_size):
            end_idx = min(start_idx + chunk_size, total_rows)
            chunk = df.iloc[start_idx:end_idx]
            
            # 1. Collect SKUs in this chunk
            chunk_skus = []
            sku_to_row = {}
            
            for idx, row in chunk.iterrows():
                sku = str(row.get('sku', '')).strip()
                if validate_sku(sku):
                    chunk_skus.append(sku)
                    sku_to_row[sku.lower()] = row
                else:
                    error_count += 1
            
            if not chunk_skus:
                processed += len(chunk)
                continue
                
            # 2. Bulk fetch existing products
            # Note: We use lower() for case-insensitive comparison
            existing_products = db.query(Product).filter(
                func.lower(Product.sku).in_([s.lower() for s in chunk_skus])
            ).all()
            
            existing_map = {p.sku.lower(): p for p in existing_products}
            
            # 3. Process rows
            new_products = []
            
            for sku_raw in chunk_skus:
                sku_lower = sku_raw.lower()
                row = sku_to_row[sku_lower]
                
                try:
                    # Extract data
                    name = str(row.get('name', '')).strip()
                    description = str(row.get('description', '')).strip() if 'description' in row else ''
                    price = float(row.get('price', 0))
                    quantity = int(row.get('quantity', 0)) if 'quantity' in row else 0
                    is_active = bool(row.get('is_active', True)) if 'is_active' in row else True
                    
                    # Validate
                    if not name or not validate_price(price) or not validate_quantity(quantity):
                        error_count += 1
                        continue
                    
                    if sku_lower in existing_map:
                        # Update existing
                        product = existing_map[sku_lower]
                        product.name = name
                        product.description = description
                        product.price = price
                        product.quantity = quantity
                        product.is_active = is_active
                        updated_count += 1
                    else:
                        # Create new
                        new_product = Product(
                            sku=sku_raw, # Use original case
                            name=name,
                            description=description,
                            price=price,
                            quantity=quantity,
                            is_active=is_active
                        )
                        new_products.append(new_product)
                        created_count += 1
                
                except Exception as e:
                    error_count += 1
                    print(f"Error processing row: {str(e)}")
                    continue
            
            # 4. Bulk insert new products
            if new_products:
                db.add_all(new_products)
                db.flush() # Get IDs
            
            processed += len(chunk)
            
            # Commit chunk
            db.commit()
            
            # Update progress
            percentage = int((processed / total_rows) * 100)
            tracker.set_progress(
                task_id,
                processed,
                f"Processed {processed}/{total_rows} products...",
                total_rows
            )
        
        # Final commit
        db.commit()
        
        # Clean up file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Set completion status
        message = f"Import complete! Created: {created_count}, Updated: {updated_count}, Errors: {error_count}"
        tracker.set_complete(task_id, message)
        
        return {
            "status": "complete",
            "created": created_count,
            "updated": updated_count,
            "errors": error_count,
            "total": total_rows
        }
    
    except Exception as e:
        error_msg = f"Error processing CSV: {str(e)}"
        tracker.set_error(task_id, error_msg)
        return {"status": "error", "message": error_msg}
    
    finally:
        db.close()
