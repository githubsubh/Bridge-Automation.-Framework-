# Bridge Portal — User Stories (Teacher Registration Lifecycle)

> **Module:** Teacher Registration & Onboarding  
> **Version:** 2.0  
> **Prepared By:** Shubham Singh — QA  
> **Last Updated:** April 21, 2026  

This document outlines user stories, acceptance criteria, and technical validations for the complete teacher registration journey on the Bridge Portal — from login to final submission.

---

## Module 1: Login

---

### US-01: Successful Login to Teacher Dashboard

**Priority:** Must Have

**As a** registered teacher,  
**I want to** log in using my email/reference number and password,  
**So that** I can access my dashboard and manage my profile services.

**Preconditions:**
- User has a registered account in the Bridge system.
- User has a valid Email Address or Reference Number and corresponding password.
- The Bridge Portal (UAT/Production) is accessible.

**Steps to Perform:**
1. Navigate to the Bridge Portal Login page.
2. Enter a valid **Email Address** or **Reference Number**.
3. Enter the corresponding **Password** in the masked field.
4. Click on the **Login** button.

**User Acceptance Criteria (UAC):**
- **Validation:** System must check that both 'Email/Ref No' and 'Password' are not empty before submission.
- **Validation:** System must verify the credential pair against the encrypted database records.
- **Validation:** System must ensure the user account is not 'Disabled' or 'Locked' due to repeated failed attempts.
- The login process should complete in under 3 seconds.

**Expected Output:**
- User is redirected to the Teacher Dashboard (`/teacher/dashboard`).
- A secure session is established; user name and reference number are displayed in the header.

**Negative Scenarios:**
- Submitting with both fields empty → Inline error: "This field is required" on both fields.
- Entering valid email but wrong password → Alert: "Invalid Email/Reference Number or Password."
- Account locked after 5 failed attempts → Alert: "Account locked. Please contact administrator."

**Business Rules:**
- Session timeout after 30 minutes of inactivity.
- Password must be stored in an encrypted (hashed + salted) format; never transmitted in plain text.

**Non-Functional:**
- Page load time < 3 seconds.
- All credentials transmitted over HTTPS (TLS 1.3).

**UI/UX Notes:**
- Password field must be masked (`type="password"`).
- Error messages should appear inline below the respective field with a red border highlight.
- Login button must show a loading spinner during authentication.

**Risk & Impact:** HIGH — If login fails, the entire portal is inaccessible. Blocks all downstream functionality.

**Dependencies:** None (Entry point of the application).

---

### US-02: Login Security & Error Validation

**Priority:** Must Have

**As a** system administrator,  
**I want** the login form to validate all inputs and reject unauthorized attempts,  
**So that** unauthorized access and incorrect data entries are prevented.

**Preconditions:**
- Login page is loaded and accessible.

**Steps to Perform:**
1. Navigate to the Login page.
2. Enter an invalid email format (e.g., `user@abc`) or an incorrect Reference Number.
3. Enter a wrong password.
4. Click **Login**.

**User Acceptance Criteria (UAC):**
- **Validation:** Email field must check for valid `@` and domain structure (e.g., `user@domain.com`).
- **Validation:** If a field is left blank, the system must show an inline error: "This field is required."
- **Validation:** If credentials don't match, the system must display: "Invalid Email/Reference Number or Password."
- **Validation:** Password characters must be masked (`type="password"`) to ensure privacy.

**Expected Output:**
- Access is denied; user remains on the login page with descriptive inline error messages.

**Negative Scenarios:**
- SQL injection attempt in email field (e.g., `' OR 1=1 --`) → Input must be sanitized; no database error exposed.
- XSS attempt in password field (e.g., `<script>alert(1)</script>`) → Must be escaped; no script execution.
- Exceeding max character limit (500+ chars) → Graceful rejection, no server crash.

**Business Rules:**
- Maximum 5 consecutive failed login attempts before account lockout.
- Lockout duration: 15 minutes or manual unlock by admin.
- All failed attempts must be logged with timestamp and IP address for audit trail.

**Non-Functional:**
- Error responses must not reveal whether the email exists in the system (to prevent enumeration attacks).
- Rate limiting: Max 10 login requests per minute per IP.

