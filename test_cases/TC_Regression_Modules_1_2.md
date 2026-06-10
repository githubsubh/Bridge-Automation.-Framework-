# Test Cases: Module 1 - Login & Security (US-01, US-02, US-03)

**Objective:** Verify the security, validation, and functionality of the Teacher Login gateway.

| TC ID | US Reference | Test Case Description | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **TC_M1_01** | US-01 | Successful Login (Positive) | Redirect to Dashboard; Session info displayed in header. | High |
| **TC_M1_02** | US-01/02 | Empty Field Validation | Inline error "This field is required" on both fields. | High |
| **TC_M1_03** | US-02 | Invalid Email Format | Error message for invalid `@` or domain structure. | Medium |
| **TC_M1_04** | US-01/02 | Incorrect Credentials | Alert/Message: "Incorrect email or password." | High |
| **TC_M1_05** | US-02 | Account Lockout (5 attempts) | Alert: "Account locked. Please contact administrator." | Critical |
| **TC_M1_06** | US-02 | SQL Injection Sanitization | Input escaped/sanitized; no DB errors or unauthorized access. | Critical |
| **TC_M1_07** | US-03 | Clear Form Functionality | All fields flushed; focus returns to first field; no error states. | Low |
| **TC_M1_08** | US-01 | Password Masking (`type=password`) | Input characters are hidden by dots/asterisks. | High |

---

# Test Cases: Module 2 - 7-Stage Registration Wizard (US-04 to US-10)

**Objective:** End-to-end verification of the teacher onboarding flow.

| TC ID | Stage | Test Case Description | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **TC_M2_01** | Stage 1 | Basic Details - Alpha-only Name | System rejects digits/special chars in Name fields. | High |
| **TC_M2_02** | Stage 1 | UDISE Code AJAX Validation | Invalid code triggers "UDISE Code not found." | Critical |
| **TC_M2_03** | Stage 1 | DOB Age Validation (18+) | System blocks users with DOB < 18 years ago. | High |
| **TC_M2_04** | Stage 2 | OTP Delivery (Email/Mobile) | OTP dispatched to both channels simultaneously. | Critical |
| **TC_M2_05** | Stage 2 | OTP Expiry (10 mins) | Expired OTP triggers "OTP has expired." | Medium |
| **TC_M2_06** | Stage 4 | Dependent District Dropdown | District list updates via AJAX based on State selection. | High |
| **TC_M2_07** | Stage 4 | Same as Correspondence Check | Permanent address fields auto-fill and lock. | Medium |
| **TC_M2_08** | Stage 6 | Document Upload Constraints | Rejects files > 2MB or invalid formats (.exe, etc). | High |
| **TC_M2_09** | Stage 7 | Review Page - Edit Mode | Clicking "Edit" returns user to specific stage; data persists. | High |
| **TC_M2_10** | Stage 7 | Final Submission & Ref Generation | Reference Number generated (e.g., BRIDGE-2026-XXXX). | Critical |
