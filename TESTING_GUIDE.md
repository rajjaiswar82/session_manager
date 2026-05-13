# Testing Guide for Session Manager Service

This guide provides step-by-step instructions for testing the Session Manager Service.

---

## 🧪 Testing Methods

1. **Swagger UI** (Recommended for beginners)
2. **Postman** (Professional API testing)
3. **cURL** (Command line testing)
4. **Python Requests** (Programmatic testing)

---

## 1️⃣ Testing with Swagger UI

### Step 1: Start the Server
```bash
cd session_manager
uvicorn app.main:app --reload
```

### Step 2: Open Swagger UI
Open browser and navigate to: `http://localhost:8000/docs`

### Step 3: Test Each Endpoint

#### A. Start a Session
1. Click on **POST /api/v1/start-session**
2. Click **"Try it out"**
3. Enter request body:
```json
{
  "candidate_id": 101,
  "interviewer_id": 201
}
```
4. Click **"Execute"**
5. Copy the `session_id` from response

#### B. Get Session Details
1. Click on **GET /api/v1/session/{session_id}**
2. Click **"Try it out"**
3. Paste the `session_id` from previous step
4. Click **"Execute"**

#### C. Update Session Status
1. Click on **PUT /api/v1/update-session/{session_id}**
2. Click **"Try it out"**
3. Paste the `session_id`
4. Enter request body:
```json
{
  "status": "paused"
}
```
5. Click **"Execute"**

#### D. Get All Sessions
1. Click on **GET /api/v1/sessions**
2. Click **"Try it out"**
3. Click **"Execute"**

#### E. End Session
1. Click on **POST /api/v1/end-session/{session_id}**
2. Click **"Try it out"**
3. Paste the `session_id`
4. Click **"Execute"**

---

## 2️⃣ Testing with Postman

### Setup Postman Collection

#### 1. Create New Collection
- Open Postman
- Click "New" → "Collection"
- Name it "Session Manager API"

#### 2. Add Environment Variables
- Click "Environments" → "Create Environment"
- Name: "Local Development"
- Add variable:
  - `base_url`: `http://localhost:8000/api/v1`
  - `session_id`: (leave empty, will be set dynamically)

#### 3. Create Requests

**Request 1: Start Session**
- Method: `POST`
- URL: `{{base_url}}/start-session`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
  "candidate_id": 101,
  "interviewer_id": 201
}
```
- Tests (to save session_id):
```javascript
var jsonData = pm.response.json();
pm.environment.set("session_id", jsonData.session_id);
```

**Request 2: Get Session**
- Method: `GET`
- URL: `{{base_url}}/session/{{session_id}}`

**Request 3: Get All Sessions**
- Method: `GET`
- URL: `{{base_url}}/sessions`

**Request 4: Update Session**
- Method: `PUT`
- URL: `{{base_url}}/update-session/{{session_id}}`
- Body (raw JSON):
```json
{
  "status": "paused"
}
```

**Request 5: End Session**
- Method: `POST`
- URL: `{{base_url}}/end-session/{{session_id}}`

### Testing Flow
1. Run "Start Session" → saves session_id automatically
2. Run "Get Session" → uses saved session_id
3. Run "Update Session" → changes status to paused
4. Run "Get Session" → verify status changed
5. Run "End Session" → marks as completed
6. Run "Get All Sessions" → see all sessions

---

## 3️⃣ Testing with cURL

### Start Session
```bash
curl -X POST "http://localhost:8000/api/v1/start-session" \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": 101, "interviewer_id": 201}'
```

### Get Session
```bash
curl -X GET "http://localhost:8000/api/v1/session/{session_id}"
```

### Get All Sessions
```bash
curl -X GET "http://localhost:8000/api/v1/sessions"
```

### Update Session
```bash
curl -X PUT "http://localhost:8000/api/v1/update-session/{session_id}" \
  -H "Content-Type: application/json" \
  -d '{"status": "paused"}'
