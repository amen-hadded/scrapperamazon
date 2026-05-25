"""
Example 1: Basic Scraping

This example demonstrates the most basic usage of scrapperAmazon
as a Python library.
"""

from scrapperamazon import AmazonScraperSelenium

# Create scraper instance (auto-detects country by IP)
scraper = AmazonScraperSelenium()

# Scrape products
products = scraper.scrape_amazon(
    search_query="laptop",
    max_results=10,
)

# Print results
for i, product in enumerate(products, 1):
    print(f"\n[{i}] {product['title']}")
    print(f"   Price: {product['price']}")
    print(f"   Rating: {product['rating']}")
    print(f"   ASIN: {product['asin']}")

# Save to CSV
scraper.save_csv(products, "laptops.csv")

# Close browser
scraper.close()
