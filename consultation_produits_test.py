import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestDemoblaze(unittest.TestCase):

    def setUp(self):
        # Initialize Chrome
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.demoblaze.com/index.html")
        self.wait = WebDriverWait(self.driver, 10)
        print("\n--- Setup: Browser started and Demoblaze loaded ---")

    def tearDown(self):
        print("--- Teardown: Closing browser ---")
        self.driver.quit()

    def test_navigation_catalogue(self):
        print("Test 1: Testing Category Navigation...")
        # Test Laptops Category
        laptop_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Laptops")))
        laptop_link.click()
        print(" -> Clicked Laptops")
        
        # Verify
        self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Sony vaio i5")))
        print(" -> Successfully navigated to Laptops")

    def test_consultation_detail_produit(self):
        print("Test 2: Testing Product Detail and Navigation...")
        # 1. Click on the first product
        first_product = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.hrefch")))
        product_name_on_home = first_product.text
        first_product.click()
        print(f" -> Selected product: {product_name_on_home}")

        # 2. Verify details page
        name_on_detail_page = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "name"))).text
        self.assertEqual(product_name_on_home, name_on_detail_page, "Product names do not match!")
        print(" -> Verified product details")

        # 3. Navigate back to Home
        home_link = self.wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Home")))
        home_link.click()
        print(" -> Navigated back to Home")
        self.wait.until(EC.url_contains("index.html"))

    def test_pagination_navigation(self):
        print("Test 3: Testing Pagination...")
        # 1. Scroll to the bottom
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # 2. Click "Next"
        next_button = self.wait.until(EC.element_to_be_clickable((By.ID, "next2")))
        next_button.click()
        print(" -> Clicked Next page")
        
        # 3. Verify we are on page 2
        self.wait.until(EC.element_to_be_clickable((By.ID, "prev2")))
        print(" -> Verified we reached page 2")
        
        # 4. Navigate back to page 1
        prev_button = self.driver.find_element(By.ID, "prev2")
        prev_button.click()
        print(" -> Clicked Previous page")
        
        # 5. Verify return to page 1
        self.wait.until(EC.element_to_be_clickable((By.ID, "next2")))
        print(" -> Verified return to page 1")

if __name__ == "__main__":
    unittest.main()