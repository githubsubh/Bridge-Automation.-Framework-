"""
Centralized CAPTCHA & OTP Manual Intervention Utilities
========================================================
Reusable helper methods that pause automation for manual entry
and resume automatically once the user completes the action.
"""
import time
from utilities.custom_logger import LogGen


class CaptchaUtils:
    logger = LogGen.loggen()

    @staticmethod
    def wait_for_manual_captcha(driver, success_url_fragment, timeout=120, poll_interval=1):
        """Waits for manual CAPTCHA entry and login completion.

        The method pauses execution, prompts the user via console, and polls
        the browser URL until the success fragment appears (indicating login
        success) or the timeout expires.

        Args:
            driver: Selenium WebDriver instance.
            success_url_fragment: URL substring that indicates successful login
                                  (e.g. 'dashboard', 'admin/site').
            timeout: Maximum seconds to wait for manual completion.
            poll_interval: Seconds between each URL check.

        Returns:
            True if login was detected within the timeout, False otherwise.
        """
        CaptchaUtils.logger.info(f"Waiting for manual CAPTCHA (timeout={timeout}s)...")

        print("\n" + "=" * 60)
        print("🔒 CAPTCHA REQUIRED — MANUAL INTERVENTION NEEDED")
        print("-" * 60)
        print("1. Look at the Browser Window.")
        print("2. Enter the CAPTCHA text into the CAPTCHA field.")
        print("3. Click the 'Login' button.")
        print(f"⏱  Waiting up to {timeout} seconds...")
        print("=" * 60 + "\n")

        end_time = time.time() + timeout
        while time.time() < end_time:
            current_url = driver.current_url
            if success_url_fragment.lower() in current_url.lower():
                CaptchaUtils.logger.info(f"Login detected! URL now: {current_url}")
                return True

            # Also check if we moved away from the login page
            if "/auth/login" not in current_url and "/login" not in current_url:
                CaptchaUtils.logger.info(f"Login detected via URL change: {current_url}")
                return True

            time.sleep(poll_interval)

        CaptchaUtils.logger.error("CAPTCHA timeout — user did not complete login in time.")
        return False

    @staticmethod
    def wait_for_manual_otp_completion(driver, otp_field_locator=None, timeout=120, poll_interval=1):
        """Waits for manual OTP entry in the browser.

        If otp_field_locator is provided, polls the field value.
        Otherwise, waits for a URL change or success alert.

        Args:
            driver: Selenium WebDriver instance.
            otp_field_locator: Tuple (By, value) for the OTP input field.
            timeout: Maximum seconds to wait.
            poll_interval: Seconds between checks.

        Returns:
            True if OTP was detected/entered, False on timeout.
        """
        CaptchaUtils.logger.info(f"Waiting for manual OTP entry (timeout={timeout}s)...")

        print("\n" + "=" * 60)
        print("📱 OTP VERIFICATION REQUIRED — MANUAL INTERVENTION NEEDED")
        print("-" * 60)
        print("1. Check your Phone/Email for the OTP.")
        print("2. Enter the OTP in the Browser.")
        print("3. Click the verification/submit button if needed.")
        print(f"⏱  Waiting up to {timeout} seconds...")
        print("=" * 60 + "\n")

        start_url = driver.current_url
        end_time = time.time() + timeout

        while time.time() < end_time:
            # Strategy 1: Check if OTP field is populated
            if otp_field_locator:
                try:
                    otp_val = driver.find_element(*otp_field_locator).get_attribute("value")
                    if otp_val and len(otp_val) >= 4:
                        CaptchaUtils.logger.info(f"OTP detected in field (length={len(otp_val)}).")
                        return True
                except Exception:
                    pass

            # Strategy 2: Check if URL changed (page navigated after OTP success)
            if driver.current_url != start_url:
                CaptchaUtils.logger.info("URL changed — OTP flow may have completed.")
                return True

            # Strategy 3: Check for success alert
            try:
                from selenium.webdriver.common.by import By
                success_alerts = driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class,'alert-success') or contains(text(),'successful')]"
                )
                if success_alerts:
                    CaptchaUtils.logger.info("Success alert detected after OTP.")
                    return True
            except Exception:
                pass

            time.sleep(poll_interval)

        CaptchaUtils.logger.error("OTP timeout — user did not complete OTP in time.")
        return False

    @staticmethod
    def wait_for_page_transition(driver, current_url_fragment, timeout=60, poll_interval=1):
        """Generic wait that blocks until the URL no longer contains the given fragment.

        Useful after any manual interaction where the page should navigate away.

        Args:
            driver: Selenium WebDriver instance.
            current_url_fragment: URL fragment that should disappear.
            timeout: Max seconds to wait.
            poll_interval: Seconds between checks.

        Returns:
            True if the page transitioned, False on timeout.
        """
        CaptchaUtils.logger.info(f"Waiting for page to transition away from '{current_url_fragment}'...")
        end_time = time.time() + timeout
        while time.time() < end_time:
            if current_url_fragment not in driver.current_url:
                CaptchaUtils.logger.info(f"Page transitioned. New URL: {driver.current_url}")
                return True
            time.sleep(poll_interval)

        CaptchaUtils.logger.error(f"Page transition timeout. Still on: {driver.current_url}")
        return False
