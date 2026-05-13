# Quick Start Guide

Get the Session Manager Service running in 5 minutes!

---

## ⚡ Quick Setup (Windows)

### Step 1: Install PostgreSQL
```bash
# Download and install from:
https://www.postgresql.org/download/windows/

# Or use chocolatey:
choco install postgresql
```

### Step 2: Create Database
```bash
# Open Command Prompt and run:
psql -U postgres

# In PostgreSQL prompt:
CREATE DATABASE session_manager;
\q
```

### Step 3: Setup Project
```bash
# Navigate to project
cd session_manager

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment
Edit `.env` file with your PostgreSQL password:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/session_manager
```

### Step 5: Run the Server
```bash
uvicorn app.main:app --reload
```

### Step 6: Test the API
Open browser: http://localhost:8000/docs

---

## ⚡ Quick Setup (Mac/Linux)

### Step 1: Install PostgreSQL
```bash
# Mac:
brew install postgresql
brew services start postgresql

# Linux:
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Create Database
```bash
psql -U postgres
CREATE DATABASE session_manager;
\q
```

### Step 3: Setup Project
```bash
cd session_manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Environment
Edit `.env` file:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/session_manager
```

### Step 5: Run the Server
```bash
uvicorn app.main:app --reload
```

### Step 6: Test the API
Open browser: http://localhost:8000/docs

---

## 🎯 First API Call

### Using Swagger UI (Easiest)
1. Go to http://localhost:8000/docs
2. Click on **POST /api/v1/start-session**
3. Click **"Try it out"**
4. Use this JSON:
```json
{
  "candidate_id": 101,
  "interviewer_id": 201
}
```
5. Click **"Execute"**
6. Copy the `session_id` from response

### Using cURL
```bash
curl -X POST "http://localhost:8000/api/v1/start-session" \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": 101, "interviewer_id": 201}'
```

### Using Python
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/start-session",
    json={"candidate_id": 101, "interviewer_id": 201}
)
print(response.json())
```

---

## 🧪 Run Test Suite

```bash
# Make sure server is running first
# Then in another terminal:

cd session_manager
python test_api.py
```

---

## 📚 Next Steps

1. **Read the README**: Full documentation in `README.md`
2. **Explore Architecture**: Learn the design in `ARCHITECTURE.md`
3. **Test Thoroughly**: Follow `TESTING_GUIDE.md`
4. **Customize**: Modify code for your needs

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
# Windows:
netstat -ano | findstr :8000

# Mac/Linux:
lsof -i :8000

# Use different port:
uvicorn app.main:app --port 8001
```

### Database connection error
```bash
# Check PostgreSQL is running
# Windows:
sc query postgresql

# Mac:
brew services list

# Linux:
sudo systemctl status postgresql
```

### Module not found
```bash
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 🎉 You're Ready!

Your Session Manager Service is now running!

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **ReDoc**: http://localhost:8000/redoc

---

**Happy Coding! 🚀**
