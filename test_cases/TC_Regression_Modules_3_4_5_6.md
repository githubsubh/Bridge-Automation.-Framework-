# Test Cases: Module 3, 4, 5 & 6 (Dashboard, E-Services, Assignments, SME)

**Objective:** Verify post-onboarding services, admin controls, and Subject Expert management.

| TC ID | Module | US Reference | Test Case Description | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_M3_01** | Dashboard | US-11 | Registration Progress Display | 100% completion unlocks all service tiles. | Medium |
| **TC_M4_01** | E-Services | US-12 | 2FA Verification Lock | E-Service form remains locked until OTP success. | Critical |
| **TC_M4_02** | E-Services | US-13 | Side-by-Side Modification | Read-only current data displayed alongside new inputs. | High |
| **TC_M4_03** | E-Services | US-13 | No Changes Submission | System prevents submission if new data == current data. | Medium |
| **TC_M5_01** | Assignments| US-14 | Multi-Medium PDF Upload | Assignment created with separate English/Hindi PDFs. | High |
| **TC_M5_02** | Assignments| US-14 | Weightage Constraint | System rejects Weightage Marks > Max Marks. | High |
| **TC_M6_01** | SME | US-15 | SME PAN Validation | Regex enforcement `[A-Z]{5}[0-9]{4}[A-Z]`. | High |
| **TC_M6_02** | SME | US-16 | SME-to-School Mapping | Expert appears in allocation list for mapped schools only. | High |
| **TC_M6_03** | SME | US-17 | TMA Allocation Logic | SME dropdown filtered by Subject AND Medium match. | Critical |
| **TC_M6_04** | SME | US-17 | In-Progress Lock | Cannot re-allocate assignment if evaluation has started. | Medium |
