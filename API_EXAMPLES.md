# API Examples - Complete Request/Response Guide

Comprehensive examples for all API endpoints with various scenarios.

---

## 🔌 Base URL

```
Local Development: http://localhost:8000
API Base Path: /api/v1
```

---

## 1️⃣ Start Session

### Endpoint
```
POST /api/v1/start-session
```

### Success Case

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/start-session" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 101,
    "interviewer_id": 201
  }'
```

**Response:** `201 Created`
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "active",
  "created_at": "2024-01-15T10:30:00.123456Z"
}
```

### Error Case: Duplicate Active Session

**Request:**
```bash
# First request succeeds
curl -X POST "http://localhost:8000/api/v1/start-session" \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": 101, "interviewer_id": 201}'

# Second request for same candidate fails
curl -X POST "http://localhost:8000/api/v1/start-session" \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": 101, "interviewer_id": 202}'
```

**Response:** `400 Bad Request`
```json
{
  "detail": "Candidate 101 already has an active session"
}
```

### Error Case: Invalid Input

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/start-session" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": -5,
    "interviewer_id": 201
  }'
```

**Response:** `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "candidate_id"],
      "msg": "Input should be greater than 0",
      "input": -5
    }
  ]
}
```

---

## 2️⃣ Get Session by ID

### Endpoint
```
GET /api/v1/session/{session_id}
```

### Success Case

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/session/550e8400-e29b-41d4-a716-446655440000"
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "candidate_id": 101,
  "interviewer_id": 201,
  "status": "active",
  "created_at": "2024-01-15T10:30:00.123456Z",
  "updated_at": "2024-01-15T10:30:00.123456Z",
  "ended_at": null
}
```

### Error Case: Session Not Found

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/session/invalid-uuid-12345"
```

**Response:** `404 Not Found`
```json
{
  "detail": "Session with ID invalid-uuid-12345 not found"
}
```

---

## 3️⃣ Get All Sessions

### Endpoint
```
GET /api/v1/sessions
```

### Success Case

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/sessions"
```

**Response:** `200 OK`
```json
[
  {
    "id": 3,
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "candidate_id": 103,
    "interviewer_id": 203,
    "status": "active",
    "created_at": "2024-01-15T11:00:00.123456Z",
    "updated_at": "2024-01-15T11:00:00.123456Z",
    "ended_at": null
  },
  {
    "id": 2,
    "session_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "candidate_id": 102,
    "interviewer_id": 202,
    "status": "completed",
    "created_at": "2024-01-15T10:45:00.123456Z",
    "updated_at": "2024-01-15T10:55:00.123456Z",
    "ended_at": "2024-01-15T10:55:00.123456Z"
  },
  {
    "id": 1,
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "candidate_id": 101,
    "interviewer_id": 201,
    "status": "paused",
    "created_at": "2024-01-15T10:30:00.123456Z",
    "updated_at": "2024-01-15T10:40:00.123456Z",
    "ended_at": null
  }
]
```

### Empty Case

**Response:** `200 OK`
```json
[]
```

---

## 4️⃣ Update Session Status

### Endpoint
```
PUT /api/v1/update-session/{session_id}
```

### Success Case: Active to Paused

**Request:**
```bash
curl -X PUT "http://localhost:8000/api/v1/update-session/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "paused"
  }'
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "candidate_id": 101,
  "interviewer_id": 201,
  "status": "paused",
  "created_at": "2024-01-15T10:30:00.123456Z",
  "updated_at": "2024-01-15T10:35:00.789012Z",
  "ended_at": null
}
```

### Success Case: Paused to Active

**Request:**
```bash
curl -X PUT "http://localhost:8000/api/v1/update-session/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "active"
  }'
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "candidate_id": 101,
  "interviewer_id": 201,
  "status": "active",
  "created_at": "2024-01-15T10:30:00.123456Z",
  "updated_at": "2024-01-15T10:40:00.456789Z",
  "ended_at": null
}
```

### Success Case: Active to Terminated

**Request:**
```bash
curl -X PUT "http://localhost:8000/api/v1/update-session/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "terminated"
  }'
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "candidate_id": 101,
  "interviewer_id": 201,
  "status": "terminated",
  "created_at": "2024-01-15T10:30:00.123456Z",
  "updated_at": "2024-01-15T10:45:00.123456Z",
  "ended_at": null
}
```

### Error Case: Update Completed Session

**Request:**
```bash
# Session is already completed
curl -X PUT "http://localhost:8000/api/v1/update-session/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "active"
  }'
```

**Response:** `400 Bad Request`
```json
{
  "detail": "Cannot update a completed session"
}
```

### Error Case: Update Terminated Session

**Request:**
```bash
# Session is already terminated
curl -X PUT "http://localhost:8000/api/v1/update-session/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "active"
  }'
```

**Response:** `400 Bad Request`
```json
{
  "detail": "Cannot update a terminated session"
}
```

### Error Case: Invalid Status

**Request:**
```bash
curl -X PUT "http://localhost:8000/api/v1/update-session/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "invalid_status"
  }'
```

**Response:** `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "type": "enum",
      "loc": ["body", "status"],
      "msg": "Input should be 'active', 'paused', 'completed' or 'terminated'",
      "input": "invalid_status"
    }
  ]
}
```

---

## 5️⃣ End Session

### Endpoint
```
POST /api/v1/end-session/{session_id}
```

