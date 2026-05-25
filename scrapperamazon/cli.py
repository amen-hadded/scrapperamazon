"""
CLI interface for scrapperAmazon - Interactive version matching scrapper.py interface
"""

import logging
import sys
import time

from .core import (
    AmazonScraperSelenium,
    AMAZON_SITES,
    remove_duplicates,
    remove_similar_duplicates,
    filter_by_search_term,
    filter_by_price_range,
    filter_by_rating,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ANSI color codes
class Colors:
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Pixel characters
PIXEL_FULL = '█'
PIXEL_HALF = '▌'
PIXEL_LIGHT = '░'
SPINNER = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']


def print_logo():
    """Print ASCII art logo"""
    logo = f"""
{Colors.CYAN}{Colors.BOLD}
    ███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗ 
    ██╔════╝██╔════╝██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ███████╗██║     ██║  ███╗███████║██████╔╝██████╔╝█████╗  ██████╔╝
    ╚════██║██║     ██║   ██║██╔══██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗
    ███████║╚██████╗╚██████╔╝██║  ██║██║     ██║     ███████╗██║  ██║
    ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝
    
    {Colors.YELLOW}Amazon Product Scraper {Colors.RESET}{Colors.GREEN}✓ PRO{Colors.RESET}{Colors.CYAN}
    {Colors.RESET}"""
    print(logo)


def print_header(title):
    """Print formatted header with pixel border"""
    width = 70
    border = PIXEL_LIGHT * width
    print(f"\n{Colors.CYAN}{border}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}  {title}{Colors.RESET}")
    print(f"{Colors.CYAN}{border}{Colors.RESET}\n")


def print_section(title):
    """Print formatted section with visual indicator"""
    print(f"\n{Colors.YELLOW}▼ {title}{Colors.RESET}")
    print(f"{Colors.YELLOW}{'-' * 60}{Colors.RESET}")


def progress_bar(current, total, width=40, label=""):
    """Draw a pixel-style progress bar"""
    if total == 0:
        percent = 100
    else:
        percent = int((current / total) * 100)
    
    filled = int((current / total) * width) if total > 0 else 0
    bar = PIXEL_FULL * filled + PIXEL_LIGHT * (width - filled)
    
    return f"{label} [{Colors.GREEN}{bar}{Colors.RESET}] {percent}%"


def loading_spinner(message="Loading"):
    """Print a loading spinner"""
    for i, frame in enumerate(SPINNER):
        sys.stdout.write(f'\r{Colors.CYAN}{frame} {message}...{Colors.RESET}')
        sys.stdout.flush()
        if i < len(SPINNER) - 1:
            time.sleep(0.1)


def display_sites_menu():
    """Display available Amazon sites and return user choice"""
    print_logo()
    
    sites_list = list(AMAZON_SITES.items())
    print(f"{Colors.BOLD}Available Amazon sites:{Colors.RESET}")
    print(f"{Colors.CYAN}{'-' * 50}{Colors.RESET}")
    for i, (code, info) in enumerate(sites_list, 1):
        icon = f"{Colors.GREEN}●{Colors.RESET}" if i % 2 == 1 else f"{Colors.YELLOW}●{Colors.RESET}"
        print(f"  {icon} {i:2d}. [{Colors.BOLD}{code}{Colors.RESET}] {info['domain']:<20} ({Colors.CYAN}{info['locale']}{Colors.RESET})")
    
    print(f"{Colors.CYAN}{'-' * 50}{Colors.RESET}")
    print(f"  {Colors.GREEN}●{Colors.RESET} 0. {Colors.YELLOW}Automatic detection by IP (recommended){Colors.RESET}\n")
    
    # Get user choice
    choice = input(f"{Colors.MAGENTA}➤{Colors.RESET} Choose a site (number, code, or 0): ").strip().upper()
    
    amazon_site = None
    
    # Check if it's a number
    if choice.isdigit():
        choice_num = int(choice)
        if 1 <= choice_num <= len(sites_list):
            amazon_site = sites_list[choice_num - 1][0]
            print(f"{Colors.GREEN}✓ Site selected:{Colors.RESET} {Colors.BOLD}{AMAZON_SITES[amazon_site]['domain']}{Colors.RESET}\n")
        elif choice_num == 0:
            print(f"{Colors.YELLOW}⟳ Auto-detecting country by IP...{Colors.RESET}\n")
        else:
            print(f"{Colors.YELLOW}⚠ Invalid number (1-{len(sites_list)}), using automatic detection{Colors.RESET}\n")
    # Check if it's a country code
    elif choice in AMAZON_SITES:
        amazon_site = choice
        print(f"{Colors.GREEN}✓ Site selected:{Colors.RESET} {Colors.BOLD}{AMAZON_SITES[choice]['domain']}{Colors.RESET}\n")
    elif choice == "":
        print(f"{Colors.YELLOW}⟳ Auto-detecting country by IP...{Colors.RESET}\n")
    else:
        print(f"{Colors.YELLOW}⚠ Invalid code, using automatic detection{Colors.RESET}\n")
    
    return amazon_site


def get_search_term():
    """Get search term from user"""
    search_term = input(f"{Colors.MAGENTA}➤{Colors.RESET} Enter search term {Colors.CYAN}(default: 'bicycle'){Colors.RESET}: ").strip()
    if not search_term:
        search_term = "bicycle"
    print(f"{Colors.GREEN}✓ Search term:{Colors.RESET} {Colors.BOLD}{search_term}{Colors.RESET}\n")
    return search_term


def get_collection_mode():
    """Display collection options and return parameters"""
    print_section("How do you want to collect data?")
    print(f"{Colors.BOLD}OPTIONS:{Colors.RESET}")
    print(f"  {Colors.CYAN}1.{Colors.RESET} Number of items      {Colors.YELLOW}(e.g., collect 50 items){Colors.RESET}")
    print(f"  {Colors.CYAN}2.{Colors.RESET} Specific page        {Colors.YELLOW}(e.g., collect from page 1){Colors.RESET}")
    print(f"  {Colors.CYAN}3.{Colors.RESET} Page range           {Colors.YELLOW}(e.g., collect pages 1 to 3){Colors.RESET}")
    print(f"  {Colors.CYAN}4.{Colors.RESET} All pages            {Colors.YELLOW}(collect all, max 7 pages){Colors.RESET}")
    print(f"  {Colors.CYAN}5.{Colors.RESET} Default              {Colors.GREEN}(20 items from page 1){Colors.RESET}")
    print(f"{Colors.CYAN}{'-' * 60}{Colors.RESET}")
    
    choice = input(f"\n{Colors.MAGENTA}➤{Colors.RESET} Select option (1-5): ").strip()
    
    max_results = 20
    collect_all_pages = False
    target_page = None
    
    if choice == '1':
        # Option 1: Number of items
        num_items = input(f"{Colors.MAGENTA}➤{Colors.RESET} Enter number of items: ").strip()
        if num_items.isdigit():
            max_results = int(num_items)
            if max_results > 20:
                collect_all_pages = True
            print(f"{Colors.GREEN}✓{Colors.RESET} Will collect {Colors.BOLD}{max_results}{Colors.RESET} items across pages")
        else:
            print(f"{Colors.YELLOW}⚠ Invalid input, using default (20 items){Colors.RESET}")
    
    elif choice == '2':
        # Option 2: Specific page
        page_num = input(f"{Colors.MAGENTA}➤{Colors.RESET} Enter page number (1-7): ").strip()
        if page_num.isdigit():
            page = int(page_num)
            if 1 <= page <= 7:
                max_results = 10000
                collect_all_pages = True
                target_page = page
                print(f"{Colors.GREEN}✓{Colors.RESET} Will collect all items from page 1 to page {Colors.BOLD}{page}{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}⚠ Invalid page number (1-7), using default (page 1){Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠ Invalid input, using default (page 1){Colors.RESET}")
    
    elif choice == '3':
        # Option 3: Page range
        page_range = input(f"{Colors.MAGENTA}➤{Colors.RESET} Enter page range (e.g., 1-3): ").strip()
        if '-' in page_range:
            try:
                parts = page_range.split('-')
                start = int(parts[0].strip())
                end = int(parts[1].strip())
                
                if 1 <= start <= 7 and 1 <= end <= 7 and start <= end:
                    max_results = 10000
                    collect_all_pages = True
                    target_page = end
                    print(f"{Colors.GREEN}✓{Colors.RESET} Will collect all items from page 1 to page {Colors.BOLD}{end}{Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}⚠ Invalid range (1-7), using default (page 1){Colors.RESET}")
            except:
                print(f"{Colors.YELLOW}⚠ Invalid format, using default (page 1){Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠ Invalid format, use 'start-end' (e.g., 1-3){Colors.RESET}")
    
    elif choice == '4':
        # Option 4: All pages
        max_results = 10000
        collect_all_pages = True
        target_page = 7
        print(f"{Colors.GREEN}✓{Colors.RESET} Will collect from {Colors.BOLD}ALL PAGES{Colors.RESET} (max 7 pages)")
    
    elif choice == '5' or choice == '':
        # Option 5: Default
        print(f"{Colors.GREEN}✓{Colors.RESET} Using default: {Colors.BOLD}20 items{Colors.RESET} from page 1")
    
    else:
        print(f"{Colors.YELLOW}⚠ Invalid option '{choice}', using default (20 items){Colors.RESET}")
    
    return max_results, collect_all_pages, target_page, choice


def get_filtering_options(search_term):
    """Get filtering options from user"""
    print_section("DATA CLEANING OPTIONS")
    print(f"  {Colors.CYAN}1.{Colors.RESET} Remove duplicates (same ASIN)")
    print(f"  {Colors.CYAN}2.{Colors.RESET} Remove similar products (similar titles)")
    print(f"  {Colors.CYAN}3.{Colors.RESET} Filter by search term\n")
    
    filter_term = input(f"{Colors.MAGENTA}➤{Colors.RESET} Filter term {Colors.CYAN}(default: '{search_term}'){Colors.RESET}: ").strip()
    if not filter_term:
        filter_term = search_term
    print()
    
    # Get cleaning preferences
    clean_duplicates = input(f"{Colors.MAGENTA}➤{Colors.RESET} Remove exact duplicates? {Colors.CYAN}(y/n, default: y){Colors.RESET}: ").strip().lower() != 'n'
    clean_similar = input(f"{Colors.MAGENTA}➤{Colors.RESET} Remove similar products? {Colors.CYAN}(y/n, default: n){Colors.RESET}: ").strip().lower() == 'y'
    filter_by_term = input(f"{Colors.MAGENTA}➤{Colors.RESET} Filter by '{filter_term}'? {Colors.CYAN}(y/n, default: y){Colors.RESET}: ").strip().lower() != 'n'
    
    # Price filter
    filter_price = input(f"{Colors.MAGENTA}➤{Colors.RESET} Filter by price? {Colors.CYAN}(y/n, default: n){Colors.RESET}: ").strip().lower() == 'y'
    min_price = None
    max_price = None
    if filter_price:
        try:
            min_input = input(f"{Colors.MAGENTA}  ➤{Colors.RESET} Min price (leave empty for no minimum): ").strip()
            if min_input:
                min_price = float(min_input)
            max_input = input(f"{Colors.MAGENTA}  ➤{Colors.RESET} Max price (leave empty for no maximum): ").strip()
            if max_input:
                max_price = float(max_input)
        except ValueError:
            print(f"{Colors.YELLOW}⚠ Invalid price input, skipping price filter{Colors.RESET}")
    
    # Rating filter
    filter_rating = input(f"{Colors.MAGENTA}➤{Colors.RESET} Filter by rating? {Colors.CYAN}(y/n, default: n){Colors.RESET}: ").strip().lower() == 'y'
    min_rating = None
    if filter_rating:
        try:
            rating_input = input(f"{Colors.MAGENTA}  ➤{Colors.RESET} Minimum rating (e.g., 3.5): ").strip()
            if rating_input:
                min_rating = float(rating_input)
        except ValueError:
            print(f"{Colors.YELLOW}⚠ Invalid rating input, skipping rating filter{Colors.RESET}")
    
    return {
        'clean_duplicates': clean_duplicates,
        'clean_similar': clean_similar,
        'filter_term': filter_term if filter_by_term else None,
        'min_price': min_price,
        'max_price': max_price,
        'min_rating': min_rating
    }


def apply_filters(products, filters):
    """Apply filters to products"""
    cleaned_products = products.copy()
    
    if filters['clean_duplicates']:
        original_count = len(cleaned_products)
        cleaned_products = remove_duplicates(cleaned_products)
        removed = original_count - len(cleaned_products)
        if removed > 0:
            print(f"\n{Colors.YELLOW}⚙{Colors.RESET} Removed {Colors.BOLD}{removed}{Colors.RESET} duplicate products (ASIN-based)")
    
    if filters['clean_similar']:
        original_count = len(cleaned_products)
        cleaned_products = remove_similar_duplicates(cleaned_products)
        removed = original_count - len(cleaned_products)
        if removed > 0:
            print(f"{Colors.YELLOW}⚙{Colors.RESET} Removed {Colors.BOLD}{removed}{Colors.RESET} similar products")
    
    if filters['filter_term']:
        original_count = len(cleaned_products)
        cleaned_products = filter_by_search_term(cleaned_products, filters['filter_term'])
        removed = original_count - len(cleaned_products)
        if removed > 0:
            print(f"{Colors.YELLOW}⚙{Colors.RESET} Filtered out {Colors.BOLD}{removed}{Colors.RESET} products not matching '{Colors.MAGENTA}{filters['filter_term']}{Colors.RESET}'")
        if len(cleaned_products) == 0:
            print(f"{Colors.RED}✗{Colors.RESET} No products found matching '{Colors.MAGENTA}{filters['filter_term']}{Colors.RESET}'")
    
    if filters['min_price'] is not None or filters['max_price'] is not None:
        original_count = len(cleaned_products)
        cleaned_products = filter_by_price_range(
            cleaned_products, 
            filters['min_price'], 
            filters['max_price']
        )
    if filters['min_price'] is not None or filters['max_price'] is not None:
        original_count = len(cleaned_products)
        cleaned_products = filter_by_price_range(
            cleaned_products, 
            filters['min_price'], 
            filters['max_price']
        )
        removed = original_count - len(cleaned_products)
        if removed > 0:
            price_range = ""
            if filters['min_price'] is not None:
                price_range += f"min: {Colors.GREEN}{filters['min_price']}{Colors.RESET}"
            if filters['max_price'] is not None:
                if price_range:
                    price_range += f", max: {Colors.GREEN}{filters['max_price']}{Colors.RESET}"
                else:
                    price_range += f"max: {Colors.GREEN}{filters['max_price']}{Colors.RESET}"
            print(f"{Colors.YELLOW}⚙{Colors.RESET} Filtered out {Colors.BOLD}{removed}{Colors.RESET} products outside price range ({price_range})")
    
    if filters['min_rating'] is not None:
        original_count = len(cleaned_products)
        cleaned_products = filter_by_rating(cleaned_products, filters['min_rating'])
        removed = original_count - len(cleaned_products)
        if removed > 0:
            print(f"{Colors.YELLOW}⚙{Colors.RESET} Filtered out {Colors.BOLD}{removed}{Colors.RESET} products with rating below {Colors.GREEN}{filters['min_rating']}{Colors.RESET}")
    
    return cleaned_products


def display_results(products):
    """Display final results with pixel formatting"""
    print_header(f"Final Results {Colors.GREEN}✓{Colors.RESET} {Colors.BOLD}{len(products)} Products{Colors.RESET}")
    
    for i, p in enumerate(products, 1):
        # Alternate colors for each product
        color = Colors.CYAN if i % 2 == 1 else Colors.MAGENTA
        
        print(f"{color}{PIXEL_FULL * 3}{Colors.RESET} [{Colors.BOLD}{i:03d}{Colors.RESET}] {Colors.BOLD}{p['title'][:55]}{Colors.RESET}")
        print(f"     {Colors.GREEN}💰 Price:{Colors.RESET} {Colors.BOLD}{p['price']}{Colors.RESET}")
        print(f"     {Colors.YELLOW}⭐ Rating:{Colors.RESET} {Colors.BOLD}{p['rating']}{Colors.RESET}")
        print(f"     {Colors.BLUE}📦 ASIN:{Colors.RESET} {p['asin']}")
        print()


def main():
    """
    scrapperAmazon - Interactive Amazon Product Scraper
    
    An interactive command-line tool to scrape Amazon products across multiple countries.
    Supports filtering, pagination, and data export to CSV.
    """
    scraper = None
    
    try:
        # 1. Display sites and get user choice
        amazon_site = display_sites_menu()
        
        # 2. Initialize scraper
        print(f"{Colors.CYAN}⟳ Initializing scraper{Colors.RESET}...")
        loading_spinner("Configuring")
        scraper = AmazonScraperSelenium(amazon_site=amazon_site)
        print(f"\r{Colors.GREEN}✓ Scraper initialized{Colors.RESET}          \n")
        
        # 3. Get search term
        search_term = get_search_term()
        
        # 4. Get collection mode
        max_results, collect_all_pages, target_page, choice = get_collection_mode()
        
        print(f"\n{Colors.BLUE}🚀 Starting scrape...{Colors.RESET}\n")
        
        # 5. Scrape Amazon
        products = scraper.scrape_amazon(
            search_query=search_term,
            max_results=max_results,
            collect_all_pages=collect_all_pages,
            target_page=target_page if choice in ['2', '3', '4'] else None
        )
        
        # 6. Handle results
        if products:
            print(f"\n{Colors.CYAN}{PIXEL_FULL * 70}{Colors.RESET}")
            print(f"{Colors.GREEN}✓ Collected {Colors.BOLD}{len(products)}{Colors.RESET}{Colors.GREEN} Products{Colors.RESET}")
            print(f"{Colors.CYAN}{PIXEL_FULL * 70}{Colors.RESET}\n")
            
            # Get filtering options
            filters = get_filtering_options(search_term)
            
            # Apply filters
            cleaned_products = apply_filters(products, filters)
            
            # Display final results
            if cleaned_products:
                display_results(cleaned_products)
                
                # Save results
                print(f"{Colors.BLUE}💾 Saving results{Colors.RESET}...")
                loading_spinner("Saving")
                scraper.save_csv(cleaned_products)
                print(f"\r{Colors.GREEN}✓ Results saved to:{Colors.RESET} {Colors.BOLD}amazon_results.csv{Colors.RESET}    ")
                print(f"{Colors.GREEN}✓ Total items saved:{Colors.RESET} {Colors.BOLD}{len(cleaned_products)}{Colors.RESET}\n")
            else:
                print(f"{Colors.YELLOW}⚠ No products remaining after filtering{Colors.RESET}")
        
        else:
            print(f"{Colors.RED}✗ No products found{Colors.RESET}")
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠ User interruption{Colors.RESET}")
        sys.exit(0)
    
    except Exception as e:
        print(f"{Colors.RED}✗ Fatal error:{Colors.RESET} {e}")
        logger.error(f"Fatal error: {e}")
        raise
    
    finally:
        # Close browser
        if scraper:
            scraper.close()
        
        print(f"\n{Colors.CYAN}{PIXEL_FULL * 70}{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Scraping completed successfully!{Colors.RESET}")
        print(f"{Colors.CYAN}{PIXEL_FULL * 70}{Colors.RESET}\n")


if __name__ == "__main__":
    main()
