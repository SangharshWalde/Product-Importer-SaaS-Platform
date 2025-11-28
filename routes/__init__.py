from routes.upload import router as upload_router
from routes.products import router as products_router
from routes.webhooks import router as webhooks_router
from routes.progress import router as progress_router

__all__ = [
    "upload_router",
    "products_router",
    "webhooks_router",
    "progress_router"
]
