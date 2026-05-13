# System Diagrams and Visual Guides

Visual representations to help understand the Session Manager Service architecture and flow.

---

## 🏗️ System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  (Browser, Postman, Mobile App, Other Services)                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS Requests
                             │ (JSON)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI APPLICATION                        │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │                    ROUTES LAYER                             │ │
│ │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │ │
│ │  │ Start Session│  │ Get Session  │  │ End Session  │     │ │
│ │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │ │
│ └─────────┼──────────────────┼──────────────────┼─────────────┘ │
│           │                  │                  │               │
│           │    ┌─────────────▼──────────────────┘               │
│           │    │                                                │
│ ┌─────────▼────▼──────────────────────────────────────────────┐ │
│ │                   SERVICES LAYER                            │ │
│ │  ┌────────────────────────────────────────────────────────┐ │ │
│ │  │         SessionService (Business Logic)                │ │ │
│ │  │  • create_session()                                    │ │ │
│ │  │  • get_session_by_id()                                 │ │ │
│ │  │  • update_session_status()                             │ │ │
│ │  │  • end_session()                                       │ │ │
│ │  │  • check_duplicate_active_session()                    │ │ │
│ │  └────────────────────┬───────────────────────────────────┘ │ │
│ └───────────────────────┼─────────────────────────────────────┘ │
│                         │                                       │
│ ┌───────────────────────▼─────────────────────────────────────┐ │
│ │                    MODELS LAYER                             │ │
│ │  ┌────────────────────────────────────────────────────────┐ │ │
│ │  │         SessionModel (SQLAlchemy ORM)                  │ │ │
│ │  │  • id, session_id, candidate_id                        │ │ │
│ │  │  • interviewer_id, status                              │ │ │
│ │  │  • created_at, updated_at, ended_at                    │ │ │
│ │  └────────────────────┬───────────────────────────────────┘ │ │
│ └───────────────────────┼─────────────────────────────────────┘ │
└─────────────────────────┼───────────────────────────────────────┘
                          │
                          │ SQL Queries
                          │ (via psycopg2)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    POSTGRESQL DATABASE                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    sessions TABLE                        │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ id | session_id | candidate_id | interviewer_id  │   │   │
│  │  │ status | created_at | updated_at | ended_at      │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Flow Diagram

### Example: Creating a New Session

```
┌─────────┐
│ CLIENT  │
└────┬────┘
     │
     │ 1. POST /api/v1/start-session
     │    Body: {"candidate_id": 101, "interviewer_id": 201}
     ▼
┌─────────────────┐
│  FastAPI Router │
└────┬────────────┘
     │
     │ 2. Validate request using SessionCreate schema
     │    ✓ candidate_id is positive integer
     │    ✓ interviewer_id is positive integer
     ▼
┌─────────────────┐
│ session_routes  │
└────┬────────────┘
     │
     │ 3. Get database session via Depends(get_db)
     │ 4. Call SessionService.create_session()
     ▼
┌──────────────────┐
│ SessionService   │
└────┬─────────────┘
     │
     │ 5. Check for duplicate active session
     │    Query: SELECT * WHERE candidate_id=101 AND status='active'
     ▼
┌──────────────────┐
│   Database       │
└────┬─────────────┘
     │
     │ 6. No duplicate found ✓
     ▼
┌──────────────────┐
│ SessionService   │
└────┬─────────────┘
     │
     │ 7. Generate UUID: "550e8400-e29b-41d4-a716-446655440000"
     │ 8. Create SessionModel instance
     │ 9. db.add(new_session)
     │ 10. db.commit()
     ▼
┌──────────────────┐
│   Database       │
└────┬─────────────┘
     │
     │ 11. INSERT INTO sessions VALUES (...)
     │ 12. Return created record
     ▼
┌──────────────────┐
│ SessionService   │
└────┬─────────────┘
     │
     │ 13. Return SessionModel object
     ▼
┌─────────────────┐
│ session_routes  │
└────┬────────────┘
     │
     │ 14. Convert to SessionStartResponse schema
     │ 15. Return HTTP 201 Created
     ▼
┌─────────┐
│ CLIENT  │
└─────────┘
     │
     │ 16. Receive JSON response:
     │     {
     │       "session_id": "550e8400-...",
     │       "status": "active",
     │       "created_at": "2024-01-15T10:30:00Z"
     │     }
     ▼
```

---

## 🔄 Session Lifecycle State Machine

