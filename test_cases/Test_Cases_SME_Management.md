# Test Cases: SME Management & Allocation (Comprehensive Suite)

## 1. SME Registration & Master Data Integrity
| TC ID | Scenario | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC_SME_REG_01 | Basic Registration Success | 1. Navigate to 'Add SME'. 2. Fill all mandatory fields. 3. Click 'Save'. | SME created with distinct ID; Success notification. | ✅ |
| TC_SME_REG_02 | Field Constraint: Name | Enter Name with numbers/special chars (e.g., "SME_123"). | Validation error: "Alphabetic characters only allowed". | |
| TC_SME_REG_03 | Field Constraint: DOB | Enter DOB making SME < 18 years old. | Validation error: "Minimum age requirement not met". | |
| TC_SME_REG_04 | Duplicate Mobile Validation | Add SME with a mobile number already in the database. | Error: "Mobile number already exists". | ✅ |
| TC_SME_REG_05 | Duplicate Email Validation | Add SME with an email already in the database. | Error: "Email address already exists". | ❌ |
| TC_SME_REG_06 | File Upload: Signature | Upload a 5MB BMP file for signature. | Validation: "File too large (Max 2MB)" and "Invalid format (Use JPG/PNG)". | |
| TC_SME_REG_07 | Field Constraint: PAN | Enter invalid PAN format (e.g., "ABC1234XYZ"). | Error: "Invalid PAN format". | |
| TC_SME_REG_08 | Optional Field Persistence | Leave 'Secondary Phone' blank and save. | Profile saved successfully without errors. | |
| TC_SME_REG_09 | Address Sync | Select State 'Uttar Pradesh' and check District list. | Only Districts belonging to UP are displayed. | |

## 2. Advanced School & Subject Mapping
| TC ID | Scenario | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC_SME_MAP_10 | Multi-Subject Binding | Map an SME to Physics, Chemistry, and Math. | Dashboard shows all 3 subjects in SME profile. | |
| TC_SME_MAP_11 | Multi-School Binding | Map an SME to 15 different schools across 3 districts. | SME appears in the allocation list of all 15 schools; pagination works. | |
| TC_SME_MAP_12 | School Unlinking | Remove 1 school from the SME's mapped list. | SME no longer visible to that school's students in real-time. | |
| TC_SME_MAP_13 | Medium Conflict | Map an English-medium SME to a Hindi-medium school. | Warning/Error: "Medium mismatch between Expert and School". | |
| TC_SME_MAP_14 | Overlap Check | Try mapping a Subject Expert to a school where they are already mapped. | Error: "Expert already mapped to this school". | |
| TC_SME_MAP_26 | Academic Session Binding | Check mapping visibility for academic year 2024-25 vs 2025-26. | SME mapping should be specific to the selected session. | |
| TC_SME_MAP_27 | UI: Bulk Selection | Use 'Select All' checkbox in school mapping list. | All visible schools should be selected/deselected instantly. | |


## 3. TMA Allocation & Workflows
| TC ID | Scenario | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC_SME_AL_15 | Regional Filtering | Superadmin filters SMEs by 'Lucknow Region'. | Only SMEs registered in Lucknow region are displayed. | |
| TC_SME_AL_16 | Medium-Specific Routing | Assign a Hindi-medium student for evaluation. | Dropdown ONLY shows Hindi-medium SMEs. | |
| TC_SME_AL_17 | Subject Specificity | Select Student with 'Biology' subject. | Only 'Biology' mapped experts appear in allocation list. | |
| TC_SME_AL_18 | Bulk Allocation (100+) | Select 100 students and assign to 1 SME. | Success message; SME receives notification/list entry. | |
| TC_SME_AL_19 | Re-allocation logic | Transfer a 'Pending' assignment from SME-01 to SME-02. | Assignment removed from SME-01 and appears for SME-02. | |
| TC_SME_AL_20 | Work in Progress Block | Try re-allocating a student whose evaluation is 'In-Progress'. | Error: "Evaluation started. Cannot change expert." | |
| TC_SME_AL_21 | Unallocated Counter | Check Dashboard stats before and after allocation. | 'Unallocated' count decreases; 'Allocated' count increases. | |
| TC_SME_AL_30 | Expert Load Visibility | Observe SME dropdown during allocation. | Each expert name should show current load (e.g., "SME Name (12/50)"). | |
| TC_SME_AL_31 | Allocation Audit | Allocate a student and check DB logs. | Allocation must record Timestamp and Principal/Admin ID. | |
| TC_SME_AL_32 | Notification Trigger | Perform an allocation. | SME should receive an Email/System notification immediately. | |
| TC_SME_AL_33 | Duplicate Prevention | Try to allocate the same student to two different SMEs simultaneously. | System prevents duplicate active assignments for the same student-subject. | |


## 4. Admin Controls & Lifecycle
| TC ID | Scenario | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC_SME_LC_22 | SME Password Reset | Admin triggers 'Send Reset Link' to SME. | SME receives email; Link works for password change. | |
| TC_SME_LC_23 | Account Suspension | Mark SME as 'Suspended' for misconduct. | SME login fails; "Account suspended" message shown. | |
| TC_SME_LC_24 | Reactive Mapping | Update SME's subject from Physics to Biology. | SME loses access to old Physics assignments; starts seeing Biology. | |
| TC_SME_LC_25 | Draft status visibility | Check if 'Draft' SMEs appear in active evaluation lists. | Draft SMEs are hidden from workflow until 'Activated'. | ❌ |

## 5. Security & Multi-Role Access
| TC ID | Scenario | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC_SME_SEC_26 | Direct URL Access | Paste SME dashboard URL without login. | System redirects to Login page. | |
| TC_SME_SEC_27 | Cross-SME Data Leak | SME-01 tries to access SME-02's evaluation ID via URL manipulation. | Error: "Access Denied" or 403 Forbidden. | |
| TC_SME_SEC_28 | Session Expiry | Leave dashboard idle for 60 minutes. | Auto-logout; System asks for re-authentication. | |
| TC_SME_SEC_29 | Concurrent Edit | Admin and SME try to update profile at same time. | Optimistic locking prevents data corruption/overwrite. | |
| TC_SME_SEC_30 | Role Restriction: SME | Login as SME and attempt to navigate to `/admin/add-assignment`. | System redirects to SME Dashboard with "Access Denied". | |
| TC_SME_SEC_31 | Role Restriction: Principal | Login as Principal and attempt to evaluate an assignment. | Access blocked; evaluations only for SMEs. | |
| TC_SME_WF_32 | Inactive Assignment Flow | Set assignment to 'Inactive'. Check student dashboard. | Assignment should not be available for submission. | |
| TC_SME_WF_33 | Data Integrity: Deleted Mapping | Unmap an SME from a school while they have pending evaluations. | SME should still be able to complete *existing* pending evaluations but receive no new ones. | |
| TC_SME_WF_34 | System Maintenance | Trigger 'System Maintenance' mode from backend. | SME sees a "Maintenance in Progress" page; login disabled. | |

