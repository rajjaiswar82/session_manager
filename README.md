# Session Manager Service

A complete backend service for managing interview session lifecycle in an AI Interview/Assessment platform.

## 🎯 Project Overview

This is a **FastAPI + PostgreSQL** backend service that handles the complete lifecycle of interview sessions:
- Start new sessions with unique UUIDs
- Track session state and status
- Update session status (active, paused, completed, terminated)
- End sessions with timestamp recording
- Retrieve session details and history

**Perfect for**: Internship projects, portfolio, college viva, backend demonstrations

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **FastAPI** - Modern, fast web framework
- **PostgreSQL** - Reliable relational database
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **UUID** - Unique session identifiers

---

## 📁 Project Structure

```
session_manager/
│
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # Database connection & session management
│   ├── config.py               # Configuration and environment variables
│   │
│   ├── models/
│   │   └── session_model.py    # SQLAlchemy ORM model
│   │
│   ├── schemas/
│   │   └── session_schema.py   # Pydantic schemas for validation
│   │
│   ├── routes/
│   │   └── session_routes.py   # API route handlers
│   │
│   ├── services/
│   │   └── session_service.py  # Business logic layer
│   │
│   └── utils/
│       └── helper.py            # Utility functions
│
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
└── README.md                    # This file
```

---

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### 2. Install PostgreSQL

**Windows:**
```bash
# Download from: https://www.postgresql.org/download/windows/
# Or use chocolatey:
choco install postgresql
```

**Mac:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 3. Create Database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE session_manager;

# Exit
\q
```

### 4. Clone/Setup Project

```bash
# Navigate to project directory
cd session_manager

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Configure Environment

Edit `.env` file with your database credentials:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/session_manager
APP_NAME=Session Manager Service
APP_VERSION=1.0.0
DEBUG=True
```

### 6. Run the Application

```bash
# From session_manager directory
uvicorn app.main:app --reload

# Or run directly
python -m app.main
```

The API will be available at: `http://localhost:8000`

---

## 📚 API Documentation

Once the server is running, access interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔌 API Endpoints

### 1. Start Session
**POST** `/api/v1/start-session`

Create a new interview session.

**Request Body:**
```json
{
  "candidate_id": 101,
  "interviewer_id": 201
}
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 2. Get Session
**GET** `/api/v1/session/{session_id}`

Retrieve session details.

**Response:**
```json
{
  "id": 1,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "candidate_id": 101,
  "interviewer_id": 201,
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "ended_at": null
}
```

### 3. Get All Sessions
**GET** `/api/v1/sessions`

Retrieve all sessions.

**Response:**
```json
[
  {
    "id": 1,
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "candidate_id": 101,
    "interviewer_id": 201,
    "status": "active",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "ended_at": null
  }
]
```

### 4. Update Session
**PUT** `/api/v1/update-session/{session_id}`

Update session status.

**Request Body:**
```json
{
  "status": "paused"
}
```

**Response:**
```json
{
  "id": 1,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "candidate_id": 101,
  "interviewer_id": 201,
  "status": "paused",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z",
  "ended_at": null
}
```

### 5. End Session
**POST** `/api/v1/end-session/{session_id}`

Mark session as completed.

**Response:**
```json
{
  "id": 1,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "candidate_id": 101,
  "interviewer_id": 201,
  "status": "completed",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z",
  "ended_at": "2024-01-15T11:00:00Z"
}
```

---

## 🔄 Session Lifecycle

```
START → active → paused → active → completed
                    ↓
                terminated
```

**Valid Status Transitions:**
- `active` → `paused`, `completed`, `terminated`
- `paused` → `active`, `completed`, `terminated`
- `completed` → (final state, no transitions)
- `terminated` → (final state, no transitions)

---

## 🧪 Testing with Swagger

1. Start the server: `uvicorn app.main:app --reload`
2. Open browser: http://localhost:8000/docs
3. Click on any endpoint
4. Click "Try it out"
5. Fill in the request body
6. Click "Execute"
7. View the response

---

## 🧪 Testing with Postman

### Import Collection

Create a new collection with these requests:

**1. Start Session**
- Method: POST
- URL: `http://localhost:8000/api/v1/start-session`
- Body (JSON):
```json
{
  "candidate_id": 101,
  "interviewer_id": 201
}
```

**2. Get Session**
- Method: GET
- URL: `http://localhost:8000/api/v1/session/{session_id}`

**3. Update Session**
- Method: PUT
- URL: `http://localhost:8000/api/v1/update-session/{session_id}`
- Body (JSON):
```json
{
  "status": "paused"
}
```

**4. End Session**
- Method: POST
- URL: `http://localhost:8000/api/v1/end-session/{session_id}`

**5. Get All Sessions**
- Method: GET
- URL: `http://localhost:8000/api/v1/sessions`

