"""
Core scraper module for Amazon product scraping
"""

import time
import random
import logging
import re
import requests
import json
import csv
from difflib import SequenceMatcher
from pathlib import Path

# Imports Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Country-to-domain mapping for Amazon
AMAZON_SITES = {
    'FR': {'domain': 'amazon.fr', 'locale': 'fr_FR', 'currency': '€'},
    'DE': {'domain': 'amazon.de', 'locale': 'de_DE', 'currency': '€'},
    'IT': {'domain': 'amazon.it', 'locale': 'it_IT', 'currency': '€'},
    'ES': {'domain': 'amazon.es', 'locale': 'es_ES', 'currency': '€'},
    'GB': {'domain': 'amazon.co.uk', 'locale': 'en_GB', 'currency': '£'},
    'US': {'domain': 'amazon.com', 'locale': 'en_US', 'currency': '$'},
    'CA': {'domain': 'amazon.ca', 'locale': 'en_CA', 'currency': '$'},
    'BR': {'domain': 'amazon.com.br', 'locale': 'pt_BR', 'currency': 'R$'},
    'JP': {'domain': 'amazon.co.jp', 'locale': 'ja_JP', 'currency': '¥'},
    'IN': {'domain': 'amazon.in', 'locale': 'en_IN', 'currency': '₹'},
    'AU': {'domain': 'amazon.com.au', 'locale': 'en_AU', 'currency': '$'},
    'SE': {'domain': 'amazon.se', 'locale': 'sv_SE', 'currency': 'kr'},
    'NL': {'domain': 'amazon.nl', 'locale': 'nl_NL', 'currency': '€'},
    'BE': {'domain': 'amazon.be', 'locale': 'fr_BE', 'currency': '€'},
    'PL': {'domain': 'amazon.pl', 'locale': 'pl_PL', 'currency': 'zł'},
}


