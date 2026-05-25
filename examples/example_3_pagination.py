"""
Example 3: Pagination and Multi-Page Scraping

This example demonstrates how to scrape multiple pages of results.
"""

from scrapperamazon import AmazonScraperSelenium

# Create scraper (auto-detect country)
scraper = AmazonScraperSelenium()

# Collect from multiple pages
products = scraper.scrape_amazon(
    search_query="smartphone",
    max_results=100,  # Will collect across multiple pages
    collect_all_pages=True,  # Continue collecting across pages
)

print(f"Total products collected: {len(products)}")

# Group products by price range for analysis
cheap = [p for p in products if 'N/A' not in p['price'] and float(p['price'].split()[0]) < 200]
mid_range = [p for p in products if 'N/A' not in p['price'] and 200 <= float(p['price'].split()[0]) < 600]
expensive = [p for p in products if 'N/A' not in p['price'] and float(p['price'].split()[0]) >= 600]

print(f"\nPrice Range Analysis:")
print(f"  Cheap (<$200): {len(cheap)} products")
print(f"  Mid-Range ($200-$600): {len(mid_range)} products")
print(f"  Expensive (>$600): {len(expensive)} products")

# Save by category
scraper.save_csv(cheap, "smartphones_cheap.csv")
scraper.save_csv(mid_range, "smartphones_midrange.csv")
scraper.save_csv(expensive, "smartphones_expensive.csv")

# Close browser
scraper.close()
