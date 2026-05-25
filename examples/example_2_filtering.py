"""
Example 2: Advanced Filtering

This example shows how to filter products using various criteria.
"""

from scrapperamazon import (
    AmazonScraperSelenium,
    remove_duplicates,
    filter_by_search_term,
    filter_by_price_range,
    filter_by_rating,
    remove_similar_duplicates,
)

# Create scraper for specific country (US)
scraper = AmazonScraperSelenium(amazon_site="US")

# Scrape products
products = scraper.scrape_amazon(
    search_query="headphones",
    max_results=50,
)

print(f"Original products: {len(products)}")

# Apply filters
products = remove_duplicates(products)
print(f"After removing duplicates: {len(products)}")

products = remove_similar_duplicates(products)
print(f"After removing similar: {len(products)}")

products = filter_by_search_term(products, "wireless")
print(f"After filter by 'wireless': {len(products)}")

products = filter_by_price_range(products, min_price=50, max_price=200)
print(f"After price filter ($50-$200): {len(products)}")

products = filter_by_rating(products, min_rating=4.0)
print(f"After rating filter (4.0+): {len(products)}")

# Save filtered results
scraper.save_csv(products, "filtered_headphones.csv")

# Close browser
scraper.close()
