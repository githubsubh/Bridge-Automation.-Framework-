# Test Cases: Student Assignment Module (Frontend)

## Test Cases

| TC ID | Linked Scenario | Description | Steps | Expected Result | Actual Result | Status | Priority | Severity |
|---|---|---|---|---|---|---|---|---|
| TC_STU_01 | TS_STU_ASGN_01 | Login Validation | 1. Open Browser. 2. Navigate to https://bridge-uat.nios.ac.in/auth/login. 3. Enter Email and Password. 4. Enter Captcha manually. 5. Click Login. | Student is redirected to the Dashboard. | | PASS | High | Major |
| TC_STU_02 | TS_STU_ASGN_02 | Menu Navigation | 1. On Dashboard, click 'Assignments' in the sidebar/menu. | Assignment list page opens. | | PASS | High | Major |
| TC_STU_03 | TS_STU_ASGN_04 | Download Function | 1. Find the target assignment. 2. Click the 'Download' icon/button. | Assignment PDF is downloaded successfully. | | PASS | High | Major |
| TC_STU_04 | TS_STU_ASGN_05 | Positive Upload | 1. Click 'Upload Assignment'. 2. Select a valid PDF file. 3. Click 'Submit'. | Success message shown: "Assignment submitted successfully." | | PASS | High | Major |
| TC_STU_05 | TS_STU_ASGN_08 | Type Validation (.txt) | 1. Attempt to upload a .txt file. | Validation error: "Only PDF files are allowed." | | PASS | High | Major |
| TC_STU_06 | TS_STU_ASGN_09 | Size Validation (>5MB) | 1. Attempt to upload a file >5MB. | Validation error: "File size exceeds limit." | | FAIL (Silent) | High | Major |
| TC_STU_07 | TS_STU_ASGN_11 | Card Layout | 1. Verify the layout of the assignment card. | Buttons and status are properly aligned. | Buttons aligned. | PASS | Medium | Minor |
| TC_STU_18 | TS_STU_ASGN_14 | Empty Selection | 1. Click Submit without selecting file. | Validation error: "Please upload a file." | Alert shown correctly. | PASS | High | Major |
| TC_STU_19 | TS_STU_ASGN_08 | Unsupported Formats | 2. Upload .exe/.html/.js file. | System should reject file. | Allows DOC, DOCX, JPG, PNG. | FAIL | High | Critical |
| TC_STU_20 | - | Corrupted PDF | 1. Upload corrupted PDF file. | System should reject file. | (Pending Manual selection) | | High | Major |
| TC_STU_21 | TS_STU_ASGN_14 | Empty File (0KB) | 1. Upload blank 0KB file. | System should reject. | (Pending Manual selection) | | High | Major |
| TC_STU_22 | - | File Name Specs | 1. Upload file with @#% special characters in name. | System should handle correctly. | | | Medium | Minor |
| TC_STU_23 | - | Duplicate Upload | 1. Upload same file again. | System should replace or warn. | | | Medium | Minor |
| TC_STU_24 | TS_STU_ASGN_15 | Rapid Clicks | 1. Click submit multiple times (Rapid). | Only one submission should occur. | Only one alert shown. | PASS | High | Critical |
| TC_STU_25 | - | Slow Network | 1. Simulate slow network during upload. | Loader shown, no duplicate upload. | | | Medium | Major |
| TC_STU_26 | - | Session Timeout | 1. Wait session expire -> Upload. | Redirect to login / error. | | | High | Major |
| TC_STU_27 | - | Unauthorized URL | 1. Direct access Upload URL without login. | Should redirect to login. | Redirects to Home. | FAIL | High | Critical |
| TC_STU_28 | - | Responsiveness | 1. Open on mobile view. | UI should adjust properly. | Responsive layout verified. | PASS | Medium | Minor |
| TC_STU_29 | - | Button Alignment | 1. Check Upload/Download buttons. | Buttons aligned properly. | Properly aligned. | PASS | Low | Minor |
| TC_STU_30 | - | Error Clarity | 1. Trigger validation errors. | Messages should be clear. | Clear & Descriptive. | PASS | Medium | Minor |
| TC_STU_31 | - | Loading Indicator | 1. Upload file. | Loader should appear. | Not seen on local fail. | PENDING | Low | Minor |
| TC_STU_32 | - | Empty State UI | 1. No assignments available for a subject. | Show proper message. | Show correct alert. | PASS | Medium | Minor |
