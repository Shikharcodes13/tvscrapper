import requests
from config import HEADERS
from utils.error_logger import log_error
import time
import random

def scrape_bestbuy(product_name, max_retries=3):
    """Scrape Best Buy using their internal API with improved product matching"""
    for attempt in range(max_retries):
        try:
            # Prepare search parameters
            search_term = product_name.replace(' ', '%20')
            url = f"https://www.bestbuy.ca/api/v2/json/search?query={search_term}&page=1&pageSize=5"
            
            # Configure headers to mimic browser request
            request_headers = {
                **HEADERS,
                "Accept": "application/json",
                "Referer": "https://www.bestbuy.ca/en-ca",
                "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"'
            }
            
            # Add random delay
            time.sleep(random.uniform(1, 3))
            
            # Make API request
            response = requests.get(url, headers=request_headers, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('products'):
                log_error("BestBuyAPI", product_name, "No products in API response")
                continue  # Try again
                
            # Improved product matching logic
            model_number = extract_model_number(product_name)
            for product in data['products']:
                if (model_number and model_number.lower() in product['name'].lower()) or \
                   (product_name.lower() in product['name'].lower()):
                    return format_product_data(product)
            
            # If no exact match, return the first product with price
            for product in data['products']:
                if product.get('salePrice'):
                    return format_product_data(product)
            
            return {"error": "No matching products with prices found"}
            
        except requests.exceptions.RequestException as e:
            log_error("BestBuyAPI", product_name, f"Request failed: {str(e)}")
            if attempt == max_retries - 1:
                return {"error": f"API request failed after {max_retries} attempts"}
        except Exception as e:
            log_error("BestBuyAPI", product_name, str(e))
            return {"error": str(e)}
    
    return {"error": "No products found after retries"}

def extract_model_number(product_name):
    """Extract model number from product name (e.g., 50A68N)"""
    parts = product_name.split('-')
    return parts[-1].strip() if len(parts) > 1 else None

def format_product_data(product):
    """Format product data into our standard structure"""
    return {
        "Website": "Best Buy",
        "Title": product['name'],
        "Price": f"${product['salePrice']:.2f}",
        "PriceValidTill": product.get('priceExpiry', '')
    }