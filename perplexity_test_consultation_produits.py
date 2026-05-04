import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TestPerplexity(unittest.TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    def tearDown(self):
        self.driver.quit()

    def test_product_flow(self):
        # Logic from Perplexity script
        self.driver.get("https://www.demoblaze.com/index.html")
        
        # Select product
        product_links_locator = (By.XPATH, "//tbody/tr/td/a[not(contains(@class, 'pull'))]")
        product_links = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located(product_links_locator)
        )
        
        selected_product_name = product_links[0].text.strip()
        product_links[0].click()
        
        # Verify
        detail_name = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "name"))
        ).text.strip()
        
        self.assertEqual(selected_product_name.lower(), detail_name.lower(), "Mismatch!")

if __name__ == "__main__":
    unittest.main()