# Test Case Execution Log — US-15: SME Onboarding

**User Story:** US-15 (SME Onboarding & Identity Validation)  
**Tester:** Shubham Singh & Antigravity AI  
**Date:** April 23, 2026  

---

| TC ID | Scenario Description | Steps | Expected Result | Actual Result | Status | Bug ID |
|-------|----------------------|-------|-----------------|---------------|--------|--------|
| **TS_SME_01** | **Positive:** Successful SME Onboarding | 1. Navigate to Add SME.<br>2. Enter valid Name, DOB (1990), Gender.<br>3. Enter valid PAN (ABCDE1234F).<br>4. Enter unique Mobile/Email.<br>5. Upload valid Sign (JPG).<br>6. Save. | Account is created in "Draft" status. Success message displayed. SME-ID generated (SME-2026-XXXX). | | PENDING | |
| **TS_SME_02** | **Negative:** Invalid PAN Format Validation | 1. Enter PAN "1234567890" or "ABCDE1234".<br>2. Fill other fields.<br>3. Save. | Error Message: "Enter a valid 10-digit PAN (e.g., ABCDE1234F)." Save is blocked. | | PENDING | |
| **TS_SME_03** | **Negative:** Duplicate PAN Entry | 1. Attempt to register with a PAN already in the DB.<br>2. Click Save. | Error Message: "This PAN is already registered with another expert." | | PENDING | |
| **TS_SME_04** | **Negative:** Underage Expert Validation | 1. Enter DOB that makes the SME 17 years old.<br>2. Save. | Error Message: "Experts must be at least 18 years old." | | PENDING | |
| **TS_SME_05** | **Negative:** Duplicate Mobile/Email Check | 1. Enter an Email/Mobile already assigned to an existing SME.<br>2. Save. | Error Message: "[Field] already exists in the system." | | PENDING | |
| **TS_SME_06** | **Negative:** Missing Mandatory Signature | 1. Fill all details except Signature Upload.<br>2. Save. | Error Message: "Please upload the SME signature." | | PENDING | |
| **TS_SME_07** | **UI:** PAN Auto-Capitalization | 1. Type "abcde1234f" in lowercase in the PAN field. | Input should automatically transform to "ABCDE1234F" while typing. | | PENDING | |
| **TS_SME_08** | **Non-Functional:** Search Performance | 1. Search for an SME using a unique Mobile number in the main list. | Results should be displayed in < 1 second. | | PENDING | |
| **TS_SME_09** | **Edge Case:** Large Signature File | 1. Attempt to upload a 5MB signature file. | Error Message: "File size must be less than 2MB." | | PENDING | |
| **TS_SME_10** | **Business Rule:** Draft Status Control | 1. Create a new SME.<br>2. Verify if they appear in the "Allocation Dropdown" for US-17. | New SME should NOT appear in allocation lists until 'Activated' by admin. | | PENDING | |
| **TS_SME_11** | **Security:** SQL Injection in PAN | 1. Enter `' OR '1'='1` in the PAN field.<br>2. Fill other fields and Save. | System should sanitize input; no DB error; validation should fail. | | PENDING | |
| **TS_SME_12** | **Negative:** Special Chars in Name | 1. Enter "SME@123" in Name field.<br>2. Save. | Error: "Name should contain alphabets only." | | PENDING | |
| **TS_SME_13** | **Negative:** Invalid Mobile Format | 1. Enter "12345" or "ABCDEFGHIJ" in Mobile field. | Validation: "Enter a valid 10-digit mobile number." | | PENDING | |
| **TS_SME_14** | **Negative:** Unsupported Signature Format | 1. Upload a `.pdf` or `.exe` as signature. | Error: "Invalid file format. Only JPG/PNG allowed." | | PENDING | |
| **TS_SME_15** | **UX:** Mandatory Field Indicators | 1. Observe the 'Add SME' form. | All mandatory fields (Name, DOB, PAN, Mobile, Email, Sign) should have a red asterisk (*). | | PENDING | |
| **TS_SME_16** | **Edge Case:** Max Length Name | 1. Enter a name with 255 characters.<br>2. Save. | System should either truncate or show "Max length exceeded". | | PENDING | |
| **TS_SME_17** | **Business Rule:** SME ID Uniqueness | 1. Register multiple SMEs.<br>2. Check IDs in the list. | Each SME should have a unique ID (SME-2026-0001, SME-2026-0002, etc.). | | PENDING | |
| **TS_SME_18** | **Security:** XSS in Email Field | 1. Enter `<script>alert(1)</script>` in Email.<br>2. Save. | Script should be escaped; no execution on list view. | | PENDING | |
| **TS_SME_19** | **Negative:** Future Date of Birth | 1. Select a future date in DOB calendar.<br>2. Save. | System should block future dates or show: "DOB cannot be in the future." | | PENDING | |
| **TS_SME_20** | **Audit:** Admin ID Logging | 1. Create an SME with Admin Account A.<br>2. Check DB 'created_by' field. | The field should correctly record Admin Account A's ID. | | PENDING | |

