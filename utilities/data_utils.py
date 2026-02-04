
import os
import random
from faker import Faker
from utilities.read_properties import ReadConfig

class DataUtils:
    faker = Faker()
    paths = ReadConfig.getPaths()
    
    @staticmethod
    def generate_email_incremental():
        """Generates an incremental email using a counter file."""
        counter_path = os.path.join(os.getcwd(), DataUtils.paths['test_data_dir'], DataUtils.paths['email_counter'])
        
        # Ensure dir exists
        os.makedirs(os.path.dirname(counter_path), exist_ok=True)
        
        if not os.path.exists(counter_path):
            with open(counter_path, "w") as f:
                f.write("1")
        
        with open(counter_path, "r") as f:
            try:
                count = int(f.read().strip())
            except ValueError:
                count = 1
            
        email = f"insphere.shubhamsingh+{count}@gmail.com"
        
        # Increment for next run
        with open(counter_path, "w") as f:
            f.write(str(count + 1))
            
        return email

    @staticmethod
    def get_fixed_mobile():
        """Returns the fixed mobile number for tests."""
        return "6268326377"

    @staticmethod
    def ensure_dummy_files():
        """Creates dummy JPG and PDF files if they don't exist."""
        test_data_dir = os.path.join(os.getcwd(), DataUtils.paths['test_data_dir'])
        os.makedirs(test_data_dir, exist_ok=True)
        
        jpg_path = os.path.join(test_data_dir, DataUtils.paths['dummy_jpg'])
        pdf_path = os.path.join(test_data_dir, DataUtils.paths['dummy_pdf'])
        
        if not os.path.exists(jpg_path) or os.path.getsize(jpg_path) == 0:
            with open(jpg_path, "wb") as f:
                f.write(os.urandom(51200)) # 50KB
                
        if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) == 0:
            with open(pdf_path, "wb") as f:
                 f.write(b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
                 f.write(os.urandom(51200))
                 f.write(b"%%EOF")
                 
        return jpg_path, pdf_path

    @staticmethod
    def get_random_name():
        return DataUtils.faker.name().replace(".", "")

    @staticmethod
    def get_random_dob():
        return "15-08-1990" 
