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
from selenium.webdriver.common.by import By
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
        WebDriverWait(self.driver, 30).until(EC.url_contains("otp"))
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
        time.sleep(2)
        
        address_page.enter_address_line1("101 dd nagar")
        address_page.enter_street_locality("netaji subhash place")
        address_page.select_state("DELHI")
        time.sleep(2)  # Wait for district dropdown to load
        address_page.select_district("CENTRAL")
        address_page.enter_pincode("110034")
        address_page.click_continue()
        
        # --- Step 7: Subject Details ---
        self.logger.info("Step 7: Subject Details")
        WebDriverWait(self.driver, 15).until(EC.url_contains("subject"))
        # Select Medium for enabled subjects (dynamically detected)
        subject_page.select_any_medium_for_enabled_subjects()
        subject_page.click_continue()

        # --- Step 8: Documents ---
        self.logger.info("Step 8: Document Upload")
        # Ensure dummy files exist
        photo_path = os.path.join(os.getcwd(), "test_data", "dummy.jpg")
        doc_path = os.path.join(os.getcwd(), "test_data", "dummy.pdf")
        
        # Create dummy JPEG if not exists
        if not os.path.exists(photo_path):
            self.logger.info("Creating dummy.jpg")
            # Create a 100x100 white square if possible, or just a dummy file
            try:
                from PIL import Image
                img = Image.new('RGB', (100, 100), color = 'white')
                img.save(photo_path)
            except:
                with open(photo_path, "wb") as f:
                    f.write(b"dummy image content")
                    
        # Create dummy PDF if not exists
        if not os.path.exists(doc_path):
            self.logger.info("Creating dummy.pdf")
            with open(doc_path, "wb") as f:
                f.write(b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << >> /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 1 >>\nstream\n \nendstream\nendobj\ntrailer\n<< /Root 1 0 R /Size 5 >>\n%%EOF")

        # Increased wait for Documents page load
        WebDriverWait(self.driver, 60).until(EC.url_contains("document"))
        docs_page.debug_print_ids() # DEBUG LOCATORS
        
        # Prepare dummy paths
        photo_path = os.path.join(os.getcwd(), "test_data", "dummy.jpg")
        doc_path = os.path.join(os.getcwd(), "test_data", "dummy.pdf")
        
        # Upload all docs dynamically
        docs_page.upload_all_documents(photo_path, doc_path)
        
        # Handle checkboxes (if any)
        docs_page.toggle_checkboxes()
        
        # Save & Continue
        docs_page.click_save_continue()
        
        # --- Step 9: Review & Payment ---
        self.logger.info("Step 9: Review and Payment")
        # Transition can be slow, wait for 'review' or 'payment' in URL
        WebDriverWait(self.driver, 60).until(lambda d: "review" in d.current_url.lower() or "payment" in d.current_url.lower())
        self.logger.info("Successfully reached Review/Payment Page!")
        
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
