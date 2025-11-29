# 🚀 High-Performance Product Importer SaaS

Hey there! 👋 This is a robust, production-ready SaaS backend designed to handle **massive data imports** efficiently.

I built this project to solve a specific engineering challenge: **How do you process 500,000+ records on a server with limited RAM without crashing it?**

Most tutorials show you how to upload a file. This project shows you how to do it **at scale**.

---

## 💡 The Problem & My Solution

### The Challenge
Loading a large CSV file (e.g., 500MB) directly into memory causes "Out of Memory" (OOM) crashes, especially on free-tier cloud hosting (like Render/Heroku) which often limits RAM to 512MB.

### How I Fixed It (The "Secret Sauce")
Instead of the naive approach, I engineered a **Stream-based Architecture**:
1.  **Streaming Uploads:** The backend writes the incoming file to disk in small **1MB chunks**. The file is never fully loaded into RAM.
2.  **Chunked Processing:** A background worker (Celery) reads the file using **Pandas iterators**, processing just **1,000 rows at a time**.
3.  **Async Pipeline:** The heavy lifting happens in the background, keeping the web server responsive. Real-time progress is pushed to the UI via **Server-Sent Events (SSE)**.

---

## 🛠️ Tech Stack

*   **Backend:** Python 3.11, FastAPI (for speed)
*   **Async Task Queue:** Celery + Redis (Upstash)
*   **Database:** PostgreSQL (Neon Tech) + SQLAlchemy
*   **Data Processing:** Pandas (optimized with chunking)
*   **Deployment:** Render (Dockerized environment)

---

## ✨ Key Features

*   ✅ **Bulk Import:** Tested with **500,000+ products**.
*   ✅ **Real-time Progress:** Watch the progress bar update live as rows are processed.
*   ✅ **Memory Efficient:** Runs smoothly on low-resource environments (512MB RAM).
*   ✅ **Data Validation:** Skips bad rows automatically and reports errors.
*   ✅ **CRUD Operations:** Full product management (Search, Filter, Edit, Delete).
*   ✅ **Webhooks:** Trigger external APIs when products are created/updated.

---

## 🚀 How to Run Locally

1.  **Clone the repo:**
    ```bash
    git clone https://github.com/SangharshWalde/Product-Importer-SaaS-Platform.git
    cd Product-Importer-SaaS-Platform
    ```

2.  **Set up environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt
    ```

3.  **Configure .env:**
    Create a `.env` file (see `.env.example`) with your DB and Redis credentials.

4.  **Run it:**
    ```bash
    # Start Redis (if local)
    # Start the Worker
    celery -A celery_app worker --loglevel=info

    # Start the Server
    uvicorn app:app --reload
    ```

---

## 📸 Screenshots

*(Add your screenshots here! Show the upload progress bar and the dashboard.)*

---

## 🤝 Connect

If you found this interesting or want to discuss System Design, feel free to reach out!

**Sangharsh Walde**
[GitHub](https://github.com/SangharshWalde) | [LinkedIn](https://linkedin.com/in/sangharsh-walde)