def detect_country_from_ip():
    """Detects country based on user's public IP"""
    try:
        # Use IP geolocation service
        response = requests.get('https://ipapi.co/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            country_code = data.get('country_code', 'FR').upper()
            country_name = data.get('country_name', 'France')
            ip = data.get('ip', 'N/A')
            logger.info(f"IP detection: {ip} ({country_name})")
            return country_code
    except Exception as e:
        logger.warning(f"Unable to detect IP: {e}")
    return 'FR'  # Default: France


def get_amazon_domain(country_code=None):
    """Returns Amazon domain for a country"""
    if country_code is None:
        country_code = detect_country_from_ip()
    
    country_code = country_code.upper()
    
    if country_code in AMAZON_SITES:
        site_info = AMAZON_SITES[country_code]
        logger.info(f"Amazon site selected: {site_info['domain']}")
        return country_code, site_info
    else:
        logger.warning(f"Country '{country_code}' not supported, using FR as default")
        return 'FR', AMAZON_SITES['FR']


class AmazonScraperSelenium:
    """Amazon Scraper with Selenium (anti-detection) - Multi-site"""
    
    def __init__(self, amazon_site=None):
        """
        Initializes the scraper
        
        Args:
            amazon_site: Optional country code (ex: 'FR', 'US', 'DE')
                        If None, automatic detection by IP
        """
        self.driver = None
        
        # Determine which Amazon site to use
        if amazon_site is None:
            self.country_code, self.site_info = get_amazon_domain()
        else:
            self.country_code, self.site_info = get_amazon_domain(amazon_site)
        
        logger.info(f"Scraper configured for: {self.site_info['domain']}")
        self.setup_driver()
    
    def setup_driver(self):
        """Configure Chrome driver to avoid detection"""
        
        logger.info("Configuring Selenium with anti-detection")
        
        options = Options()
        
        # Headless mode - hide browser window
        options.add_argument("--headless=new")
        
        # Anti-detection options
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Realistic User-Agent
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        options.add_argument(f"user-agent={user_agent}")
        
        # Disable images for faster loading
        options.add_argument("--blink-settings=imagesEnabled=false")
        
        # Window size (human-like)
        options.add_argument("--window-size=1920,1080")
        
        # Use webdriver-manager to manage ChromeDriver automatically
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Inject JavaScript to hide bot markers
        self.driver.execute_script("""
            // Hide navigator.webdriver
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Hide chrome
            Object.defineProperty(navigator, 'chrome', {
                get: () => undefined
            });
        """)
        
        logger.info("Chrome driver configured (anti-detection)")
    
    def scrape_amazon(self, search_query: str, max_results: int = 10, collect_all_pages: bool = False, target_page: int = None):
        """
        Scrape Amazon for a given search with pagination support
        
        Args:
            search_query: Search term (ex: "lenovo legion")
            max_results: Number of products to extract (ignored if target_page is set)
            collect_all_pages: If True, collect from all pages up to max_results
            target_page: If set, collect all items up to this page (1-7)
            
        Returns:
            List of products
        """
        
        all_products = []
        current_page_url = None
        page_number = 1
        
        try:
            # 1. Build URL with appropriate Amazon domain
            search_query_encoded = search_query.replace(" ", "+")
            domain = self.site_info['domain']
            current_page_url = f"https://www.{domain}/s?k={search_query_encoded}"
            
            logger.info(f"Accessing: {current_page_url}")
            
            # Determine collection mode
            use_page_limit = target_page is not None
            
            # Loop through pages
            while current_page_url and (page_number <= target_page if use_page_limit else len(all_products) < max_results):
                # 2. Load the page
                self.driver.get(current_page_url)
                
                # Realistic pause (human reading page)
                time.sleep(random.uniform(3, 7))
                
                # 3. Wait for results to load
                try:
                    wait = WebDriverWait(self.driver, 15)
                    wait.until(EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, '[data-component-type="s-search-result"]')
                    ))
                except:
                    # Fallback: just wait
                    time.sleep(5)
                
                logger.info(f"Page {page_number} loaded, extracting products...")
                
                # Simulate human scrolling
                for _ in range(3):
                    self.driver.execute_script("window.scrollBy(0, 300)")
                    time.sleep(random.uniform(1, 2))
                
                # 4. Get the HTML
                html = self.driver.page_source
                
                # 5. Parse with Parsel
                remaining = max_results - len(all_products)
                page_products = self._extract_products(html, remaining)
                all_products.extend(page_products)
                
                logger.info(f"Collected {len(all_products)} products so far")
                
                # Check if we need to continue to next page
                should_continue = False
                
                if use_page_limit:
                    # Continue if we haven't reached target page
                    should_continue = page_number < target_page
                else:
                    # Continue if we need more items
                    should_continue = collect_all_pages and len(all_products) < max_results
                
                if should_continue:
                    next_page_url = self._get_next_page_url(html)
                    if next_page_url:
                        current_page_url = next_page_url
                        page_number += 1
                        logger.info(f"Moving to page {page_number}...")
                        time.sleep(random.uniform(2, 5))
                    else:
                        logger.info("No next page available")
                        break
                else:
                    break
            
            return all_products
            
        except Exception as e:
            logger.error(f"Error: {e}")
            return all_products
    
    def _get_next_page_url(self, html: str) -> str:
        """
        Extracts the URL of the next page from pagination
        
        Args:
            html: HTML content of the current page
            
        Returns:
            URL of next page or None if not available
        """
        try:
            selector = Selector(text=html)
            
            # Look for next page link in pagination
            # Pattern: a tag with s-pagination-next class
            next_links = selector.css('a.s-pagination-next::attr(href)').getall()
            
            if next_links:
                next_url = next_links[0]
                # Ensure it's a full URL
                domain = self.site_info['domain']
                if not next_url.startswith('http'):
                    next_url = f"https://www.{domain}{next_url}"
                logger.info(f"Found next page: {next_url}")
                return next_url
            
            # Alternative: look for page buttons and get next available
            page_buttons = selector.css('a.s-pagination-button::attr(href)').getall()
            if page_buttons:
                next_url = page_buttons[0]
                domain = self.site_info['domain']
                if not next_url.startswith('http'):
                    next_url = f"https://www.{domain}{next_url}"
                logger.info(f"Found next page via pagination: {next_url}")
                return next_url
            
            logger.info("No next page found")
            return None
            
        except Exception as e:
            logger.error(f"Error extracting next page URL: {e}")
            return None
    
    def _extract_products(self, html: str, max_results: int) -> list:
        """Extracts products from HTML"""
        
        selector = Selector(text=html)
        products = []
        
        # Find product cards
        cards = selector.css('[data-component-type="s-search-result"]')
        logger.info(f"{len(cards)} products found on this page")
        
        for idx, card in enumerate(cards[:max_results], 1):
            try:
                # Title
                title_spans = card.css("h2 span::text").getall()
                title = " ".join(title_spans).strip() if title_spans else "N/A"
                
                # Price - Use intelligent logic
                price = self._extract_price_intelligent(card)
                
                # Rating
                rating_text = card.css(".a-icon-alt::text").get()
                rating = rating_text.split()[0] if rating_text else "N/A"
                
                # ASIN
                asin = card.attrib.get("data-asin", "N/A")
                
                # URL - Use appropriate Amazon domain
                href = card.css("a.a-link-normal.s-no-outline::attr(href)").get()
                domain = self.site_info['domain']
                url = href if href and href.startswith("http") else f"https://www.{domain}{href}" if href else "N/A"
                
                product = {
                    "asin": asin,
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "url": url[:100]
                }
                
                products.append(product)
                logger.info(f"[{idx}] {title[:60]}... | {price}")
                
                # Random pause for each product
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                logger.error(f"  Extraction error [{idx}]: {e}")
                continue
        
        return products
    
    def _extract_price_intelligent(self, card) -> str:
        """
        Intelligent and dynamic price extraction with multiple strategies
        Adapts to all price formats and currencies (€, $, £, ¥, etc.)
        """
        try:
            currency = self.site_info['currency']  # Get currency from site
            
            # Strategy 1: Classic method (whole + fraction)
            price_whole = card.css(".a-price-whole::text").get()
            price_frac = card.css(".a-price-fraction::text").get()
            
            if price_whole and price_frac:
                # Format with fraction (ex: "123,45" or "123.45")
                return f"{price_whole.strip()}.{price_frac.strip()} {currency}"
            elif price_whole:
                return f"{price_whole.strip()} {currency}"
            
            # Strategy 2: Look in price spans
            price_spans = card.css("span.a-price::text").getall()
            if price_spans:
                for span in price_spans:
                    span_clean = span.strip()
                    if currency in span_clean or re.match(r"[\d,.\s]+", span_clean):
                        return span_clean
            
            # Strategy 3: Patterns for different currencies
            all_text = " ".join(card.css("::text").getall())
            
            # Pattern for currency before number (ex: "£123" or "$456")
            if currency in ["$", "£", "€", "¥"]:
                escaped_currency = re.escape(currency)
                price_pattern = re.search(
                    rf"{escaped_currency}\s*([\d]+[\s,.\d]*)",
                    all_text
                )
                if price_pattern:
                    return f"{currency}{price_pattern.group(1).strip()}"
            
            # Strategy 4: Pattern for currency after number (ex: "123€" or "456£")
            if currency in ["€", "£", "¥", "₹", "kr", "zł", "R$"]:
                escaped_currency = re.escape(currency)
                price_pattern = re.search(
                    rf"([\d]+[\s,.\d]*)\s*{escaped_currency}",
                    all_text
                )
                if price_pattern:
                    return f"{price_pattern.group(1).strip()} {currency}"
            
            # Strategy 5: Look for numbers with comma or period only
            numbers = re.findall(r"[\d]{2,4}[\s.,]*[\d]{0,2}", all_text)
            if numbers:
                price_candidate = numbers[0].strip()
                if len(price_candidate) > 2:
                    return f"{price_candidate} {currency}"
            
            # Strategy 6: Look in data-attributes
            price_attr = card.attrib.get("data-price", None)
            if price_attr:
                return f"{price_attr} {currency}"
            
            # Strategy 7: Look in div.a-price-range
            range_price = card.css(".a-price-range::text").get()
            if range_price:
                return range_price.strip()
            
            # Fallback
            return "N/A"
            
        except Exception as e:
            logger.debug(f"Price extraction error: {e}")
            return "N/A"
    
    def save_csv(self, products: list, filename: str = "amazon_results.csv"):
        """Saves results to CSV"""
        
        if not products:
            logger.warning("No products to save")
            return
        
        try:
            # Create output directory if it doesn't exist
            output_path = Path(filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=products[0].keys())
                writer.writeheader()
                writer.writerows(products)
            
            logger.info(f"Results saved: {filename}")
            
        except Exception as e:
            logger.error(f"CSV save error: {e}")
    
    def close(self):
        """Closes the browser"""
        if self.driver:
            self.driver.quit()


