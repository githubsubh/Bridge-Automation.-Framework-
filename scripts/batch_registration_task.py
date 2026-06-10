import time
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.registration_page import RegistrationPage
from pages.eligibility_page import EligibilityPage
from pages.authentication_page import AuthenticationPage
from pages.personal_information_page import PersonalInformationPage
from pages.address_details_page import AddressDetailsPage
from pages.subject_details_page import SubjectDetailsPage
from pages.documents_page import DocumentsPage
from pages.payment_flow_page import PaymentFlowPage
from utilities.data_utils import DataUtils
from utilities.read_properties import ReadConfig

def run_batch_registration():
    # Registration Constants
    UDISE_CODE = "09150101103"
    MEDIUM = "Hindi"
    ADDRESS = "b gwalior madhyapradesh"
    PINCODE = "474020"
    TOTAL_REGISTRATIONS = 3
    
    # Payment Constants
    PAYMENT_DATA = {
        'card_number': "4029484589897107",
        'card_expiry': "12/30",
        'card_cvv': "234",
        'card_holder': "Test Automation User",
        'gateway_name': "SabPaisa",
        'mode': "Cards"
    }

    # Number mapping for names
    num_map = {3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 
               8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}

    baseURL = "https://bridge-uat.nios.ac.in/registration/basic-details"

    for i in range(3, 3 + TOTAL_REGISTRATIONS):
        current_name = DataUtils.get_random_name().upper()
        father_name = f"Father {DataUtils.get_random_name()}"
        mother_name = f"Mother {DataUtils.get_random_name()}"
        
        print(f"\n--- Starting Registration {i-2}/{TOTAL_REGISTRATIONS}: {current_name} ---")
        
        # Fresh Chrome for every registration — SabPaisa closes the window after payment
        options = Options()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()

        try:
            driver.get(baseURL)
            time.sleep(2)
            
            # Initialize Pages
            reg_page = RegistrationPage(driver)
            elig_page = EligibilityPage(driver)
            auth_page = AuthenticationPage(driver)
            personal_page = PersonalInformationPage(driver)
            address_page = AddressDetailsPage(driver)
            subject_page = SubjectDetailsPage(driver)
            docs_page = DocumentsPage(driver)
            payment_page = PaymentFlowPage(driver)

            # Step 1: Basic Details
            reg_page.handle_modal()
            reg_page.set_name(current_name)
            reg_page.set_father_name(father_name)
            reg_page.set_mother_name(mother_name)
            reg_page.set_dob("15-08-1990")
            reg_page.set_gender("Male")
            reg_page.set_udise_code(UDISE_CODE)
            reg_page.click_verify_udise()
            time.sleep(1)
            reg_page.handle_modal()
            reg_page.click_continue()
            time.sleep(2)

            # Step 2 & 3: Eligibility and Authentication
            from selenium.webdriver.support.wait import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            print("Waiting for transition from Basic Details...")
            try:
                WebDriverWait(driver, 25).until(
                    lambda d: "eligibility" in d.current_url or "authentication" in d.current_url
                )
            except Exception:
                print(f"Timed out waiting for transition. Current URL: {driver.current_url}")
                continue

            if "eligibility" in driver.current_url:
                print("Landed on Eligibility page. Filling details...")
                try:
                    elig_page.set_date_of_appointment("01-01-2022")
                    elig_page.click_continue()
                    time.sleep(2)
                    WebDriverWait(driver, 20).until(EC.url_contains("authentication"))
                except Exception as e:
                    print(f"Eligibility step failed or was skipped: {e}")

            print("Proceeding to Authentication...")
            email = DataUtils.generate_email_incremental()
            mobile = DataUtils.get_fixed_mobile()
            auth_page.set_email(email)
            auth_page.set_mobile(mobile)
            auth_page.click_submit()
            time.sleep(2)

            # Step 4: OTP (Auto-bypassed on UAT)
            try:
                WebDriverWait(driver, 20).until(
                    lambda d: "personal" in d.current_url or "otp" in d.current_url
                )
                if "otp" in driver.current_url:
                    print("OTP page detected — waiting for auto-bypass...")
                    WebDriverWait(driver, 20).until(EC.url_contains("/personal"))
                print("Reached Personal Information page.")
            except Exception:
                print(f"Could not reach personal page for {current_name}. Skipping...")
                continue

            # Step 5: Personal Information
            personal_page.set_social_category("General")
            personal_page.set_medium_of_study(MEDIUM)
            personal_page.click_continue()
            time.sleep(2)

            # Step 6: Address Details
            address_page.enter_address_line1(ADDRESS)
            address_page.enter_street_locality("Lashkar")
            address_page.select_state("MADHYA PRADESH")
            time.sleep(1)
            address_page.select_district("GWALIOR")
            address_page.enter_pincode(PINCODE)
            address_page.click_continue()
            time.sleep(2)

            # Step 7: Subject Details
            time.sleep(5)
            subject_page.select_any_medium_for_enabled_subjects()
            time.sleep(5)
            subject_page.click_continue()
            time.sleep(2)

            # Step 8: Document Upload
            photo_path, doc_path = DataUtils.ensure_dummy_files()
            docs_page.upload_all_documents(photo_path, doc_path)
            docs_page.toggle_checkboxes()
            docs_page.click_save_continue()
            time.sleep(3)

            # Step 9: Review & Payment
            payment_page.check_all_confirmation_boxes()
            payment_page.select_sabpaisa_gateway()
            payment_page.click_pay_now()
            time.sleep(5)

            print(f"Processing SabPaisa payment for {current_name}...")
            payment_page.process_standard_payment(PAYMENT_DATA)
            
            print(f"✅ Successfully completed registration {i-2}/{TOTAL_REGISTRATIONS}: {current_name}")
            time.sleep(3)

        except Exception as e:
            print(f"❌ Registration {i-2} failed for {current_name}: {e}")
        finally:
            try:
                driver.quit()
            except Exception:
                pass  # Driver may already be closed by SabPaisa

if __name__ == "__main__":
    run_batch_registration()
