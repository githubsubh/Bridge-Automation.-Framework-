# Test Cases: Assignment Module (Add Assignment)

## Test Execution Status (2026-04-10)

| TC ID | Linked Scenario | Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| TC_ASGN_01 | TS_ASGN_01 | 1. Login as Superadmin. 2. Click **Masters** in sidebar. 3. Expand **Assignments** and select **Add Assignment**. | Add Assignment page loads with empty form. | Page and modal loaded successfully. | PASS |
| TC_ASGN_02 | TS_ASGN_02 | 1. Fill **Academic Year** = "2025-26". 2. Choose **Subject** = "Mathematics". 3. Enter **Weightage Marks** = 30. 4. Enter **Max Marks** = 100. 5. Expand a language section (e.g. English). 6. Upload a valid PDF file. 7. Click **Create**. | Success message shown: "Created successfully". Record appears in summary. | | |
| TC_ASGN_18 | TS_ASGN_18 | 1. Navigate to Add Assignment. 2. Expand multiple language sections. 3. Upload a unique PDF for each. 4. Click **Create**. | Multiple files are uploaded and associated with the single assignment record. | | |
| TC_ASGN_19 | TS_ASGN_19 | 1. Upload a file to a medium section. 2. Click the 'Remove' or 'X' button next to the filename. | The file name disappears and is removed from the pending submission. | | |
| TC_ASGN_20 | TS_ASGN_20 | 1. Attempt to upload a 10MB PDF file. 2. Click **Create**. | Error message: "File size exceeds the limit of 5MB". | N/A (Manual Needed) | |
| TC_ASGN_22 | TS_ASGN_22 | Enter marks with 15+ digits (e.g. 9999999...). | System should reject or truncate logically. | **BUG**: System accepted 15+ digit value. | FAIL |
| TC_ASGN_23 | TS_ASGN_23 | Enter decimals (e.g. 10.5) in marks fields. | System should only accept integers. | **BUG**: System accepts decimals. | FAIL |
| TC_ASGN_25 | TS_ASGN_25 | Set Weightage = 0 and Max Marks = 0. | System should require non-zero marks. | **BUG**: System allows saving 0/0. | FAIL |
| TC_ASGN_26 | Boundary: Wt > Max | Enter Weightage = 110, Max Marks = 100. | Error: "Weightage marks cannot exceed total marks." | | |
| TC_ASGN_27 | Duplicate Check | Create an assignment for Year 2025-26, Subject Physics. Try to create another for same combo. | Error: "Assignment already exists for this Year and Subject." | | |
| TC_ASGN_28 | Mandatory Medium | Fill all fields but do not upload any PDF in any language section. Click Create. | Error: "At least one language medium section must have an uploaded document." | | |
| TC_ASGN_29 | Invalid File Type | Upload a `.docx` or `.png` file in the English section. | Error: "Only PDF files are allowed for assignments." | | |
| TC_ASGN_30 | Status Toggle | Toggle 'Status' switch from Active to Inactive and save. | Record should be saved with Inactive status; not visible to students. | | |
| TC_ASGN_31 | Idempotency | Click 'Create' button rapidly multiple times. | System should process only one request; no duplicate records. | | |


## UI/UX Test Cases

| TC ID | Linked Scenario | Steps | Expected Result |
|---|---|---|---|
| TC_ASGN_15 | TS_ASGN_15 | Visually inspect the form layout on a 1920×1080 screen. | All labels are left‑aligned, inputs have consistent spacing, and the form is fully visible without scrolling. |
| TC_ASGN_16 | TS_ASGN_16 | Compare each label text with the functional requirement document. | All labels match exactly (e.g., "Academic Year", "Medium", "Subject"). |
| TC_ASGN_17 | TS_ASGN_17 | Navigate through the sidebar to **Masters > Assignments**. | Sidebar highlights the current path and the **Add Assignment** menu item is visually distinct. |
