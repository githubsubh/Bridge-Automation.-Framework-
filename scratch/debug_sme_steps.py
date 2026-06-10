import os
import sys
import time
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pages.admin_login_page import AdminLoginPage
from pages.sme_registration_page import SMERegistrationPage
from utilities.data_utils import DataUtils
from utilities.valid_aadhaar_list import VALID_AADHAAR_NUMBERS

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver

def main():
    driver = create_driver()
    try:
        print("Navigating to Admin Portal...")
        driver.get("https://bridge-uat-admin.nios.ac.in")
        
        login_page = AdminLoginPage(driver)
        # Login with manual captcha (timeout of 120 seconds)
        success = login_page.login_with_manual_captcha("superadmin", "Admin@2025", timeout=120)
        if not success:
            print("Admin login failed or timed out.")
            return

        print("Logged in successfully. Navigating to SME registration page...")
        reg_page = SMERegistrationPage(driver)
        reg_page.navigate_to_sme_registration()

        # Step 1: Basic Information
        print("Filling Step 1: Basic Details...")
        email = DataUtils.generate_email_incremental()
        mobile = f"98{random.randint(10000000, 99999999)}"
        name = "SME Expert"
        dob = "01011985"
        random_aadhaar = random.choice(VALID_AADHAAR_NUMBERS)
        school_text = "deen"
        study_centre_text = "09150101103"
        district = "AGRA"

        reg_page.fill_basic_info(
            name=name,
            designation="Senior Expert",
            dob=dob,
            gender="Male",
            aadhaar=random_aadhaar,
            school_name=school_text,
            experience="10"
        )
        reg_page.click_next()
        time.sleep(2)

        # Step 2: User Credentials
        print("Filling Step 2: User Credentials...")
        # Custom logic for study centre to prevent dropdown failure:
        # Instead of select_by_visible_text which requires exact match, let's try selecting by value or partial text
        reg_page.fill_user_credentials(
            first_name="SME",
            last_name="Expert",
            email=email,
            mobile=mobile,
            level="School",
            role="Subject Experts",
            username=f"sme_{int(time.time())}",
            password="Password@12",
            district=district,
            study_centre=None # We will select study centre manually/custom here
        )

        # Custom select study centre
        try:
            print("Selecting Study Centre using custom logic...")
            sc_locator = reg_page.get_dropdown_by_label("Study Centres")
            sc_element = driver.find_element(*sc_locator)
            if sc_element.tag_name.lower() == 'select':
                from selenium.webdriver.support.ui import Select
                select = Select(sc_element)
                # Try finding option by value containing study_centre_text, or text containing it
                selected = False
                for option in select.options:
                    val = option.get_attribute('value')
                    txt = option.text
                    if study_centre_text in val or study_centre_text in txt:
                        select.select_by_value(val)
                        print(f"Successfully selected Study Centre: {txt}")
                        selected = True
                        break
                if not selected:
                    # Select first option if match not found
                    if len(select.options) > 1:
                        select.select_by_index(1)
                        print(f"Selected first available Study Centre: {select.options[1].text}")
        except Exception as e:
            print(f"Failed custom Study Centre selection: {e}")

        reg_page.click_next()
        time.sleep(2)

        # Step 3: Address Details
        print("Filling Step 3: Address Details...")
        reg_page.fill_address_details(
            house="123 Automation St",
            street="Test Locality",
            state="MADHYA PRADESH",
            district="GWALIOR",
            pincode="474020",
            same_as_permanent=True
        )
        reg_page.click_next()
        time.sleep(3)

        # Now we capture DOM and Screenshot for steps 4 to 8
        os.makedirs("DOM", exist_ok=True)
        os.makedirs("screenshots", exist_ok=True)

        for step in range(4, 9):
            print(f"\n--- REACHED STEP {step} ---")
            screenshot_path = f"screenshots/sme_step_{step}.png"
            dom_path = f"DOM/sme_step_{step}.html"
            
            driver.save_screenshot(screenshot_path)
            with open(dom_path, "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print(f"Saved screenshot to: {screenshot_path}")
            print(f"Saved DOM to: {dom_path}")
            
            # Pause and ask for user to press enter in console, or check fields
            # We will wait up to 30 seconds for the page/DOM to settle, then proceed or wait for keyboard input
            input(f"Inspect step {step} in browser if you want. Press Enter here in console to try filling step {step} and click Next...")
            
            if step == 4:
                print("Trying to fill step 4...")
                reg_page.fill_qualification(
                    qualification="M.Sc. Mathematics",
                    board="Test University",
                    passing_year="2010",
                    percentage="85"
                )
            elif step == 5:
                print("Trying to fill step 5...")
                reg_page.fill_employment_details(
                    office_name="Test School",
                    designation="Teacher",
                    start_date="01-01-2015"
                )
            elif step == 6:
                print("Trying to fill step 6...")
                reg_page.fill_subject_details(subject="Mathematics")
            elif step == 7:
                print("Trying to fill step 7...")
                jpg_path, pdf_path = DataUtils.ensure_dummy_files()
                reg_page.upload_documents(photo_path=jpg_path, signature_path=jpg_path)
            
            reg_page.click_next()
            time.sleep(3)

        print("\nReached Step 8 (Review & Submit). Capturing review page...")
        driver.save_screenshot("screenshots/sme_step_8_review.png")
        with open("DOM/sme_step_8_review.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Review page details saved.")
        
        input("Press Enter to click submit and finish registration...")
        reg_page.click_submit()
        time.sleep(5)
        
        success = reg_page.is_registration_successful()
        print(f"Registration success status: {success}")
        driver.save_screenshot("screenshots/sme_final_result.png")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("screenshots/sme_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
