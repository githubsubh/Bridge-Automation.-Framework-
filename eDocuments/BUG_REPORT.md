# Bug Report: E-Services - Change Date of Birth (DOB) Loading Issue

## Bug Description
The "Change Date of Birth" (DOB) e-service fails to load the form data consistently. When navigating to the service or after OTP verification, the page often results in a loading error or the form fields remain blank/unpopulated, blocking further automation or manual processing.

## Steps to Reproduce
1. Login to the Bridge portal.
2. Navigate to "E-Services" -> "Apply".
3. Click on the "Change Date of Birth" service.
4. Complete OTP verification.
5. Observed: The form page does not load correctly or shows a loading error.

## Impact
- **Automation Impact**: Script fails to find form elements for DOM analysis and automation.
- **User Impact**: Teachers cannot update their Date of Birth through the e-service due to technical instability.


---

# Bug Report: E-Services - Change Disability Category OTP Submission Issue

## Bug Description
The "Change Disability Category" e-service throws a system error during OTP submission. After entering a valid OTP and clicking verify, a red error toast appears stating "An error occurred. Please try again.", preventing the user from reaching the form page.

## Steps to Reproduce
1. Login to the Bridge portal.
2. Navigate to "E-Services" -> "Apply".
3. Click on the "Change Disability Category" service.
4. Enter OTP and click Verify.
5. Observed: Red Toast Error: **"An error occurred. Please try again."**

## Impact
- **Automation Impact**: Script is blocked at the OTP verification stage.
- **User Impact**: Teachers cannot update their disability category.

## Workaround Implemented (Automation)
- None (System-level failure). The script skips this service if it fails to progress.
