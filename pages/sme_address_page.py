"""
SME Address Details Page — Step 3 of the Subject Expert Registration Wizard.
=============================================================================
Handles Permanent Address and Correspondence Address entry including
AJAX-driven State → District cascading dropdowns on the Admin portal.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utilities.wait_utils import WaitUtils
import time


class SMEAddressPage(BasePage):
    """Page Object for Step 3 (Address Details) of SME Registration Wizard."""

    # ── Step Tab ──
    STEP_TAB = (By.XPATH, "//a[contains(text(), '3. Address Details') or contains(text(), 'Address Details')]")

    # ═══════════════════════════════════════════════════════════════════════
    # PERMANENT ADDRESS FIELDS
    # ═══════════════════════════════════════════════════════════════════════

    # Text inputs — try ID first, then name, then label-based fallback
    PERM_HOUSE = (
        By.XPATH,
        "//input[contains(@name, 'permanent_address1') or contains(@id, 'permanent_address1')]"
        " | //label[contains(text(), 'House') or contains(text(), 'Building')]"
        "/..//input[not(@type='hidden')]"
    )

    PERM_STREET = (
        By.XPATH,
        "//input[contains(@name, 'permanent_address2') or contains(@id, 'permanent_address2')]"
        " | //label[contains(text(), 'Street') or contains(text(), 'Locality')]"
        "/..//input[not(@type='hidden')]"
    )

    PERM_CITY = (
        By.XPATH,
        "//input[contains(@name, 'permanent_city') or contains(@id, 'permanent_city')]"
        " | //label[contains(text(), 'City') or contains(text(), 'Town')]"
        "/..//input[not(@type='hidden')]"
    )

    PERM_PINCODE = (
        By.XPATH,
        "//input[contains(@name, 'permanent_pincode') or contains(@id, 'permanent_pincode')]"
        " | //label[contains(text(), 'Pincode') or contains(text(), 'PIN')]"
        "/..//input[not(@type='hidden')]"
    )

    # Dropdowns — State/District use Chosen.js on admin portal
    # Multiple ID patterns: the admin wizard may use state_id_chosen, state_chosen,
    # permanent_state_chosen, state_dropdown_chosen etc.
    PERM_STATE_CHOSEN = (
        By.XPATH,
        "//div[contains(@id, 'state') and contains(@id, 'chosen')]"
        " | //label[contains(text(), 'State')]/..//div[contains(@class, 'chosen-container')]"
        " | //label[contains(text(), 'State')]/..//span[contains(@class, 'select2')]"
    )
    PERM_STATE_SELECT = (
        By.XPATH,
        "//select[contains(@name, 'permanent_state') or contains(@id, 'permanent_state')"
        " or contains(@name, 'state_id') or contains(@id, 'state_id')]"
    )

    PERM_DISTRICT_CHOSEN = (
        By.XPATH,
        "//div[contains(@id, 'district') and contains(@id, 'chosen')]"
        " | //label[contains(text(), 'District')]/..//div[contains(@class, 'chosen-container')]"
        " | //label[contains(text(), 'District')]/..//span[contains(@class, 'select2')]"
    )
    PERM_DISTRICT_SELECT = (
        By.XPATH,
        "//select[contains(@name, 'permanent_district') or contains(@id, 'permanent_district')"
        " or contains(@name, 'district_id') or contains(@id, 'district_id')]"
    )

    # ═══════════════════════════════════════════════════════════════════════
    # CORRESPONDENCE ADDRESS
    # ═══════════════════════════════════════════════════════════════════════

    SAME_AS_PERMANENT_CHECKBOX = (
        By.XPATH,
        "//input[@type='checkbox' and (contains(@name, 'same_as') or contains(@id, 'same_as')"
        " or contains(@name, 'is_same') or contains(@id, 'is_same'))]"
        " | //label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'same as permanent')]"
        " | //label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'correspondence address is same')]"
    )

    CORR_HOUSE = (
        By.XPATH,
        "//input[contains(@name, 'correspondence_address1') or contains(@id, 'correspondence_address1')]"
    )
    CORR_STREET = (
        By.XPATH,
        "//input[contains(@name, 'correspondence_address2') or contains(@id, 'correspondence_address2')]"
    )
    CORR_CITY = (
        By.XPATH,
        "//input[contains(@name, 'correspondence_city') or contains(@id, 'correspondence_city')]"
    )
    CORR_STATE_SELECT = (
        By.XPATH,
        "//select[contains(@name, 'correspondence_state') or contains(@id, 'correspondence_state')]"
    )
    CORR_DISTRICT_SELECT = (
        By.XPATH,
        "//select[contains(@name, 'correspondence_district') or contains(@id, 'correspondence_district')]"
    )
    CORR_PINCODE = (
        By.XPATH,
        "//input[contains(@name, 'correspondence_pincode') or contains(@id, 'correspondence_pincode')]"
    )

    # ═══════════════════════════════════════════════════════════════════════
    # WIZARD NAVIGATION
    # ═══════════════════════════════════════════════════════════════════════
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(),'Next') or contains(text(),'Save & Next')]")
    BACK_BUTTON = (By.XPATH, "//button[contains(text(),'Back') or contains(text(),'Previous')]")

    # ── Validation ──
    VALIDATION_ERRORS = (By.CSS_SELECTOR, ".help-block, .invalid-feedback, .field-error, .text-danger")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success, .swal2-success")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WaitUtils(self.driver)

    # ═══════════════════════════════════════════════════════════════════════
    # PERMANENT ADDRESS
    # ═══════════════════════════════════════════════════════════════════════
    def enter_house(self, house_address):
        """Enter House/Building number for permanent address."""
        self.logger.info(f"Entering House/Building: {house_address}")
        self._safe_send_keys(self.PERM_HOUSE, house_address)

    def enter_street(self, street):
        """Enter Street/Locality for permanent address."""
        self.logger.info(f"Entering Street/Locality: {street}")
        self._safe_send_keys(self.PERM_STREET, street)

    def enter_city(self, city):
        """Enter City/Town for permanent address."""
        self.logger.info(f"Entering City: {city}")
        self._safe_send_keys(self.PERM_CITY, city)

    def enter_pincode(self, pincode):
        """Enter Pincode for permanent address."""
        self.logger.info(f"Entering Pincode: {pincode}")
        self._safe_send_keys(self.PERM_PINCODE, pincode)

    def select_state(self, state_name):
        """Select State from Chosen.js/Select2 dropdown (permanent address).
        Uses a 3-tier strategy: native select → Chosen UI → JS injection.
        """
        self.logger.info(f"Selecting State: {state_name}")
        if self._try_native_select(self.PERM_STATE_SELECT, state_name):
            return
        self._select_chosen_dropdown(self.PERM_STATE_CHOSEN, state_name)

    def select_district(self, district_name):
        """Select District from AJAX-loaded Chosen.js dropdown.
        Waits for district options to load after state selection.
        """
        self.logger.info(f"Selecting District: {district_name} (waiting for AJAX load)...")
        self._wait_for_district_load()
        if self._try_native_select(self.PERM_DISTRICT_SELECT, district_name):
            return
        self._select_chosen_dropdown(self.PERM_DISTRICT_CHOSEN, district_name)

    # ═══════════════════════════════════════════════════════════════════════
    # CORRESPONDENCE ADDRESS
    # ═══════════════════════════════════════════════════════════════════════
    def check_same_as_permanent(self):
        """Ticks the 'Same as permanent address' checkbox."""
        self.logger.info("Checking 'Same as Permanent Address' checkbox...")
        try:
            checkbox_els = self.driver.find_elements(*self.SAME_AS_PERMANENT_CHECKBOX)
            for el in checkbox_els:
                if el.tag_name == "input" and el.get_attribute("type") == "checkbox":
                    if not el.is_selected():
                        try:
                            el.click()
                        except Exception:
                            self.driver.execute_script("arguments[0].click();", el)
                    self.logger.info("Checkbox clicked successfully.")
                    time.sleep(1)
                    return
                elif el.tag_name == "label":
                    try:
                        el.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", el)
                    self.logger.info("Clicked label for same-as checkbox.")
                    time.sleep(1)
                    return
            self.logger.warning("Same-as checkbox element not found among matched elements.")
        except Exception as e:
            self.logger.warning(f"Could not click same-as-permanent checkbox: {e}")

    def fill_correspondence_address(self, house, street, city, state, district, pincode):
        """Fills separate correspondence address fields (used when NOT same as permanent)."""
        self.logger.info("Filling Correspondence Address (separate)...")
        self._safe_send_keys(self.CORR_HOUSE, house)
        self._safe_send_keys(self.CORR_STREET, street)
        self._safe_send_keys(self.CORR_CITY, city)
        self._try_native_select(self.CORR_STATE_SELECT, state)
        time.sleep(2)
        self._try_native_select(self.CORR_DISTRICT_SELECT, district)
        self._safe_send_keys(self.CORR_PINCODE, pincode)

    # ═══════════════════════════════════════════════════════════════════════
    # COMBINED FILL METHOD
    # ═══════════════════════════════════════════════════════════════════════
    def fill_address_step(self, house, street, state, district, pincode,
                          city=None, same_as_permanent=True,
                          corr_house=None, corr_street=None, corr_city=None,
                          corr_state=None, corr_district=None, corr_pincode=None):
        """
        Complete Step 3: Fill permanent address, optionally set correspondence.

        Args:
            house: House/Building number
            street: Street/Locality
            state: State name (for Chosen dropdown)
            district: District name (AJAX-loaded after state)
            pincode: 6-digit PIN code
            city: City/Town (optional, not all forms have it)
            same_as_permanent: If True, checks the 'same' checkbox
            corr_*: Correspondence address fields (used only if same_as_permanent=False)
        """
        self.logger.info("═══ STEP 3: Filling Address Details ═══")

        # Permanent Address
        self.enter_house(house)
        self.enter_street(street)
        if city:
            self.enter_city(city)
        self.select_state(state)
        self.select_district(district)
        self.enter_pincode(pincode)

        # Correspondence Address
        if same_as_permanent:
            self.check_same_as_permanent()
        elif corr_house:
            self.fill_correspondence_address(
                corr_house, corr_street or street,
                corr_city or city or "",
                corr_state or state,
                corr_district or district,
                corr_pincode or pincode,
            )

        self.logger.info("═══ Address Details filled ═══")

    # ═══════════════════════════════════════════════════════════════════════
    # WIZARD NAVIGATION
    # ═══════════════════════════════════════════════════════════════════════
    def click_next(self):
        """Click Next to proceed to Step 4 (Qualification Details)."""
        self.logger.info("Clicking Next on Address step...")
        time.sleep(1)  # Let any AJAX validation complete
        self.do_click(self.NEXT_BUTTON)
        time.sleep(2)

    def click_back(self):
        """Click Back to return to Step 2 (User Credentials)."""
        self.logger.info("Clicking Back on Address step...")
        self.do_click(self.BACK_BUTTON)
        time.sleep(2)

    # ═══════════════════════════════════════════════════════════════════════
    # VALIDATION CHECKS
    # ═══════════════════════════════════════════════════════════════════════
    def get_validation_errors(self):
        """Returns list of visible validation error messages."""
        errors = self.driver.find_elements(*self.VALIDATION_ERRORS)
        return [e.text.strip() for e in errors if e.is_displayed() and e.text.strip()]

    def has_validation_errors(self):
        """Returns True if any validation errors are shown."""
        return len(self.get_validation_errors()) > 0

    def is_on_address_step(self):
        """Returns True if the wizard is currently on the Address Details step."""
        try:
            tab = self.driver.find_element(*self.STEP_TAB)
            classes = tab.get_attribute("class") or ""
            parent_classes = tab.find_element(By.XPATH, "..").get_attribute("class") or ""
            return "active" in classes.lower() or "active" in parent_classes.lower()
        except Exception:
            # Fallback: check page content
            body = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            return "address details" in body and ("house" in body or "building" in body or "street" in body)

    # ═══════════════════════════════════════════════════════════════════════
    # PRIVATE HELPERS
    # ═══════════════════════════════════════════════════════════════════════
    def _safe_send_keys(self, locator, text):
        """Sends keys with multiple fallback strategies."""
        try:
            self.do_send_keys(locator, text)
        except Exception as e:
            self.logger.warning(f"Standard send_keys failed for {locator}: {e}")
            try:
                el = self.driver.find_element(*locator)
                self.driver.execute_script(
                    "arguments[0].value = arguments[1];"
                    "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));"
                    "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
                    el, text
                )
            except Exception as js_e:
                self.logger.error(f"JS fallback also failed: {js_e}")

    def _try_native_select(self, select_locator, option_text):
        """Attempts to select from a native <select> element. Returns True on success."""
        try:
            elements = self.driver.find_elements(*select_locator)
            for el in elements:
                if el.tag_name.lower() == "select":
                    # Unhide if Chosen.js has hidden it
                    if not el.is_displayed():
                        self.driver.execute_script(
                            "arguments[0].style.display = 'block';"
                            "arguments[0].style.visibility = 'visible';"
                            "arguments[0].style.opacity = '1';",
                            el
                        )
                        time.sleep(0.3)

                    select = Select(el)

                    # Wait for options to populate
                    if len(select.options) <= 1:
                        time.sleep(2)
                        select = Select(self.driver.find_element(*select_locator))

                    # Try exact match first
                    try:
                        select.select_by_visible_text(option_text)
                    except Exception:
                        # Case-insensitive partial match
                        matched = False
                        for opt in select.options:
                            if option_text.lower() in opt.text.lower():
                                select.select_by_visible_text(opt.text)
                                matched = True
                                break
                        if not matched:
                            return False

                    # Fire change event for AJAX
                    self.driver.execute_script(
                        "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));"
                        "try { $(arguments[0]).trigger('chosen:updated').trigger('change'); } catch(e) {}",
                        el
                    )
                    self.logger.info(f"Selected '{option_text}' via native select")
                    time.sleep(1)
                    return True
        except Exception as e:
            self.logger.warning(f"Native select failed: {e}")
        return False

    def _select_chosen_dropdown(self, chosen_locator, option_text):
        """Selects from a Chosen.js/Select2 dropdown via UI interaction."""
        try:
            elements = self.driver.find_elements(*chosen_locator)
            clicked = False
            for el in elements:
                if el.is_displayed():
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                        time.sleep(0.3)
                        el.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", el)
                    clicked = True
                    break

            if not clicked and elements:
                self.driver.execute_script("arguments[0].click();", elements[0])

            time.sleep(1)

            # Type into search field
            self.driver.implicitly_wait(0)
            search_inputs = self.driver.find_elements(
                By.XPATH,
                "//input[contains(@class, 'chosen-search-input')"
                " or contains(@class, 'select2-search__field')"
                " or @type='search']"
            )
            for inp in search_inputs:
                if inp.is_displayed():
                    inp.clear()
                    inp.send_keys(option_text)
                    time.sleep(1)
                    break

            # Click matching option
            option_xpath = (
                f"//li[contains(@class, 'active-result') and contains("
                f"translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                f"'{option_text.lower()}')]"
                f" | //li[contains(@class, 'select2-results__option') and contains("
                f"translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                f"'{option_text.lower()}')]"
            )
            opts = self.driver.find_elements(By.XPATH, option_xpath)
            displayed = [o for o in opts if o.is_displayed()]
            if displayed:
                try:
                    displayed[0].click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", displayed[0])
                self.logger.info(f"Selected '{option_text}' from Chosen/Select2 dropdown")
            else:
                # Press Enter as fallback
                from selenium.webdriver.common.keys import Keys
                for inp in search_inputs:
                    if inp.is_displayed():
                        inp.send_keys(Keys.ENTER)
                        break
                self.logger.warning(f"No matching option found for '{option_text}', tried Enter key")

            self.driver.implicitly_wait(10)
            time.sleep(0.5)

        except Exception as e:
            self.driver.implicitly_wait(10)
            self.logger.error(f"Chosen dropdown selection failed for '{option_text}': {e}")

    def _wait_for_district_load(self, max_wait=5):
        """Waits for the district dropdown to be populated after state selection (AJAX)."""
        self.logger.info("Waiting for district dropdown to load...")
        start = time.time()
        while time.time() - start < max_wait:
            try:
                district_selects = self.driver.find_elements(*self.PERM_DISTRICT_SELECT)
                for sel in district_selects:
                    if sel.tag_name.lower() == "select":
                        options = sel.find_elements(By.TAG_NAME, "option")
                        if len(options) > 1:
                            self.logger.info(f"District dropdown loaded with {len(options)} options")
                            return
            except Exception:
                pass
            time.sleep(0.5)
        self.logger.warning(f"District dropdown may not have loaded after {max_wait}s")
