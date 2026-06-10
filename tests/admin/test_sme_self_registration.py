import pytest
import time
import os
from pages.admin_login_page import AdminLoginPage
from pages.sme_registration_page import SMERegistrationPage
from utilities.data_utils import DataUtils
from utilities.read_properties import ReadConfig

@pytest.mark.sme_registration
class TestSMESelfRegistration:

    def test_sme_self_registration_flow(self, admin_login):
        driver = admin_login
        driver.get(os.getenv("ADMIN_URL", "https://bridge-uat-admin.nios.ac.in"))
        
        login_page = AdminLoginPage(driver)
        success = login_page.login_with_manual_captcha(admin_login.username, admin_login.password, timeout=120)
        assert success, "Admin login failed"
        
        reg_page = SMERegistrationPage(driver)
        reg_page.navigate_to_sme_registration()
        
        import random
        # Data Setup
        email = DataUtils.generate_email_incremental()
        # Generate a random 10-digit dummy mobile number to avoid uniqueness errors
        mobile = f"98{random.randint(10000000, 99999999)}"
        name = "SME Expert"
        dob = "01011985"
        jpg_path, pdf_path = DataUtils.ensure_dummy_files()
        
        # Unique School Code to avoid ambiguity
        school_text = "deen"
        study_centre_text = "09150101103"
        district = "AGRA"
        
        # User explicitly requested to use their provided list of 126 valid Aadhaar numbers
        # The UAT sandbox API rejects even mathematically valid numbers if they aren't whitelisted.
        from utilities.valid_aadhaar_list import VALID_AADHAAR_NUMBERS
        import random
        random_aadhaar = random.choice(VALID_AADHAAR_NUMBERS)
        
        # Step 1: Basic Information
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
        
        # Step 2: User Credentials
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
            study_centre=study_centre_text
        )
        reg_page.click_next()
        
        # Step 3: Address Details
        reg_page.fill_address_details(
            house="123 Automation St",
            street="Test Locality",
            state="MADHYA PRADESH",
            district="GWALIOR",
            pincode="474020",
            same_as_permanent=True
        )
        reg_page.click_next()
        
        # Step 4: Qualification
        reg_page.fill_qualification(
            qualification="M.Sc. Mathematics",
            board="Test University",
            passing_year="2010",
            percentage="85"
        )
        reg_page.click_next()
        
        # Step 5: Employment
        reg_page.fill_employment_details(
            office_name="Test School",
            designation="Teacher",
            start_date="01-01-2015"
        )
        reg_page.click_next()
        
        # Step 6: Subjects Details
        reg_page.fill_subject_details(subject="Mathematics")
        reg_page.click_next()
        
        # Step 7: Documents
        reg_page.upload_documents(
            photo_path=jpg_path,
            signature_path=jpg_path
        )
        reg_page.click_next()
        
        # Step 8: Review & Submit
        reg_page.click_submit()
        
        assert reg_page.is_registration_successful(), "SME Self-Registration failed"
