from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import SELENIUM_CONFIG, RETAILER_URLS
import logging
import random
import time
from config import DELAY  # Make sure this import exists

logger = logging.getLogger(__name__)

def scrape_amazon(product_name, driver):
    result = {"Website": "Amazon", "Title": "", "Price": "", "URL": "", "error": None}
    
    try:
        url = RETAILER_URLS["amazon"].format(query=product_name.replace(" ", "+"))
        driver.get(url)
        
        # Handle captcha if present
        if "captcha" in driver.page_source.lower():
            raise Exception("CAPTCHA detected")
        
        product = WebDriverWait(driver, SELENIUM_CONFIG["timeout"]).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']"))
        )
        
        result["Title"] = product.find_element(By.CSS_SELECTOR, "h2 a span").text
        price_whole = product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
        price_fraction = product.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
        result["Price"] = f"${price_whole}{price_fraction}"
        result["URL"] = product.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
        
    except Exception as e:
        result["error"] = f"Amazon error: {str(e)}"
        logger.error(result["error"])
    
    time.sleep(random.uniform(*DELAY))
    return result