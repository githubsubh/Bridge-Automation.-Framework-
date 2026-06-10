# 📘 Bridge Automation Framework — User Manual

> **Project:** NIOS Bridge Course Registration & E-Services Automation
> **Environment:** UAT — `https://bridge-uat.nios.ac.in`
> **Framework:** Python · Selenium WebDriver · Pytest
> **Version:** 1.0 | February 2026

---

## Table of Contents

1. [Overview](#1-overview)
2. [Framework Architecture](#2-framework-architecture)
3. [Prerequisites & Setup](#3-prerequisites--setup)
4. [Project Structure](#4-project-structure)
5. [Configuration Guide](#5-configuration-guide)
6. [Registration Flow — Step-by-Step](#6-registration-flow--step-by-step)
   - Step 1: Basic Details
   - Step 2: Eligibility
   - Step 3: Authentication
   - Step 4: OTP Verification
   - Step 5: Personal Information
   - Step 6: Address Details
   - Step 7: Subject Details
   - Step 8: Document Upload
   - Step 9: Review Page
   - Step 10: Payment
7. [E-Services Flow](#7-e-services-flow)
8. [Running the Tests](#8-running-the-tests)
9. [Test Data Management](#9-test-data-management)
10. [Page Object Reference](#10-page-object-reference)
11. [Utilities Reference](#11-utilities-reference)
12. [Troubleshooting Guide](#12-troubleshooting-guide)
13. [Test Results & Reports](#13-test-results--reports)

---

## 1. Overview

The **Bridge Automation Framework** is a Selenium-based end-to-end test automation suite designed to automate the **NIOS Bridge Course** portal hosted at `https://bridge-uat.nios.ac.in`. It covers:

| Module | Coverage |
|---|---|
| **Registration** | Complete 10-step new teacher registration flow with payment |
| **E-Services** | All 14 available e-services applied through UI automation |
| **Negative Testing** | Invalid input handling, error message validation |
| **Dashboard** | Post-login dashboard navigation and feature verification |

### Key Design Principles

- **Page Object Model (POM):** All UI interactions are encapsulated in Page classes under `/pages`
- **Data-Driven:** Test data is externalized in `config/config.ini` and `test_data/`
- **Human-in-the-loop:** OTP and CAPTCHA steps pause and wait for manual human input
- **Robust Waits:** Uses explicit WebDriverWait (not `time.sleep`) wherever possible
- **Centralized Logging:** All actions logged via `utilities/custom_logger.py`

---

## 2. Framework Architecture

```
Bridge-Automation.-Framework-
│
├── config/               ← config.ini (URLs, credentials, timeouts)
├── pages/                ← Page Object classes (one per page)
├── tests/
│   ├── conftest.py       ← Pytest fixtures (browser setup/teardown)
│   └── test/
│       ├── registration/ ← Registration test suites
│       ├── eservices/    ← E-Services test suites
│       ├── auth/         ← Authentication tests
│       └── dashboard/    ← Dashboard tests
├── utilities/            ← Helper utilities (logging, data, config reader)
├── test_data/            ← Dummy files (dummy.jpg, dummy.pdf) and counters
├── screenshots/          ← Auto-captured step screenshots
├── logs/                 ← Test run logs
└── reports/              ← HTML test reports
```

### Dependency Flow

```
conftest.py (browser fixture)
    └── Tests (test_registration.py, test_functional_eservices_workflow.py)
            └── Page Objects (RegistrationPage, LoginPage, etc.)
                    └── BasePage (shared interactions: click, send_keys, etc.)
                            └── Utilities (ReadConfig, LogGen, DataUtils)
```

---

## 3. Prerequisites & Setup

### 3.1 System Requirements

| Requirement | Version |
|---|---|
| Python | 3.9+ |
| Google Chrome | Latest stable |
| ChromeDriver | Matching Chrome version |
| pip | Latest |

### 3.2 Installation

```bash
# 1. Clone / unzip the project
cd "Bridge-Automation.-Framework-"

# 2. Install Python dependencies
pip install pytest selenium faker configparser

# 3. Verify ChromeDriver is on PATH
chromedriver --version

# 4. Confirm config is set up correctly
type config\config.ini
```

### 3.3 Folder Preparation

The following folders must exist (created automatically on first run):
- `test_data/` — for dummy files and email counter
- `screenshots/`
- `logs/`

---

## 4. Project Structure

### 4.1 Pages Directory (`/pages`)

| File | Purpose |
|---|---|
| `base_page.py` | Base class with shared Selenium helpers (click, type, hover, waits) |
| `home_page.py` | Homepage navigation → Teacher Login |
| `login_page.py` | Login form + manual CAPTCHA handler |
| `registration_page.py` | Step 1 — Basic Details form |
| `eligibility_page.py` | Step 2 — Eligibility / Date of Appointment |
| `authentication_page.py` | Step 3 — Email & Mobile entry |
| `otp_page.py` | Step 4 — OTP entry (manual by human) |
| `personal_information_page.py` | Step 5 — Social Category & Medium |
| `address_details_page.py` | Step 6 — Address form |
| `subject_details_page.py` | Step 7 — Subject medium selection |
| `documents_page.py` | Step 8 — Document upload |
| `payment_flow_page.py` | Steps 9-10 — Review, gateway, payment |
| `dashboard_page.py` | Post-login dashboard navigation |
| `eservices_page.py` | E-Services list page: discover & iterate services |

### 4.2 Tests Directory (`/tests/test`)

| Folder | Key Files |
|---|---|
| `registration/` | `test_registration.py` (positive), `test_registration_negative.py` |
| `eservices/` | `test_functional_eservices_workflow.py` (all 14 services) |
| `auth/` | Authentication-specific tests |
| `dashboard/` | Dashboard navigation tests |

---

## 5. Configuration Guide

All framework settings live in `config/config.ini`:

```ini
[common info]
base_url = https://bridge-uat.nios.ac.in/registration/basic-details
browser = chrome
implicit_wait = 10
explicit_wait = 10

[login]
url = https://bridge-uat.nios.ac.in/auth/login
email = subh7409@gmail.com
password = Password@1

[payment]
gateway_name = SabPaisa
mode = Cards
card_number = 4000020000000000
card_holder = Test Automation User
card_expiry = 12/30
card_cvv = 234

[paths]
test_data_dir = test_data
email_counter_file = email_counter.txt
dummy_jpg = dummy.jpg
dummy_pdf = dummy.pdf

[timeouts]
stabilization_wait = 1
page_load_wait = 10
otp_wait = 120
gateway_wait = 2
```

### Configuration Key Points

> **⚠️ Important:** Update `[login]` credentials before running tests in a new environment.

| Setting | Description |
|---|---|
| `base_url` | Starting URL for new registrations |
| `otp_wait` | Seconds the script waits for OTP input (default: 120s) |
| `gateway_name` | Payment gateway (`SabPaisa`) |
| `mode` | Payment mode — `Cash` (Challan) or `Cards` |
| `card_number` | Test card for sandbox — `4000020000000000` |

---

## 6. Registration Flow — Step-by-Step

The registration test is run via:

```bash
pytest tests/test/registration/test_registration.py -v -s
```

The script automates a **10-step registration process**. Steps requiring human input (OTP, CAPTCHA) pause the script and display console prompts.

---

### Step 1 — Basic Details

**File:** `pages/registration_page.py`
**URL:** `https://bridge-uat.nios.ac.in/registration/basic-details`

**What the script does:**
1. Navigates to the registration URL
2. Waits for the form to be visible
3. Handles any dismissal modal (SweetAlert2)
4. Generates a random name using `Faker`
5. Fills in Name, Father's Name, Mother's Name
6. Sets Date of Birth via JavaScript (`15-08-1990`)
7. Selects Gender from Chosen.js dropdown (`Male`)
8. Enters UDISE Code (`10101000101`)
9. Clicks **Verify UDISE**
10. Clicks **Continue**

**Test Data Used:**

| Field | Value |
|---|---|
| Name | Auto-generated (Faker) |
| Father Name | "Father " + generated name |
| Mother Name | "Mother " + generated name |
| Date of Birth | 15-08-1990 |
| Gender | Male |
| UDISE Code | 10101000101 |

**Screenshot:**

![Step 1 - Basic Details](screenshots/Step1_Basic_Details.png)

---

### Step 2 — Eligibility

**File:** `pages/eligibility_page.py`
**URL:** `https://bridge-uat.nios.ac.in/registration/eligibility`

**What the script does:**
1. Waits for URL to contain `eligibility`
2. Sets Date of Appointment: `01-01-2022`
3. Clicks Continue (step is skipped gracefully if already pre-filled)

**Screenshot:**

![Step 2 - Eligibility](screenshots/Step2_Eligibility.png)

> **Note:** The eligibility page may sometimes be auto-filled or skipped by the system. The test handles this gracefully with a `try/except`.

---

### Step 3 — Authentication

**File:** `pages/authentication_page.py`
**URL:** `https://bridge-uat.nios.ac.in/registration/authentication`

**What the script does:**
1. Waits for URL to contain `authentication`
2. Generates an **incremental email** (e.g., `subh7409+5@gmail.com`) using a counter file
3. Uses **fixed mobile number:** `6268326377`
4. Fills Email and Mobile fields
5. Clicks **Submit** to trigger OTP

**Screenshot:**

![Step 3 - Authentication](screenshots/Step3_Authentication.png)

> **How email counter works:** Each run reads `test_data/email_counter.txt`, uses the current number as suffix, then increments it for the next run. This ensures unique emails across all test runs.

---

### Step 4 — OTP Verification ⚠️ Manual Step

**File:** `pages/otp_page.py`
**URL:** `https://bridge-uat.nios.ac.in/registration/otp`

**What the script does:**
1. Detects navigation to `/otp` URL
2. Pauses and displays:
   ```
   ==================================================
   ATTENTION: OTP SENT. Please enter it MANUALLY in the browser.
   The script will wait up to 300 seconds for you to complete this.
   ==================================================
   ```
3. Waits up to **300 seconds** for the URL to advance to `/personal`
4. Once OTP is confirmed, automation resumes automatically

**Action Required from Tester:**
- Check the registered email (`subh7409+N@gmail.com`) or mobile (`6268326377`) for OTP
- Enter OTP in the browser
- Click Submit/Verify

> **⏱️ Timeout:** Script waits 5 minutes (300 seconds). If OTP is not entered in time, the test fails.

---

### Step 5 — Personal Information

**File:** `pages/personal_information_page.py`
**URL:** `https://bridge-uat.nios.ac.in/registration/personal`

**What the script does:**
1. Waits for URL to contain `personal`
2. Sets **Social Category:** `General`
3. Sets **Medium of Study:** `Hindi`
4. Clicks Continue

**Screenshot:**

![Step 5 - Personal Information](screenshots/Step5_Personal_Information.png)

---

### Step 6 — Address Details

**File:** `pages/address_details_page.py`
**URL:** `https://bridge-uat.nios.ac.in/registration/address`

**What the script does:**
1. Fills **Address Line 1:** `101 dd nagar`
2. Fills **Street/Locality:** `netaji subhash place`
3. Selects **State:** `DELHI`
4. Selects **District:** `CENTRAL`
5. Enters **Pincode:** `110034`
6. Clicks Continue

**Screenshot:**

![Step 6 - Address Details](screenshots/Step6_Address_Details.png)

---

### Step 7 — Subject Details

**File:** `pages/subject_details_page.py`
**URL:** `https://bridge-uat.nios.ac.in/registration/subject`

**What the script does:**
1. Waits for URL to contain `subject`
2. Calls `select_any_medium_for_enabled_subjects()` — dynamically selects the first available medium for each enabled subject dropdown
3. Clicks Continue

**Screenshot:**

![Step 7 - Subject Details](screenshots/Step7_Subject_Details.png)

> **Dynamic Subject Logic:** The script scans all subject dropdowns and selects any available medium option, adapting to whatever subjects are enabled for the given school.

---

### Step 8 — Document Upload

**File:** `pages/documents_page.py`
**URL:** `https://bridge-uat.nios.ac.in/registration/document`

**What the script does:**
1. Uses `DataUtils.ensure_dummy_files()` to auto-create dummy files if missing:
   - `test_data/dummy.jpg` (50KB random binary — acts as photo)
   - `test_data/dummy.pdf` (minimal valid PDF structure)
2. Calls `docs_page.upload_all_documents(photo_path, doc_path)` to upload to all file inputs
3. Calls `docs_page.toggle_checkboxes()` to check all consent checkboxes
4. Clicks **Save & Continue**

**Screenshot:**

![Step 8 - Documents](screenshots/Step8_Documents.png)

> **Dummy File Strategy:** Files are created programmatically — no real scanned documents needed. The system accepts them in UAT.

---

### Step 9 — Review Page

**File:** `pages/payment_flow_page.py`
**URL:** `https://bridge-uat.nios.ac.in/registration/review` or `/payment`

**What the script does:**
1. Waits for URL to contain `review` or `payment`
2. Checks all **confirmation/declaration checkboxes**
3. Selects **SabPaisa** payment gateway
4. Clicks **Pay Now**

**Screenshot:**

![Step 9 - Review Page](screenshots/Step9_Review_Page.png)

---

### Step 10 — Payment (SabPaisa Gateway)

**File:** `pages/payment_flow_page.py`

**What the script does:**
1. Enters the **SabPaisa** payment gateway
2. Executes `process_standard_payment()` which attempts (in order):
   - **Cash / Challan** — preferred mode; downloads challan PDF
   - **Cards** — fallback using test card `4000020000000000`
3. Handles new windows/tabs opened by the gateway
4. Waits for payment success confirmation

**Payment Config:**

| Setting | Value |
|---|---|
| Gateway | SabPaisa |
| Primary Mode | Cash (Challan) |
| Fallback Mode | Cards |
| Test Card | 4000020000000000 |
| Expiry | 12/30 |
| CVV | 234 |

**Screenshot:**

![Step 10 - Payment Success](screenshots/Step10_Payment_Success.png)

---

## 7. E-Services Flow

### Overview

The E-Services test is run via:

```bash
pytest tests/test/eservices/test_functional_eservices_workflow.py -v -s
```

The script:
1. **Logs in** to the portal (requires manual CAPTCHA entry)
2. Navigates to **E-Services → Apply**
3. Dynamically discovers all available services
4. Iterates through each service one by one

### Login Flow

**File:** `pages/home_page.py`, `pages/login_page.py`

1. Opens `https://bridge-uat.nios.ac.in/`
2. Hovers over **Login Corner** menu
3. Clicks **Teacher Login**
4. On login page — enters email and password
5. **⚠️ Pauses for human to solve CAPTCHA** (waits up to 120 seconds)
6. Upon successful login, navigates to E-Services list

> **Credentials (from config.ini):**
> - Email: `subh7409@gmail.com`
> - Password: `Password@1`

### Services Iterated (Discovered Dynamically)

The framework discovers services dynamically via `eservices_page.get_all_services_details()`. Known services include:

| # | Service Name | Automation Status |
|---|---|---|
| 1 | Change Correspondence Address | ✅ Automated |
| 2 | Change Appointment Date | ✅ Automated |
| 3 | Change Name | ⏸ Wait for manual fill |
| 4 | Change Date of Birth | ⏭ Skipped (system issue) |
| 5 | Change Disability Category | ⏭ Skipped (loading issue) |
| 6 | Change Mobile Number | ⏸ Wait for manual OTP |
| 7 | Change Email ID | ⏸ Wait for manual OTP |
| 8 | Change Medium | ⏸ Wait for manual fill |
| 9 | Cancel Registration | ⏸ Wait for manual fill |
| 10 | Change School | ⏸ Wait for manual fill |
| 11 | Re-admission | ⏸ Wait for manual fill |
| 12 | Change Subjects | ⏸ Wait for manual fill |
| 13 | Print Form | ⏸ Wait for manual action |
| 14 | Payment History | ⏸ Wait for manual review |

### Service Processing Logic

```
For each service:
  1. Click service link (scroll into view, hover, click)
  2. If OTP required → Print prompt, wait up to 300s for human to enter
  3. If form page detected (no OTP):
     a. If "Appointment Date" → automate_appointment_date()
     b. If "Correspondence Address" → automate_address_change()
     c. Else → Capture DOM to html file, pause, wait for human to fill & submit
  4. Recover → Navigate back to E-Services list
  5. Pause 3 seconds before next service
```

### Appointment Date Service — Automated Fields

| Field | Value |
|---|---|
| New Date of Appointment | 10-08-2023 |
| Supporting Document | `test_data/official_certificate.pdf` |

### Correspondence Address Service — Automated Fields

| Field | Value |
|---|---|
| Address Line 1 | House 123 |
| Address Line 2 | Test Street |
| State | Delhi (value: 9107) |
| District | value: 910720 |
| Pincode | 110001 |

---

## 8. Running the Tests

### 8.1 Run Full Registration

```bash
pytest tests/test/registration/test_registration.py -v -s
```

> `-s` is **required** — it allows `print()` and `input()` prompts to appear in the console (needed for OTP instructions).

### 8.2 Run All E-Services

```bash
pytest tests/test/eservices/test_functional_eservices_workflow.py -v -s
```

### 8.3 Run Negative Tests

```bash
pytest tests/test/registration/test_registration_negative.py -v -s
pytest tests/test/registration/test_registration_advanced_negative.py -v -s
pytest tests/test/eservices/test_eservices_negative.py -v -s
```

### 8.4 Run All Tests (with HTML Report)

```bash
pytest tests/ -v -s --html=reports/report.html --self-contained-html
```

### 8.5 Run with Specific Markers

```bash
# Run only smoke tests (if marked)
pytest tests/ -v -s -m smoke

# Run and stop on first failure
pytest tests/ -v -s -x
```

### 8.6 Expected Console Output

During a successful registration run, you'll see:

```
============= test session starts ==============
tests/test/registration/test_registration.py::Test_001_Registration::test_registration

**** Starting Restored Test_001_Registration ****
Step 1: Basic Details
Waiting for registration form to be ready...
Registration form is ready.
Set DOB to '15-08-1990' using JavaScript
Selected gender: Male
Verify UDISE clicked
Clicked Continue button

Step 2: Eligibility
Step 3: Authentication
Using Email: subh7409+5@gmail.com and Mobile: 6268326377

==================================================
ATTENTION: OTP SENT. Please enter it MANUALLY in the browser.
The script will wait up to 300 seconds for you to complete this.
==================================================

Step 5: Personal Information
...
**** Registration and Payment Flow Completed Successfully ****
```

---

## 9. Test Data Management

### 9.1 Email Counter

Each test run generates a **unique email** for registration:

- Counter is stored in `test_data/email_counter.txt`
- Format: `subh7409+{counter}@gmail.com`
- Counter auto-increments after each use

```bash
# Check current counter value
type test_data\email_counter.txt

# Reset counter manually (if needed)
echo 1 > test_data\email_counter.txt
```

### 9.2 Dummy Files

Automatically created on first run:

| File | Description |
|---|---|
| `test_data/dummy.jpg` | 50KB random binary (accepted as photo upload) |
| `test_data/dummy.pdf` | Minimal valid PDF structure + random bytes |
| `test_data/official_certificate.pdf` | Certificate for Appointment Date service |

### 9.3 Test Data for Known Forms

| Parameter | Value | Used in |
|---|---|---|
| Name | Faker-generated | Registration Step 1 |
| DOB | 15-08-1990 | Registration Step 1 |
| Mobile | 6268326377 | Registration Step 3 |
| UDISE Code | 10101000101 | Registration Step 1 |
| Address | 101 dd nagar | Registration Step 6 |
| State | DELHI | Registration Step 6 |
| District | CENTRAL | Registration Step 6 |
| Pincode | 110034 | Registration Step 6 |

---

## 10. Page Object Reference

### BasePage (`pages/base_page.py`)

Core helper methods available to ALL page objects:

| Method | Description |
|---|---|
| `do_click(by_locator)` | Waits for element visibility then clicks |
| `do_send_keys(by_locator, text)` | Clears field and sends keys; JS fallback |
| `get_element_text(by_locator)` | Returns element's text content |
| `is_visible(by_locator)` | Returns bool — element visible or not |
| `mouse_hover(by_locator)` | ActionChains hover |
| `select_chosen_option(locator, text)` | Handles Chosen.js dropdowns (2-strategy: UI click + JS fallback) |
| `enter_text_typewriter(element, text)` | Human-like character-by-character typing |
| `get_element(by_locator)` | Returns WebElement (presence-based) |
| `wait_for_invisibility(by_locator)` | Blocks until element disappears |

### Key Timeout Settings

| Timeout | Default | Purpose |
|---|---|---|
| `TIMEOUT` | 10s | All explicit waits in BasePage |
| `otp_wait` | 120s (config) | Login CAPTCHA wait |
| OTP registration wait | 300s | Registration OTP human entry |
| Gateway wait | 2s | Post-gateway stabilization |

---

## 11. Utilities Reference

### ReadConfig (`utilities/read_properties.py`)

Reads from `config/config.ini`:

```python
ReadConfig.getApplicationURL()    # base_url
ReadConfig.getLoginEmail()        # login > email
ReadConfig.getLoginPassword()     # login > password
ReadConfig.getPaymentConfig()     # payment section dict
ReadConfig.getTimeouts()          # timeouts section dict
ReadConfig.getPaths()             # paths section dict
ReadConfig.getExplicitWait()      # explicit_wait value
```

### DataUtils (`utilities/data_utils.py`)

```python
DataUtils.generate_email_incremental()  # subh7409+N@gmail.com
DataUtils.get_fixed_mobile()            # 6268326377
DataUtils.ensure_dummy_files()          # returns (jpg_path, pdf_path)
DataUtils.get_random_name()             # Faker-generated name
DataUtils.get_random_dob()              # 15-08-1990
```

### LogGen (`utilities/custom_logger.py`)

```python
logger = LogGen.loggen()
logger.info("Step started")
logger.warning("Non-critical issue")
logger.error("Critical failure")
```

Logs are written to files in the `logs/` directory.

---

## 12. Troubleshooting Guide

### ❌ Browser doesn't open
**Cause:** ChromeDriver not on PATH or version mismatch
```bash
# Check versions match
chromedriver --version
chrome --version
```
**Fix:** Download matching ChromeDriver from https://chromedriver.chromium.org/

---

### ❌ Test fails at "Waiting for registration form"
**Cause:** Page load too slow, network issues, or URL changed
**Fix:**
- Increase `implicit_wait` and `explicit_wait` in `config.ini`
- Verify URL is accessible: `https://bridge-uat.nios.ac.in/registration/basic-details`

---

### ❌ OTP step times out (StaleElement / TimeoutException)
**Cause:** OTP not entered within 300 seconds, or page navigated away
**Fix:**
- Enter OTP quickly after test prints the prompt
- Ensure the correct OTP source (email vs mobile) is checked

---

### ❌ Gender dropdown not selecting
**Cause:** Chosen.js dropdown interaction failure
**Fix:** The `RegistrationPage.set_gender()` uses two strategies. If both fail:
- Check the Chosen container ID: `basicdetailform_gender_chosen`
- Verify the option text matches exactly: `Male`, `Female`, `Transgender`

---

### ❌ Payment gateway: "No suitable payment option found"
**Cause:** Gateway UI changed or Cash/Challan tab not visible
**Fix:**
- Check `payment > mode` in `config.ini`
- The payment method tries Cash first, then Cards
- Verify gateway URL is accessible: SabPaisa UAT sandbox

---

### ❌ E-Services: "Login failed"
**Cause:** CAPTCHA not solved in time (120s window)
**Fix:**
- Solve CAPTCHA immediately when browser opens login page
- If auto-solving is needed, consider integrating a CAPTCHA resolver service

---

### ❌ File upload fails
**Cause:** Dummy file doesn't exist or path is incorrect
**Fix:**
```bash
# Check if dummy files exist
dir test_data\
# If missing, delete email_counter.txt and re-run (files are auto-created)
```

---

### ❌ "stale element reference" exceptions
**Cause:** Page reloaded between locating and interacting with element
**Fix:** The `BasePage.do_click()` re-fetches elements using `WebDriverWait`. If persistent, add a short `time.sleep(1)` before the failing action.

---

## 13. Test Results & Reports

### Log Files (`logs/`)

All test runs produce detailed logs:
```
2026-02-26 10:15:22 - INFO - **** Starting Restored Test_001_Registration ****
2026-02-26 10:15:22 - INFO - Step 1: Basic Details
2026-02-26 10:15:25 - INFO - Set DOB to '15-08-1990' using JavaScript
2026-02-26 10:15:25 - INFO - Selected gender: Male
...
```

### Screenshots (`screenshots/`)

| File | Description |
|---|---|
| `Step1_Basic_Details.png` | Registration form filled |
| `Step2_Eligibility.png` | Eligibility page |
| `Step3_Authentication.png` | Email & mobile entry |
| `Step5_Personal_Information.png` | Category & medium |
| `Step6_Address_Details.png` | Address form |
| `Step7_Subject_Details.png` | Subject selection |
| `Step8_Documents.png` | Document upload |
| `Step9_Review_Page.png` | Review & declaration |
| `Step10_Payment_Success.png` | Payment confirmation |

### HTML Report

Generated when running with `--html` flag:
```bash
pytest tests/ -v -s --html=reports/report.html --self-contained-html
open reports/report.html
```

### Pytest Log Files (`pytest log/`)

Previous run logs are preserved in `pytest log/` directory for audit trail.

---

## Appendix A — Registration Flow Diagram

```
[START]
   │
   ▼
[Step 1] Basic Details ──────────────────────► Fill: Name, DOB, Gender, UDISE
   │                                           Click: Verify UDISE → Continue
   ▼
[Step 2] Eligibility ───────────────────────► Fill: Date of Appointment → Continue
   │                                           (may be auto-skipped)
   ▼
[Step 3] Authentication ────────────────────► Fill: Email (incremental), Mobile
   │                                           Click: Submit → OTP sent
   ▼
[Step 4] OTP ⚠️ MANUAL ─────────────────────► Human enters OTP in browser
   │                                           Script waits up to 300s
   ▼
[Step 5] Personal Information ──────────────► Select: Social Category, Medium
   │                                           Click: Continue
   ▼
[Step 6] Address Details ───────────────────► Fill: Address, State, District, PIN
   │                                           Click: Continue
   ▼
[Step 7] Subject Details ───────────────────► Dynamic: Select medium for each subject
   │                                           Click: Continue
   ▼
[Step 8] Document Upload ───────────────────► Upload: dummy.jpg + dummy.pdf
   │                                           Toggle: checkboxes → Save & Continue
   ▼
[Step 9] Review Page ───────────────────────► Check: declarations
   │                                           Select: SabPaisa gateway
   │                                           Click: Pay Now
   ▼
[Step 10] Payment ──────────────────────────► Try: Cash/Challan → Else: Cards
   │                                           Handle: new gateway window
   ▼
[SUCCESS] Registration Complete ✅
```

---

## Appendix B — E-Services Flow Diagram

```
[START]
   │
   ▼
[Homepage] bridge-uat.nios.ac.in
   │
   ▼
[Login Corner → Teacher Login] ⚠️ MANUAL CAPTCHA (120s)
   │
   ▼
[Dashboard → E-Services → Apply]
   │
   ▼
[Discover all services dynamically]
   │
   ├──► For each service:
   │         │
   │         ├─ [OTP required?] → Print prompt → Wait for human (300s)
   │         │
   │         ├─ [Known service: Appointment Date] → automate_appointment_date()
   │         │
   │         ├─ [Known service: Correspondence Address] → automate_address_change()
   │         │
   │         ├─ [Unknown service] → Capture DOM → Pause → Wait for human fill
   │         │
   │         └─ [Skip: DOB / Disability Category]
   │
   └──► Recovery: Return to E-Services list after each service
   │
   ▼
[All services processed]
   │
   ▼
[Log: SUCCESS or list FAILURES]
```

---

*Document generated: February 2026*
*Framework maintained by: Subhrajit*
*Testing Environment: NIOS Bridge UAT — https://bridge-uat.nios.ac.in*
