import pytest
import time
from pages.registration_page import RegistrationPage
from pages.eligibility_page import EligibilityPage
from pages.authentication_page import AuthenticationPage
from pages.otp_page import OTPPage
from pages.personal_information_page import PersonalInformationPage
from pages.address_details_page import AddressDetailsPage
from pages.subject_details_page import SubjectDetailsPage
from pages.documents_page import DocumentsPage
from pages.payment_flow_page import PaymentFlowPage

from utilities.read_properties import ReadConfig
from utilities.custom_logger import LogGen
from utilities.data_utils import DataUtils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test_001_Registration:
    baseURL = ReadConfig.getApplicationURL()
    logger = LogGen.loggen()
    timeouts = ReadConfig.getTimeouts()
    payment_conf = ReadConfig.getPaymentConfig()
    
    def test_registration(self, setup):
        self.logger.info("**** Starting Restored Test_001_Registration ****")
        self.driver = setup
        self.driver.get(self.baseURL)
        
        # Initialize Pages
        reg_page = RegistrationPage(self.driver)
        elig_page = EligibilityPage(self.driver)
        auth_page = AuthenticationPage(self.driver)
        personal_page = PersonalInformationPage(self.driver)
        address_page = AddressDetailsPage(self.driver)
        subject_page = SubjectDetailsPage(self.driver)
        docs_page = DocumentsPage(self.driver)
        payment_page = PaymentFlowPage(self.driver)
        
        # --- Step 1: Basic Details ---
        self.logger.info("Step 1: Basic Details")
        reg_page.handle_modal()
        
        name = DataUtils.get_random_name()
        reg_page.set_name(name)
        reg_page.set_father_name("Father " + name)
        reg_page.set_mother_name("Mother " + name)
        reg_page.set_dob(DataUtils.get_random_dob())
        reg_page.set_gender("Male")
        reg_page.set_udise_code("10101000101")
        reg_page.click_verify_udise()
        reg_page.handle_modal()
        reg_page.click_continue()
        
        # --- Step 2: Eligibility ---
        self.logger.info("Step 2: Eligibility")
        WebDriverWait(self.driver, self.timeouts['page_load']).until(EC.url_contains("eligibility"))
        try:
            elig_page.set_date_of_appointment("01-01-2022")
            elig_page.click_continue()
        except:
             self.logger.info("Eligibility step skipped or auto-filled")

        # --- Step 3: Authentication ---
        self.logger.info("Step 3: Authentication")
        WebDriverWait(self.driver, self.timeouts['page_load']).until(EC.url_contains("authentication"))
        
        email = DataUtils.generate_email_incremental()
        mobile = DataUtils.get_fixed_mobile()
        
        self.logger.info(f"Using Email: {email} and Mobile: {mobile}")
        
        auth_page.set_email(email)
        auth_page.set_mobile(mobile)
        auth_page.click_submit()
        
        # --- Step 4: OTP (Human Loop) ---
        self.logger.info("Step 4: OTP Verification")
        WebDriverWait(self.driver, self.timeouts['page_load']).until(EC.url_contains("otp"))
        print("\n" + "="*50)
        print("ATTENTION: OTP SENT. Please enter it MANUALLY in the browser.")
        print(f"The script will wait up to {self.timeouts['otp_wait']} seconds for you to complete this.")
        print("="*50)
        
        # --- Step 5: Personal Information ---
        self.logger.info("Step 5: Personal Information")
        WebDriverWait(self.driver, self.timeouts['otp_wait']).until(EC.url_contains("personal"))
        personal_page.set_social_category("General")
        personal_page.set_medium_of_study("English")
        personal_page.click_continue()
        
        # --- Step 6: Address Details ---
        self.logger.info("Step 6: Address Details")
        
        address_page.enter_address_line1("101 dd nagar")
        address_page.enter_street_locality("netaji subhash place")
        address_page.select_state("DELHI")
        address_page.select_district("CENTRAL")
        address_page.enter_pincode("110034")
        address_page.click_continue()
        
        # --- Step 7: Subject Details ---
        self.logger.info("Step 7: Subject Details")
        WebDriverWait(self.driver, self.timeouts['page_load']).until(EC.url_contains("subject"))
        subject_page.select_any_medium_for_enabled_subjects()
        subject_page.click_continue()

        # --- Step 8: Documents ---
        self.logger.info("Step 8: Document Upload")
        photo_path, doc_path = DataUtils.ensure_dummy_files()

        WebDriverWait(self.driver, self.timeouts['page_load']).until(EC.url_contains("document"))
        # docs_page.debug_print_ids() # Removed debug print
        
        docs_page.upload_all_documents(photo_path, doc_path)
        docs_page.toggle_checkboxes()
        docs_page.click_save_continue()
        
        # --- Step 9: Review & Payment ---
        self.logger.info("Step 9: Review and Payment")
        time.sleep(1) # Reduced buffer for docs upload API response
        WebDriverWait(self.driver, self.timeouts['page_load']).until(lambda d: "review" in d.current_url.lower() or "payment" in d.current_url.lower())
        self.logger.info("Successfully reached Review/Payment Page!")
        
        payment_page.check_all_confirmation_boxes()
        payment_page.select_sabpaisa_gateway()
        payment_page.click_pay_now()

        # --- SabPaisa Gateway Interaction ---
        self.logger.info(f"Entering {self.payment_conf['gateway']} Gateway...")
        payment_page.select_payment_mode(self.payment_conf['mode'])
        payment_page.enter_card_details(
            number=self.payment_conf['card_number'],
            name=self.payment_conf['card_holder'],
            expiry=self.payment_conf['card_expiry'],
            cvv=self.payment_conf['card_cvv']
        )
        payment_page.simulate_success()
        
        self.logger.info("**** Registration and Payment Flow Completed Successfully ****")
        time.sleep(self.timeouts['gateway_wait'])
