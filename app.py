from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from config import settings
from database import init_db
from routes import upload_router, products_router, webhooks_router, progress_router

# Initialize FastAPI app
app = FastAPI(
    title="Product Importer SaaS",
    description="Scalable product import system with CSV upload and webhook notifications",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(products_router, prefix="/api", tags=["Products"])
app.include_router(webhooks_router, prefix="/api", tags=["Webhooks"])
app.include_router(progress_router, prefix="/api", tags=["Progress"])

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Product Importer SaaS"}


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✅ Database initialized")
    print("🚀 Product Importer SaaS is running!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
