# Test Cases: US-01 - Successful Login to Teacher Dashboard

**Objective:** Verify that a registered teacher can successfully log in to the Bridge Portal and that security/validation rules are enforced.

| TC ID | Test Case Description | Steps | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **TC_01_01** | Successful Login with Valid Credentials | 1. Navigate to Login Page.<br>2. Enter valid Email/Ref No.<br>3. Enter valid Password.<br>4. Click Login. | User is redirected to `/teacher/dashboard`. Header shows Name/Ref No. | High |
| **TC_01_02** | Validation - Empty Fields Submission | 1. Leave Email and Password empty.<br>2. Click Login. | Inline error "This field is required" appears for both fields with red border. | Medium |
| **TC_01_03** | Validation - Invalid Password | 1. Enter valid Email.<br>2. Enter incorrect Password.<br>3. Click Login. | Alert: "Invalid Email/Reference Number or Password." | High |
| **TC_01_04** | Security - Account Locking | 1. Enter valid Email.<br>2. Enter wrong password 5 times. | Alert: "Account locked. Please contact administrator." | High |
| **TC_01_05** | UI/UX - Password Masking | 1. Enter text in Password field. | Password must be masked (`type="password"`). | Low |
| **TC_01_06** | UI/UX - Loading Spinner | 1. Click Login with valid credentials. | Login button shows a loading spinner during authentication. | Low |
| **TC_01_07** | Performance - Login Time | 1. Measure time from Click Login to Dashboard load. | Process completes in under 3 seconds. | Medium |
| **TC_01_08** | Security - HTTPS Check | 1. Check browser URL protocol. | Connection must be HTTPS (TLS 1.3). | High |
