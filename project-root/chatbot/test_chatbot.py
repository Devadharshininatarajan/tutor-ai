#!/usr/bin/env python3
"""
Test script for the AI PDF Assistant chatbot
Run this script to test the backend functionality
"""

import requests
import json
import os
import time

# Configuration
BASE_URL = "http://127.0.0.1:5000"
TEST_PDF_PATH = "test_sample.pdf"  # You'll need to create this or use an existing PDF

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on port 5000")
        return False

def test_status_endpoint():
    """Test the status endpoint"""
    print("\n🔍 Testing status endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/status")
        if response.status_code == 200:
            print("✅ Status endpoint working")
            status = response.json()
            print(f"   Has PDF: {status.get('has_pdf', False)}")
            print(f"   Filename: {status.get('filename', 'None')}")
            print(f"   Chunks: {status.get('chunks_count', 0)}")
            print(f"   Vector Store: {status.get('vector_store_ready', False)}")
            print(f"   Mistral AI Configured: {status.get('mistral_ai_configured', False)}")
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend")
        return False

def test_pdf_upload():
    """Test PDF upload functionality"""
    print("\n🔍 Testing PDF upload...")
    
    # Check if test PDF exists
    if not os.path.exists(TEST_PDF_PATH):
        print(f"⚠️  Test PDF not found at {TEST_PDF_PATH}")
        print("   Please create a test PDF or update TEST_PDF_PATH in this script")
        return False
    
    try:
        with open(TEST_PDF_PATH, 'rb') as pdf_file:
            files = {'pdf': (TEST_PDF_PATH, pdf_file, 'application/pdf')}
            response = requests.post(f"{BASE_URL}/upload", files=files)
            
            if response.status_code == 200:
                print("✅ PDF upload successful")
                data = response.json()
                print(f"   Message: {data.get('message', '')}")
                print(f"   Filename: {data.get('filename', '')}")
                print(f"   Pages: {data.get('pages', 0)}")
                if data.get('summary'):
                    print(f"   Summary: {data.get('summary', '')[:100]}...")
                return True
            else:
                print(f"❌ PDF upload failed: {response.status_code}")
                print(f"   Error: {response.json().get('error', 'Unknown error')}")
                return False
    except Exception as e:
        print(f"❌ PDF upload error: {e}")
        return False

def test_chat_functionality():
    """Test chat functionality"""
    print("\n🔍 Testing chat functionality...")
    
    test_questions = [
        "What is this document about?",
        "Summarize the main points",
        "What are the key findings?"
    ]
    
    for question in test_questions:
        print(f"\n   Testing question: '{question}'")
        try:
            response = requests.post(f"{BASE_URL}/chat", 
                                  json={'message': question},
                                  headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Response received")
                print(f"      Answer: {data.get('response', '')[:100]}...")
            else:
                print(f"   ❌ Chat failed: {response.status_code}")
                print(f"      Error: {response.json().get('error', 'Unknown error')}")
        except Exception as e:
            print(f"   ❌ Chat error: {e}")
    
    return True

def test_summary_endpoint():
    """Test the summary endpoint"""
    print("\n🔍 Testing summary endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/summary")
        if response.status_code == 200:
            print("✅ Summary endpoint working")
            data = response.json()
            if data.get('summary'):
                print(f"   Summary: {data.get('summary', '')[:150]}...")
            else:
                print("   No summary available")
        else:
            print(f"❌ Summary endpoint failed: {response.status_code}")
            print(f"   Error: {response.json().get('error', 'Unknown error')}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting AI PDF Assistant Tests (Mistral AI)")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Status Endpoint", test_status_endpoint),
        ("PDF Upload", test_pdf_upload),
        ("Chat Functionality", test_chat_functionality),
        ("Summary Endpoint", test_summary_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The chatbot is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    print("AI PDF Assistant - Test Suite (Mistral AI)")
    print("Make sure the backend is running on http://127.0.0.1:5000")
    print("You can start it with: cd backend && python app.py")
    print()
    
    # Wait a moment for user to read
    time.sleep(2)
    
    # Run tests
    success = run_all_tests()
    
    if not success:
        print("\n🔧 Troubleshooting Tips:")
        print("1. Ensure the backend is running: python app.py")
        print("2. Check if port 5000 is available")
        print("3. Verify Mistral AI API key is set in .env file")
        print("4. Check backend console for error messages")
        print("5. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("6. Get your free Mistral AI API key from: https://console.mistral.ai/")
    
    print("\nTest completed!") 