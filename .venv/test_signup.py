# ============================================================
# DEMOBLAZE - SIGNUP TESTS
# Selenium + Pytest
# Senior QA Automation Version
# ============================================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pytest
import time


# ============================================================
# FIXTURE
# ============================================================

@pytest.fixture
def driver():

    driver = webdriver.Chrome()

    driver.maximize_window()

    driver.get("https://www.demoblaze.com/index.html")

    yield driver

    driver.quit()


# ============================================================
# UTILITIES
# ============================================================

def open_signup_modal(driver):

    driver.find_element(By.ID, "signin2").click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "sign-username"))
    )


def signup(driver, username, password):

    username_input = driver.find_element(By.ID, "sign-username")
    password_input = driver.find_element(By.ID, "sign-password")

    username_input.clear()
    password_input.clear()

    username_input.send_keys(username)
    password_input.send_keys(password)

    signup_button = driver.find_element(
        By.XPATH,
        "//button[text()='Sign up']"
    )

    signup_button.click()


def get_alert_text(driver):

    alert = WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )

    text = alert.text

    alert.accept()

    return text


# ============================================================
# TF-01
# Signup avec données valides
# ============================================================

def test_TF01_signup_valid_data(driver):

    open_signup_modal(driver)

    unique_user = f"user_{int(time.time())}"

    signup(driver, unique_user, "Password123")

    alert_text = get_alert_text(driver)

    assert alert_text == "Sign up successful."


# ============================================================
# TF-02
# Username déjà existant
# ============================================================

def test_TF02_existing_username(driver):

    open_signup_modal(driver)

    signup(driver, "existinguser", "Password123")

    alert_text = get_alert_text(driver)

    assert "This user already exist" in alert_text


# ============================================================
# TF-03
# Username et Password vides
# ============================================================

def test_TF03_empty_fields(driver):

    open_signup_modal(driver)

    signup(driver, "", "")

    alert_text = get_alert_text(driver)

    assert alert_text == "Please fill out Username and Password."


# ============================================================
# TF-04
# Signup avec espaces uniquement
# ============================================================

def test_TF04_spaces_only(driver):

    open_signup_modal(driver)

    signup(driver, "     ", "     ")

    try:

        alert_text = get_alert_text(driver)

        # comportement attendu
        assert alert_text == "Please fill out Username and Password."

    except TimeoutException:

        pytest.fail(
            "BUG DETECTED: Application accepted spaces-only input."
        )


# ============================================================
# TF-05
# Données invalides
# ============================================================

def test_TF05_invalid_data(driver):

    open_signup_modal(driver)

    signup(driver, "testUser", "12")

    try:

        alert_text = get_alert_text(driver)

        # comportement attendu
        assert "invalid" in alert_text.lower()

    except TimeoutException:

        pytest.fail(
            "BUG DETECTED: Invalid password accepted without validation."
        )
# ============================================================
# TF-06
# Temps de réponse après soumission Signup
# ============================================================

def test_TF06_signup_response_time(driver):

    open_signup_modal(driver)

    unique_user = f"user_perf_{int(time.time())}"

    start_time = time.time()

    signup(driver, unique_user, "Password123")

    get_alert_text(driver)

    end_time = time.time()

    response_time = end_time - start_time

    print(f"\nResponse Time: {response_time:.2f} seconds")

    # seuil acceptable : 5 secondes
    assert response_time < 5, (
        f"Performance issue: response time too high "
        f"({response_time:.2f}s)"
    )


# ============================================================
# TF-07
# Injection XSS dans username
# ============================================================

def test_TF07_xss_injection_signup(driver):

    open_signup_modal(driver)

    xss_payload = "<script>alert(1)</script>"

    signup(driver, xss_payload, "Password123")

    try:

        alert_text = get_alert_text(driver)

        print(f"\nApplication Response: {alert_text}")

        # Si le système accepte le payload :
        # vulnérabilité potentielle

        assert "Sign up successful" not in alert_text, (
            "SECURITY BUG: XSS payload accepted during signup."
        )

    except TimeoutException:

        # Aucun alert système = comportement potentiellement sécurisé
        pass

    # Vérification supplémentaire :
    # s'assurer qu'aucune popup JS inattendue n'apparaît

    try:

        browser_alert = driver.switch_to.alert

        unexpected_alert = browser_alert.text

        browser_alert.accept()

        pytest.fail(
            f"XSS Vulnerability Detected! "
            f"Unexpected JS Alert Triggered: {unexpected_alert}"
        )

    except:

        # Aucun alert JS déclenché
        assert True