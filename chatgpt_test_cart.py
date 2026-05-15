from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup driver
service = Service("C:\\edgedriver\\msedgedriver.exe")
driver = webdriver.Edge(service=service)
driver.maximize_window()

wait = WebDriverWait(driver, 10)

# Accéder au site
driver.get("https://www.demoblaze.com/index.html")

print("✅ Site ouvert")

# ==============================
# 🧪 TEST 1 : Ajouter produit
# ==============================
def test_add_product():
    print("🔹 Test: Ajouter produit")

    # Cliquer sur premier produit
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Samsung galaxy s6')]"))).click()

    # Cliquer Add to cart
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Add to cart']"))).click()

    # Gérer alert
    wait.until(EC.alert_is_present())
    alert = Alert(driver)
    print("Alert:", alert.text)
    alert.accept()

    time.sleep(2)

# ==============================
# 🧪 TEST 2 : Ajouter plusieurs produits
# ==============================
def test_add_multiple_products():
    print("🔹 Test: Ajouter plusieurs produits")

    driver.get("https://www.demoblaze.com/index.html")

    products = ["Nokia lumia 1520", "Nexus 6"]

    for product in products:
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, product))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Add to cart']"))).click()

        wait.until(EC.alert_is_present())
        Alert(driver).accept()

        driver.get("https://www.demoblaze.com/index.html")
        time.sleep(2)

# ==============================
# 🧪 TEST 3 : Vérifier panier + total
# ==============================
def test_cart_total():
    print("🔹 Test: Vérifier total panier")

    driver.find_element(By.ID, "cartur").click()

    time.sleep(3)

    total = driver.find_element(By.ID, "totalp").text
    print("💰 Total affiché:", total)

# ==============================
# 🧪 TEST 4 : Supprimer produit
# ==============================
def test_delete_product():
    print("🔹 Test: Supprimer produit")

    # ✅ Aller directement au panier
    driver.get("https://www.demoblaze.com/cart.html")

    wait.until(EC.presence_of_element_located((By.ID, "tbodyid")))

    time.sleep(3)

    delete_btns = driver.find_elements(By.LINK_TEXT, "Delete")

    if delete_btns:
        delete_btns[0].click()
        print("🗑 Produit supprimé")
    else:
        print("⚠ Aucun produit à supprimer")

    time.sleep(2)
# ==============================
# 🧪 TEST 5 : Modifier quantité (BUG attendu)
# ==============================
def test_modify_quantity():
    print("🔹 Test: Modifier quantité (Edge Case)")

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cart"))).click()
    time.sleep(3)

    rows = driver.find_elements(By.XPATH, "//tr[@class='success']")

    if len(rows) > 0:
        print("⚠ Impossible de modifier la quantité → fonctionnalité absente")
        print("👉 BUG détecté : Pas de gestion quantité")
    else:
        print("Panier vide")

# ==============================
# 🧪 TEST PERFORMANCE : Temps de réponse
# ==============================
def test_performance_add_to_cart():
    print("🔹 Test Performance : Temps de réponse Add to cart")

    driver.get("https://www.demoblaze.com/index.html")

    wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Samsung galaxy s6")
        )
    ).click()

    # Début chronométrage
    start_time = time.time()

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[text()='Add to cart']")
        )
    ).click()

    wait.until(EC.alert_is_present())

    end_time = time.time()

    response_time = round(end_time - start_time, 2)

    alert = Alert(driver)
    alert.accept()

    print(f"⏱ Temps de réponse : {response_time} secondes")

    if response_time < 2:
        print("✅ TEST PERFORMANCE PASSÉ")
    else:
        print("❌ TEST PERFORMANCE ÉCHOUÉ")


# ==============================
# 🧪 TEST SECURITE : Sans authentification
# ==============================
def test_security_without_login():
    print("🔹 Test Sécurité : Ajout panier sans authentification")

    # Vérifier que l'utilisateur n'est pas connecté
    driver.get("https://www.demoblaze.com/index.html")

    wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Nokia lumia 1520")
        )
    ).click()

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[text()='Add to cart']")
        )
    ).click()

    wait.until(EC.alert_is_present())

    alert = Alert(driver)

    print("⚠ Message reçu :", alert.text)

    # Demoblaze accepte même sans login
    print("❌ FAIL : Produit ajouté sans authentification")

    alert.accept()

    time.sleep(2)

# ==============================
# ▶️ EXECUTION
# ==============================

test_add_product()
test_add_multiple_products()
test_cart_total()
test_delete_product()
test_modify_quantity()
test_performance_add_to_cart()
test_security_without_login()

print("✅ Tests terminés")

# driver.quit()