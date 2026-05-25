import sys
from fastapi.testclient import TestClient
from main import app

def test_api():
    with TestClient(app) as client:
        print("Testing /login (admin / admin123)...")
        response = client.post("/login", json={"username": "admin", "password": "admin123"})
        assert response.status_code == 200
        print("Login successful:", response.json())
        
        print("Testing invalid login...")
        response = client.post("/login", json={"username": "admin", "password": "wrongpassword"})
        assert response.status_code == 401
        print("Invalid login correctly blocked.")
        
        print("All tests passed.")

if __name__ == "__main__":
    test_api()
