# Test Scenarios: SME Management & Assignment Allocation

## SME Management (Registration & Mapping)
| ID | Description |
|---|---|
| TS_SME_MGMT_01 | Successfully add a new Subject Matter Expert (SME) with valid details. |
| TS_SME_MGMT_02 | Map an SME to a specific School and verify the binding. |
| TS_SME_MGMT_03 | Attempt to add duplicate SME details (Email/Phone). |
| TS_SME_MGMT_04 | Map one SME to multiple schools and verify visibility. |
| TS_SME_MGMT_05 | Attempt to save an SME without assigning any school (Mandatory check). |

## Assignment Allocation Logic
| ID | Description |
|---|---|
| TS_ALOC_01 | Verify student assignments are allocated to SMEs based on the matching School Name. |
| TS_ALOC_02 | Check if an SME can see only the students from their assigned school(s). |
| TS_ALOC_03 | Verify behavior when a student submits an assignment but No SME is mapped to their school. |
| TS_ALOC_04 | Test manual reallocation of an assignment to a different SME. |

## Workflow Integrity
| ID | Description |
|---|---|
| TS_WF_01 | Verify the SME login accessibility once the user is created in the backend. |
| TS_WF_02 | Verify the 'Evaluated' count updates in the SME dashboard after marks are awarded. |
