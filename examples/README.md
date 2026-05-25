# scrapperAmazon Examples

This directory contains practical examples of how to use scrapperAmazon both as a CLI tool and as a Python library.

## Interactive CLI Usage

Launch the interactive CLI interface:

```bash
python -m scrapperamazon.cli
```

This will guide you through an interactive session where you:

1. **Select Country** - Choose from 15 Amazon domains or auto-detect by IP
2. **Enter Search Query** - Type what you're looking for
3. **Choose Collection Mode** - Select how many items/pages to collect
4. **Apply Filters** - Optionally filter by price, rating, duplicates, etc.
5. **View Results** - See all products with prices and links
6. **Save to CSV** - Export results for analysis

### Example Interactive Session

```
$ python -m scrapperamazon.cli

    ███████╗ ██████╗ ██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗
    ██╔════╝██╔════╝██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ...

Available Amazon sites:
  ● 1. [FR] amazon.fr
  ● 2. [DE] amazon.de
  ... (15 options)
  ● 0. Automatic detection by IP

➤ Choose a site: 0
📍 Auto-detecting country by IP...
✓ Selected: amazon.fr

➤ Enter search term: laptop

📦 Collection Mode:
  1. Specific number of items
  2. Specific number of pages
  3. Range of pages
  4. All available products
  5. Default (5 pages)

➤ Choose mode: 1
➤ How many items? 10

🚀 Starting scrape...
✓ Collected 10 products

💾 Save to CSV? (y/n): y
✓ Saved to: products.csv
```

## Python Library Examples (Advanced)

If you want to use scrapperAmazon as a Python library in your own code:

All examples can be run directly:

```bash
python example_1_basic.py
python example_2_filtering.py
python example_3_pagination.py
```

### Example 1: Basic Scraping

[example_1_basic.py](example_1_basic.py) shows:

- How to create a scraper instance
- Basic scraping of products
- Saving results to CSV
- Properly closing the browser

### Example 2: Advanced Filtering

[example_2_filtering.py](example_2_filtering.py) demonstrates:

- Removing exact duplicates
- Removing similar products
- Filtering by search term
- Filtering by price range
- Filtering by minimum rating
- Combining multiple filters

### Example 3: Pagination and Multi-Page Scraping

[example_3_pagination.py](example_3_pagination.py) shows:

- Collecting products across multiple pages
- Setting maximum results limit
- Analyzing products by price ranges
- Saving results to multiple CSV files

## Common Patterns

### Pattern 1: Scrape and Filter

```python
from scrapperamazon import AmazonScraperSelenium, remove_duplicates, filter_by_price_range

scraper = AmazonScraperSelenium(amazon_site="US")
products = scraper.scrape_amazon("laptop", max_results=50)
products = remove_duplicates(products)
products = filter_by_price_range(products, min_price=500, max_price=1500)
scraper.save_csv(products, "gaming_laptops.csv")
scraper.close()
```

### Pattern 2: Multi-Country Comparison

```python
from scrapperamazon import AmazonScraperSelenium

for country in ["US", "GB", "DE", "FR"]:
    scraper = AmazonScraperSelenium(amazon_site=country)
    products = scraper.scrape_amazon("smartphone", max_results=20)
    scraper.save_csv(products, f"smartphones_{country}.csv")
    scraper.close()
```

### Pattern 3: Real-Time Price Monitoring

```python
import time
from datetime import datetime
from scrapperamazon import AmazonScraperSelenium

scraper = AmazonScraperSelenium()

for i in range(5):
    products = scraper.scrape_amazon("laptop", max_results=10)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scraper.save_csv(products, f"prices_{timestamp}.csv")

    if i < 4:
        print("Waiting 1 hour before next scrape...")
        time.sleep(3600)  # Wait 1 hour

scraper.close()
```

## Tips & Tricks

1. **Always close the browser**: Don't forget to call `scraper.close()` to free up resources

2. **Use appropriate delays**: The tool already includes realistic delays, but you can add more for large-scale scraping

3. **Test with small limits first**: Start with `max_results=10` to verify everything works

4. **Check country codes**: Use `scrapperAmazon list-countries` to see all supported countries

5. **Handle exceptions**: Wrap scraping in try/except blocks for production code:

```python
try:
    scraper = AmazonScraperSelenium()
    products = scraper.scrape_amazon("query", max_results=20)
    scraper.save_csv(products, "output.csv")
finally:
    scraper.close()
```

## Performance Tips

- **Use country filtering**: Scraping from a specific country is faster than auto-detection
- **Set reasonable limits**: Don't try to scrape 10,000 products at once
- **Use headless mode**: The tool uses headless Chrome by default for speed
- **Combine filters**: Filter your data to reduce the amount of processing

## Troubleshooting

- **Chrome not found**: Install Chrome or Chromium on your system
- **Connection timeout**: Wait a few minutes and try again
- **No results**: Try a different search query
- **Memory usage**: Limit your `max_results` to prevent memory issues

---

For more information, see the main [README.md](../README.md)
