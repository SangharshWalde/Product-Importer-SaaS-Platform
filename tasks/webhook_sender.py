import requests
from celery_app import celery_app
from database import SessionLocal
from models import Webhook
from datetime import datetime


@celery_app.task(bind=True, max_retries=3)
def send_webhook_notification(self, event_type: str, data: dict):
    """
    Send webhook notification to configured endpoints
    
    Args:
        event_type: Type of event (product.created, product.updated, product.deleted)
        data: Event data to send
    """
    db = SessionLocal()
    
    try:
        # Get all enabled webhooks for this event type
        webhooks = db.query(Webhook).filter(
            Webhook.event_type == event_type,
            Webhook.is_enabled == True
        ).all()
        
        for webhook in webhooks:
            try:
                # Prepare payload
                payload = {
                    "event": event_type,
                    "data": data,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                # Send POST request
                response = requests.post(
                    webhook.url,
                    json=payload,
                    timeout=10,
                    headers={"Content-Type": "application/json"}
                )
                
                # Update last triggered time
                webhook.last_triggered_at = datetime.utcnow()
                db.commit()
                
                # Log response
                print(f"Webhook sent to {webhook.url}: {response.status_code}")
                
            except requests.exceptions.RequestException as e:
                print(f"Error sending webhook to {webhook.url}: {str(e)}")
                # Don't fail the entire task if one webhook fails
                continue
        
        return {"status": "success", "webhooks_sent": len(webhooks)}
    
    except Exception as e:
        print(f"Error in webhook task: {str(e)}")
        # Retry on failure
        raise self.retry(exc=e, countdown=60)
    
    finally:
        db.close()