---

## 🗃️ Database Schema

```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR UNIQUE NOT NULL,
    candidate_id INTEGER NOT NULL,
    interviewer_id INTEGER NOT NULL,
    status VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_session_id ON sessions(session_id);
CREATE INDEX idx_candidate_id ON sessions(candidate_id);
CREATE INDEX idx_interviewer_id ON sessions(interviewer_id);
```

---

## ⚠️ Edge Cases Handled

1. **Duplicate Active Sessions**: Prevents same candidate from having multiple active sessions
2. **Invalid Session ID**: Returns 404 if session doesn't exist
3. **Updating Completed Sessions**: Prevents modification of completed/terminated sessions
4. **Ending Completed Sessions**: Prevents ending already completed sessions
5. **Invalid Status Values**: Validates status using enum constraints
6. **Concurrent Updates**: Uses database transactions for consistency
7. **Timestamp Management**: Automatically handles created_at, updated_at, ended_at

---

## 🎓 Key Concepts Explained

### Why FastAPI?

1. **Fast Performance**: Built on Starlette and Pydantic, one of the fastest Python frameworks
2. **Automatic Documentation**: Generates Swagger UI and ReDoc automatically
3. **Type Safety**: Uses Python type hints for validation
4. **Modern Python**: Supports async/await for high concurrency
5. **Easy to Learn**: Clean, intuitive syntax perfect for beginners
6. **Production Ready**: Used by companies like Microsoft, Uber, Netflix

### How Session Lifecycle Works

1. **Start**: Generate UUID → Create database record → Return session_id
2. **Active**: Session is ongoing, can be paused or completed
3. **Paused**: Temporarily stopped, can resume to active
4. **Completed**: Successfully finished, immutable
5. **Terminated**: Abruptly ended, immutable

### How Database Integration Works

1. **SQLAlchemy ORM**: Maps Python classes to database tables
2. **Connection Pooling**: Reuses database connections for efficiency
3. **Session Management**: Each request gets isolated database session
4. **Automatic Commits**: Changes saved automatically after successful operations
5. **Rollback on Error**: Failed operations don't corrupt database

### How Edge Cases Are Handled

1. **Validation Layer**: Pydantic schemas validate input before processing
2. **Business Logic Layer**: Service functions check business rules
3. **Database Constraints**: Unique constraints prevent duplicates
4. **HTTP Exceptions**: Return proper status codes (400, 404, 500)
5. **Transaction Management**: Atomic operations prevent partial updates

### How Timestamps Are Managed

1. **created_at**: Set by database on INSERT using `server_default=func.now()`
2. **updated_at**: Set on INSERT and UPDATE using `onupdate=func.now()`
3. **ended_at**: Manually set when session ends
4. **UTC Timezone**: All timestamps in UTC for consistency

### How Duplicate Sessions Are Prevented

1. **Database Query**: Check for existing active session before creating
2. **Candidate Filter**: Query by candidate_id and status='active'
3. **HTTP 400 Error**: Return error if duplicate found
4. **Atomic Check**: Query and insert in same transaction

### How Concurrent Updates Are Minimized

1. **Database Transactions**: Each operation is atomic
2. **Row-Level Locking**: PostgreSQL locks rows during updates
3. **Optimistic Locking**: updated_at timestamp tracks changes
4. **Connection Pooling**: Manages concurrent database connections

---

## 🐛 Troubleshooting

### Database Connection Error
```
sqlalchemy.exc.OperationalError: could not connect to server
```
**Solution**: Check PostgreSQL is running and credentials in `.env` are correct

### Port Already in Use
```
ERROR: [Errno 48] Address already in use
```
**Solution**: Change port in uvicorn command: `uvicorn app.main:app --port 8001`

### Module Not Found
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution**: Activate virtual environment and install dependencies

---

## 📝 Development Tips

1. **Use Virtual Environment**: Keeps dependencies isolated
2. **Check Swagger Docs**: Test APIs interactively at /docs
3. **Read Error Messages**: FastAPI provides detailed error information
4. **Use Database GUI**: Tools like pgAdmin or DBeaver help visualize data
5. **Enable Debug Mode**: Set DEBUG=True in .env for detailed logs

---

## 🎯 Future Enhancements

- Add authentication (JWT tokens)
- Implement session duration tracking
- Add session notes/feedback
- Create session analytics dashboard
- Add WebSocket for real-time updates
- Implement session recording
- Add email notifications

---

## 📄 License

This project is open source and available for educational purposes.

---

## 👨‍💻 Author

Created as an intern-level backend project for learning FastAPI and PostgreSQL.

---

## 🙏 Acknowledgments

- FastAPI documentation
- SQLAlchemy documentation
- PostgreSQL documentation

---

**Happy Coding! 🚀**
