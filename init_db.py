# Initialize database tables
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Base, engine
from models.product import Product
from models.webhook import Webhook

try:
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    print("Tables: products, webhooks")
except Exception as e:
    print(f"Error creating tables: {e}")
    sys.exit(1)
