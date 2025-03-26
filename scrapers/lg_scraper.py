import requests
from bs4 import BeautifulSoup
from config import HEADERS, TIMEOUT
import logging

logger = logging.getLogger(__name__)

def scrape_lg(product_name):
    result = {
        "Website": "LG",
        "Title": "",
        "Price": "",
        "PriceValidTill": "",
        "error": None
    }
    
    try:
        # Updated LG search URL
        query = product_name.replace(" ", "%20")
        url = f"https://www.lg.com/ca_en/search/ajax?query={query}"
        
        response = requests.get(url, headers=HEADERS["default"], timeout=TIMEOUT)
        
        if response.status_code == 404:
            # Fallback to main search page
            url = f"https://www.lg.com/ca_en/search?searchValue={query}"
            response = requests.get(url, headers=HEADERS["default"], timeout=TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            product = soup.find("div", class_="product-item")
        else:
            response.raise_for_status()
            data = response.json()
            if not data.get("products"):
                raise Exception("No products found in search results")
            product = data["products"][0]
        
        if isinstance(product, dict):
            # JSON response case
            result["Title"] = product.get("name", "")
            result["Price"] = product.get("price", "")
        else:
            # HTML response case
            title = product.find("h4", class_="product-title")
            price = product.find("span", class_="price")
            if title:
                result["Title"] = title.text.strip()
            if price:
                result["Price"] = price.text.strip()
        
        if not result["Title"] or not result["Price"]:
            raise Exception("Could not extract complete product details")
            
    except Exception as e:
        result["error"] = f"LG scraping failed: {str(e)}"
        logger.error(result["error"])
    
    return result