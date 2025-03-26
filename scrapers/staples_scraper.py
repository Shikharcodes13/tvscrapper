from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import SELENIUM_CONFIG, RETAILER_URLS
import logging
import random
import time
from config import DELAY  # Make sure this import exists

logger = logging.getLogger(__name__)

def scrape_staples(product_name, driver):
    result = {"Website": "Staples", "Title": "", "Price": "", "URL": "", "error": None}
    
    try:
        url = RETAILER_URLS["staples"].format(query=product_name.replace(" ", "+"))
        driver.get(url)
        
        # Staples often has bot protection
        if "access denied" in driver.page_source.lower():
            raise Exception("Blocked by bot protection")
        
        product = WebDriverWait(driver, SELENIUM_CONFIG["timeout"]).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-card"))
        )
        
        result["Title"] = product.find_element(By.CSS_SELECTOR, "h3.product-title").text
        result["Price"] = product.find_element(By.CSS_SELECTOR, "span.price").text
        result["URL"] = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        
    except Exception as e:
        result["error"] = f"Staples error: {str(e)}"
        logger.error(result["error"])
    
    time.sleep(random.uniform(*DELAY))
    return result