```
                    ┌─────────────┐
                    │   START     │
                    │  (Initial)  │
                    └──────┬──────┘
                           │
                           │ POST /start-session
                           │ Generate UUID
                           │ Set status = "active"
                           ▼
                    ┌─────────────┐
              ┌────▶│   ACTIVE    │◀────┐
              │     │  (Running)  │     │
              │     └──────┬──────┘     │
              │            │            │
              │            │ PUT /update-session
              │            │ status = "paused"
              │            ▼            │
              │     ┌─────────────┐    │
              │     │   PAUSED    │    │
              │     │ (Suspended) │    │
              │     └──────┬──────┘    │
              │            │            │
              │            │ PUT /update-session
              │            │ status = "active"
              └────────────┘            │
                           │            │
                           │            │
              ┌────────────┴────────────┘
              │
              │ POST /end-session
              │ OR PUT status = "completed"
              │ Set ended_at timestamp
              ▼
       ┌─────────────┐
       │  COMPLETED  │
       │   (Final)   │
       └─────────────┘
              │
              │ ❌ No further transitions allowed
              │ ❌ Cannot update
              │ ❌ Cannot end again
              ▼
         [IMMUTABLE]


Alternative Path:
       ┌─────────────┐
       │   ACTIVE    │
       │     OR      │
       │   PAUSED    │
       └──────┬──────┘
              │
              │ PUT /update-session
              │ status = "terminated"
              │ (Abrupt end)
              ▼
       ┌─────────────┐
       │ TERMINATED  │
       │   (Final)   │
       └─────────────┘
              │
              │ ❌ No further transitions allowed
              ▼
         [IMMUTABLE]
```

---

## 📊 Database Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    sessions TABLE                       │
├─────────────────────────────────────────────────────────┤
│ PK  id                    SERIAL                        │
│ UK  session_id            VARCHAR(255)                  │
│ FK  candidate_id          INTEGER                       │
│ FK  interviewer_id        INTEGER                       │
│     status                ENUM('active', 'paused',      │
│                                'completed', 'terminated')│
│     created_at            TIMESTAMP WITH TIME ZONE      │
│     updated_at            TIMESTAMP WITH TIME ZONE      │
│     ended_at              TIMESTAMP WITH TIME ZONE      │
└─────────────────────────────────────────────────────────┘
         │                           │
         │                           │
         │ (Future Extension)        │ (Future Extension)
         ▼                           ▼
┌──────────────────┐        ┌──────────────────┐
│   candidates     │        │   interviewers   │
│   (Not in v1)    │        │   (Not in v1)    │
└──────────────────┘        └──────────────────┘

Indexes:
• PRIMARY KEY: id
• UNIQUE INDEX: session_id
• INDEX: candidate_id (for duplicate check)
• INDEX: interviewer_id (for queries)
• INDEX: status (for filtering)
• INDEX: created_at (for sorting)
```

---

## 🔐 Data Flow - Security & Validation

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT REQUEST                           │
│  POST /api/v1/start-session                                 │
│  Body: {"candidate_id": 101, "interviewer_id": 201}         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              LAYER 1: PYDANTIC VALIDATION                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ SessionCreate Schema                                  │  │
│  │ ✓ candidate_id: int (must be > 0)                     │  │
│  │ ✓ interviewer_id: int (must be > 0)                   │  │
│  │ ✓ Type checking                                       │  │
│  │ ✓ Field validation                                    │  │
│  └───────────────────────────────────────────────────────┘  │
│  ❌ If invalid → HTTP 422 Unprocessable Entity              │
└────────────────────────┬────────────────────────────────────┘
                         │ ✓ Valid
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           LAYER 2: BUSINESS LOGIC VALIDATION                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ SessionService.create_session()                       │  │
│  │ ✓ Check duplicate active session                      │  │
│  │ ✓ Verify business rules                              │  │
│  │ ✓ Generate secure UUID                               │  │
│  └───────────────────────────────────────────────────────┘  │
│  ❌ If duplicate → HTTP 400 Bad Request                     │
└────────────────────────┬────────────────────────────────────┘
                         │ ✓ Valid
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              LAYER 3: DATABASE CONSTRAINTS                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ PostgreSQL Constraints                                │  │
│  │ ✓ UNIQUE constraint on session_id                     │  │
│  │ ✓ NOT NULL constraints                                │  │
│  │ ✓ CHECK constraint on status enum                     │  │
│  │ ✓ Data type validation                                │  │
│  └───────────────────────────────────────────────────────┘  │
│  ❌ If constraint violation → HTTP 500 Internal Error       │
└────────────────────────┬────────────────────────────────────┘
                         │ ✓ Valid
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   LAYER 4: SQL INJECTION PREVENTION         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ SQLAlchemy ORM                                        │  │
│  │ ✓ Parameterized queries                               │  │
│  │ ✓ Automatic escaping                                  │  │
│  │ ✓ No raw SQL concatenation                            │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ ✓ Secure
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE STORAGE                         │
│  Record saved securely with all validations passed          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 Testing Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    TESTING METHODS                          │
└─────────────────────────────────────────────────────────────┘
         │
         ├──────────────┬──────────────┬──────────────┐
         │              │              │              │
         ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│  Swagger UI  │ │ Postman  │ │  cURL    │ │ Python Script│
│   (Manual)   │ │ (Manual) │ │(Command) │ │ (Automated)  │
└──────┬───────┘ └────┬─────┘ └────┬─────┘ └──────┬───────┘
       │              │            │              │
       │              │            │              │
       └──────────────┴────────────┴──────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │   FastAPI Application  │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │   PostgreSQL Database  │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │   Verify Results       │
         │   • Status codes       │
         │   • Response data      │
         │   • Database state     │
         │   • Edge cases         │
         └────────────────────────┘
```

