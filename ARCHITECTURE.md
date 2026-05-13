# Architecture Documentation

## 🏗️ System Architecture

### Overview
The Session Manager Service follows a **layered architecture** pattern, separating concerns into distinct layers for maintainability and scalability.

```
┌─────────────────────────────────────────┐
│         Client (Browser/Postman)        │
└─────────────────┬───────────────────────┘
                  │ HTTP Requests
                  ▼
┌─────────────────────────────────────────┐
│         FastAPI Application             │
│  ┌───────────────────────────────────┐  │
│  │     Routes Layer (API Handlers)   │  │
│  └───────────────┬───────────────────┘  │
│                  │                       │
│  ┌───────────────▼───────────────────┐  │
│  │   Services Layer (Business Logic) │  │
│  └───────────────┬───────────────────┘  │
│                  │                       │
│  ┌───────────────▼───────────────────┐  │
│  │    Models Layer (ORM/Database)    │  │
│  └───────────────┬───────────────────┘  │
└──────────────────┼───────────────────────┘
                   │ SQL Queries
                   ▼
┌─────────────────────────────────────────┐
│         PostgreSQL Database             │
└─────────────────────────────────────────┘
```

---

## 📦 Layer Breakdown

### 1. Routes Layer (`app/routes/`)
**Responsibility**: Handle HTTP requests and responses

**Components**:
- `session_routes.py`: API endpoint definitions

**Functions**:
- Parse incoming HTTP requests
- Validate request data using Pydantic schemas
- Call service layer functions
- Format and return HTTP responses
- Handle HTTP status codes

**Example**:
```python
@router.post("/start-session")
def start_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    session = SessionService.create_session(db, session_data)
    return SessionStartResponse(...)
```

---

### 2. Services Layer (`app/services/`)
**Responsibility**: Implement business logic

**Components**:
- `session_service.py`: Session management logic

**Functions**:
- Validate business rules
- Coordinate database operations
- Handle edge cases
- Generate UUIDs
- Manage timestamps
- Prevent duplicate sessions

**Example**:
```python
@staticmethod
def create_session(db: Session, session_data: SessionCreate):
    # Check for duplicates
    if SessionService.check_duplicate_active_session(...):
        raise HTTPException(...)
    
    # Generate UUID
    session_id = SessionService.generate_session_id()
    
    # Create and save
    new_session = SessionModel(...)
    db.add(new_session)
    db.commit()
    return new_session
```

---

### 3. Models Layer (`app/models/`)
**Responsibility**: Define database structure

**Components**:
- `session_model.py`: SQLAlchemy ORM model

**Functions**:
- Map Python classes to database tables
- Define column types and constraints
- Handle database relationships
- Provide database abstraction

**Example**:
```python
class SessionModel(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String, unique=True)
    status = Column(SQLEnum(SessionStatus))
    created_at = Column(DateTime, server_default=func.now())
```

---

### 4. Schemas Layer (`app/schemas/`)
**Responsibility**: Data validation and serialization

**Components**:
- `session_schema.py`: Pydantic models

**Functions**:
- Validate incoming request data
- Serialize outgoing response data
- Define data structure contracts
- Provide automatic documentation

**Example**:
```python
class SessionCreate(BaseModel):
    candidate_id: int = Field(..., gt=0)
    interviewer_id: int = Field(..., gt=0)
```

---

### 5. Database Layer (`app/database.py`)
**Responsibility**: Database connection management

**Functions**:
- Create database engine
- Manage connection pooling
- Provide database sessions
- Initialize database tables

**Example**:
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### 6. Configuration Layer (`app/config.py`)
**Responsibility**: Application configuration

**Functions**:
- Load environment variables
- Provide application settings
- Centralize configuration

---

### 7. Utilities Layer (`app/utils/`)
**Responsibility**: Reusable helper functions

**Functions**:
- Date/time formatting
- Validation helpers
- Common utilities

---

## 🔄 Request Flow

### Example: Creating a New Session

```
1. Client sends POST request
   ↓
2. FastAPI receives request at /api/v1/start-session
   ↓
3. Routes layer (session_routes.py)
   - Validates request body using SessionCreate schema
   - Gets database session via dependency injection
   ↓
4. Services layer (session_service.py)
   - Checks for duplicate active sessions
   - Generates unique UUID
   - Creates SessionModel instance
   ↓
5. Models layer (session_model.py)
   - ORM converts Python object to SQL
   ↓
6. Database layer
   - Executes INSERT query
   - Returns created record
   ↓
7. Services layer
   - Returns SessionModel object
   ↓
8. Routes layer
   - Converts to SessionStartResponse schema
   - Returns HTTP 201 with JSON response
   ↓
9. Client receives response
```

---

## 🎯 Design Patterns Used

### 1. Dependency Injection
**Where**: Database session management
**Why**: Automatic resource cleanup, testability

