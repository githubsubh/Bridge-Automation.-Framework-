# Test Scenarios: Student Assignment Module (Frontend)

## Positive Scenarios
| ID | Description |
|---|---|
| TS_STU_ASGN_01 | Successfully login to the student portal. |
| TS_STU_ASGN_02 | Navigate to the 'Assignments' section from the dashboard. |
| TS_STU_ASGN_03 | Verify that the assignment added in the backend is visible to the student. |
| TS_STU_ASGN_04 | Successfully download the assignment document (PDF). |
| TS_STU_ASGN_05 | Upload a completed assignment (PDF format). |
| TS_STU_ASGN_06 | Verify submission status changes to 'Submitted' or 'Pending Evaluation'. |

## Negative Scenarios
| ID | Description |
|---|---|
| TS_STU_ASGN_07 | Attempt to upload a file after the submission deadline. |
| TS_STU_ASGN_08 | Attempt to upload an invalid file format (e.g. .exe, .zip). |
| TS_STU_ASGN_09 | Attempt to upload a file exceeding the maximum size limit. |
| TS_STU_ASGN_13 | **MIME-type Bypass**: Rename a .txt file to .pdf and try to upload. |
| TS_STU_ASGN_14 | **Empty File**: Attempt to upload a 0-byte file. |
| TS_STU_ASGN_15 | **Rapid Click**: Double/Triple click the 'Submit' button. |
| TS_STU_ASGN_16 | **XSS/SQLi**: Enter malicious payloads into any text/comment fields. |

## UI/UX Scenarios
| ID | Description |
|---|---|
| TS_STU_ASGN_11 | Verify 'Download' and 'Upload' buttons are clearly visible and intuitive. |
| TS_STU_ASGN_12 | Verify success/error messages during the upload process. |
