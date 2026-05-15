import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =========================
# FIXTURE DRIVER
# =========================
@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    yield driver
    driver.quit()


# =========================
# PAGE OBJECT MODEL
# =========================
class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators
        self.login_link = (By.ID, "login2")
        self.username = (By.ID, "loginusername")
        self.password = (By.ID, "loginpassword")
        self.login_btn = (By.XPATH, "//button[text()='Log in']")
        self.logged_user = (By.ID, "nameofuser")

    def open(self):
        self.driver.get("https://www.demoblaze.com/index.html")

    def open_login_modal(self):
        self.driver.find_element(*self.login_link).click()

    def login(self, username, password):
        self.wait.until(EC.visibility_of_element_located(self.username)).clear()
        self.driver.find_element(*self.username).send_keys(username)

        self.driver.find_element(*self.password).clear()
        self.driver.find_element(*self.password).send_keys(password)

        self.driver.find_element(*self.login_btn).click()

    def get_logged_user_text(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.logged_user)
        ).text


# =========================
# TF-01 : LOGIN VALIDE
# =========================
def test_valid_login(driver):
    page = LoginPage(driver)
    page.open()
    page.open_login_modal()

    page.login("intissar m", "123aze")

    assert "Welcome" in page.get_logged_user_text()


# =========================
# TF-02 : MAUVAIS PASSWORD
# =========================
def test_wrong_password(driver):
    page = LoginPage(driver)
    page.open()
    page.open_login_modal()

    page.login("intissar ma", "wrong_pass")

    # attendre l'apparition de l'alert
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())

    assert "Wrong password" in alert.text
    alert.accept()

# =========================
# TF-03 : CHAMPS VIDES
# =========================
def test_empty_fields(driver):
    page = LoginPage(driver)
    page.open()
    page.open_login_modal()

    page.login("", "")

    # attendre l'alert
    alert = WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )

    assert "Please fill out Username and Password" in alert.text
    alert.accept()



# =========================
# TF-04 : USER INEXISTANT
# =========================
def test_user_not_exist(driver):
    page = LoginPage(driver)
    page.open()
    page.open_login_modal()

    page.login("unknown_user_12345", "aze1235")

    # attendre l'alert
    alert = WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )

    assert "User does not exist" in alert.text


# =========================
# TS-01 : SESSION F5
# =========================
# =========================
# TS-01 : SESSION F5
# =========================
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def test_session_persistence(driver):

    # open website
    driver.get("https://www.demoblaze.com/index.html")

    # open login modal
    driver.find_element(By.ID, "login2").click()

    # wait modal visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginusername"))
    )

    # enter credentials
    driver.find_element(By.ID, "loginusername").send_keys("intissar ma")
    driver.find_element(By.ID, "loginpassword").send_keys("YOUR_PASSWORD")

    # click login
    driver.find_element(By.XPATH, "//button[text()='Log in']").click()

    # VERY IMPORTANT:
    # wait until modal disappears
    WebDriverWait(driver, 20).until(
        EC.invisibility_of_element_located((By.ID, "logInModal"))
    )

    # wait until welcome appears
    welcome = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "nameofuser"))
    )

    assert "Welcome" in welcome.text

    # wait extra time for cookie/session
    time.sleep(5)

    # refresh page
    driver.refresh()

    # wait after refresh
    welcome_after_refresh = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "nameofuser"))
    )

    assert "Welcome" in welcome_after_refresh.text

# =========================
# TP-01 : ROBUSTESSE LOGIN MULTIPLE FAILS
# =========================
def test_multiple_failed_login_attempts(driver):
    page = LoginPage(driver)
    page.open()

    for i in range(5):
        page.open_login_modal()
        page.login("valid_user", f"wrong_pass_{i}")

        alert = Alert(driver)
        assert (
            "Wrong password" in alert.text
            or "User does not exist" in alert.text
        )
        alert.accept()