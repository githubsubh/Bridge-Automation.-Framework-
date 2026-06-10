import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from utilities.screenshot_utils import ScreenshotUtils

# ---------------------------------------------------------------------------
# Session-scoped URL fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def admin_url():
    """Admin portal base URL (login page)."""
    return os.getenv("ADMIN_URL", "https://bridge-uat-admin.nios.ac.in")


@pytest.fixture(scope="session")
def frontend_url():
    """Frontend portal base URL (teacher login)."""
    return os.getenv("FRONTEND_URL", "https://bridge-uat.nios.ac.in")

@pytest.fixture(scope="session")
def set_test_env():
    """Force non‑headless mode and skip CAPTCHA for automated runs."""
    os.environ["HEADLESS"] = "false"
    os.environ["SKIP_CAPTCHA"] = "true"


# ---------------------------------------------------------------------------
# Helper to create a Chrome WebDriver instance
# ---------------------------------------------------------------------------
def _create_driver():
    chrome_options = Options()
    # Run headless if the environment variable HEADLESS is set to "true"
    if os.getenv("HEADLESS", "false").lower() == "true":
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

    # Common stability options
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")

    # Set download directory to test_data for assignment downloads
    download_dir = os.path.abspath(os.path.join(os.getcwd(), "test_data", "downloads"))
    os.makedirs(download_dir, exist_ok=True)
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Use webdriver_manager to fetch a compatible ChromeDriver automatically
    from webdriver_manager.chrome import ChromeDriverManager
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver


# ---------------------------------------------------------------------------
# Generic setup fixture — used by most test classes via `setup` parameter
# ---------------------------------------------------------------------------
@pytest.fixture(scope="function")
def setup():
    """Generic browser setup fixture. Returns driver, quits after test."""
    driver = _create_driver()
    yield driver
    driver.quit()


# ---------------------------------------------------------------------------
# Login fixtures – each returns the driver instance and injects credentials
# ---------------------------------------------------------------------------
@pytest.fixture(scope="function")
def admin_login():
    driver = _create_driver()
    # Attach credential attributes expected by the test helpers
    driver.username = os.getenv("ADMIN_USER", "superadmin")
    driver.password = os.getenv("ADMIN_PASS", "Admin@2025")
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def teacher_login():
    driver = _create_driver()
    driver.username = os.getenv("TEACHER_USER", "subh7409+234@gmail.com")
    driver.password = os.getenv("TEACHER_PASS", "Password@12")
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def student_login():
    driver = _create_driver()
    driver.username = os.getenv("STUDENT_USER", "subh7409+234@gmail.com")
    driver.password = os.getenv("STUDENT_PASS", "Password@12")
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def sme_login():
    driver = _create_driver()
    driver.username = os.getenv("SME_USER", "sme@example.com")
    driver.password = os.getenv("SME_PASS", "sme123")
    yield driver
    driver.quit()

# ---------------------------------------------------------------------------
# Simple configuration fixture for wait/simulation
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def wait_config():
    """Configuration used by the workflow test.
    assignment_wait_days – how many days to simulate (default 2)
    seconds_per_day – conversion factor; set higher for faster runs.
    """
    return {
        "assignment_wait_days": int(os.getenv("ASSIGNMENT_WAIT_DAYS", "2")),
        "seconds_per_day": int(os.getenv("SECONDS_PER_DAY", "1")),
    }


# ---------------------------------------------------------------------------
# Pytest hooks for screenshot-on-failure and reporting
# ---------------------------------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot when a test fails."""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = None
        # Try to get driver from the test's fixture
        if "setup" in item.funcargs:
            driver = item.funcargs["setup"]
        elif "admin_login" in item.funcargs:
            driver = item.funcargs["admin_login"]
        elif "student_login" in item.funcargs:
            driver = item.funcargs["student_login"]
        elif "teacher_login" in item.funcargs:
            driver = item.funcargs["teacher_login"]
        elif "sme_login" in item.funcargs:
            driver = item.funcargs["sme_login"]

        if driver:
            test_name = item.name.replace(" ", "_")
            ScreenshotUtils.capture_screenshot(driver, f"FAIL_{test_name}")