```python
def endpoint(db: Session = Depends(get_db)):
    # db is automatically provided and cleaned up
```

### 2. Repository Pattern
**Where**: Service layer
**Why**: Separates data access from business logic

### 3. DTO (Data Transfer Object)
**Where**: Pydantic schemas
**Why**: Type-safe data transfer between layers

### 4. Singleton Pattern
**Where**: Configuration settings
**Why**: Single source of truth for configuration

```python
@lru_cache()
def get_settings():
    return Settings()
```

### 5. Factory Pattern
**Where**: UUID generation
**Why**: Centralized object creation

---

## 🔐 Security Considerations

### 1. SQL Injection Prevention
- **Method**: SQLAlchemy ORM with parameterized queries
- **Benefit**: Automatic escaping of user input

### 2. Input Validation
- **Method**: Pydantic schemas with type checking
- **Benefit**: Reject invalid data before processing

### 3. Database Connection Security
- **Method**: Connection pooling with limits
- **Benefit**: Prevent connection exhaustion attacks

### 4. Error Handling
- **Method**: Structured exception handling
- **Benefit**: Don't expose internal details in errors

---

## 📊 Database Design

### Sessions Table

```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR UNIQUE NOT NULL,
    candidate_id INTEGER NOT NULL,
    interviewer_id INTEGER NOT NULL,
    status VARCHAR NOT NULL CHECK (status IN ('active', 'paused', 'completed', 'terminated')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE
);
```

### Indexes
- `session_id`: Unique index for fast lookups
- `candidate_id`: Index for duplicate checking
- `interviewer_id`: Index for interviewer queries

### Constraints
- `session_id`: UNIQUE constraint
- `status`: CHECK constraint for valid values
- `candidate_id`, `interviewer_id`: NOT NULL

---

## 🚀 Performance Optimizations

### 1. Connection Pooling
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,      # Keep 10 connections ready
    max_overflow=20    # Allow 20 extra connections
)
```

### 2. Database Indexes
- Fast lookups by session_id
- Fast duplicate checking by candidate_id

### 3. Efficient Queries
- Use SQLAlchemy ORM for optimized queries
- Avoid N+1 query problems

### 4. Caching
- Settings cached with `@lru_cache()`
- Reduces repeated environment variable reads

---

## 🧪 Testability

### Unit Testing
Each layer can be tested independently:

```python
# Test service layer
def test_create_session():
    mock_db = Mock()
    session = SessionService.create_session(mock_db, data)
    assert session.status == "active"
```

### Integration Testing
Test full request flow:

```python
# Test API endpoint
def test_start_session_endpoint():
    response = client.post("/api/v1/start-session", json={...})
    assert response.status_code == 201
```

---

## 📈 Scalability Considerations

### Current Architecture
- **Single server**: Good for 100-1000 requests/second
- **Single database**: Good for small to medium workloads

### Future Scaling Options

1. **Horizontal Scaling**
   - Add more FastAPI servers behind load balancer
   - Current stateless design supports this

2. **Database Scaling**
   - Add read replicas for GET requests
   - Use connection pooling (already implemented)

3. **Caching Layer**
   - Add Redis for frequently accessed sessions
   - Cache session lookups

4. **Async Operations**
   - FastAPI supports async/await
   - Can add async database operations

---

## 🔧 Maintenance & Monitoring

### Logging
- FastAPI automatic request logging
- SQLAlchemy query logging (when DEBUG=True)

### Health Checks
- `/health` endpoint for monitoring
- Database connection verification

### Error Tracking
- Structured error responses
- HTTP status codes for different error types

---

## 📚 Technology Choices Explained

### Why FastAPI?
- **Fast**: High performance (comparable to Node.js)
- **Modern**: Uses Python 3.8+ features
- **Auto-docs**: Swagger UI generated automatically
- **Type-safe**: Leverages Python type hints
- **Easy**: Simple, intuitive syntax

### Why PostgreSQL?
- **Reliable**: ACID compliance
- **Feature-rich**: Advanced data types, constraints
- **Scalable**: Handles millions of records
- **Popular**: Large community, good tooling

### Why SQLAlchemy?
- **ORM**: Object-relational mapping
- **Safe**: Prevents SQL injection
- **Flexible**: Raw SQL when needed
- **Portable**: Works with multiple databases

### Why Pydantic?
- **Validation**: Automatic data validation
- **Type-safe**: Runtime type checking
- **Documentation**: Auto-generates API docs
- **Performance**: Fast validation using Rust

---

## 🎓 Learning Path

For understanding this architecture:

1. **Start with**: Routes layer (API endpoints)
2. **Then**: Schemas (data validation)
3. **Next**: Services (business logic)
4. **Finally**: Models (database)

Each layer builds on the previous one!

---

**Architecture designed for clarity, maintainability, and growth! 🏗️**