**UI/UX Notes:**
- Invalid fields should have a red border and shake animation on submission.
- Error text should use a consistent red color (#DC2626) and 0.85rem font size.

**Risk & Impact:** CRITICAL — Security vulnerabilities here expose the entire user database and portal.

**Dependencies:** None.

---

### US-03: Clear/Reset Login Form

**Priority:** Should Have

**As a** user,  
**I want to** clear the login form with a single click,  
**So that** I can quickly re-enter my credentials if I make a mistake.

**Preconditions:**
- Login page is loaded.
- User has entered text in one or both input fields.

**Steps to Perform:**
1. Navigate to the Login page.
2. Type text into the **Email/Reference No.** field.
3. Type text into the **Password** field.
4. Click the **Clear** button.

**User Acceptance Criteria (UAC):**
- **Validation:** System must flush all input buffers and set field values to empty immediately upon clicking 'Clear'.
- **Validation:** System must remove any existing error states (red borders, inline error messages) during the reset.
- **Validation:** Clear action must not trigger form validation or any API call.

**Expected Output:**
- Both input fields are emptied, and the cursor focus returns to the first field (Email/Ref No).

**Negative Scenarios:**
- Clicking Clear when fields are already empty → No error; fields remain empty, no flicker.
- Clicking Clear during an active login API request → Clear should not interrupt the in-flight request.

**Business Rules:**
- Clear button must not submit the form or make any backend call.
- Clearing the form should not reset the failed attempt counter.

**Non-Functional:**
- Clear action must be instantaneous (< 100ms).

**UI/UX Notes:**
- Clear button should be visually distinct (outlined/secondary style) from the primary Login button.
- Focus should return to the Email/Ref No field after clear.

**Risk & Impact:** LOW — Convenience feature; no data loss or security impact.

**Dependencies:** None.

---

## Module 2: Teacher Registration (7-Stage Onboarding Wizard)

---

### US-04: Registration — Stage 1: Basic Details Entry

**Priority:** Must Have

**As a** new teacher,  
**I want to** enter my basic identity details (Full Name, Parent Names, DOB, Gender, UDISE Code, Teacher ID),  
**So that** my identity is recorded in the system as the first step of enrollment.

**Preconditions:**
- User has navigated to the Bridge Registration page.
- User possesses a valid UDISE code issued by their school.
- User has not already completed registration with the same credentials.

**Steps to Perform:**
1. Navigate to the Bridge Portal Registration / Enroll Now page.
2. Enter **Full Name** (alphabetic only, max 100 characters).
3. Enter **Father's Name** and **Mother's Name** (alphabetic only).
4. Select **Date of Birth** using the date picker (must be a past date, age 18+).
5. Select **Gender** from the dropdown (Male / Female / Transgender).
6. Enter **UDISE Code** (numeric, system performs AJAX validation against master database).
7. Enter **Teacher ID** (alphanumeric, unique identifier).
8. Click **Save & Next** to proceed to Stage 2.

**User Acceptance Criteria (UAC):**
- **Validation:** Full Name, Father's Name, and Mother's Name must accept only alphabetic characters and spaces (no digits, no special chars).
- **Validation:** DOB must not be a future date; teacher must be at least 18 years old.
- **Validation:** UDISE Code must be numeric and validated against the school master database via AJAX call; invalid code shows: "UDISE Code not found."
- **Validation:** All mandatory fields must show a red asterisk (*) indicator.
- **Validation:** Clicking "Save & Next" with any empty mandatory field triggers inline error: "This field is required."
- **Validation:** Teacher ID must be unique; duplicate shows: "Teacher ID already registered."

**Expected Output:**
- Basic details are saved to the database.
- User is automatically advanced to **Stage 2 — OTP Authentication**.
- Progress bar updates to show Stage 1 as completed (e.g., 14% or 1/7).

**Negative Scenarios:**
- Entering digits in name fields (e.g., "Raj123") → "Only alphabetic characters are allowed."
- Future date in DOB → "Date of Birth cannot be a future date."
- UDISE code with alphabets (e.g., "ABC12345") → "Only numeric values allowed."
- UDISE code that doesn't exist in master data → "UDISE Code not found in records."
- Duplicate Teacher ID → "This Teacher ID is already registered."
- Submitting with all fields blank → All mandatory fields highlight with inline errors simultaneously.

**Business Rules:**
- Registration stages must follow strict sequential order; Stage 2 is locked until Stage 1 is saved.
- Names are auto-converted to UPPERCASE on save for consistency.
- UDISE validation is a hard prerequisite — form cannot proceed without a verified UDISE.

**Non-Functional:**
- UDISE AJAX validation must respond within 2 seconds.
- All data transmitted over HTTPS.
- Form must be responsive (works on tablets and desktops).

**UI/UX Notes:**
- Progress stepper at the top showing stages 1–7 with current stage highlighted.
- Mandatory fields marked with red asterisk (*).
- UDISE field should show a green checkmark (✓) on successful validation and a red cross (✗) on failure.
- Date picker should restrict selectable dates (no future dates).

**Risk & Impact:** CRITICAL — This is the entry point of the entire registration pipeline. If Stage 1 fails, no teacher can register.

**Dependencies:** None (Entry point of registration).

---

### US-05: Registration — Stage 2: OTP Authentication

**Priority:** Must Have

**As a** registering teacher,  
**I want to** verify my identity via OTP sent to my email and mobile number,  
**So that** the system confirms my contact details are valid and belong to me.

**Preconditions:**
- Stage 1 (Basic Details) is successfully completed and saved.
- User has access to the registered email inbox and mobile phone for receiving OTP.

**Steps to Perform:**
1. System auto-navigates to Stage 2 after Stage 1 completion.
2. Enter **Email Address** (valid format: `user@domain.com`).
3. Enter **Mobile Number** (10-digit Indian mobile number).
4. Click **Send OTP** — system dispatches a 6-digit numeric OTP to both email and mobile.
5. Enter the received **6-digit OTP** in the verification field.
6. Click **Verify OTP**.
7. On success, click **Save & Next** to proceed to Stage 3.

**User Acceptance Criteria (UAC):**
- **Validation:** Email field must enforce valid email format (`@` + domain with valid TLD).
- **Validation:** Mobile number must be exactly 10 digits, starting with 6/7/8/9 (Indian mobile format).
- **Validation:** OTP field must accept only 6 numeric digits — no alphabets, no special characters.
- **Validation:** OTP expires after 10 minutes; entering expired OTP shows: "OTP has expired. Please request a new one."
- **Validation:** Maximum 3 OTP resend attempts per session.
- **Validation:** Incorrect OTP entry shows: "Invalid OTP. Please try again."
- System must send OTP via both SMS gateway and Email gateway simultaneously.

**Expected Output:**
- On successful OTP verification, a green confirmation message: "Verification Successful."
- User advances to **Stage 3 — Personal Information**.
- Progress bar updates to 2/7 completed.

**Negative Scenarios:**
- Invalid email format (e.g., `user@abc`) → "Please enter a valid email address."
- Mobile number with less than 10 digits → "Mobile number must be 10 digits."
- Mobile number starting with 0-5 → "Please enter a valid Indian mobile number."
- Entering alphabets in OTP field → Only numeric input allowed (input restriction).
- Wrong OTP → "Invalid OTP. Please try again." (with remaining attempts count).
- OTP expired after 10 mins → "OTP has expired. Please request a new one."
- Exceeding 3 resend attempts → "Maximum OTP attempts reached. Please try after 15 minutes."
- Using an already-registered email → "This email is already associated with another account."

**Business Rules:**
- OTP is a 6-digit randomly generated numeric code.
- OTP validity window: 10 minutes from generation.
- Each OTP is single-use; cannot be reused even within the validity window.
- Both email and mobile must be verified before proceeding.
- OTP delivery must use separate SMS and Email gateways for redundancy.

**Non-Functional:**
- OTP delivery must complete within 30 seconds of request.
- OTP generation must use cryptographically secure random number generation.
- Failed OTP attempts must be logged with timestamps for security audit.

**UI/UX Notes:**
- OTP input field should auto-focus and show a countdown timer (10:00 → 0:00).
- "Resend OTP" link should be disabled during the countdown and enable after 60 seconds.
- On successful verification, the OTP field should turn green with a checkmark icon.
- Loading spinner should appear on the "Send OTP" and "Verify" buttons during processing.

**Risk & Impact:** CRITICAL — If OTP fails, registration is completely blocked. Depends on third-party SMS/Email gateway reliability.

**Dependencies:** US-04 (Stage 1 must be completed first).

---

### US-06: Registration — Stage 3: Personal Information

**Priority:** Must Have

**As a** registering teacher,  
**I want to** provide my personal details (Social Category, Religion, Medium of Study),  
**So that** the system captures my demographic and academic profile data.

**Preconditions:**
- Stage 2 (OTP Authentication) is successfully verified.
- User is on the Personal Information form.

**Steps to Perform:**
1. Select **Social Category** from dropdown (General / SC / ST / OBC / Others).
2. Select **Religion** from dropdown (if applicable).
3. Select **Medium of Study** from dropdown (Hindi / English / Regional).
4. Fill any other optional fields as applicable (e.g., Marital Status, Nationality).
5. Click **Save & Next** to proceed to Stage 4.

**User Acceptance Criteria (UAC):**
- **Validation:** Social Category is a mandatory dropdown; must not remain on the default "-- Select --" placeholder.
- **Validation:** Medium of Study is mandatory and must be selected.
- **Validation:** Optional fields, if left blank, should not trigger any error.
- **Validation:** Dropdown values must be loaded from the master database (not hardcoded).
- All selected values must persist if user navigates back to this stage.

**Expected Output:**
- Personal information is saved to the database.
- User advances to **Stage 4 — Address Details**.
- Progress bar updates to 3/7 completed.

**Negative Scenarios:**
- Clicking "Save & Next" without selecting mandatory dropdowns → "Please select [field name]."
- Network failure during save → Graceful error: "Unable to save. Please check your connection and try again."
- Attempting to skip to Stage 4 via URL manipulation → System redirects back to current incomplete stage.

**Business Rules:**
- Social Category selection may affect fee structure or eligibility in downstream E-Services.
- Medium of Study determines which language-specific assignments and resources are shown post-registration.
- All field selections must be editable in Stage 7 (Review) before final submission.

**Non-Functional:**
- Dropdown options must load within 1 second of page render.
- Form state must auto-save on field change (debounced at 500ms) to prevent data loss.

**UI/UX Notes:**
- Dropdowns must use a searchable select component for long lists (e.g., Religion).
- Selected values should show a subtle blue highlight/chip.
- Mandatory fields marked with red asterisk (*).

**Risk & Impact:** MEDIUM — Data here affects downstream eligibility. Incorrect category could lead to wrong fee calculation.

**Dependencies:** US-05 (OTP Authentication must be verified).

---

### US-07: Registration — Stage 4: Address Details

**Priority:** Must Have

**As a** registering teacher,  
**I want to** enter my correspondence and permanent address,  
**So that** the system has my location details for official communication and records.

**Preconditions:**
- Stage 3 (Personal Information) is successfully saved.
- User is on the Address Details form.

**Steps to Perform:**
1. Enter **House/Flat Number** (alphanumeric, max 100 characters).
2. Enter **Locality / Street** (alphanumeric, max 200 characters).
3. Select **State** from the dropdown (loaded from master data).
4. Select **District** from the dependent dropdown (dynamically filtered by selected State via AJAX).
5. Enter **Pincode** (6-digit numeric, Indian postal code format).
6. Optionally check "Same as Correspondence Address" to auto-fill Permanent Address.
7. Click **Save & Next** to proceed to Stage 5.

**User Acceptance Criteria (UAC):**
- **Validation:** House No., Locality, State, District, and Pincode are all mandatory.
- **Validation:** State dropdown must load all Indian states/UTs from the master database.
- **Validation:** District dropdown must dynamically update based on selected State (AJAX call). It should be disabled/empty until a State is selected.
- **Validation:** Pincode must be exactly 6 numeric digits.
- **Validation:** "Same as Correspondence" checkbox must auto-populate all permanent address fields and lock them from editing.
- **Validation:** Unchecking the "Same as" checkbox must re-enable permanent address fields and clear the auto-filled data.

**Expected Output:**
- Address details are saved to the database.
- User advances to **Stage 5 — Eligibility & Subjects**.
- Progress bar updates to 4/7 completed.

**Negative Scenarios:**
- Entering alphabets in Pincode → "Pincode must be numeric."
- Pincode with less than 6 digits (e.g., "1234") → "Pincode must be exactly 6 digits."
- Selecting State but no District available (data gap) → Graceful message: "No districts available for selected state."
- Attempting to proceed without selecting District → "Please select a District."
- Special characters in House No. / Locality (e.g., `<script>`) → Input sanitized, no XSS execution.
- Network failure during District AJAX load → "Unable to load districts. Please refresh and try again."

**Business Rules:**
- District dropdown is AJAX-dependent on State; cannot be pre-loaded or independently selected.
- Address fields are auto-converted to UPPERCASE on save for postal consistency.
- Both Correspondence and Permanent Address are collected; at least Correspondence is mandatory.

**Non-Functional:**
- District AJAX call must respond within 2 seconds of State selection.
- Form must work on slow 3G connections (graceful degradation with loading indicators).

**UI/UX Notes:**
- State → District should show a loading spinner in the District dropdown while AJAX is in progress.
- Pincode field should enforce numeric-only input via keypress restriction (not just validation on submit).
- "Same as Correspondence" checkbox should trigger a smooth animation filling the permanent address fields.
- Address fields should auto-capitalize text as user types.

**Risk & Impact:** MEDIUM — Incorrect address impacts official communications. AJAX dependency on State → District is a common failure point.

**Dependencies:** US-06 (Personal Information must be completed).

---

### US-08: Registration — Stage 5: Eligibility & Subject Selection

**Priority:** Must Have

**As a** registering teacher,  
**I want to** provide my appointment details and select the subjects I teach,  
**So that** the system can map me to the correct academic resources and assignments.

**Preconditions:**
- Stage 4 (Address Details) is successfully saved.
- User is on the Eligibility & Subjects form.

**Steps to Perform:**
1. Select or enter **Date of Appointment** using the date picker (must be a past or present date).
2. Select **Employment Type** from dropdown (if applicable — Regular / Contractual / Guest).
3. Select **Subject(s)** from the multi-select dropdown or checkbox list.
4. Select **Medium of Instruction** for each selected subject (Hindi / English / Regional).
5. Click **Save & Next** to proceed to Stage 6.

**User Acceptance Criteria (UAC):**
- **Validation:** Date of Appointment must not be a future date.
- **Validation:** Date of Appointment must be after the teacher's Date of Birth (cross-stage validation).
- **Validation:** At least one subject must be selected.
- **Validation:** For each selected subject, a Medium of Instruction must be assigned.
- **Validation:** Subject list must be loaded from the master database based on teacher's school level (Primary / Secondary / Senior Secondary).

**Expected Output:**
- Eligibility and subject details are saved to the database.
- User advances to **Stage 6 — Document Upload**.
- Progress bar updates to 5/7 completed.

**Negative Scenarios:**
- Future Date of Appointment → "Date of Appointment cannot be a future date."
- Date of Appointment before DOB → "Date of Appointment cannot be before your Date of Birth."
- No subject selected → "Please select at least one subject."
- Subject selected but no medium assigned → "Please select Medium of Instruction for all subjects."
- Attempting to select more subjects than the allowed limit (if applicable) → "Maximum [N] subjects allowed."

**Business Rules:**
- Subject options are filtered by the school's recognized level (UDISE-linked from Stage 1).
- The selected subjects determine which TMA assignments appear on the teacher's dashboard after registration.
- Date of Appointment may have min/max year constraints based on organizational policy.
- Employment Type field may have an asterisk (*) indicating mandatory status (verify UI consistency).

**Non-Functional:**
- Subject list API call must complete within 2 seconds.
- Multi-select should support keyboard navigation and search filtering.

**UI/UX Notes:**
- Date picker should restrict selectable dates (disable future dates).
- Multi-select subject dropdown should show selected items as removable chips/tags.
- A clear visual mapping between subject ↔ medium selections (e.g., table format or paired rows).
- Date of Appointment field should have a calendar icon trigger.

**Risk & Impact:** HIGH — Incorrect subject mapping means teachers receive wrong assignments and study materials. Cascading data integrity issue.

**Dependencies:** US-07 (Address Details must be completed). Cross-validates with US-04 (DOB from Stage 1).

---

### US-09: Registration — Stage 6: Document Upload

**Priority:** Must Have

**As a** registering teacher,  
**I want to** upload my required documents (Photo, Signature, B.Ed Certificate, ID Proof),  
**So that** the system has verifiable proof of my identity and qualifications.

**Preconditions:**
- Stage 5 (Eligibility & Subjects) is successfully saved.
- User has digital copies of required documents in JPG, PNG, or PDF format (each < 2MB).

**Steps to Perform:**
1. Upload **Profile Photo** (JPG/PNG, < 2MB, passport-size dimensions recommended).
2. Upload **Signature** (JPG/PNG, < 2MB).
3. Upload **B.Ed / D.El.Ed Certificate** (JPG/PDF, < 2MB).
4. Upload **ID Proof** (Aadhaar / PAN / Voter ID) (JPG/PDF, < 2MB).
5. Upload any other mandatory documents as specified by the system.
6. Preview each uploaded document by clicking the thumbnail.
7. Click **Save & Next** to proceed to Stage 7.

**User Acceptance Criteria (UAC):**
- **Validation:** Each upload field must accept only allowed formats: JPG, JPEG, PNG, PDF.
- **Validation:** Each file must be under 2MB; exceeding this shows: "File size must be less than 2MB."
- **Validation:** Uploading an unsupported format (e.g., `.exe`, `.php`, `.html`) → "Invalid file type. Only JPG, PNG, and PDF are allowed."
- **Validation:** All mandatory document fields must be filled before proceeding.
- **Validation:** Uploaded files should show a thumbnail preview (for images) or file name (for PDFs).
- **Validation:** Users must be able to remove/replace an uploaded file before saving.

**Expected Output:**
- All documents are uploaded and stored in the server's document management system.
- User advances to **Stage 7 — Review & Submit**.
- Progress bar updates to 6/7 completed.

**Negative Scenarios:**
- Uploading a .exe file → "Invalid file type. Only JPG, PNG, and PDF are allowed."
- Uploading a 5MB image → "File size must be less than 2MB."
- Uploading a corrupt/empty file → "File could not be processed. Please upload a valid document."
- Attempting to proceed without mandatory uploads → "Please upload [Document Name]."
- Attempting to upload when server storage is full → Graceful error, not a server crash.
- Network timeout during upload → "Upload failed. Please try again."
- Uploading an image with malicious EXIF data or embedded scripts → Server-side sanitization must strip metadata.

**Business Rules:**
- B.Ed Certificate is mandatory for all registrations — no exceptions.
- Photo must meet dimensional or aspect ratio guidelines (if enforced).
- All uploaded documents are stored in an encrypted format at rest (AES-256).
- Documents are retained for a minimum of 10 years as per retention policy.

**Non-Functional:**
- Upload must support progress indicator for files, especially on slow connections.
- Maximum upload time: 30 seconds per file before timeout.
- Server must validate file content (MIME type) not just extension (to prevent extension spoofing).

**UI/UX Notes:**
- Each upload slot should show a drag-and-drop zone with a file browser fallback.
- Thumbnail preview for images; file icon + name for PDFs.
- A "Remove" (✗) button on each uploaded file for replacement.
- Progress bar inside each upload slot showing upload percentage.
- Green checkmark (✓) on successful upload; red cross (✗) on failure.

**Risk & Impact:** HIGH — Without documents, registration cannot be verified. Blocking stage for final submission.

**Dependencies:** US-08 (Eligibility must be completed).

---

### US-10: Registration — Stage 7: Review & Submit

**Priority:** Must Have

**As a** registering teacher,  
**I want to** review all the information I've entered across all stages before final submission,  
**So that** I can verify accuracy and make corrections before my application is locked.

**Preconditions:**
- Stages 1 through 6 are all successfully completed and saved.
- User is on the Review & Submit page.

**Steps to Perform:**
1. System displays a **read-only summary** of all data entered across Stages 1–6, organized section-wise.
2. Each section (Basic Details, Authentication, Personal Info, Address, Eligibility, Documents) has an **"Edit"** button.
3. Click **Edit** on any section → User is redirected to that specific stage for modification.
4. After editing, user returns to the Review page with updated data reflected.
5. Review all uploaded document thumbnails to verify correct files.
6. Check the **Declaration checkbox** (e.g., "I confirm all details are correct and truthful").
7. Click **Submit** to finalize the registration.

**User Acceptance Criteria (UAC):**
- **Validation:** All data from Stages 1–6 must be displayed accurately in read-only format.
- **Validation:** Each section must have a functional "Edit" link that navigates to the correct stage.
- **Validation:** After editing and returning, the Review page must reflect the updated data immediately.
- **Validation:** The declaration checkbox must be checked before "Submit" is enabled.
- **Validation:** Clicking "Submit" without the checkbox checked → "Please accept the declaration to proceed."
- **Validation:** On successful submission, a unique **Registration / Reference Number** must be generated and displayed.
- **Validation:** Post-submission, the user should not be able to re-access the registration wizard; they are redirected to the Dashboard or a confirmation page.

**Expected Output:**
- Registration data is finalized and locked in the database.
- A unique **Reference Number** is generated and displayed to the user.
- Confirmation screen shows registration success with transaction details (if payment is involved).
- User can download or print the confirmation receipt.
- Progress bar shows 7/7 — 100% complete.

**Negative Scenarios:**
- Attempting to submit without the declaration checkbox → "Please accept the declaration to proceed."
- Network failure during submission → "Submission failed. Your data is saved. Please try again."
- Double-clicking the Submit button rapidly → System must prevent duplicate submissions (idempotency).
- Browser back button after submission → Should not re-trigger submission; show confirmation page or dashboard.
- Session timeout on the Review page (30+ mins idle) → Redirect to login with data preserved.

**Business Rules:**
- Once submitted, data is locked for admin review — the teacher cannot modify it from their side.
- A unique Reference Number (e.g., `BRIDGE-2026-XXXXX`) is auto-generated.
- The registration status after submission is "Pending Verification" until an admin/principal reviews it.
- Payment (if applicable) is a prerequisite before the final submission button is enabled.
- All submitted data must be immutable in the audit trail — any subsequent changes go through E-Services.

**Non-Functional:**
- Submission API call must complete within 5 seconds.
- Reference Number generation must be atomic (no duplicate numbers under concurrent load).
- Submission must be idempotent — multiple clicks produce only one registration entry.

**UI/UX Notes:**
- Review page should use a clean card-based layout with collapsible sections.
- Uploaded documents should show clickable thumbnails that open in a lightbox/modal.
- Edit buttons should be clearly visible (icon + text) aligned to the right of each section header.
- Submit button should show a confirmation modal: "Are you sure? This action cannot be undone."
- On success, display a prominent green success banner with the Reference Number in large bold text.
- Provide a "Download Receipt" / "Print" button on the confirmation screen.

**Risk & Impact:** CRITICAL — This is the final gate. Any failure here means the entire 6-stage effort is wasted. Double-submission creates duplicate records. Must be bulletproof.

**Dependencies:** US-04 through US-09 (All previous stages must be completed).

---

## Module 3: Teacher Dashboard (Post-Enrollment)

---

### US-11: Dashboard Overview & Progress Tracking

**Priority:** Must Have

**As a** fully registered teacher,  
**I want to** see my profile progress and service tiles upon login,  
**So that** I can easily navigate to various educational and administrative services.

**Preconditions:**
- User is successfully logged in.
- User has completed 100% of the registration process.

**Steps to Perform:**
1. Log in to the Bridge Portal.
2. System redirects to the Teacher Dashboard.
3. Observe the **Progress Tile** and **Service Grid**.

**User Acceptance Criteria (UAC):**
- **Validation:** If registration is incomplete ( < 100%), the Progress tile must show the current percentage and a "Complete Registration" button.
- **Validation:** If registration is 100% complete, the dashboard must unlock the E-Services, Study Material, and Results tiles.
- **Validation:** The header must display the Teacher's Full Name and unique Reference Number.
- **Validation:** Clicking on any service tile (e.g., E-Services) must redirect the user to the respective module without re-authentication (SSO).

**Expected Output:**
- User sees a clean, tile-based interface showing 100% completion and accessible service modules.

**Negative Scenarios:**
- Login with partially completed profile → System redirects to the specific incomplete registration stage, not the dashboard home.
- Session expired → Clicking any tile redirects to the Login page with a message: "Session expired. Please login again."
- Manual URL entry to E-Services when profile is < 100% → Authorization bounce-back to dashboard.

**Business Rules:**
- Dashboard accessibility is strictly linked to Stage 7 (Submission) completion.
- Data on the dashboard (Name, School) must be read-only and fetched from the latest verified profile.

**Non-Functional:**
- Dashboard load time < 2 seconds.
- All dynamic tiles must load via asynchronous API calls to prevent UI blocking.

**UI/UX Notes:**
- Multi-colored tiles (e.g., Green for Progress, Blue for E-Services, Yellow for Grievances).
- Responsive grid (2x2 on mobile, 4x2 on desktop).
- Animated progress bar showing 100% movement on page load.

**Risk & Impact:** MEDIUM — The dashboard is the central hub. Incorrect progress reporting may confuse users or block access to valid services.

**Dependencies:** US-10 (Registration must be submitted).

---

## Module 4: E-Services (Profile Modifications)

---

### US-12: E-Service Access & 2FA Verification

**Priority:** Must Have

**As a** registered teacher,  
**I want to** verify my identity via OTP before accessing any profile modification form,  
**So that** my profile data remains secure even if my session is compromised.

**Preconditions:**
- User is on the "Available E-Services" page.
- User selects a specific service (e.g., Name Correction).

**Steps to Perform:**
1. Click on a service tile in the E-Services grid.
2. Observe the OTP Verification screen.
3. Click "Send OTP" and enter the 6-digit code received.
4. Click "Verify and Proceed".

**User Acceptance Criteria (UAC):**
- **Validation:** System must not load the modification form until OTP is successfully verified.
- **Validation:** OTP must be sent to the registered mobile/email stored during registration (Stage 2).
- **Validation:** The "Verify" button must remain disabled until a 6-digit numeric input is provided.
- **Validation:** System must provide a "Resend OTP" option after a 60-second cooldown.

**Expected Output:**
- Upon successful verification, the specific E-Service form is loaded.

**Negative Scenarios:**
- Entering an incorrect OTP → "Invalid verification code. Please try again."
- OTP expired → "Verification code expired. Please resend."
- Attempting to resend OTP before the 60-second cooldown → Resend link remains disabled.
- Entering alphabets in the OTP numeric boxes → Validation prevents non-numeric input.

**Business Rules:**
- 2FA is mandatory for ALL 16 E-Services; no bypass allowed.
- Verification is service-specific; completing OTP for "Change Address" does not grant access to "Name Correction" without another OTP.
- OTP generated must be cryptographically secure and unique per request.

**Non-Functional:**
- OTP delivery time < 30 seconds.
- Verification API response < 1 second.
- Service remains locked in the browser session until the specific OTP success flag is received.

**UI/UX Notes:**
- Multi-box (6 individual inputs) for OTP entry for better mobile experience.
- Visual countdown timer (e.g., 5:00) displayed next to the resend link.

**Risk & Impact:** CRITICAL — This is the primary security gate for profile hijacking prevention.

**Dependencies:** US-05 (Registration OTP logic).

---

### US-13: Profile Modification — Field Comparison & Upload

**Priority:** Must Have

**As a** teacher,  
**I want to** see my current data side-by-side with new input fields,  
**So that** I can accurately update my details and provide required proof.

**Preconditions:**
- OTP for the specific E-Service is verified.
- User is on the Modification Form (e.g., Change Correspondence Address).

**Steps to Perform:**
1. Observe the "Current Data" (Read-only) on the left/top.
2. Enter "New Data" in the editable fields on the right/bottom.
3. Upload the mandatory supporting document.
4. Click "Preview & Submit".

**User Acceptance Criteria (UAC):**
- **Validation:** Form must display existing database values in a clear Read-Only format.
- **Validation:** New input fields must enforce the same validation rules as the registration module (e.g., Pincode must be 6 digits).
- **Validation:** System must require at least one supporting document (JPG/PDF < 2MB).
- **Validation:** If "New Data" is identical to "Current Data", the system should prevent submission: "No changes detected."

**Expected Output:**
- User successfully fills the update request and attaches proof.

**Negative Scenarios:**
- Submitting with mandatory fields blank → Inline errors: "This field is required."
- Uploading a file larger than 2MB → "File size exceeds the 2MB limit."
- Uploading an unsupported format (.exe, .txt) → "Invalid file format. Please upload JPG/PNG/PDF."
- Entering same data as current profile → "No changes detected. You cannot submit without modifying data."

**Business Rules:**
- All changes go into a "Pending Verification" status until Admin approval.
- B.Ed Certificate is mandatory for all academic corrections.
- New data is only committed to the master record after final Admin/Principal approval.
- Submission must generate a unique Request ID for tracking.

**Non-Functional:**
- Form submission < 3 seconds.
- Side-by-side view must handle long text strings without breaking layout.

**UI/UX Notes:**
- Split-screen layout (Current vs New).
- Highlight changed fields in a different color (e.g., subtle yellow background).
- Clear labels indicating "Old Data" and "Updated Data".

**Risk & Impact:** HIGH — Data integrity issue if new data isn't validated correctly. Leads to certificate errors.

**Dependencies:** US-12 (2FA must be verified first).

## Module 5: Assignment Management (Admin / Superadmin)

---

### US-14: Centralized Assignment Creation (Multi-Medium)

**Priority:** Must Have

**As a** Superadmin,  
**I want to** create assignments by selecting an academic year, subject, and uploading language-specific documents,  
**So that** teachers and students receive the correct TMA resources for their chosen medium.

**Preconditions:**
- User is logged in as Superadmin.
- User is on the "Add Assignment" modal/page.

**Steps to Perform:**
1. Select **Academic Year** (e.g., 2025-26).
2. Select **Subject** from the searchable dropdown.
3. Enter **Weightage Marks** and **Max Marks** (integers only).
4. Expand a **Language Section** (e.g., English or Hindi).
5. Upload a **PDF Assignment Document** (< 5MB).
6. Provide an **Assignment Title** and set Status to "Active".
7. Click **Create**.

**User Acceptance Criteria (UAC):**
- **Validation:** System must restrict Weightage Marks to be less than or equal to Max Marks.
- **Validation:** System must reject non-numeric characters and decimals in marks fields.
- **Validation:** At least one language medium section must have an uploaded document before submission.
- **Validation:** Duplicate check: System should prevent creating the same assignment (Same Year + Subject) twice.

**Expected Output:**
- Assignment record is created; success message "Created Successfully" is displayed.
- The record appears in the Assignment Summary list with a "Preview" capability.

**Negative Scenarios:**
- Uploading a non-PDF file (.docx, .png) → "Only PDF files are allowed for assignments."
- Setting Max Marks to 0 → "Marks must be greater than zero."
- Rapidly double-clicking "Create" → System must process only one request (Idempotency).
- Weightage marks > Max Marks → "Weightage marks cannot exceed total marks."
- Entering special characters in mark fields → "Please enter numeric values only."

**Business Rules:**
- Assignment Status defaults to "Active" but can be toggled to "Inactive".
- Assignments are mapped to a specific Subject and Academic Year combined uniquely.
- Mark fields must accept only whole numbers (integers).

**Non-Functional:**
- Modal/Page for creation must load < 2 seconds.
- Uploaded PDF must be viewable via a secure blob URL for preview.

**UI/UX Notes:**
- Card-based layout for different media (English, Hindi, Regional).
- Status toggle with toggle-switch UI.
- Subject dropdown should be searchable (Chosen.js or Select2).

**Risk & Impact:** HIGH — Assignments are core to the certification process. Errors here impact all students.

**Dependencies:** Superadmin authorization; Subject Master Data.

## Module 6: Subject Expert Management (SME)

---

### US-15: SME Onboarding & Identity Validation

**Priority:** Must Have

**As a** system administrator,  
**I want to** register Subject Experts with validated identity and professional details,  
**So that** only qualified experts are authorized to evaluate student assignments.

**Preconditions:**
- Admin is on the "Add SME" page.

**Steps to Perform:**
1. Enter **SME Name**, **DOB**, and **Gender**.
2. Enter **PAN Number** (must follow regex `[A-Z]{5}[0-9]{4}[A-Z]`).
3. Enter **Mobile Number** and **Email Address**.
4. Upload **SME Signature** (JPG/PNG < 2MB).
5. Click **Save**.

**User Acceptance Criteria (UAC):**
- **Validation:** DOB must ensure the expert is at least 18 years old.
- **Validation:** PAN format must be strictly enforced.
- **Validation:** Email and Mobile must be unique; duplicate entries must show: "[Field] already exists in the system."
- **Validation:** Signature upload is mandatory for digitized evaluation results.

**Expected Output:**
- Account is created in "Draft" or "Active" status.
- Primary credentials (Email/Mobile) are verified via the database unique index.

**Negative Scenarios:**
- Entering invalid PAN format (e.g., 123456) → "Enter a valid 10-digit PAN (e.g., ABCDE1234F)."
- Duplicate PAN entry → "This PAN is already registered with another expert."
- SME age < 18 based on DOB → "Experts must be at least 18 years old."
- Missing signature upload → "Please upload the SME signature."

**Business Rules:**
- PAN Number is mandatory for financial payroll/payout tracking.
- SME ID is auto-generated in the format `SME-2026-XXXX`.
- Draft SMEs cannot be used for TMA allocation until 'Activated' by admin.

**Non-Functional:**
- Search for existing SMEs by Mobile/Email < 1 second.
- Account creation logs IP and Admin ID for audit trailing.

**UI/UX Notes:**
- Form should have clear section headers (Personal, Professional, Documents).
- PAN field should auto-capitalize input.

**Risk & Impact:** MEDIUM — Inaccurate SME data leads to payment and verification issues later.

**Dependencies:** Admin login; Document storage module.

### US-16: SME-to-School Mapping & Subject Binding

**Priority:** Must Have

**As a** system administrator,  
**I want to** map an SME to multiple schools and subjects across districts,  
**So that** the expert is available for allocation in those specific school-subject clusters.

**Preconditions:**
- SME profile is active.
- Admin is on the "SME Mapping" interface.

**Steps to Perform:**
1. Select **SME** from the list.
2. Select **District** (loads State-filtered schools).
3. Select **School(s)** from the checkbox list.
4. Select **Subject(s)** the expert is qualified for.
5. Click **Map**.

**User Acceptance Criteria (UAC):**
- **Validation:** SME must be able to bind to 10+ schools and multiple subjects simultaneously.
- **Validation:** System must prevent mapping an SME to a school they are already linked to.
- **Validation:** If an SME is unlinked from a school, they should immediately disappear from that school's allocation dropdown.

**Expected Output:**
- Mapping record is created; SME appears in the corresponding allocation lists.

**Negative Scenarios:**
- Attempting to map to a school already linked → "SME is already mapped to this school."
- Mapping to a district where the SME has no address/operating record (if restricted) → Warning.
- Selecting 0 schools before saving → "Please select at least one school."

**Business Rules:**
- Mapping is time-bound (usually for an academic session).
- One SME can be mapped to multiple subjects but must be verified for each.
- Unlinking does not delete past evaluation records for that mapping.

**Non-Functional:**
- Mapping table should handle bulk selections (50+ schools) without reload lag.
- District-based filtering of schools must be dynamic (AJAX).

**UI/UX Notes:**
- Dual-list box or Multi-select with search for schools.
- Select All / Clear All functionality for rapid mapping.

**Risk & Impact:** HIGH — Mapping errors result in experts receiving subjects they aren't qualified in.

**Dependencies:** US-15 (SME must be registered).

### US-17: Student Evaluation Allocation (TMA Routing)

**Priority:** Must Have

**As a** Principal/Superadmin,  
**I want to** allocate student assignments to Subject Experts based on Medium and Subject match,  
**So that** evaluation happens by the correct specialist.

**Preconditions:**
- Student has submitted their assignment.
- SME is mapped to the school and subject.

**Steps to Perform:**
1. Navigate to "TMA Allocation".
2. Filter students by **Subject** and **Medium**.
3. Select students and choose an **SME** from the dynamic dropdown.
4. Click **Allocate**.

**User Acceptance Criteria (UAC):**
- **Validation:** The SME dropdown must ONLY show experts who match the student's Subject AND Medium (Hindi/English).
- **Validation:** System must record the allocation with timestamp and Principal ID.
- **Validation:** Allocation status must change from 'Unallocated' to 'Allocated' globally.

**Expected Output:**
- Students are successfully assigned to the Subject Expert; counts update in real-time.

**Negative Scenarios:**
- Selecting an SME who doesn't match the student's medium → Allocation should be prevented by UI (dropdown filter).
- Re-allocating an assignment that is already 'In-Progress' → "Evaluation started. Cannot change expert."
- Double allocation of the same student → System prevents duplicate active assignments.

**Business Rules:**
- Allocation is one-to-one per student-subject pair.
- The 'Unallocated' counter must be the primary KPI for the Principal dashboard.
- If an expert is 'Suspended', their name must be removed from the allocation list.

**Non-Functional:**
- Allocation batch process for 100+ students < 5 seconds.
- Real-time notification (WebSocket or Email) to the expert upon allocation.

**UI/UX Notes:**
- Bulk action toolbar for selecting multiple students.
- Display "Expert Load" (how many assignments currently with them) in the dropdown.

**Risk & Impact:** CRITICAL — Wrong allocation (e.g., Hindi student to English expert) blocks the evaluation pipeline.

**Dependencies:** US-14 (Assignments must exist), US-16 (SME must be mapped).

## Summary: Story Coverage Matrix (Finalized)

| Story ID | Module | Title | Priority | Risk |
|----------|-------|-------|----------|------|
| US-01 | Login | Successful Login | Must Have | HIGH |
| US-02 | Login | Security & Error Validation | Must Have | CRITICAL |
| US-03 | Login | Clear/Reset Form | Should Have | LOW |
| US-04 | Stage 1 | Basic Details Entry | Must Have | CRITICAL |
| US-05 | Stage 2 | OTP Authentication | Must Have | CRITICAL |
| US-06 | Stage 3 | Personal Information | Must Have | MEDIUM |
| US-07 | Stage 4 | Address Details | Must Have | MEDIUM |
| US-08 | Stage 5 | Eligibility & Subjects | Must Have | HIGH |
| US-09 | Stage 6 | Document Upload | Must Have | HIGH |
| US-10 | Stage 7 | Review & Submit | Must Have | CRITICAL |
| US-11 | Dashboard | Dashboard & Progress Tracking | Must Have | MEDIUM |
| US-12 | E-Services | Access & 2FA Verification | Must Have | CRITICAL |
| US-13 | E-Services | Field Comparison & Upload | Must Have | HIGH |
| **US-14** | Assignments | Multi-Medium Creation | Must Have | HIGH |
| **US-15** | SME | Onboarding & Validation | Must Have | MEDIUM |
| **US-16** | SME | School/Subject Mapping | Must Have | HIGH |
| **US-17** | SME/TMA | Evaluation Allocation | Must Have | CRITICAL |

---

> **Completed Modules:** Login, Registration (7 Stages), Dashboard, E-Services, Assignment Management


