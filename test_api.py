"""
Sample test script for Session Manager API
Run this after starting the server to test all endpoints
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000/api/v1"


def print_response(title: str, response: requests.Response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"📍 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2, default=str)}")
    except:
        print(f"Response: {response.text}")


def test_session_lifecycle():
    """Test complete session lifecycle"""
    
    print("\n🚀 Starting Session Manager API Tests")
    print("="*60)
    
    session_id: Optional[str] = None
    
    try:
        # Test 1: Start Session
        print("\n✅ Test 1: Start Session")
        response = requests.post(
            f"{BASE_URL}/start-session",
            json={
                "candidate_id": 101,
                "interviewer_id": 201
            }
        )
        print_response("POST /start-session", response)
        
        if response.status_code == 201:
            session_id = response.json()["session_id"]
            print(f"\n✨ Session created with ID: {session_id}")
        else:
            print("\n❌ Failed to create session")
            return
        
        # Test 2: Get Session by ID
        print("\n✅ Test 2: Get Session by ID")
        response = requests.get(f"{BASE_URL}/session/{session_id}")
        print_response(f"GET /session/{session_id}", response)
        
        # Test 3: Get All Sessions
        print("\n✅ Test 3: Get All Sessions")
        response = requests.get(f"{BASE_URL}/sessions")
        print_response("GET /sessions", response)
        
        if response.status_code == 200:
            sessions = response.json()
            print(f"\n📊 Total sessions found: {len(sessions)}")
        
        # Test 4: Update Session Status to Paused
        print("\n✅ Test 4: Update Session Status to Paused")
        response = requests.put(
            f"{BASE_URL}/update-session/{session_id}",
            json={"status": "paused"}
        )
        print_response(f"PUT /update-session/{session_id}", response)
        
        # Test 5: Update Session Status back to Active
        print("\n✅ Test 5: Update Session Status to Active")
        response = requests.put(
            f"{BASE_URL}/update-session/{session_id}",
            json={"status": "active"}
        )
        print_response(f"PUT /update-session/{session_id}", response)
        
        # Test 6: End Session
        print("\n✅ Test 6: End Session")
        response = requests.post(f"{BASE_URL}/end-session/{session_id}")
        print_response(f"POST /end-session/{session_id}", response)
        
        # Test 7: Try to update completed session (should fail)
        print("\n✅ Test 7: Try to Update Completed Session (Should Fail)")
        response = requests.put(
            f"{BASE_URL}/update-session/{session_id}",
            json={"status": "active"}
        )
        print_response(f"PUT /update-session/{session_id}", response)
        
        if response.status_code == 400:
            print("\n✨ Correctly prevented updating completed session")
        
        # Test 8: Try to end completed session (should fail)
        print("\n✅ Test 8: Try to End Completed Session (Should Fail)")
        response = requests.post(f"{BASE_URL}/end-session/{session_id}")
        print_response(f"POST /end-session/{session_id}", response)
        
        if response.status_code == 400:
            print("\n✨ Correctly prevented ending completed session")
        
        # Test 9: Test duplicate active session prevention
        print("\n✅ Test 9: Test Duplicate Active Session Prevention")
        response = requests.post(
            f"{BASE_URL}/start-session",
            json={
                "candidate_id": 102,
                "interviewer_id": 202
            }
        )
        print_response("POST /start-session (Candidate 102)", response)
        
        if response.status_code == 201:
            # Try to create another session for same candidate
            response = requests.post(
                f"{BASE_URL}/start-session",
                json={
                    "candidate_id": 102,
                    "interviewer_id": 203
                }
            )
            print_response("POST /start-session (Duplicate for Candidate 102)", response)
            
            if response.status_code == 400:
                print("\n✨ Correctly prevented duplicate active session")
        
        # Test 10: Test invalid session ID
        print("\n✅ Test 10: Test Invalid Session ID")
        response = requests.get(f"{BASE_URL}/session/invalid-uuid-12345")
        print_response("GET /session/invalid-uuid-12345", response)
        
        if response.status_code == 404:
            print("\n✨ Correctly returned 404 for invalid session ID")
        
        print("\n" + "="*60)
        print("🎉 All tests completed!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server")
        print("Make sure the server is running:")
        print("  uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def test_health_check():
    """Test health check endpoints"""
    print("\n🏥 Testing Health Check Endpoints")
    print("="*60)
    
    try:
        # Test root endpoint
        response = requests.get("http://localhost:8000/")
        print_response("GET /", response)
        
        # Test health endpoint
        response = requests.get("http://localhost:8000/health")
        print_response("GET /health", response)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server")


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║       Session Manager Service - API Test Suite          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Test health check first
    test_health_check()
    
    # Run main tests
    test_session_lifecycle()
    
    print("\n✅ Test suite completed!\n")
