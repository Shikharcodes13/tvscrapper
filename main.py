from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from scrapers.amazon_scraper import scrape_amazon
from scrapers.bestbuy_scraper import scrape_bestbuy
from scrapers.costco_scraper import scrape_costco
from scrapers.staples_scraper import scrape_staples
from scrapers.visions_scraper import scrape_visions
from scrapers.londondrugs_scraper import scrape_londondrugs 
from scrapers.canadiantire_scraper import scrape_canadiantire
from scrapers.dufresne_scraper import scrape_dufresne
from scrapers.tanguay_scraper import scrape_tanguay
from scrapers.teppermans_scraper import scrape_teppermans
from scrapers.lg_scraper import scrape_lg
from scrapers.samsung_scraper import scrape_samsung

from config import SELENIUM_CONFIG, DELAY
import json
import time
import random

def get_driver():
    options = Options()
    if SELENIUM_CONFIG["headless"]:
        options.add_argument("--headless")
    options.add_argument(f"--window-size={SELENIUM_CONFIG['window_size']}")
    if SELENIUM_CONFIG["disable_images"]:
        options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument(f"user-agent={SELENIUM_CONFIG['user_agent']}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def main():
    products = [
        { "name": "Hisense 50\" 4K Smart Google AI Upscaler LED TV - 50A68N" },
        { "name": "Hisense 55\" 4K Smart Google AI Upscaler LED TV - 55A68N" },
        { "name": "Samsung 75\u201d 4K Tizen Smart CUHD TV - UN75DU7100FXZC" },
        { "name": "LG 50\" UHD 4K Smart LED TV - 50UT7570PUB" },
        { "name": "Samsung 65\u201d 4K Tizen Smart QLED TV - QN65Q60DAFXZC" },
        { "name": "Hisense 32\" HD Smart VIDAA LED TV - 32A4KV" },
        { "name": "Samsung 43\u201d 4K Tizen Smart CUHD TV-UN43DU7100FXZC" },
        { "name": "LG 65\" UHD 4K Smart LED TV - 65UT7570PUB" },
        { "name": "Samsung 75\u201d 4K Tizen Smart QLED TV - QN75Q60DAFXZC" },
        { "name": "Samsung 65\u201d Neo QLED 4K Tizen Smart TV QN85D - QN65QN85DBFXZC" },
        { "name": "LG 65\" 4K Smart evo C4 OLED TV - OLED65C4PUA" },
        { "name": "LG 86\" UHD 4K Smart LED TV - 86UT7590PUA" },
        { "name": "SONY 75\" X77L 4K HDR LED TV Google TV - KD75X77L" },
        { "name": "LG 55\" QNED80 4K Smart QLED TV - 55QNED80TUC" },
        { "name": "Samsung 65\u201d OLED 4K Tizen Smart TV S90D - QN65S90DAFXZC" },
        { "name": "Samsung 75\u201d 4K Tizen Smart QLED TV - QN75Q80DAFXZC" },
        { "name": "Samsung 65\u201d 4K Tizen Smart QLED TV - QN65Q80DAFXZC" },
        { "name": "Samsung 65\u201d 4K Tizen Smart CUHD TV - UN65DU7100FXZC" },
        { "name": "Samsung 75\u201d 4K Tizen Smart CUHD TV - UN75DU8000FXZC" }, 
    ]
    
    results = []
    driver = get_driver()
    
    try:
        for product in products:
            product_result = {
                "product": product["name"],
                "retailers": []
            }
            
            scrapers = [
                ("Amazon", scrape_amazon),
                ("Best Buy", scrape_bestbuy),
                ("Costco", scrape_costco),
                ("Staples", scrape_staples),
                ("Visions", scrape_visions),
                ("London Drugs", scrape_londondrugs),
                ("Canadian Tire", scrape_canadiantire),
                ("Dufresne", scrape_dufresne),
                ("Tanguay", scrape_tanguay),
                ("Teppermans", scrape_teppermans),
                ("LG", scrape_lg),
                ("Samsung", scrape_samsung)
            ]
            
            for retailer_name, scraper in scrapers:
                try:
                    print(f"Scraping {retailer_name} for {product['name']}")
                    result = scraper(product["name"], driver)
                    product_result["retailers"].append({
                        "retailer": retailer_name,
                        "data": result
                    })
                    time.sleep(random.uniform(*DELAY))
                except Exception as e:
                    print(f"Error scraping {retailer_name}: {str(e)}")
            
            results.append(product_result)
    
    finally:
        driver.quit()
    
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()