### Success Case

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/end-session/550e8400-e29b-41d4-a716-446655440000"
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "candidate_id": 101,
  "interviewer_id": 201,
  "status": "completed",
  "created_at": "2024-01-15T10:30:00.123456Z",
  "updated_at": "2024-01-15T11:00:00.789012Z",
  "ended_at": "2024-01-15T11:00:00.789012Z"
}
```

### Error Case: End Already Completed Session

**Request:**
```bash
# Try to end the same session again
curl -X POST "http://localhost:8000/api/v1/end-session/550e8400-e29b-41d4-a716-446655440000"
```

**Response:** `400 Bad Request`
```json
{
  "detail": "Session is already completed"
}
```

### Error Case: Session Not Found

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/end-session/nonexistent-uuid"
```

**Response:** `404 Not Found`
```json
{
  "detail": "Session with ID nonexistent-uuid not found"
}
```

---

## 6️⃣ Health Check Endpoints

### Root Endpoint

**Request:**
```bash
curl -X GET "http://localhost:8000/"
```

**Response:** `200 OK`
```json
{
  "service": "Session Manager Service",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

### Health Endpoint

**Request:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "Session Manager Service"
}
```

---

## 🧪 Complete Test Scenario

### Scenario: Full Session Lifecycle

```bash
# 1. Start a new session
SESSION_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/start-session" \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": 101, "interviewer_id": 201}')

echo "Started session: $SESSION_RESPONSE"

# Extract session_id (requires jq)
SESSION_ID=$(echo $SESSION_RESPONSE | jq -r '.session_id')
echo "Session ID: $SESSION_ID"

# 2. Get session details
curl -X GET "http://localhost:8000/api/v1/session/$SESSION_ID"

# 3. Pause the session
curl -X PUT "http://localhost:8000/api/v1/update-session/$SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "paused"}'

# 4. Resume the session
curl -X PUT "http://localhost:8000/api/v1/update-session/$SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'

# 5. End the session
curl -X POST "http://localhost:8000/api/v1/end-session/$SESSION_ID"

# 6. Verify session is completed
curl -X GET "http://localhost:8000/api/v1/session/$SESSION_ID"

# 7. Try to update (should fail)
curl -X PUT "http://localhost:8000/api/v1/update-session/$SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

---

## 🐍 Python Examples

### Using requests library

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 1. Start session
response = requests.post(
    f"{BASE_URL}/start-session",
    json={
        "candidate_id": 101,
        "interviewer_id": 201
    }
)
print(f"Status: {response.status_code}")
session_data = response.json()
print(f"Response: {json.dumps(session_data, indent=2)}")
session_id = session_data["session_id"]

# 2. Get session
response = requests.get(f"{BASE_URL}/session/{session_id}")
print(f"Session: {json.dumps(response.json(), indent=2)}")

# 3. Update session
response = requests.put(
    f"{BASE_URL}/update-session/{session_id}",
    json={"status": "paused"}
)
print(f"Updated: {json.dumps(response.json(), indent=2)}")

# 4. Get all sessions
response = requests.get(f"{BASE_URL}/sessions")
print(f"All sessions: {len(response.json())} found")

# 5. End session
response = requests.post(f"{BASE_URL}/end-session/{session_id}")
print(f"Ended: {json.dumps(response.json(), indent=2)}")
```

---

## 📱 Postman Collection JSON

```json
{
  "info": {
    "name": "Session Manager API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Start Session",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"candidate_id\": 101,\n  \"interviewer_id\": 201\n}"
        },
        "url": {
          "raw": "{{base_url}}/start-session",
          "host": ["{{base_url}}"],
          "path": ["start-session"]
        }
      },
      "response": []
    },
    {
      "name": "Get Session",
      "request": {
        "method": "GET",
        "url": {
          "raw": "{{base_url}}/session/{{session_id}}",
          "host": ["{{base_url}}"],
          "path": ["session", "{{session_id}}"]
        }
      },
      "response": []
    },
    {
      "name": "Get All Sessions",
      "request": {
        "method": "GET",
        "url": {
          "raw": "{{base_url}}/sessions",
          "host": ["{{base_url}}"],
          "path": ["sessions"]
        }
      },
      "response": []
    },
    {
      "name": "Update Session",
      "request": {
        "method": "PUT",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"status\": \"paused\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/update-session/{{session_id}}",
          "host": ["{{base_url}}"],
          "path": ["update-session", "{{session_id}}"]
        }
      },
      "response": []
    },
    {
      "name": "End Session",
      "request": {
        "method": "POST",
        "url": {
          "raw": "{{base_url}}/end-session/{{session_id}}",
          "host": ["{{base_url}}"],
          "path": ["end-session", "{{session_id}}"]
        }
      },
      "response": []
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000/api/v1"
    },
    {
      "key": "session_id",
      "value": ""
    }
  ]
}
```

---

## 🔍 Response Status Code Summary

| Status Code | Meaning | When It Occurs |
|-------------|---------|----------------|
| 200 | OK | Successful GET, PUT requests |
| 201 | Created | Successful POST (session created) |
| 400 | Bad Request | Business logic error (duplicate, update completed) |
| 404 | Not Found | Session doesn't exist |
| 422 | Unprocessable Entity | Validation error (invalid input) |
| 500 | Internal Server Error | Unexpected server error |

---

**Use these examples to test and understand the API! 🚀**
