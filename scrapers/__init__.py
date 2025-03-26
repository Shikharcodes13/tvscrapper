# Import all scrapers
from .amazon_scraper import scrape_amazon
from .bestbuy_scraper import scrape_bestbuy
from .costco_scraper import scrape_costco
from .staples_scraper import scrape_staples
from .visions_scraper import scrape_visions
from .londondrugs_scraper import scrape_londondrugs
from .canadiantire_scraper import scrape_canadiantire
from .dufresne_scraper import scrape_dufresne
from .tanguay_scraper import scrape_tanguay
from .teppermans_scraper import scrape_teppermans
from .lg_scraper import scrape_lg
from .samsung_scraper import scrape_samsung

__all__ = [
    'scrape_amazon',
    'scrape_bestbuy',
    'scrape_costco',
    'scrape_staples',
    'scrape_visions',
    'scrape_londondrugs',
    'scrape_canadiantire',
    'scrape_dufresne',
    'scrape_tanguay',
    'scrape_teppermans',
    'scrape_lg',
    'scrape_samsung'
]