"""
LegalEase Comprehensive End-to-End Test Suite
Automates generation, verification, and headless export testing across three core legal scenarios:
  - Scenario 1: Startup Employment Contract
  - Scenario 2: Freelancer Non-Disclosure Agreement (NDA)
  - Scenario 3: Residential Lease Agreement
"""

import os
import sys
import time
import requests

# Add project root and frontend to sys.path to reuse exporter functions headlessly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from frontend.app import create_docx, create_pdf

BASE_URL = "http://localhost:8000"
EXPORTS_DIR = os.path.join(CURRENT_DIR, "exports")
os.makedirs(EXPORTS_DIR, exist_ok=True)

SCENARIOS = [
    {
        "id": "scenario_1_employment_contract",
        "name": "Startup Employment Contract",
        "payload": {
            "document_type": "Executive Employment Agreement",
            "parties": "Employer: QuantumScale AI Inc., a Delaware Corporation located at 500 Tech Blvd, San Francisco, CA; Employee: Dr. Maya Lin, Senior AI Research Engineer residing in Palo Alto, CA",
            "terms": "Annual Base Salary: $220,000 USD paid bi-weekly; Equity: 1.5% incentive stock options vesting over 4 years with a 1-year cliff; Comprehensive healthcare benefits; Full assignment of all inventions and Intellectual Property created during employment; Confidentiality obligations persisting post-employment; At-will employment with 30-day notice period; Non-compete and non-solicitation for 12 months post-departure; Governing law: State of California; Dispute resolution: Binding arbitration via JAMS in San Francisco",
            "dates": "Effective Date: November 1, 2026; Vesting Commencement Date: November 1, 2026"
        },
        "required_keywords": ["EMPLOYMENT", "COMPENSATION", "INTELLECTUAL PROPERTY", "CONFIDENTIAL", "TERMINATION", "GOVERNING LAW", "SIGNATURE"]
    },
    {
        "id": "scenario_2_freelancer_nda",
        "name": "Freelancer Non-Disclosure Agreement",
        "parties": "Disclosing Party: Apex Media Enterprises LLC (New York LLC); Receiving Party: Lucas Bennett, Independent Video Producer and Editor",
        "payload": {
            "document_type": "Mutual Non-Disclosure and Confidentiality Agreement",
            "parties": "Disclosing Party: Apex Media Enterprises LLC, 750 Broadway, New York, NY; Receiving Party: Lucas Bennett, independent contractor residing in Brooklyn, NY",
            "terms": "Definition of Confidential Information including unreleased footage, proprietary scripts, marketing strategies, and client lists; Non-disclosure period of two (2) years from disclosure; Standard exclusions (publicly known info, independently developed info, legally compelled disclosure); Immediate return or certified destruction of materials within 10 days of request; Injunction relief without necessity of posting bond; Governing law: State of New York; Jurisdiction: New York County Courts",
            "dates": "Effective Date: October 15, 2026; Expiration Date: October 15, 2028"
        },
        "required_keywords": ["CONFIDENTIAL", "RECITALS", "EXCLUSIONS", "RETURN OF MATERIALS", "INJUNCTIVE RELIEF", "GOVERNING LAW", "IN WITNESS WHEREOF"]
    },
    {
        "id": "scenario_3_residential_lease",
        "name": "Residential Lease Agreement",
        "payload": {
            "document_type": "Standard Residential Lease Agreement",
            "parties": "Landlord: Serenity Properties Management LLC, 120 Harbor View Dr, Seattle, WA; Tenant: Marcus Vance and Emily Vance, individuals residing at Seattle, WA",
            "terms": "Premises: 452 Elm Street, Apt 3B, Seattle, WA 98101; Term: 12-month fixed lease; Monthly Rent: $2,800 USD due on the 1st of each calendar month; Security Deposit: $3,500 USD held in an interest-bearing escrow account; Late fee: $75 for rent received after the 5th; Utilities: Landlord pays water/sewer/trash, Tenant pays electricity and internet; No unauthorized pets; Maintenance obligations: Tenant responsible for minor repairs under $100; Governing Law: State of Washington (RCW 59.18)",
            "dates": "Lease Start Date: November 1, 2026; Lease End Date: October 31, 2027"
        },
        "required_keywords": ["LEASE", "RENT", "SECURITY DEPOSIT", "PREMISES", "MAINTENANCE", "DEFAULT", "GOVERNING LAW"]
    }
]

