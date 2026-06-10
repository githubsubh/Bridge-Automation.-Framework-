import os
import time
from utilities.custom_logger import LogGen

class ScreenshotUtils:
    logger = LogGen.loggen()

    @staticmethod
    def capture_screenshot(driver, name):
        """Captures a screenshot and saves it to the screenshots directory."""
        directory = os.path.join(os.getcwd(), "screenshots")
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_path = os.path.join(directory, f"{name}_{timestamp}.png")
        
        try:
            driver.save_screenshot(file_path)
            ScreenshotUtils.logger.info(f"Screenshot saved to: {file_path}")
            return file_path
        except Exception as e:
            ScreenshotUtils.logger.error(f"Failed to capture screenshot: {e}")
            return None
