from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Webhook
from pydantic import BaseModel
from typing import Optional
from utils import validate_url
import requests
from datetime import datetime

router = APIRouter()


class WebhookCreate(BaseModel):
    url: str
    event_type: str
    is_enabled: bool = True


class WebhookUpdate(BaseModel):
    url: Optional[str] = None
    event_type: Optional[str] = None
    is_enabled: Optional[bool] = None


@router.get("/webhooks")
def get_webhooks(db: Session = Depends(get_db)):
    """Get all webhooks"""
    webhooks = db.query(Webhook).order_by(Webhook.created_at.desc()).all()
    return {"webhooks": [w.to_dict() for w in webhooks]}


@router.post("/webhooks")
def create_webhook(webhook_data: WebhookCreate, db: Session = Depends(get_db)):
    """Create new webhook"""
    # Validate URL
    if not validate_url(webhook_data.url):
        raise HTTPException(status_code=400, detail="Invalid webhook URL")
    
    # Validate event type
    valid_events = [
        "product.created",
        "product.updated",
        "product.deleted",
        "product.bulk_deleted"
    ]
    if webhook_data.event_type not in valid_events:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid event type. Must be one of: {', '.join(valid_events)}"
        )
    
    # Create webhook
    webhook = Webhook(
        url=webhook_data.url,
        event_type=webhook_data.event_type,
        is_enabled=webhook_data.is_enabled
    )
    
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    
    return webhook.to_dict()


@router.put("/webhooks/{webhook_id}")
def update_webhook(
    webhook_id: int,
    webhook_data: WebhookUpdate,
    db: Session = Depends(get_db)
):
    """Update existing webhook"""
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    # Update fields
    if webhook_data.url is not None:
        if not validate_url(webhook_data.url):
            raise HTTPException(status_code=400, detail="Invalid webhook URL")
        webhook.url = webhook_data.url
    
    if webhook_data.event_type is not None:
        valid_events = [
            "product.created",
            "product.updated",
            "product.deleted",
            "product.bulk_deleted"
        ]
        if webhook_data.event_type not in valid_events:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid event type. Must be one of: {', '.join(valid_events)}"
            )
        webhook.event_type = webhook_data.event_type
    
    if webhook_data.is_enabled is not None:
        webhook.is_enabled = webhook_data.is_enabled
    
    db.commit()
    db.refresh(webhook)
    
    return webhook.to_dict()


@router.delete("/webhooks/{webhook_id}")
def delete_webhook(webhook_id: int, db: Session = Depends(get_db)):
    """Delete webhook"""
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    db.delete(webhook)
    db.commit()
    
    return {"message": "Webhook deleted successfully"}


@router.post("/webhooks/{webhook_id}/test")
def test_webhook(webhook_id: int, db: Session = Depends(get_db)):
    """Test webhook by sending a test payload"""
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    # Prepare test payload
    test_payload = {
        "event": webhook.event_type,
        "data": {
            "test": True,
            "message": "This is a test webhook notification"
        },
        "timestamp": datetime.utcnow().isoformat()
    }
    
    try:
        # Send test request
        response = requests.post(
            webhook.url,
            json=test_payload,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        
        # Update last triggered time
        webhook.last_triggered_at = datetime.utcnow()
        db.commit()
        
        return {
            "message": "Webhook test successful",
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds()
        }
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Webhook test failed: {str(e)}"
        )
