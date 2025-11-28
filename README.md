# Product Importer SaaS 📦

A high-performance, scalable SaaS application for importing large product datasets (up to 500,000+ records) with real-time progress tracking.

## 🚀 Features

-   **Massive CSV Import**: Process 500k+ products in seconds using bulk database operations.
-   **Real-Time Feedback**: Live progress bar powered by Server-Sent Events (SSE).
-   **Product Management**: Full CRUD (Create, Read, Update, Delete) with Search & Pagination.
-   **Bulk Actions**: "Delete All" functionality with custom confirmation modal.
-   **Webhooks**: Event-driven architecture triggering external URLs on product changes.
-   **Robust Stack**: FastAPI, PostgreSQL, Redis, Celery.

## 🛠️ How to Run

The application requires two separate terminal windows to run the backend server and the background worker.

### 1. Start Backend & Redis
Open PowerShell in the project folder:
```powershell
.\start_backend.ps1
```
*This starts Redis and the FastAPI server on http://localhost:8000*

### 2. Start Background Worker
Open a **second** PowerShell window:
```powershell
.\start_celery.ps1
```
*This starts the Celery worker to handle file processing and webhooks.*

### 3. Access the App
Open your browser to: **http://localhost:8000**

## 📚 Usage Guide

### Importing Products
1.  Click the "Upload CSV File" area.
2.  Select a CSV file (Format: `sku,name,description,price,quantity`).
3.  Watch the progress bar as products are imported.

### Managing Products
-   **Search**: Type in the search box to filter by SKU or Name.
-   **Edit**: Click "Edit" on any row to modify details.
-   **Delete**: Click "Delete" to remove a single item.
-   **Delete All**: Click "Delete All" to clear the database (requires confirmation).

### Webhooks
1.  Click "Add Webhook".
2.  Enter a target URL (e.g., `https://webhook.site/...`).
3.  Select an event type (e.g., `product.created`).
4.  The system will now send POST requests to that URL when events occur.

## 🔧 Troubleshooting

-   **"Waiting 0%" stuck**: Ensure the Celery worker (`start_celery.ps1`) is running.
-   **Database Error**: Check that PostgreSQL is running and credentials in `.env` are correct.
-   **Redis Error**: Ensure `redis-server.exe` is running (started automatically by `start_backend.ps1`).

## 📁 Project Structure

-   `app.py`: Main FastAPI application.
-   `tasks/`: Celery task definitions (CSV processing, webhooks).
-   `routes/`: API endpoints.
-   `models/`: Database schemas.
-   `static/`: Frontend assets (HTML, CSS, JS).
