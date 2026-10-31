# Step 4: Hosting on Render with MySQL (`4_render_withdb`)

Deploy the Flask registration form application to [Render](https://render.com) using **Gunicorn** (a production WSGI server) connected to a hosted MySQL database (e.g. TiDB Cloud, Aiven, or any cloud MySQL).

## Project Structure

```text
4_render_withdb/
├── static/
│   ├── index.html       # HTML form
│   ├── script.js        # Form submission to /register
│   └── style.css        # Form styling
├── app.py               # Flask app with cloud MySQL insert
├── requirements.txt     # flask, pymysql, gunicorn
├── .env.example         # Template for environment variables
└── README.md            # Hosting instructions for Render
```

---

## Why Gunicorn?

In local development, we run `python app.py` (Flask's built-in single-threaded server).
For cloud hosting on platforms like Render, we use **Gunicorn** (`gunicorn app:app`):
- It is a production-grade WSGI HTTP server.
- It handles concurrent requests across multiple worker processes.
- It automatically binds to the `$PORT` assigned by Render.

---

## Step-by-Step Instructions to Host on Render

### 1. Push Code to GitHub
Ensure this repository is pushed to your GitHub account.

### 2. Create a Web Service on Render
1. Log in to [dashboard.render.com](https://dashboard.render.com).
2. Click **New +** in the top right, then select **Web Service**.
3. Select **Build and deploy from a Git repository** and connect your repo.

### 3. Configure Service Settings
Fill in the following fields:

| Setting | Value |
| :--- | :--- |
| **Name** | `registration-app` (or any name you like) |
| **Region** | Choose the region closest to you (e.g. *Singapore* or *Frankfurt*) |
| **Branch** | `main` |
| **Root Directory** | `4_render_withdb` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | `Free` |

---

### 4. Add Database Environment Variables
Scroll down to **Environment Variables** on the same page and add the credentials for your hosted MySQL database:

| Key | Example Value | Description |
| :--- | :--- | :--- |
| `DB_HOST` | `gateway01.ap-southeast-1.prod.aws.tidbcloud.com` | Hosted DB Host |
| `DB_USER` | `xxxxxx.root` | Database Username |
| `DB_PASSWORD` | `your_db_password` | Database Password |
| `DB_NAME` | `test` (for TiDB) or `users_db` | Database Name |
| `DB_PORT` | `4000` (for TiDB) or `3306` (standard) | MySQL Port |
| `DB_SSL` | `true` | `true` for TiDB Cloud / Aiven |

*(Note: Render automatically provides the `PORT` variable; Gunicorn detects it without manual input).*

---

### 5. Deploy & Access
1. Click **Deploy Web Service**.
2. Render will run `pip install -r requirements.txt` and launch `gunicorn app:app`.
3. Once live, open your generated `https://<your-app-name>.onrender.com` URL in your browser!
