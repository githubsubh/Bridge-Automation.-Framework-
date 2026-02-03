import pytest
import os
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

class Test_001_Registration:
    baseURL = ReadConfig.getApplicationURL()
    logger = LogGen.loggen()
    
    def test_registration(self, setup):
        self.logger.info("**** Starting Restored Test_001_Registration ****")
        self.driver = setup
        self.driver.get(self.baseURL)
        
        # Initialize Pages
        reg_page = RegistrationPage(self.driver)
        elig_page = EligibilityPage(self.driver)
        auth_page = AuthenticationPage(self.driver)
        otp_page = OTPPage(self.driver)
        personal_page = PersonalInformationPage(self.driver)
        address_page = AddressDetailsPage(self.driver)
        subject_page = SubjectDetailsPage(self.driver)
        docs_page = DocumentsPage(self.driver)
        payment_page = PaymentFlowPage(self.driver)
        
        faker = Faker()
        
        # --- Step 1: Basic Details ---
        self.logger.info("Step 1: Basic Details")
        reg_page.handle_modal()
        
        name = faker.name().replace(".", "")
        reg_page.set_name(name)
        reg_page.set_father_name("Father " + name)
        reg_page.set_mother_name("Mother " + name)
        reg_page.set_dob("15-08-1990")
        reg_page.set_gender("Male")
        reg_page.set_udise_code("10101000101")
        reg_page.click_verify_udise()
        reg_page.handle_modal()
        reg_page.click_continue()
        
        # --- Step 2: Eligibility ---
        self.logger.info("Step 2: Eligibility")
        WebDriverWait(self.driver, 15).until(EC.url_contains("eligibility"))
        try:
            elig_page.set_date_of_appointment("01-01-2022")
            elig_page.click_continue()
        except:
             self.logger.info("Eligibility step skipped or auto-filled")

        # --- Step 3: Authentication ---
        self.logger.info("Step 3: Authentication")
        WebDriverWait(self.driver, 15).until(EC.url_contains("authentication"))
        # Incremental Email Logic
        counter_path = os.path.join(os.getcwd(), "test_data", "email_counter.txt")
        if not os.path.exists(counter_path):
            with open(counter_path, "w") as f:
                f.write("1")
        
        with open(counter_path, "r") as f:
            count = int(f.read().strip())
            
        email = f"insphere.shubhamsingh+{count}@gmail.com"
        
        # Increment counter for next run
        with open(counter_path, "w") as f:
            f.write(str(count + 1))
            
        mobile = "6268326377" # Fixed mobile number
        
        self.logger.info(f"Using Email: {email} and Mobile: {mobile}")
        
        auth_page.set_email(email)
        auth_page.set_mobile(mobile)
        auth_page.click_submit()
        
        # --- Step 4: OTP (Human Loop) ---
        self.logger.info("Step 4: OTP Verification")
        WebDriverWait(self.driver, 15).until(EC.url_contains("otp"))
        print("\n" + "="*50)
        print("ATTENTION: OTP SENT. Please enter it MANUALLY in the browser.")
        print("The script will wait up to 5 minutes for you to complete this.")
        print("="*50)
        # We process nothing here, just waiting for the user to finish.
        
        # --- Step 5: Personal Information ---
        self.logger.info("Step 5: Personal Information")
        # Increasing wait time to 300s to allow manual OTP entry
        WebDriverWait(self.driver, 300).until(EC.url_contains("personal"))
        personal_page.set_social_category("General")
        personal_page.set_medium_of_study("English")
        personal_page.click_continue()
        
        # --- Step 6: Address Details ---
        self.logger.info("Step 6: Address Details")
        WebDriverWait(self.driver, 15).until(EC.url_contains("address"))
        address_page.enter_address_line1(faker.address())
        address_page.select_state("DELHI")
        address_page.select_district("Central Delhi") # Example
        address_page.enter_pincode("110001")
        address_page.click_continue()
        
        # --- Step 7: Subject Details ---
        self.logger.info("Step 7: Subject Details")
        WebDriverWait(self.driver, 15).until(EC.url_contains("subject"))
        subject_page.select_all_mediums("English")
        subject_page.click_continue()

        # --- Step 8: Documents ---
        self.logger.info("Step 8: Document Upload")
        WebDriverWait(self.driver, 15).until(EC.url_contains("documents"))
        
        # Prepare dummy paths
        base_dir = os.getcwd()
        dummy_img = os.path.join(base_dir, "test_data", "dummy.jpg")
        dummy_pdf = os.path.join(base_dir, "test_data", "dummy.pdf")
        
        docs_page.upload_document("photo", dummy_img)
        docs_page.upload_document("signature", dummy_img)
        docs_page.upload_document("aadhar", dummy_pdf)
        docs_page.upload_document("10th", dummy_pdf)
        docs_page.upload_document("12th", dummy_pdf)
        
        docs_page.toggle_checkboxes()
        docs_page.click_save_continue()
        
        # --- Step 9: Review & Payment ---
        self.logger.info("Step 9: Review and Payment")
        WebDriverWait(self.driver, 15).until(EC.url_contains("review"))
        
        payment_page.review_and_pay()
        
        # Wait for Gateway
        time.sleep(5) 
        # SabPaisa Automation
        self.logger.info("Payment Gateway Interaction")
        card_num = "4029484589897107"
        name = "Test User"
        expiry = "12/30"
        cvv = "234"
        
        payment_page.select_payment_mode("Card")
        payment_page.enter_card_details(card_num, name, expiry, cvv)
        
        self.logger.info("Payment Submitted. Teacher Registration Restoration Complete.")
        
        time.sleep(10) # Wait to see result