# Utility functions for filtering and processing

def remove_duplicates(products: list) -> list:
    """Remove duplicate products based on ASIN"""
    seen = set()
    unique = []
    for p in products:
        asin = p.get('asin', '')
        if asin and asin not in seen:
            seen.add(asin)
            unique.append(p)
    return unique


def filter_by_search_term(products: list, search_term: str) -> list:
    """Filter products that contain search term in title"""
    filtered = []
    search_lower = search_term.lower()
    
    for p in products:
        title = p.get('title', '').lower()
        if search_lower in title:
            filtered.append(p)
    
    return filtered


def remove_similar_duplicates(products: list, threshold: float = 0.85) -> list:
    """Remove products with very similar titles (likely duplicates)"""
    if not products:
        return products
    
    unique = [products[0]]
    
    for current in products[1:]:
        is_duplicate = False
        current_title = current.get('title', '').lower()
        
        for existing in unique:
            existing_title = existing.get('title', '').lower()
            similarity = SequenceMatcher(None, current_title, existing_title).ratio()
            
            if similarity >= threshold:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique.append(current)
    
    return unique


def extract_price_value(price_str: str) -> float:
    """Extract numeric price from price string"""
    try:
        # Remove currency symbols and extra spaces
        cleaned = re.sub(r'[^\d.,]', '', price_str)
        # Replace comma with period for decimal
        cleaned = cleaned.replace(',', '.')
        # Get only the number part
        match = re.search(r'\d+\.?\d*', cleaned)
        if match:
            return float(match.group())
    except:
        pass
    return float('inf')  # Return infinity if can't parse


def filter_by_price_range(products: list, min_price: float = None, max_price: float = None) -> list:
    """Filter products by price range"""
    if not products or (min_price is None and max_price is None):
        return products
    
    filtered = []
    for p in products:
        price_str = p.get('price', 'N/A')
        if price_str == 'N/A':
            continue
        
        price_value = extract_price_value(price_str)
        
        # Check if price is within range
        if min_price is not None and price_value < min_price:
            continue
        if max_price is not None and price_value > max_price:
            continue
        
        filtered.append(p)
    
    return filtered


def filter_by_rating(products: list, min_rating: float = None) -> list:
    """Filter products by minimum rating"""
    if not products or min_rating is None:
        return products
    
    filtered = []
    for p in products:
        rating_str = p.get('rating', 'N/A')
        if rating_str == 'N/A':
            continue
        
        try:
            rating_value = float(rating_str)
            if rating_value >= min_rating:
                filtered.append(p)
        except:
            continue
    
    return filtered
