# Viva Questions & Answers

Common questions asked during project viva/presentation with detailed answers.

---

## 🎯 Project Overview Questions

### Q1: What is this project about?
**Answer**: This is a Session Manager Service for an AI Interview Platform. It manages the complete lifecycle of interview sessions - from starting a session with unique IDs, tracking status changes (active, paused, completed, terminated), to ending sessions with proper timestamp recording. It's built using FastAPI and PostgreSQL.

### Q2: Why did you choose FastAPI?
**Answer**: I chose FastAPI because:
1. **Performance**: It's one of the fastest Python frameworks, comparable to Node.js
2. **Automatic Documentation**: It generates Swagger UI and ReDoc automatically
3. **Type Safety**: Uses Python type hints for validation
4. **Modern**: Supports async/await for high concurrency
5. **Easy to Learn**: Clean syntax, perfect for beginners
6. **Industry Standard**: Used by companies like Microsoft, Uber, and Netflix

### Q3: Why PostgreSQL instead of MySQL or MongoDB?
**Answer**: PostgreSQL because:
1. **ACID Compliance**: Ensures data consistency and reliability
2. **Advanced Features**: Better support for constraints, triggers, and data types
3. **Scalability**: Handles millions of records efficiently
4. **Open Source**: Free and well-documented
5. **Relational Model**: Perfect for structured data like sessions with clear relationships

---

## 🏗️ Architecture Questions

### Q4: Explain your project architecture
**Answer**: The project follows a **layered architecture**:
1. **Routes Layer**: Handles HTTP requests/responses
2. **Services Layer**: Contains business logic
3. **Models Layer**: Defines database structure using SQLAlchemy ORM
4. **Schemas Layer**: Validates data using Pydantic
5. **Database Layer**: Manages connections and sessions

This separation makes the code modular, testable, and maintainable.

### Q5: What is the difference between Models and Schemas?
**Answer**:
- **Models** (SQLAlchemy): Define database table structure, map Python classes to database tables
- **Schemas** (Pydantic): Define API request/response structure, validate incoming data

Example: SessionModel defines how data is stored in database, SessionCreate defines what data the API accepts.

### Q6: What design patterns did you use?
**Answer**:
1. **Dependency Injection**: For database session management
2. **Repository Pattern**: Service layer abstracts data access
3. **DTO Pattern**: Pydantic schemas for data transfer
4. **Singleton Pattern**: Configuration settings cached with @lru_cache()
5. **Factory Pattern**: UUID generation centralized in service

---

## 🔄 Session Lifecycle Questions

### Q7: Explain the session lifecycle
**Answer**: 
```
START → active → paused → active → completed
                    ↓
                terminated
```

1. **active**: Session is ongoing
2. **paused**: Temporarily stopped, can resume
3. **completed**: Successfully finished (final state)
4. **terminated**: Abruptly ended (final state)

Once completed or terminated, sessions cannot be modified.

### Q8: How do you prevent duplicate active sessions?
**Answer**: Before creating a new session, I query the database to check if the candidate already has an active session:
```python
existing_session = db.query(SessionModel).filter(
    and_(
        SessionModel.candidate_id == candidate_id,
        SessionModel.status == SessionStatus.ACTIVE
    )
).first()
```
If found, return HTTP 400 error. This prevents duplicate active sessions for the same candidate.

---

## 🗃️ Database Questions

### Q9: Explain your database schema
**Answer**: The sessions table has:
- **id**: Primary key (auto-increment)
- **session_id**: Unique UUID for each session
- **candidate_id**: Reference to candidate
- **interviewer_id**: Reference to interviewer
- **status**: Enum (active, paused, completed, terminated)
- **created_at**: Timestamp when session started
- **updated_at**: Timestamp of last update
- **ended_at**: Timestamp when session ended (nullable)

Indexes on session_id, candidate_id for fast queries.

### Q10: How do you handle timestamps?
**Answer**: 
- **created_at**: Set automatically by database using `server_default=func.now()`
- **updated_at**: Set on insert and updated automatically using `onupdate=func.now()`
- **ended_at**: Set manually when session ends using `datetime.utcnow()`

All timestamps use UTC timezone for consistency.

### Q11: What is SQLAlchemy ORM?
**Answer**: SQLAlchemy is an Object-Relational Mapping (ORM) library that:
1. Maps Python classes to database tables
2. Converts Python objects to SQL queries automatically
3. Prevents SQL injection through parameterized queries
4. Provides database abstraction (works with multiple databases)
5. Makes database operations more Pythonic

---

## 🔐 Security Questions

### Q12: How do you prevent SQL injection?
**Answer**: I use SQLAlchemy ORM which automatically uses parameterized queries. User input is never directly concatenated into SQL strings. All queries use placeholders that are safely escaped by the database driver.

### Q13: How do you validate input data?
**Answer**: Using Pydantic schemas with:
1. **Type validation**: Ensures correct data types
2. **Field constraints**: e.g., `Field(..., gt=0)` ensures positive integers
3. **Enum validation**: Status must be one of predefined values
4. **Automatic validation**: FastAPI validates before reaching route handler

Invalid data returns HTTP 422 Unprocessable Entity.

---

## ⚠️ Error Handling Questions

### Q14: What HTTP status codes do you use?
**Answer**:
- **200 OK**: Successful GET/PUT requests
- **201 Created**: Successful POST (session created)
- **400 Bad Request**: Business logic errors (duplicate session, updating completed session)
- **404 Not Found**: Session doesn't exist
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Unexpected server errors

