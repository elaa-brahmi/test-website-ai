import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestChatGPT(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--incognito")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)

    def tearDown(self):
        self.driver.quit()

    def test_product_flow(self):
        self.driver.get("https://www.demoblaze.com/index.html")
        
        # 1. Capture the product
        products = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title")))
        product_element = products[0]
        home_name = product_element.text.strip()
        
        # 2. Click and Wait for URL change (Crucial for reliability!)
        product_element.click()
        
        # Instead of waiting for visibility, wait for the URL to change 
        # so we know the page has navigated
        self.wait.until(lambda d: "prod.html" in d.current_url)
        
        # 3. Use CSS_SELECTOR, which is safer than CLASS_NAME
        # The "." prefix is the standard CSS selector for a class
        detail_element = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".name")))
        detail_name = detail_element.text.strip()
        
        self.assertEqual(home_name, detail_name, "Data mismatch!")

if __name__ == "__main__":
    unittest.main()