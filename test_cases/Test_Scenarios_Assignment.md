# Test Scenarios: Assignment Module (Add Assignment)

## Positive Scenarios
| ID | Description |
|---|---|
| TS_ASGN_01 | Navigate to Add Assignment page successfully. |
| TS_ASGN_02 | Add assignment with all mandatory fields filled correctly. |
| TS_ASGN_03 | Verify Academic Year dropdown options. |
| TS_ASGN_04 | Verify Subject dropdown updates based on selected criteria. |
| TS_ASGN_05 | Accept valid numeric values for Weightage Marks and Max Marks. |
| TS_ASGN_06 | Change Status between Active and Inactive. |
| TS_ASGN_07 | After saving, assignment appears in the summary list with 'Verified' status or 'Preview' link available. |
| TS_ASGN_08 | Reset button clears the form. |
| TS_ASGN_18 | Verify file upload functionality for each medium section. |
| TS_ASGN_19 | Verify that uploaded files can be removed/replaced before saving. |
| TS_ASGN_20 | Verify system handles large file uploads (>5MB) correctly. |

## Negative Scenarios (Validation)
| ID | Description |
|---|---|
| TS_ASGN_09 | Attempt to save with mandatory fields blank – expect validation messages. |
| TS_ASGN_10 | Weightage Marks greater than Max Marks – expect error. |
| TS_ASGN_11 | Negative numbers in marks fields – expect rejection. |
| TS_ASGN_12 | Non‑numeric characters in marks fields – expect validation. |
| TS_ASGN_13 | Duplicate assignment (same Year, Subject, Medium) – expect duplicate warning. |
| TS_ASGN_14 | Upload invalid file type (e.g. .exe, .php, .html) – expect server-side rejection. |
| TS_ASGN_21 | Attempt to save without uploading at least one assignment document. |
| TS_ASGN_22 | **Extreme Values**: Enter marks with 10+ digits (e.g. 9999999999). |
| TS_ASGN_23 | **Special Characters**: Enter alphabets or symbols in numeric marks fields. |
| TS_ASGN_24 | **Double Submission**: Rapidly click the 'Create' button multiple times. |
| TS_ASGN_25 | **Zero Check**: Set Max Marks and Weightage Marks to 0. |
| TS_ASGN_26 | **Whitespace Test**: Check if leading/trailing spaces in dropdown choices (if dynamic) are handled. |
| TS_ASGN_27 | **Session Timeout**: Keep the modal open for 30+ mins and then try to save. |

## UI/UX Scenarios
| ID | Description |
|---|---|
| TS_ASGN_15 | Verify alignment, readability, and spacing of form elements. |
| TS_ASGN_16 | Ensure all labels match functional requirement documentation. |
| TS_ASGN_17 | Verify sidebar navigation highlights the Masters > Assignments path.