### Q15: How do you handle errors?
**Answer**: Using FastAPI's HTTPException:
```python
if not session:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Session not found"
    )
```
FastAPI automatically converts this to proper JSON error response.

---

## 🧪 Testing Questions

### Q16: How did you test your API?
**Answer**: Multiple methods:
1. **Swagger UI**: Interactive testing at /docs
2. **Postman**: Professional API testing with collections
3. **Python Script**: Automated test script (test_api.py)
4. **cURL**: Command-line testing
5. **Database Verification**: Direct PostgreSQL queries

### Q17: What edge cases did you handle?
**Answer**:
1. Duplicate active sessions for same candidate
2. Invalid session IDs (404 error)
3. Updating completed/terminated sessions (400 error)
4. Ending already completed sessions (400 error)
5. Invalid status values (422 validation error)
6. Concurrent updates (database transactions)

---

## 🚀 Performance Questions

### Q18: How do you handle concurrent requests?
**Answer**:
1. **Connection Pooling**: Maintain pool of database connections (pool_size=10, max_overflow=20)
2. **Database Transactions**: Each operation is atomic
3. **Row-Level Locking**: PostgreSQL locks rows during updates
4. **Stateless Design**: Each request is independent

### Q19: How would you scale this application?
**Answer**:
1. **Horizontal Scaling**: Add more FastAPI servers behind load balancer (already stateless)
2. **Database Scaling**: Add read replicas for GET requests
3. **Caching**: Add Redis for frequently accessed sessions
4. **Async Operations**: Convert to async/await for better concurrency
5. **Database Indexing**: Already implemented on key columns

---

## 🔧 Implementation Questions

### Q20: What is dependency injection in FastAPI?
**Answer**: Dependency injection automatically provides resources to route handlers:
```python
def endpoint(db: Session = Depends(get_db)):
    # db is automatically provided and cleaned up
```
Benefits:
- Automatic resource management
- Easy testing (can inject mocks)
- Clean code (no manual setup/teardown)

### Q21: How does UUID generation work?
**Answer**: Using Python's uuid module:
```python
import uuid
session_id = str(uuid.uuid4())
```
UUID4 generates random 128-bit identifiers with extremely low collision probability (1 in 2^122). Perfect for distributed systems.

### Q22: What is Pydantic?
**Answer**: Pydantic is a data validation library that:
1. Validates data using Python type hints
2. Converts data types automatically
3. Provides clear error messages
4. Generates JSON schemas for documentation
5. Ensures type safety at runtime

---

## 💡 Conceptual Questions

### Q23: What is REST API?
**Answer**: REST (Representational State Transfer) is an architectural style where:
1. Resources are identified by URLs
2. HTTP methods define operations (GET, POST, PUT, DELETE)
3. Stateless communication
4. Standard status codes
5. JSON for data exchange

Example: `GET /session/123` retrieves session 123

### Q24: What is ORM?
**Answer**: Object-Relational Mapping (ORM) bridges object-oriented programming and relational databases:
- Maps classes to tables
- Maps objects to rows
- Maps attributes to columns
- Converts method calls to SQL queries

Benefits: More Pythonic, prevents SQL injection, database-agnostic.

### Q25: Difference between PUT and POST?
**Answer**:
- **POST**: Create new resource (e.g., start new session)
- **PUT**: Update existing resource (e.g., update session status)

POST is not idempotent (multiple calls create multiple resources).
PUT is idempotent (multiple calls have same effect).

---

## 🎓 Learning Questions

### Q26: What did you learn from this project?
**Answer**:
1. Building REST APIs with FastAPI
2. Database design and PostgreSQL
3. ORM concepts with SQLAlchemy
4. Data validation with Pydantic
5. Error handling and edge cases
6. API documentation and testing
7. Project structure and architecture

### Q27: What challenges did you face?
**Answer**:
1. **Database Connection**: Learning connection pooling and session management
2. **Timestamp Management**: Understanding server-side vs application-side timestamps
3. **Edge Cases**: Identifying and handling all possible error scenarios
4. **Testing**: Creating comprehensive test cases
5. **Documentation**: Writing clear, beginner-friendly documentation

### Q28: How would you improve this project?
**Answer**:
1. Add JWT authentication
2. Implement session duration tracking
3. Add WebSocket for real-time updates
4. Create admin dashboard
5. Add comprehensive logging
6. Implement rate limiting
7. Add unit and integration tests
8. Deploy to cloud (AWS/Heroku)

---

## 🔍 Deep Dive Questions

### Q29: Explain the request flow for starting a session
**Answer**:
1. Client sends POST request to /api/v1/start-session
2. FastAPI receives request, validates using SessionCreate schema
3. Route handler calls SessionService.create_session()
4. Service checks for duplicate active sessions
5. If no duplicate, generates UUID
6. Creates SessionModel instance
7. SQLAlchemy converts to SQL INSERT
8. PostgreSQL executes query, returns created record
9. Service returns SessionModel
10. Route converts to SessionStartResponse
11. FastAPI serializes to JSON
12. Client receives HTTP 201 with session data

### Q30: How does database session management work?
**Answer**: Using FastAPI's dependency injection:
```python
def get_db():
    db = SessionLocal()  # Create session
    try:
        yield db  # Provide to route
    finally:
        db.close()  # Always cleanup
```
Each request gets isolated database session, automatically closed after request completes. Prevents connection leaks.

---

**Pro Tip**: Practice explaining these concepts in your own words. Understanding is more important than memorization! 🎓
