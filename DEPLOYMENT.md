# Deployment Guide 🚀

This guide will help you upload your code to GitHub and deploy it to the web using **Render** (a popular, easy-to-use cloud platform).

## Part 1: Upload to GitHub

1.  **Create a GitHub Repository**

---

## Part 2: Deploy to Render (Recommended)

Render is great because it supports Python, PostgreSQL, and Redis easily.

1.  **Sign Up / Login**
    *   Go to [render.com](https://render.com) and log in with your GitHub account.

2.  **Create a Blueprint (Easiest Method)**
    ```powershell
    # Link to your GitHub repo
    git remote add origin https://github.com/SangharshWalde/Product-Importer-Saas-Platform.git

    # Push to GitHub
    git push -u origin master
    ```
    *   Click **New +** and select **Blueprint**.
    *   Connect your `product-importer-saas` repository.
    *   Render will automatically detect the `render.yaml` file I created for you.
    *   Click **Apply**.

3.  **Manual Setup (If Blueprint fails or for Free Tier)**
    If you want to stay strictly on the free tier, you might need to set up services individually:

    *   **Web Service**:
        *   Build Command: `pip install -r requirements.txt`
        *   Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
        *   Env Vars: Add `DATABASE_URL` and `REDIS_URL`.
    *   **PostgreSQL**: Create a new PostgreSQL database on Render. Copy the `Internal Connection URL` to the Web Service's `DATABASE_URL`.
    *   **Redis**: Render's Redis is paid. For a **free Redis**, use [Upstash](https://upstash.com/). Create a database there and copy the URL to `REDIS_URL`.

---

## Part 3: Environment Variables

When deploying, ensure you set these Environment Variables in your cloud dashboard:

*   `DATABASE_URL`: (Provided by your cloud database)
*   `REDIS_URL`: (Provided by your cloud Redis)
*   `SECRET_KEY`: Generate a random string (e.g., `openssl rand -hex 32`)

---

## Part 4: Database Migration

After deployment, the application will automatically create tables when it starts. No manual migration command is needed for this setup.

**That's it! Your app will be live!** 🌍
