# Registration – Test Cases

> **How to use:**
> - Change `Status` to `Skipped` for test cases you want to drop.
> - Change `Status` to `Automated` once the pytest script is written and fill in Script Location.
> - `Priority` → `High` = must automate | `Medium` = nice to have | `Low` = skip for now

---

## Legend

| Status Value | Meaning |
|---|---|
| `To Automate` | Approved for automation, script not written yet |
| `In Progress` | Script being written |
| `Automated` | Script written and passing |
| `Skipped` | Decided NOT to automate (reason in Notes) |

---

## Test Cases

| TC ID | Feature | Test Scenario | Preconditions | Test Steps | Expected Result | Test Type | Priority | Status | Script Location | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| TC_REG_001 | Eligibility Text | Verify eligibility instruction text | On Registration page | Review eligibility instruction text | Text is grammatically correct and approved wording displayed | UI | Medium | Skipped | | UI text validation – manual review preferred |
| TC_REG_002 | UDISE Verification | Verify valid UDISE verification | On Basic Details page | Enter valid UDISE → Click Verify | Verification successful and Continue enabled | Functional | High | To Automate | | |
| TC_REG_003 | UDISE Verification | Verify invalid UDISE shows error | On Basic Details page | Enter invalid UDISE → Click Verify | Error shown and Continue remains disabled | Functional | High | To Automate | | |
| TC_REG_004 | UDISE Security | Force-enable Continue without verification | Using browser DevTools | Force enable Continue without verification → Submit | Server rejects submission | Security | High | To Automate | | |
| TC_REG_005 | Clear Button | Verify Clear button resets only Basic Details | Basic Details filled | Click Clear button | Only Basic Details fields reset | Functional | Medium | To Automate | | |
| TC_REG_006 | Dropdowns | Gender placeholder not selectable | On Basic Details | Open Gender dropdown | Placeholder not selectable | UI | Medium | To Automate | | |
| TC_REG_007 | Dropdowns | Social Category placeholder not selectable | On Personal Info | Open Social Category dropdown | Placeholder not selectable | UI | Medium | To Automate | | |
| TC_REG_008 | Dropdowns | Study Medium placeholder not selectable | On Personal Info | Open Study Medium dropdown | Placeholder not selectable | UI | Medium | To Automate | | |
| TC_REG_009 | Dropdowns | Disability placeholder not selectable | On Personal Info | Open Disability dropdown | Placeholder not selectable | UI | Medium | To Automate | | |
| TC_REG_010 | Dropdowns | District placeholder not selectable | On Address page | Open District dropdown | Placeholder not selectable | UI | Medium | To Automate | | |
| TC_REG_011 | Dropdowns | State placeholder not selectable | On Address page | Open State dropdown | Placeholder not selectable | UI | Medium | To Automate | | |
| TC_REG_012 | Dropdowns | Subject 3 medium placeholder not selectable | On Subject page | Open Subject 3 medium dropdown | Placeholder not selectable | UI | Medium | To Automate | | |
| TC_REG_013 | Dropdowns | Subject 4 medium placeholder not selectable | On Subject page | Open Subject 4 medium dropdown | Placeholder not selectable | UI | Medium | To Automate | | |
| TC_REG_014 | Address | State-Pincode combination validation | On Address page | Select state → Enter invalid pincode → Submit | Validation error displayed | Functional | High | To Automate | | |
| TC_REG_015 | Document Upload | Upload file exceeding 2MB limit | On My Documents | Upload file > 2MB | Upload blocked with size message | Functional | High | To Automate | | |
| TC_REG_016 | Document Upload | Upload invalid file type (MP4) | On My Documents | Upload MP4/video file | Upload rejected | Functional | High | To Automate | | |
| TC_REG_017 | Document Upload | PDF preview after upload | On My Documents | Upload valid PDF → Click View | PDF preview opens | Functional | Medium | To Automate | | |
| TC_REG_018 | Document Upload | Rejected document re-upload flow | Document rejected by admin | Open document section | Rejection reason shown with re-upload option | Functional | High | To Automate | | |
| TC_REG_019 | Document Upload | Upload button disabled without file selection | On My Documents | Do not select file → Click Upload | Upload button disabled | Functional | Medium | To Automate | | |
| TC_REG_020 | Review Screen | All fields shown as read-only | On Review page | Check all displayed fields | Fields shown as read-only text consistently | UI | Medium | To Automate | | |
| TC_REG_021 | Payment | Only approved gateways visible | On Payment page | Check available gateways | Only approved gateways visible | Functional | High | To Automate | | |
| TC_REG_022 | Payment | Declaration checkbox mandatory | On Payment page | Attempt payment without checkbox | Payment blocked | Functional | High | To Automate | | |
| TC_REG_023 | Navigation | Left nav editable on Review page | On Review page | Click previous section in side menu | User navigates successfully | Functional | Medium | To Automate | | |
| TC_REG_024 | Review Screen | Regional centre data populated | On Review page | Verify regional centre details | All required fields populated | UI | Medium | To Automate | | |
| TC_REG_025 | Login | Login loader displays | On Login page | Click Login | Loader displayed until response | UI | Medium | Skipped | | Timing-sensitive UI check – low value |
| TC_REG_026 | Login | Password visibility toggle (Login) | On Login page | Click eye icon | Password visibility toggles correctly | UI | Medium | To Automate | | |
| TC_REG_027 | Password | Change password same as current blocked | On Change Password page | Enter same current & new password | Validation error displayed | Functional | High | To Automate | | |
| TC_REG_028 | Password | Password toggle on Change Password page | On Change Password page | Toggle eye icon | Correct masking/unmasking | UI | Medium | To Automate | | |
| TC_REG_029 | Email | NIOS logo in confirmation email | After registration | Check confirmation email | NIOS logo displayed | UI | Medium | Skipped | | External email validation – not suited for automation |
| TC_REG_030 | Mobile UI | Back & Continue button size on mobile | On Mobile view | Check Back & Continue buttons | Buttons proportionate | UI/Mobile | Medium | To Automate | | Chrome mobile emulation |
| TC_REG_031 | Mobile UI | Clear button label on mobile | On Mobile view | Check clear button text | Displays 'Clear Details' | UI/Mobile | Medium | To Automate | | Chrome mobile emulation |
| TC_REG_032 | Auth | No unexpected auth error during registration | During registration | Complete registration process | No unexpected authentication error | Functional | High | To Automate | | |
| TC_REG_033 | Mobile UI | Upload label consistency on mobile | On Mobile view | Upload document | Label remains consistent | UI/Mobile | Medium | To Automate | | Chrome mobile emulation |
| TC_REG_034 | Mobile UI | Fee table alignment on mobile Review | On Mobile Review | Check fee table alignment | Fee type and amount aligned properly | UI/Mobile | Medium | To Automate | | Chrome mobile emulation |
| TC_REG_035 | Validation | Mandatory field validation on Basic Details | On Basic Details | Leave mandatory fields blank → Click Continue | Validation messages displayed | Functional | High | To Automate | | |
| TC_REG_036 | Validation | Name field rejects numeric/special chars | On Basic Details | Enter numeric/special characters in Name | Invalid characters rejected | Functional | Medium | To Automate | | |
| TC_REG_037 | Validation | Mobile number format validation | On Basic Details | Enter invalid mobile numbers | Only valid 10-digit number accepted | Functional | High | To Automate | | |
| TC_REG_038 | Validation | Email format validation | On Basic Details | Enter invalid email format | Validation error displayed | Functional | High | To Automate | | |
| TC_REG_039 | Validation | Duplicate email blocked | Existing user email | Attempt new registration | Duplicate registration blocked | Functional | High | To Automate | | |
| TC_REG_040 | Validation | Future DOB rejected | On Basic Details | Enter future date | Future date rejected | Functional | Medium | To Automate | | |
| TC_REG_041 | Security | SQL injection prevention | On any text field | Enter SQL payload | Input sanitized | Security | High | To Automate | | |
| TC_REG_042 | Security | XSS prevention | On any text field | Enter script tag | Script not executed | Security | High | To Automate | | |
| TC_REG_043 | UDISE | Timeout handling during UDISE verification | Slow network | Click Verify during interruption | Graceful error message shown | Functional | Medium | To Automate | | |
| TC_REG_044 | UDISE | Multiple UDISE verifications create no duplicate | On Basic Details | Verify same code multiple times | No duplicate record created | Functional | Medium | To Automate | | |
| TC_REG_045 | Eligibility | B.Ed No flow blocks registration | On Eligibility page | Select No → Continue | Blocked with message | Functional | High | To Automate | | |
| TC_REG_046 | Eligibility | B.Ed Yes flow allows registration | On Eligibility page | Select Yes → Continue | Allowed to proceed | Functional | High | To Automate | | |
| TC_REG_047 | Address | Pincode rejects alphabets | On Address page | Enter alphabets in pincode | Validation error shown | Functional | Medium | To Automate | | |
| TC_REG_048 | Address | Pincode length validation | On Address page | Enter less/more than 6 digits | Validation error shown | Functional | Medium | To Automate | | |
| TC_REG_049 | Security | Address special character sanitization | On Address page | Enter restricted special characters | Input rejected or sanitized | Security | Medium | To Automate | | |
| TC_REG_050 | Document Upload | Corrupted file upload rejected | On My Documents | Upload damaged PDF | Upload rejected gracefully | Functional | Medium | To Automate | | |
| TC_REG_051 | Document Upload | Replace uploaded file before submit | On My Documents | Upload file → Replace before submit | Latest file saved | Functional | Medium | To Automate | | |
| TC_REG_052 | Document Upload | Upload progress indicator | On My Documents | Upload valid file | Progress indicator visible | UI | Low | Skipped | | Timing-sensitive UI – low value |
| TC_REG_053 | OTP | Invalid OTP rejected | On OTP screen | Enter incorrect OTP | Error message shown | Functional | High | To Automate | | |
| TC_REG_054 | OTP | Expired OTP shows expiry message | On OTP screen | Enter OTP after expiry | Expiry message displayed | Functional | High | To Automate | | |
| TC_REG_055 | OTP | Resend OTP generates new OTP | On OTP screen | Click Resend OTP | New OTP generated | Functional | Medium | To Automate | | |
| TC_REG_056 | OTP | Repeated wrong OTP triggers lock | On OTP screen | Enter wrong OTP repeatedly | Temporary lock applied | Security | High | To Automate | | |
| TC_REG_057 | Payment | Successful payment updates status | On Payment page | Complete successful transaction | Status updated to Paid | Functional | High | To Automate | | |
| TC_REG_058 | Payment | Failed payment keeps status unpaid | On Payment page | Simulate failed transaction | Application remains unpaid | Functional | High | To Automate | | |
| TC_REG_059 | Payment | Double-click Pay Now issues single transaction | On Payment page | Double-click Pay Now | Single transaction processed | Functional | High | To Automate | | |
| TC_REG_060 | Session | Idle timeout during registration | During registration | Remain idle until timeout | User redirected to login | Functional | Medium | To Automate | | |
| TC_REG_061 | Payment | Cancel payment from gateway | On Payment Gateway page | Cancel transaction from gateway | User redirected safely and status remains unpaid | Functional | High | To Automate | | |
| TC_REG_062 | Payment | Refresh after payment no duplicate | After successful payment | Refresh browser | No duplicate transaction created | Functional | High | To Automate | | |
| TC_REG_063 | Payment | Back navigation after payment | After payment success | Click browser Back button | User cannot modify paid application | Functional | High | To Automate | | |
| TC_REG_064 | Login | Invalid login credentials | On Login page | Enter wrong username/password | Error message displayed | Functional | High | To Automate | | |
| TC_REG_065 | Login | Multiple failed logins lock account | On Login page | Enter wrong password multiple times | Account temporarily locked after threshold | Security | High | To Automate | | |
| TC_REG_066 | Login | Forgot password reset flow | On Login page | Click Forgot Password → Complete reset process | Password reset email received and reset successful | Functional | Medium | To Automate | | |
| TC_REG_067 | Dashboard | Informative video link navigation | On Dashboard | Click Informative Video link | Relevant page opens successfully | Functional | Medium | To Automate | | |
| TC_REG_068 | Dashboard | E-Services access from dashboard | On Dashboard | Click E-Services option | Proper response as per business configuration | Functional | Medium | To Automate | | |
| TC_REG_069 | Dashboard | Results panel navigation | On Dashboard | Click On Demand Exam / Track Marksheet | Correct redirection or configured behavior | Functional | Medium | To Automate | | |
| TC_REG_070 | Email | Confirmation email content correct | After Registration | Open confirmation email | Correct name, application number and details displayed | UI | Medium | Skipped | | External email validation – not suited for automation |
| TC_REG_071 | Email | Links in confirmation email clickable | In confirmation email | Click links inside email | Links redirect correctly | Functional | Medium | Skipped | | External email validation – not suited for automation |
| TC_REG_072 | Mobile UI | Landscape layout stability | On Mobile Device | Rotate device to landscape mode | Layout remains stable and readable | UI/Mobile | Medium | To Automate | | Chrome mobile emulation |
| TC_REG_073 | Mobile UI | Keyboard does not cover input field | On Mobile Device | Focus input field and open keyboard | Input field remains visible | UI/Mobile | Medium | Skipped | | Requires real device – emulation not reliable |
| TC_REG_074 | Mobile UI | Scroll on long registration form | On Mobile Device | Scroll long registration form | No layout break or overlap | UI/Mobile | Medium | To Automate | | Chrome mobile emulation |
| TC_REG_075 | Mobile UI | Rapid tap on Continue triggers once | On Mobile Device | Tap Continue button rapidly | Single action triggered | Functional | Medium | To Automate | | Chrome mobile emulation |
| TC_REG_076 | Mobile UI | Dropdown rendering on mobile | On Mobile Device | Open dropdown fields | Dropdown renders properly without UI distortion | UI/Mobile | Medium | To Automate | | Chrome mobile emulation |
| TC_REG_077 | Mobile UI | Camera upload on mobile | On Mobile Device | Upload document using camera option | File uploads successfully within allowed size | Functional | Medium | Skipped | | Requires real device camera – not automatable |
| TC_REG_078 | Performance | Slow network handling | Under slow network | Perform registration actions | Loader shown and system handles delay gracefully | Functional | Medium | To Automate | | Use network throttling in Chrome DevTools |
| TC_REG_079 | Compatibility | Browser compatibility (Chrome, Edge, Firefox) | On Chrome, Edge, Firefox | Execute registration workflow | No functional or UI issues observed | Functional | Medium | To Automate | | Run via parametrised browser fixture |
| TC_REG_080 | Session | Session persistence across multi-step form | During multi-step registration | Navigate between sections before payment | Data retained correctly across steps | Functional | High | To Automate | | |

---

## Summary

| Priority | Total | To Automate | Skipped |
|---|---|---|---|
| High | 36 | 36 | 0 |
| Medium | 43 | 35 | 8 |
| Low | 1 | 0 | 1 |
| **Total** | **80** | **71** | **9** |

### Skipped Reasons

| TC ID | Reason |
|---|---|
| TC_REG_001 | UI text validation – manual review preferred |
| TC_REG_025 | Timing-sensitive loader check – low value |
| TC_REG_029 | External email inbox – cannot automate reliably |
| TC_REG_052 | Timing-sensitive upload progress UI |
| TC_REG_070 | External email inbox – cannot automate reliably |
| TC_REG_071 | External email inbox – cannot automate reliably |
| TC_REG_073 | Requires real device (keyboard overlap test) |
| TC_REG_077 | Requires real device camera |

---

*Last Updated: 2026-02-28*
