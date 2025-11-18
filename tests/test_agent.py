#!/usr/bin/env python3
"""
Simple test script for the automation agent
"""
import requests
import time
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print(" Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f" Health check: {response.json()}\n")

def test_run_task():
    """Test task submission and retrieval"""
    print(" Submitting new task...")
    
    # Submit task
    response = requests.post(
        f"{BASE_URL}/api/run-task",
        json={"data_source": "dummy"}
    )
    
    if response.status_code != 200:
        print(f" Error: {response.status_code}")
        return
    
    result = response.json()
    task_id = result["task_id"]
    print(f" Task submitted: {task_id}")
    print(f"   Status: {result['status']}\n")
    
    # Wait for processing
    print(" Waiting for task to complete...")
    time.sleep(3)
    
    # Get task result
    print(" Fetching task results...")
    response = requests.get(f"{BASE_URL}/api/task/{task_id}")
    
    if response.status_code != 200:
        print(f" Error fetching results: {response.status_code}")
        return
    
    result = response.json()
    print(f"\n Task completed!\n")
    print(json.dumps(result, indent=2))
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Task ID: {result['task_id']}")
    print(f"Status: {result['status']}")
    print(f"Category: {result['category']}")
    print(f"Reasoning: {result['reasoning']}")
    print(f"Action Taken: {result['action_taken']}")
    print("="*60)

def main():
    print("\n" + "="*60)
    print("ENTERPRISE AUTOMATION AGENT - TEST SUITE")
    print("="*60 + "\n")
    
    try:
        test_health()
        test_run_task()
        print("\n All tests completed successfully!\n")
    except requests.exceptions.ConnectionError:
        print("\n Error: Cannot connect to server.")
        print("   Make sure the server is running:")
        print("   cd app && uvicorn main:app --reload\n")
    except Exception as e:
        print(f"\n Error: {str(e)}\n")

if __name__ == "__main__":
    main()