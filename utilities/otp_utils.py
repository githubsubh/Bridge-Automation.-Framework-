import time
from utilities.custom_logger import LogGen

class OTPUtils:
    logger = LogGen.loggen()

    @staticmethod
    def wait_for_manual_otp(driver, otp_field_locator, timeout=60):
        """
        Pauses execution and waits for the OTP field to be populated manually.
        """
        OTPUtils.logger.info(f"Waiting for manual OTP entry in {otp_field_locator} (Timeout: {timeout}s)...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            otp_val = driver.find_element(*otp_field_locator).get_attribute("value")
            if otp_val and len(otp_val) >= 4: # Assuming OTP is at least 4 digits
                OTPUtils.logger.info(f"OTP detected: {otp_val}")
                return True
            time.sleep(1)
        
        OTPUtils.logger.warning("Timed out waiting for manual OTP entry.")
        return False

    @staticmethod
    def get_otp_via_api(api_endpoint, params):
        """Placeholder for future API-based OTP retrieval."""
        pass

    @staticmethod
    def get_otp_via_email(email_service_config):
        """Placeholder for future Email-based OTP retrieval."""
        pass

    @staticmethod
    def get_otp_via_sms(sms_gateway_config):
        """Placeholder for future SMS-based OTP retrieval."""
        pass
