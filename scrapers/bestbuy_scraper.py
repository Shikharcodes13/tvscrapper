from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import SELENIUM_CONFIG, RETAILER_URLS
import logging
import random
import time
from config import DELAY  # Make sure this import exists

logger = logging.getLogger(__name__)

def scrape_bestbuy(product_name, driver):
    result = {"Website": "Best Buy", "Title": "", "Price": "", "URL": "", "error": None}
    
    try:
        url = RETAILER_URLS["bestbuy"].format(query=product_name.replace(" ", "+"))
        driver.get(url)
        
        product = WebDriverWait(driver, SELENIUM_CONFIG["timeout"]).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.productItem"))
        )
        
        result["Title"] = product.find_element(By.CSS_SELECTOR, "div.productItemName").text
        result["Price"] = product.find_element(By.CSS_SELECTOR, "div.price_FHDfG").text
        result["URL"] = product.find_element(By.CSS_SELECTOR, "a.link_3hcyN").get_attribute("href")
        
    except Exception as e:
        result["error"] = f"Best Buy error: {str(e)}"
        logger.error(result["error"])
    
    time.sleep(random.uniform(*DELAY))
    return result