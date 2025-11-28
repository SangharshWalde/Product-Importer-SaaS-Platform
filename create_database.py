# Create database using Python and SQLAlchemy
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL without database name
db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost:5432/postgres')
# Connect to default postgres database
base_url = db_url.rsplit('/', 1)[0] + '/postgres'

try:
    # Create engine for postgres database
    engine = create_engine(base_url, isolation_level='AUTOCOMMIT')
    
    with engine.connect() as conn:
        # Check if database exists
        result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='product_importer'"))
        exists = result.fetchone()
        
        if not exists:
            # Create database
            conn.execute(text("CREATE DATABASE product_importer"))
            print("✅ Database 'product_importer' created successfully!")
        else:
            print("ℹ️  Database 'product_importer' already exists")
    
    # Now connect to the new database and create tables
    from database import Base, engine as app_engine
    Base.metadata.create_all(bind=app_engine)
    print("✅ Database tables created successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nPlease check:")
    print("1. PostgreSQL is running")
    print("2. Password in .env is correct")
    print("3. PostgreSQL user 'postgres' exists")
