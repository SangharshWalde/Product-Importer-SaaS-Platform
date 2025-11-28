from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from database import get_db
from models import Product
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class ProductCreate(BaseModel):
    sku: str
    name: str
    description: Optional[str] = ""
    price: float
    quantity: int = 0
    is_active: bool = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    is_active: Optional[bool] = None


@router.get("/products")
def get_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Get paginated list of products with optional filtering
    
    Args:
        page: Page number (1-indexed)
        per_page: Items per page
        search: Search term for SKU, name, or description
        is_active: Filter by active status
        db: Database session
        
    Returns:
        Paginated product list
    """
    query = db.query(Product)
    
    # Apply filters
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Product.sku.ilike(search_term),
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )
    
    if is_active is not None:
        query = query.filter(Product.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * per_page
    products = query.order_by(Product.created_at.desc()).offset(offset).limit(per_page).all()
    
    return {
        "products": [p.to_dict() for p in products],
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }


@router.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get single product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.to_dict()


@router.post("/products")
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """Create new product"""
    # Check if SKU already exists (case-insensitive)
    existing = db.query(Product).filter(
        func.lower(Product.sku) == product_data.sku.lower()
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Product with this SKU already exists")
    
    # Create product
    product = Product(
        sku=product_data.sku,
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        quantity=product_data.quantity,
        is_active=product_data.is_active
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # Trigger webhook
    from tasks import send_webhook_notification
    send_webhook_notification.delay("product.created", product.to_dict())
    
    return product.to_dict()


@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update existing product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update fields
    if product_data.name is not None:
        product.name = product_data.name
    if product_data.description is not None:
        product.description = product_data.description
    if product_data.price is not None:
        product.price = product_data.price
    if product_data.quantity is not None:
        product.quantity = product_data.quantity
    if product_data.is_active is not None:
        product.is_active = product_data.is_active
    
    db.commit()
    db.refresh(product)
    
    # Trigger webhook
    from tasks import send_webhook_notification
    send_webhook_notification.delay("product.updated", product.to_dict())
    
    return product.to_dict()


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete single product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product_dict = product.to_dict()
    db.delete(product)
    db.commit()
    
    # Trigger webhook
    from tasks import send_webhook_notification
    send_webhook_notification.delay("product.deleted", product_dict)
    
    return {"message": "Product deleted successfully"}


@router.delete("/products")
def bulk_delete_products(db: Session = Depends(get_db)):
    """Delete all products"""
    count = db.query(Product).count()
    db.query(Product).delete()
    db.commit()
    
    return {"message": f"Deleted {count} products successfully", "count": count}
