"""
SME Self-Registration Page — Page Object for Subject Matter Expert registration.
=================================================================================
Handles the full SME registration wizard steps: Basic Info, Credentials, Address, etc.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.wait_utils import WaitUtils
import time
import os

class SMERegistrationPage(BasePage):
    """Page Object for SME Registration Wizard on the Admin Portal."""

    # ── Navigation ──
    SME_MENU = (By.XPATH, "//a[contains(.,'Subject Experts')]")
    SUMMARY_SUBMENU = (By.XPATH, "//a[contains(@href, 'subject-expert') and contains(.,'Summary')] | //ul[contains(@class, 'submenu')]//a[contains(., 'Summary')]")
    ADD_SME_BTN = (By.XPATH, "//a[contains(.,'Add Subject Expert')]")

    # ── Generic Action Buttons ──
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(),'Next') or contains(text(),'Save & Next')]")
    PREVIOUS_BUTTON = (By.XPATH, "//button[contains(text(),'Previous') or contains(text(),'Back')]")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(),'Submit') or contains(text(),'Register')]")

    # ── Generic Locator Helper ──
    def get_input_by_label(self, label_text):
        # Finds input next to label, or inside the same parent container
        return (By.XPATH, f"//label[contains(normalize-space(text()), '{label_text}')]/following-sibling::input | //label[contains(normalize-space(text()), '{label_text}')]/..//input[not(@type='hidden')] | //input[contains(@placeholder, '{label_text}')]")

    def get_dropdown_by_label(self, label_text):
        return (By.XPATH, f"//label[contains(normalize-space(text()), '{label_text}')]/following-sibling::select | //label[contains(normalize-space(text()), '{label_text}')]/..//select | //label[contains(normalize-space(text()), '{label_text}')]/..//div[contains(@class, 'chosen-container')] | //label[contains(normalize-space(text()), '{label_text}')]/..//span[contains(@class, 'select2-container')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WaitUtils(self.driver)

    def navigate_to_sme_registration(self):
        """Navigate to Subject Experts -> Summary -> Add Subject Expert"""
        self.logger.info("Navigating to Subject Experts -> Summary...")
        try:
            self.do_click(self.SME_MENU)
            time.sleep(1)
            self.do_click(self.SUMMARY_SUBMENU)
            time.sleep(2)
            self.logger.info("Clicking 'Add Subject Expert' button...")
            self.do_click(self.ADD_SME_BTN)
            time.sleep(2)
        except Exception as e:
            self.logger.warning(f"Sidebar navigation failed: {e}. Trying direct URL...")
            self.driver.get("https://bridge-uat-admin.nios.ac.in/subject-expert/create")
            time.sleep(2)
        self.logger.info(f"On SME Registration form. URL: {self.driver.current_url}")

    # ── Step Navigation ──
    def click_next(self):
        self.logger.info("Clicking Next...")
        self.do_click(self.NEXT_BUTTON)
        time.sleep(2)

    def click_submit(self):
        self.logger.info("Clicking Submit...")
        try:
            self.do_click(self.SUBMIT_BUTTON)
        except Exception as e:
            self.logger.warning(f"Standard click on Submit button failed: {e}. Trying JS click...")
            try:
                el = self.driver.find_element(*self.SUBMIT_BUTTON)
                self.driver.execute_script("arguments[0].click();", el)
            except Exception as js_err:
                self.logger.error(f"JS click on Submit button failed: {js_err}")
                raise js_err
        time.sleep(5)

    # ── Step 1: Basic Information ──
    def fill_basic_info(self, name, designation, dob, gender, aadhaar, school_name, experience):
        self.logger.info("Filling Step 1: Basic Information...")
        self.do_send_keys(self.get_input_by_label("Name"), name)
        self.do_send_keys(self.get_input_by_label("Designation"), designation)
        
        # DOB
        try:
            self._set_date_field(self.get_input_by_label("Date of Birth"), dob)
        except:
            self.do_send_keys(self.get_input_by_label("Date of Birth"), dob)

        self._select_dropdown(self.get_dropdown_by_label("Gender"), gender)
        
        if aadhaar:
            self.do_send_keys(self.get_input_by_label("Aadhaar Number"), aadhaar)
            
        if school_name:
            self.logger.info("Custom selecting school...")
            try:
                self.logger.info("Manually interacting with School dropdown based on exact instructions...")
                
                # 1. Click on the School dropdown.
                school_dropdown = (By.XPATH, "//label[contains(normalize-space(text()), 'School')]/following-sibling::div[contains(@class, 'chosen-container') or contains(@class, 'select2')] | //label[contains(normalize-space(text()), 'School')]/..//span[contains(@class, 'select2-selection')] | //div[contains(@id, 'school_chosen') or contains(@class, 'select2-container')]")
                elements = self.driver.find_elements(*school_dropdown)
                clicked = False
                for el in elements:
                    if el.is_displayed():
                        try:
                            el.click()
                        except:
                            self.driver.execute_script("arguments[0].click();", el)
                        clicked = True
                        break
                        
                if not clicked and elements:
                    self.driver.execute_script("arguments[0].click();", elements[0])
                
                time.sleep(1)
                
                # 2. Locate the search field using class: field-search-study_centre_id required
                # We'll use XPath to look for the input that either has this class, or is inside a container with this class, or is a generic select2 search field.
                search_input_xpath = "//input[contains(@class, 'field-search-study_centre_id') or contains(@class, 'select2-search__field') or contains(@class, 'chosen-search-input')] | //*[contains(@class, 'field-search-study_centre_id')]//input"
                inp = self.wait.visibility_wait((By.XPATH, search_input_xpath))
                inp.clear()
                
                # 3. Enter the School name in the search field.
                for char in school_name:
                    inp.send_keys(char)
                    time.sleep(0.1)
                
                # 4. Do NOT press Enter after typing.
                # 5. Wait for a second until the filtered results appear automatically.
                time.sleep(2)
                
                # 6. Select the first available option from the filtered list.
                # Looking for the first actual selectable result (avoiding "Loading..." elements).
                first_option_xpath = "(//ul[contains(@class, 'select2-results__options')]/li[contains(@class, 'select2-results__option') and not(contains(@class, 'loading')) and not(contains(text(), 'Searching'))] | //li[contains(@class, 'active-result') and not(contains(@class, 'loading'))])[1]"
                first_opt = self.wait.presence_wait((By.XPATH, first_option_xpath))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_opt)
                time.sleep(0.5)
                
                try:
                    first_opt.click()
                except:
                    self.driver.execute_script("arguments[0].click();", first_opt)
                    
                self.logger.info("Successfully selected the first option from the filtered list.")
            except Exception as e:
                self.logger.error(f"Failed to manually select school using explicit steps: {e}")
        self.do_send_keys(self.get_input_by_label("Experience"), experience)
        self.logger.info("Basic Information filled.")

    # ── Step 2: User Credentials ──
    def fill_user_credentials(self, first_name, last_name, email, mobile, level, role, username, password, district, study_centre):
        self.logger.info("Filling Step 2: User Credentials...")
        self.do_send_keys(self.get_input_by_label("Firstname"), first_name)
        self.do_send_keys(self.get_input_by_label("Lastname"), last_name)
        self.do_send_keys(self.get_input_by_label("Email address"), email)
        self.do_send_keys(self.get_input_by_label("Mobile Number"), mobile)
        
        if level:
            self._select_dropdown(self.get_dropdown_by_label("Level"), level)
        if role:
            self._select_dropdown(self.get_dropdown_by_label("Role"), role)
            
        self.do_send_keys(self.get_input_by_label("Username"), username)
        self.do_send_keys(self.get_input_by_label("Password"), password)
        self.do_send_keys(self.get_input_by_label("Confirm Password"), password)
        
        if district:
            self._select_dropdown(self.get_dropdown_by_label("Districts"), district)
        if study_centre:
            self._select_dropdown(self.get_dropdown_by_label("Study Centres"), study_centre)
            
        self.logger.info("User Credentials filled.")

    # ── Step 3: Address Details ──
    def fill_address_details(self, house, street, state, district, pincode, same_as_permanent=True):
        self.logger.info("Filling Step 3: Address Details...")
        self.do_send_keys(self.get_input_by_label("House/Building"), house)
        self.do_send_keys(self.get_input_by_label("Street"), street)
        
        self._select_dropdown(self.get_dropdown_by_label("State"), state)
        time.sleep(2) # wait for district AJAX
        self._select_dropdown(self.get_dropdown_by_label("District"), district)
        self.do_send_keys(self.get_input_by_label("Pincode"), pincode)
        
        if same_as_permanent:
            try:
                checkbox = (By.XPATH, "//input[@type='checkbox' and contains(@name, 'same_as') or contains(@id, 'same_as')] | //label[contains(text(), 'Correspondence address is same')]")
                self.do_click(checkbox)
            except Exception as e:
                self.logger.warning(f"Could not click same address checkbox: {e}")
                
        self.logger.info("Address Details filled.")

    # ── Step 4: Qualification Details ──
    def fill_qualification(self, qualification, board, passing_year, percentage):
        self.logger.info("Filling Step 4: Qualification Details...")
        try:
            self._select_dropdown(self.get_dropdown_by_label("Qualification"), qualification)
            self.do_send_keys(self.get_input_by_label("Board"), board)
            self.do_send_keys(self.get_input_by_label("Passing"), passing_year)
            self.do_send_keys(self.get_input_by_label("Percentage"), percentage)
        except Exception as e:
            self.logger.warning(f"Error filling Qualification: {e}. Attempting generic fallbacks...")
            self.do_send_keys((By.XPATH, "(//input[@type='text'])[1]"), qualification)
        self.logger.info("Qualification Details filled.")

    # ── Step 5: Employment Details ──
    def fill_employment_details(self, office_name, designation, start_date):
        self.logger.info("Filling Step 5: Employment Details...")
        try:
            self.do_send_keys(self.get_input_by_label("Office"), office_name)
            self.do_send_keys((By.XPATH, "(//label[contains(text(), 'Designation')]/following-sibling::input)[last()]"), designation)
            self.do_send_keys(self.get_input_by_label("Start Date"), start_date)
        except Exception as e:
            self.logger.warning(f"Error filling Employment: {e}")
        self.logger.info("Employment Details filled.")

    # ── Step 6: Subjects Details ──
    def fill_subject_details(self, subject):
        self.logger.info("Filling Step 6: Subject Details...")
        try:
            self._select_dropdown(self.get_dropdown_by_label("Subject"), subject)
        except Exception as e:
            self.logger.warning(f"Error selecting subject: {e}")
            
    # ── Step 7: Documents ──
    def upload_documents(self, photo_path, signature_path):
        self.logger.info("Filling Step 7: Documents Upload...")
        try:
            file_inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")
            if len(file_inputs) >= 2:
                file_inputs[0].send_keys(os.path.abspath(photo_path))
                time.sleep(1)
                file_inputs[1].send_keys(os.path.abspath(signature_path))
        except Exception as e:
            self.logger.warning(f"Error uploading documents: {e}")

    def click_next(self):
        self.logger.info("Clicking Next...")
        time.sleep(2) # Give AJAX validations time to complete before clicking
        self.do_click((By.XPATH, "//button[contains(text(),'Next') or contains(text(),'Save & Next')]"))
        time.sleep(2) # Give the next step time to render

    # ── Validation ──
    def is_registration_successful(self):
        """Returns True if a success alert appears."""
        alert = (By.CSS_SELECTOR, ".alert-success, .swal2-success")
        return self.is_visible(alert)

    # ── Helpers ──
    def _select_dropdown(self, locator, option_text):
        """Ultra-fast, robust dropdown selection for native selects, Select2, and Chosen."""
        try:
            elements = self.driver.find_elements(*locator)
            
            # 1. Native Select handling
            for el in elements:
                if el.tag_name.lower() == 'select' and el.is_displayed():
                    from selenium.webdriver.support.ui import Select
                    Select(el).select_by_visible_text(option_text)
                    self.logger.info(f"Selected native dropdown value '{option_text}'")
                    return

            # 2. Select2/Chosen handling (No do_click)
            clicked = False
            for el in elements:
                if el.is_displayed():
                    try:
                        el.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", el)
                    clicked = True
                    break
                    
            if not clicked and elements:
                self.driver.execute_script("arguments[0].click();", elements[0])
                
            time.sleep(1)
            
            # Type in search if available
            self.driver.implicitly_wait(0) # Temporarily disable implicit wait to prevent hangs
            search_inputs = self.driver.find_elements(By.XPATH, "//input[contains(@class, 'select2-search__field') or contains(@class, 'chosen-search-input') or @type='search'] | //div[contains(@class, 'chosen-search') or contains(@class, 'chosen-drop')]//input")
            active_search_input = None
            for inp in search_inputs:
                if inp.is_displayed():
                    active_search_input = inp
                    inp.clear()
                    inp.send_keys(option_text)
                    time.sleep(1)
                    break
                    
            # Click the matching option (JS to avoid any Selenium timeouts)
            option_xpath = (
                f"//li[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{option_text.lower()}')] | "
                f"//li[contains(@class, 'active-result') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{option_text.lower()}')] | "
                f"//div[contains(@class, 'select2-result-label') and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{option_text.lower()}')]"
            )
            
            opts = self.driver.find_elements(By.XPATH, option_xpath)
            displayed_opts = [o for o in opts if o.is_displayed()]
            if displayed_opts:
                try:
                    displayed_opts[0].click()
                except:
                    self.driver.execute_script("arguments[0].click();", displayed_opts[0])
            elif active_search_input:
                from selenium.webdriver.common.keys import Keys
                active_search_input.send_keys(Keys.ENTER)
            elif opts:
                try:
                    opts[0].click()
                except:
                    self.driver.execute_script("arguments[0].click();", opts[0])
            else:
                # Fallback to pure JS injection if UI completely fails
                if elements and elements[0].tag_name.lower() == 'select':
                    opt_xpath = f".//option[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{option_text.lower()}')]"
                    select_opts = elements[0].find_elements(By.XPATH, opt_xpath)
                    if select_opts:
                        val = select_opts[0].get_attribute('value')
                        self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change', {bubbles:true})); if(typeof jQuery != 'undefined') { $(arguments[0]).trigger('change'); }", elements[0], val)
                        self.logger.info(f"Fell back to JS injection for '{option_text}'")
                        self.driver.implicitly_wait(10)
                        return

            self.driver.implicitly_wait(10) # Restore implicit wait
            self.logger.info(f"Selected searchable dropdown value '{option_text}'")
            time.sleep(0.5)
        except Exception as e:
            self.driver.implicitly_wait(10)
            self.logger.warning(f"Dropdown selection failed for '{option_text}': {e}")

    def _set_date_field(self, locator, date_value):
        """Types the date directly and dispatches events to satisfy JS frameworks."""
        try:
            element = self.driver.find_element(*locator)
            element.click()
            element.clear()
            element.send_keys(date_value)
            # Force JS frameworks to register the change
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true })); arguments[0].dispatchEvent(new Event('input', { bubbles: true })); arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));", element)
            time.sleep(0.5)
        except Exception as e:
            self.logger.warning(f"Failed to set date field: {e}")
