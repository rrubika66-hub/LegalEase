"""
LegalEase Automated Verification & Test Script
Tests health endpoint and generates a Freelance Work Contract via POST /generate.
"""
import sys
import json
import requests

BASE_URL = "http://localhost:8000"

def test_health():
    print("1. Testing Root Health Check (GET /)...")
    try:
        res = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"   Status Code: {res.status_code}")
        print(f"   Response: {res.json()}")
        assert res.status_code == 200, "Health check failed"
        print("   -> PASS: Health check succeeded.\n")
    except Exception as e:
        print(f"   -> FAIL: Could not reach {BASE_URL}/. Error: {e}\n")
        return False
    return True

def test_document_generation():
    print("2. Testing Document Generation (POST /generate) with Freelance Work Contract...")
    payload = {
        "document_type": "Freelance Software Development Contract",
        "parties": "Client: Alpha Global Inc., a Delaware Corporation with offices at 100 Main St, Wilmington, DE; Contractor: Alex Morgan, an independent software engineer residing in Austin, TX",
        "terms": "Scope: Full-stack web application development for inventory management; Total Fee: $15,000 USD payable in 3 milestones (30% upfront, 40% upon beta release, 30% upon final delivery); Term: 3 months; Full assignment of all Intellectual Property upon final payment; Mutual confidentiality for 2 years; 14 days written notice for termination; Governing Law: State of Delaware; Arbitration: AAA rules in Wilmington, DE.",
        "dates": "Effective Date: October 1, 2026; Completion Deadline: December 31, 2026"
    }

    try:
        print("   Sending request to Gemini 1.5 Pro AI drafting engine...")
        res = requests.post(f"{BASE_URL}/generate", json=payload, timeout=120)
        print(f"   Status Code: {res.status_code}")
        
        if res.status_code != 200:
            print(f"   Error detail: {res.text}")
            return False

        data = res.json()
        assert "document" in data, "Response missing 'document' key"
        doc_text = data["document"]
        
        print("\n==================== GENERATED DOCUMENT PREVIEW ====================")
        # Print first 500 characters
        print(doc_text[:600] + "\n\n[... truncated preview ...]\n")
        print("====================================================================")
        
        print(f"   Total Generated Characters: {len(doc_text)}")
        print("   -> PASS: Document successfully generated and validated with HTTP 200!\n")
        return True
    except Exception as e:
        print(f"   -> FAIL: Document generation test encountered an error: {e}\n")
        return False

if __name__ == "__main__":
    print("=============================================================")
    print("       LegalEase Automated API Test & Verification Suite      ")
    print("=============================================================\n")
    
    if test_health():
        test_document_generation()