```

### End Session
```bash
curl -X POST "http://localhost:8000/api/v1/end-session/{session_id}"
```

---

## 4️⃣ Testing with Python

Create a test script `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_session_lifecycle():
    # 1. Start session
    print("1. Starting session...")
    response = requests.post(
        f"{BASE_URL}/start-session",
        json={"candidate_id": 101, "interviewer_id": 201}
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    session_id = data["session_id"]
    
    # 2. Get session
    print("\n2. Getting session details...")
    response = requests.get(f"{BASE_URL}/session/{session_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 3. Update session
    print("\n3. Updating session to paused...")
    response = requests.put(
        f"{BASE_URL}/update-session/{session_id}",
        json={"status": "paused"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 4. Get all sessions
    print("\n4. Getting all sessions...")
    response = requests.get(f"{BASE_URL}/sessions")
    print(f"Status: {response.status_code}")
    print(f"Found {len(response.json())} sessions")
    
    # 5. End session
    print("\n5. Ending session...")
    response = requests.post(f"{BASE_URL}/end-session/{session_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_session_lifecycle()
```

Run the test:
```bash
python test_api.py
```

---

## 🧪 Edge Case Testing

### Test 1: Duplicate Active Session
```bash
# Start first session
curl -X POST "http://localhost:8000/api/v1/start-session" \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": 101, "interviewer_id": 201}'

# Try to start another session for same candidate
curl -X POST "http://localhost:8000/api/v1/start-session" \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": 101, "interviewer_id": 202}'

# Expected: 400 Bad Request - "Candidate 101 already has an active session"
```

### Test 2: Invalid Session ID
```bash
curl -X GET "http://localhost:8000/api/v1/session/invalid-uuid"

# Expected: 404 Not Found - "Session with ID invalid-uuid not found"
```

### Test 3: Update Completed Session
```bash
# First, end a session
curl -X POST "http://localhost:8000/api/v1/end-session/{session_id}"

# Then try to update it
curl -X PUT "http://localhost:8000/api/v1/update-session/{session_id}" \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'

# Expected: 400 Bad Request - "Cannot update a completed session"
```

### Test 4: End Already Completed Session
```bash
# End session twice
curl -X POST "http://localhost:8000/api/v1/end-session/{session_id}"
curl -X POST "http://localhost:8000/api/v1/end-session/{session_id}"

# Expected: 400 Bad Request - "Session is already completed"
```

### Test 5: Invalid Status Value
```bash
curl -X PUT "http://localhost:8000/api/v1/update-session/{session_id}" \
  -H "Content-Type: application/json" \
  -d '{"status": "invalid_status"}'

# Expected: 422 Unprocessable Entity - Validation error
```

---

## 📊 Expected HTTP Status Codes

| Scenario | Status Code | Description |
|----------|-------------|-------------|
| Successful creation | 201 | Created |
| Successful retrieval | 200 | OK |
| Successful update | 200 | OK |
| Session not found | 404 | Not Found |
| Duplicate session | 400 | Bad Request |
| Invalid status | 422 | Unprocessable Entity |
| Update completed session | 400 | Bad Request |
| Server error | 500 | Internal Server Error |

---

## 🔍 Verifying Database

### Connect to PostgreSQL
```bash
psql -U postgres -d session_manager
```

### Check Sessions Table
```sql
-- View all sessions
SELECT * FROM sessions;

-- View active sessions
SELECT * FROM sessions WHERE status = 'active';

-- View completed sessions
SELECT * FROM sessions WHERE status = 'completed';

-- Count sessions by status
SELECT status, COUNT(*) FROM sessions GROUP BY status;
```

---

## 📝 Test Checklist

- [ ] Server starts without errors
- [ ] Swagger UI loads at /docs
- [ ] Can create new session
- [ ] Session ID is valid UUID
- [ ] Can retrieve session by ID
- [ ] Can retrieve all sessions
- [ ] Can update session status
- [ ] Can end session
- [ ] Duplicate session prevention works
- [ ] Cannot update completed session
- [ ] Cannot end completed session
- [ ] Invalid session ID returns 404
- [ ] Invalid status returns 422
- [ ] Timestamps are recorded correctly
- [ ] Database records match API responses

---

## 🐛 Common Issues

### Issue: Connection Refused
**Cause**: Server not running
**Solution**: Start server with `uvicorn app.main:app --reload`

### Issue: Database Connection Error
**Cause**: PostgreSQL not running or wrong credentials
**Solution**: Check PostgreSQL service and .env file

### Issue: 404 on All Endpoints
**Cause**: Wrong URL or port
**Solution**: Verify using `http://localhost:8000/api/v1/...`

### Issue: 422 Validation Error
**Cause**: Invalid request body format
**Solution**: Check JSON syntax and required fields

---

**Happy Testing! 🧪**
