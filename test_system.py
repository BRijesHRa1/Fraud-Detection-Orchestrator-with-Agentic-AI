"""
Simple test script for the Fraud Detection System
Run this after starting the main application
"""

import requests
import json
from datetime import datetime
import uuid

# API base URL - automatically detects Docker or local setup
import os
BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# Try Docker URL first, then local
def get_base_url():
    docker_url = "http://localhost:8000"
    local_url = "http://127.0.0.1:8000"
    
    try:
        import requests
        response = requests.get(f"{docker_url}/api/v1/fraud/health", timeout=2)
        if response.status_code == 200:
            return docker_url
    except:
        pass
    
    return local_url

BASE_URL = get_base_url()

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/api/v1/fraud/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_quick_test():
    """Test the quick test endpoint"""
    print("🔍 Testing quick test endpoint...")
    response = requests.post(f"{BASE_URL}/api/v1/fraud/quick-test")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Transaction Amount: ${result['test_transaction']['amount']}")
    print(f"Fraud Detected: {result['prediction']['is_fraud']}")
    print(f"Confidence Score: {result['prediction']['confidence_score']:.2f}")
    print(f"Action: {result['action']}")
    print(f"Processing Time: {result['prediction']['processing_time_ms']}ms")
    print()

def test_custom_transaction():
    """Test with a custom transaction"""
    print("🔍 Testing custom transaction...")
    
    # Create a test transaction
    transaction_data = {
        "transaction": {
            "transaction_id": str(uuid.uuid4()),
            "user_id": "test_user_456",
            "amount": 2500.0,  # Moderate amount
            "transaction_type": "purchase",
            "merchant": "Amazon",
            "location": "Seattle, WA",
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "device": "desktop",
                "ip": "192.168.1.100"
            }
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/fraud/analyze",
        json=transaction_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Transaction ID: {result['transaction_id']}")
        print(f"Fraud Detected: {result['prediction']['is_fraud']}")
        print(f"Confidence Score: {result['prediction']['confidence_score']:.2f}")
        print(f"Risk Factors: {result['prediction']['risk_factors']}")
        print(f"Action: {result['action']}")
        print(f"Message: {result['message']}")
        print(f"Processing Time: {result['prediction']['processing_time_ms']}ms")
    else:
        print(f"Error: {response.text}")
    print()

def main():
    """Run all tests"""
    print("🚀 Testing Fraud Detection System")
    print("=" * 40)
    
    try:
        # Test health check
        test_health_check()
        
        # Test quick test endpoint
        test_quick_test()
        
        # Test custom transaction
        test_custom_transaction()
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the server is running with: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 