---

## 📦 Deployment Architecture (Future)

```
┌─────────────────────────────────────────────────────────────┐
│                      PRODUCTION SETUP                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────┐
│   CLIENTS   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Load Balancer  │ (Nginx/AWS ALB)
└────────┬────────┘
         │
         ├──────────────┬──────────────┐
         ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ FastAPI      │ │ FastAPI      │ │ FastAPI      │
│ Instance 1   │ │ Instance 2   │ │ Instance 3   │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┴────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │ PostgreSQL       │
              │ Primary          │
              └────────┬─────────┘
                       │
                       ├──────────────┐
                       ▼              ▼
              ┌──────────────┐ ┌──────────────┐
              │ PostgreSQL   │ │ PostgreSQL   │
              │ Replica 1    │ │ Replica 2    │
              └──────────────┘ └──────────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Redis Cache      │
              │ (Optional)       │
              └──────────────────┘
```

---

## 🔄 Error Handling Flow

```
┌─────────────┐
│   REQUEST   │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Pydantic Schema  │
│   Validation     │
└────┬─────────────┘
     │
     ├─ Valid ──────────────────────────────┐
     │                                      │
     ├─ Invalid ──→ HTTP 422               │
     │              Unprocessable Entity    │
     │                                      │
     ▼                                      ▼
┌──────────────────┐              ┌──────────────────┐
│ Business Logic   │              │   Continue...    │
│   Validation     │              └──────────────────┘
└────┬─────────────┘
     │
     ├─ Valid ──────────────────────────────┐
     │                                      │
     ├─ Duplicate Session ──→ HTTP 400     │
     │                        Bad Request   │
     │                                      │
     ├─ Session Not Found ──→ HTTP 404     │
     │                        Not Found     │
     │                                      │
     ├─ Cannot Update ──────→ HTTP 400     │
     │                        Bad Request   │
     │                                      │
     ▼                                      ▼
┌──────────────────┐              ┌──────────────────┐
│ Database         │              │   Continue...    │
│   Operation      │              └──────────────────┘
└────┬─────────────┘
     │
     ├─ Success ────────────────────────────┐
     │                                      │
     ├─ Constraint Violation ─→ HTTP 500   │
     │                          Internal    │
     │                                      │
     ├─ Connection Error ────→ HTTP 500    │
     │                         Internal     │
     │                                      │
     ▼                                      ▼
┌──────────────────┐              ┌──────────────────┐
│ Return Success   │              │   Error Response │
│   HTTP 200/201   │              │   with detail    │
└──────────────────┘              └──────────────────┘
```

---

## 📊 Performance Optimization Points

```
┌─────────────────────────────────────────────────────────────┐
│                  OPTIMIZATION LAYERS                        │
└─────────────────────────────────────────────────────────────┘

1. APPLICATION LAYER
   ┌────────────────────────────────────┐
   │ • Connection Pooling (10 + 20)     │
   │ • Settings Caching (@lru_cache)    │
   │ • Async/Await Support (Future)     │
   └────────────────────────────────────┘

2. DATABASE LAYER
   ┌────────────────────────────────────┐
   │ • Indexes on key columns           │
   │ • Query optimization               │
   │ • Connection reuse                 │
   └────────────────────────────────────┘

3. CACHING LAYER (Future)
   ┌────────────────────────────────────┐
   │ • Redis for session lookups        │
   │ • Cache frequently accessed data   │
   │ • TTL-based invalidation           │
   └────────────────────────────────────┘

4. NETWORK LAYER (Future)
   ┌────────────────────────────────────┐
   │ • Load balancing                   │
   │ • CDN for static content           │
   │ • Compression                      │
   └────────────────────────────────────┘
```

---

**These diagrams provide visual understanding of the system architecture and flows! 📊**
