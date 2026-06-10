# Test Cases: Subject Matter Expert (SME) Evaluation

## 1. Evaluation Interface & Navigation
| TC ID | Scenario | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC_SME_EV_01 | Module Accessibility | Login as SME; Click 'TMA Manager'. | Dashboard with 'Pending' and 'Evaluated' counts appears. | |
| TC_SME_EV_02 | Global Search | Search by Student Reference No in evaluation list. | Correct student record is isolated. | |
| TC_SME_EV_03 | Filter Persistence | Apply 'Biology' filter; Refresh page. | Filter remains active (if stateful) or resets cleanly. | |
| TC_SME_EV_04 | Sorting Logic | Click 'Submission Date' header. | List alternates between Ascending/Descending order. | |

## 2. Document Handling & Verification
| TC ID | Scenario | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC_SME_DOC_05 | Inline PDF Viewer | Click 'View' on a PDF submission. | PDF opens in the built-in browser viewer (not a download). | |
| TC_SME_DOC_06 | Non-PDF Handling | Access a student who uploaded a JPG/PNG. | Image opens in viewer or a preview modal. | |
| TC_SME_DOC_07 | Multi-Page PDF | Open a 10-page assignment. | SME can scroll through all pages without loading errors. | |
| TC_SME_DOC_08 | Corrupt File Check | Open a file that failed to upload correctly. | Error: "File cannot be opened; ask student to re-upload". | |

## 3. Scoring & Validation Rules
| TC ID | Scenario | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC_SME_SCR_09 | Partial Scoring | Enter marks for 3 out of 5 questions (if modular). | System sums up correctly or allows total entry. | |
| TC_SME_SCR_10 | Boundary: Max Marks | Enter marks = Max Marks (e.g. 100/100). | System accepts and saves successfully. | |
| TC_SME_SCR_11 | Boundary: Overflow | Enter marks = 101/100. | Error: "Marks cannot exceed the limit". | |
| TC_SME_SCR_12 | Boundary: Zero | Award 0 marks for a blank assignment. | System accepts 0 and status becomes 'Evaluated'. | |
| TC_SME_SCR_13 | Negative Entry | Award -5 marks. | Error: "Negative values not allowed". | |
| TC_SME_SCR_14 | Decimal Entry | Enter 25.5 marks. | System rounds or displays "Integers only" depending on rule. | |
| TC_SME_SCR_15 | Mandatory Remarks | Try to award < 33% marks without writing a remark. | System prompts: "Kindly provide feedback for low score". | |

## 4. Evaluation Workflow & Data Lifecycle
| TC ID | Scenario | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC_SME_WF_16 | 'Save as Draft' | Award 20 marks; Click 'Save as Draft'. | Status remains 'Pending'; Marks are saved for later. | |
| TC_SME_WF_17 | 'Final Submit' | Award 25 marks; Click 'Final Submit'. | Status changes to 'Evaluated'; Entry becomes read-only. | |
| TC_SME_WF_18 | Result Sync: Student | Award 30 marks; Login as the specific student. | Marks and remarks are visible in 'My Results' section. | |
| TC_SME_WF_19 | Finalized Modification | Try to edit marks of a student with 'Evaluated' status. | Edit button is disabled; modification blocked. | |
| TC_SME_WF_20 | Bulk Mark Entry | Select 10 students; enter 20 marks for all via bulk tool. | All 10 students updated simultaneously correctly. | |

## 5. UI/UX & Responsive Feedback
| TC ID | Scenario | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC_SME_UX_21 | Remark Character Limit | Type 2000 characters in the remarks box. | Character counter stops at limit (e.g., 500); truncation. | |
| TC_SME_UX_22 | Success Toast | Click 'Final Submit'. | Green checkmark or success toast "Evaluation Submitted". | |
| TC_SME_UX_23 | Mobile Viewer | Access Evaluation page via smartphone. | PDF viewer and scoring boxes adjust for vertical screen. | |
| TC_SME_UX_24 | Loading States | Open evaluation during slow internet. | Loading spinner or skeleton loader is visible. | |
