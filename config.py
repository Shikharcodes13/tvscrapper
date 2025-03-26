# config.py
import logging
from fake_useragent import UserAgent

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Timing Configuration
DELAY = (1, 3)  # Random delay range between requests in seconds
RETRIES = 3     # Number of retry attempts for failed scrapes

# Selenium Settings
SELENIUM_CONFIG = {
    "timeout": 30,          # Seconds to wait for elements
    "headless": True,       # Run browser in headless mode
    "disable_images": True, # Disable images for faster loading
    "window_size": "1920,1080",
    "user_agent": UserAgent().random
}

# Retailer URLs
RETAILER_URLS = {
    "amazon": "https://www.amazon.ca/s?k={query}",
    "bestbuy": "https://www.bestbuy.ca/en-ca/search?search={query}",
    "costco": "https://www.costco.ca/CatalogSearch?dept=All&keyword={query}",
    "staples": "https://www.staples.ca/collections/search?q={query}",
    "visions": "https://www.visions.ca/search-results?keywords={query}",
    "londondrugs": "https://www.londondrugs.com/search/?text={query}",
    "canadiantire": "https://www.canadiantire.ca/en/search-results.html?q={query}",
    "dufresne": "https://www.dufresne.ca/search?q={query}",
    "tanguay": "https://www.tanguay.ca/en/search?controller=search&s={query}",
    "teppermans": "https://www.teppermans.com/search?q={query}",
    "lg": "https://www.lg.com/ca_en/search?q={query}",
    "samsung": "https://www.samsung.com/ca/search/?searchvalue={query}"
}

# Proxy Configuration (if needed)
PROXY_LIST = []  # Add your proxies here if using
USE_PROXY = False