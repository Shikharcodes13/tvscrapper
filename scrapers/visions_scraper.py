from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import SELENIUM_CONFIG, RETAILER_URLS
import logging
import random
import time
from config import DELAY  # Make sure this import exists
logger = logging.getLogger(__name__)

def scrape_visions(product_name, driver):
    result = {"Website": "Visions", "Title": "", "Price": "", "URL": "", "error": None}
    
    try:
        url = RETAILER_URLS["visions"].format(query=product_name.replace(" ", "%20"))
        driver.get(url)
        
        product = WebDriverWait(driver, SELENIUM_CONFIG["timeout"]).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-item"))
        )
        
        result["Title"] = product.find_element(By.CSS_SELECTOR, "h2.product-name").text
        result["Price"] = product.find_element(By.CSS_SELECTOR, "span.price").text
        result["URL"] = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        
    except Exception as e:
        result["error"] = f"Visions error: {str(e)}"
        logger.error(result["error"])
    
    time.sleep(random.uniform(*DELAY))
    return result