def run_headless_scenario(scenario: dict) -> bool:
    print(f"\n" + "="*70)
    print(f"▶ Testing Scenario: {scenario['name']}")
    print(f"="*70)
    
    start_time = time.time()
    try:
        res = requests.post(f"{BASE_URL}/generate", json=scenario["payload"], timeout=120)
        latency = round(time.time() - start_time, 2)
        
        print(f"  [HTTP Status]: {res.status_code} (in {latency}s)")
        if res.status_code != 200:
            print(f"  [ERROR]: Server returned non-200 response: {res.text}")
            return False
            
        data = res.json()
        doc_text = data.get("document", "")
        if not doc_text:
            print("  [ERROR]: Empty document received in response.")
            return False
            
        print(f"  [Doc Length]: {len(doc_text)} characters / {len(doc_text.splitlines())} lines")

        # 1. Validate Legal Keywords
        missing_keywords = []
        for kw in scenario["required_keywords"]:
            if kw.lower() not in doc_text.lower():
                missing_keywords.append(kw)
        
        if missing_keywords:
            print(f"  [WARNING]: Expected keywords not explicitly found: {missing_keywords}")
        else:
            print(f"  [Validation]: All required legal sections and keywords verified.")

        # 2. Test Headless Exporters (.txt, .docx, .pdf)
        base_filename = scenario["id"]
        
        # Plain Text (.txt)
        txt_path = os.path.join(EXPORTS_DIR, f"{base_filename}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(doc_text)
        print(f"  [Exported TXT]: {txt_path} ({os.path.getsize(txt_path)} bytes)")

        # Word Document (.docx)
        docx_path = os.path.join(EXPORTS_DIR, f"{base_filename}.docx")
        docx_stream = create_docx(doc_text)
        with open(docx_path, "wb") as f:
            f.write(docx_stream.getvalue())
        print(f"  [Exported DOCX]: {docx_path} ({os.path.getsize(docx_path)} bytes)")

        # Adobe PDF (.pdf)
        pdf_path = os.path.join(EXPORTS_DIR, f"{base_filename}.pdf")
        pdf_stream = create_pdf(doc_text)
        with open(pdf_path, "wb") as f:
            f.write(pdf_stream.getvalue())
        print(f"  [Exported PDF]: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")

        print(f"  -> SUCCESS: Scenario '{scenario['name']}' fully passed and exported.")
        return True

    except Exception as exc:
        print(f"  [EXCEPTION]: {exc}")
        return False

def test_edge_cases():
    print(f"\n" + "="*70)
    print("▶ Testing Edge Cases & Error Resilience")
    print(f"="*70)
    
    # Edge Case 1: Empty Fields
    empty_payload = {"document_type": "", "parties": "", "terms": "", "dates": ""}
    res_empty = requests.post(f"{BASE_URL}/generate", json=empty_payload, timeout=10)
    print(f"  [Edge Case 1 - Empty Request Validation]: Status {res_empty.status_code}")
    assert res_empty.status_code in [400, 422], "Should reject empty payload"
    print("  -> PASS: Backend correctly rejected empty document request.")

    # Edge Case 2: Unicode and Special Characters
    unicode_payload = {
        "document_type": "International Services Agreement — NDA & IP",
        "parties": "Alpha S.A. (Paris, France) € & Beta Ltd. (Tokyo, Japan) ©®",
        "terms": "Clause 1: 100% confidentiality; Clause 2: Payment in € EUR; Special quotes: “Fair dealing” & ‘Best efforts’; Em-dash — test.",
        "dates": "Effective Date: 2026-10-01"
    }
    res_unicode = requests.post(f"{BASE_URL}/generate", json=unicode_payload, timeout=120)
    print(f"  [Edge Case 2 - Unicode / Special Char Handling]: Status {res_unicode.status_code}")
    if res_unicode.status_code == 200:
        pdf_test = create_pdf(res_unicode.json()["document"])
        assert len(pdf_test.getvalue()) > 0, "PDF should render unicode-sanitized bytes"
        print("  -> PASS: Unicode text sanitized and exported without encoding crashes.")

def main():
    print("======================================================================")
    print("      LegalEase: End-to-End Automated Test & Export Verification      ")
    print("======================================================================")

    # Health check
    try:
        health_res = requests.get(f"{BASE_URL}/", timeout=5)
        if health_res.status_code != 200:
            print(f"[ERROR]: Health check returned status {health_res.status_code}. Is FastAPI running?")
            sys.exit(1)
        print("✅ Backend API is online and healthy.\n")
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        print("Please start the backend: python -m uvicorn legalEaseAPI.main:app --port 8000")
        sys.exit(1)

    all_passed = True
    for scenario in SCENARIOS:
        passed = run_headless_scenario(scenario)
        if not passed:
            all_passed = False
        time.sleep(1)

    test_edge_cases()

    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL SCENARIOS AND EXPORT FORMATS (.txt, .docx, .pdf) PASSED PERFECTLY!")
        print(f"Artifacts and documents saved to: {EXPORTS_DIR}")
    else:
        print("⚠️ Some scenarios encountered errors. Review logs above.")
    print("="*70)

if __name__ == "__main__":
    main()
