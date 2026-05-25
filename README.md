# scrapperAmazon 🛒

A powerful, easy-to-use CLI tool to scrape Amazon products across multiple countries. Built with Python, Selenium, and Click.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

## Features ✨

- 🌍 **Multi-country Support**: Scrape from 15+ Amazon domains (US, FR, DE, UK, JP, etc.)
- 🤖 **Anti-Detection**: Uses Selenium with anti-bot headers and realistic user behavior
- 📊 **Advanced Filtering**: Filter by price, rating, search term, and more
- 📄 **CSV Export**: Save results to CSV format for analysis
- 🧹 **Data Cleaning**: Remove duplicates and similar products automatically
- ⚡ **Pagination Support**: Scrape multiple pages with configurable limits
- 🖥️ **Cross-Platform**: Works on Windows, macOS, and Linux
- 🔧 **Easy to Use**: Simple CLI with helpful commands and examples

## Requirements 📋

- Python 3.8 or higher
- Chrome/Chromium browser installed
- Internet connection

## Installation 🚀

### Option 1: Install from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/amen-hadded/scrapperamazon.git
cd scrapperamazon

# Install in development mode (recommended for development)
pip install -e .

# Or install normally
pip install .
```

### Option 2: Install from PyPI (when available)

```bash
pip install scrapperAmazon
```

### Option 3: Install from requirements.txt

```bash
git clone https://github.com/amen-hadded/scrapperamazon.git
cd scrapperamazon

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start 🎯

### Basic Usage

Run the interactive CLI:

```bash
# Launch interactive mode
python -m scrapperamazon.cli

# Or using the installed command (if PATH is configured)
scrapperAmazon
```

The tool will guide you through:

1. Select your Amazon region (15 countries available)
2. Enter search query
3. Choose collection mode (items, pages, range, all, or default)
4. Apply optional filters (duplicates, similar products, price, rating, terms)
5. View results and save to CSV

## Usage Examples 📚

### 1. Interactive Mode (Recommended)

```bash
python -m scrapperamazon.cli
```

The tool launches with a beautiful interactive menu:

- Select country from 15 Amazon domains
- Enter your search query
- Choose how many products to collect
- Apply filters (price, rating, duplicates, etc.)
- View results with colors and emojis
- Save to CSV

### 2. Using as Python Library

```python
from scrapperamazon import AmazonScraperSelenium, remove_duplicates, filter_by_price_range

# Create scraper
scraper = AmazonScraperSelenium(amazon_site="https://amazon.com")

# Scrape products
products = scraper.scrape_amazon("laptop", max_results=20)

# Apply filters
products = remove_duplicates(products)
products = filter_by_price_range(products, min_price=500, max_price=1500)

# Save to CSV
scraper.save_csv(products, "laptops.csv")
```

### 3. Advanced Python Usage

```python
from scrapperamazon import AmazonScraperSelenium
from scrapperamazon import (
    remove_duplicates,
    remove_similar_duplicates,
    filter_by_search_term,
    filter_by_price_range,
    filter_by_rating
)

# Multi-page scraping with all filters
scraper = AmazonScraperSelenium(amazon_site="https://amazon.de")
products = scraper.scrape_amazon("headphones", max_results=100, collect_all_pages=True)

# Clean and filter
products = remove_duplicates(products)
products = remove_similar_duplicates(products, threshold=0.85)
products = filter_by_price_range(products, min_price=30, max_price=200)
products = filter_by_rating(products, min_rating=4.0)

scraper.save_csv(products, "results/headphones_filtered.csv")
scraper.close()
```

## Supported Countries 🌐

The tool supports the following Amazon domains:

| Code | Domain        | Locale | Currency |
| ---- | ------------- | ------ | -------- |
| US   | amazon.com    | en_US  | $        |
| GB   | amazon.co.uk  | en_GB  | £        |
| FR   | amazon.fr     | fr_FR  | €        |
| DE   | amazon.de     | de_DE  | €        |
| IT   | amazon.it     | it_IT  | €        |
| ES   | amazon.es     | es_ES  | €        |
| CA   | amazon.ca     | en_CA  | $        |
| BR   | amazon.com.br | pt_BR  | R$       |
| JP   | amazon.co.jp  | ja_JP  | ¥        |
| IN   | amazon.in     | en_IN  | ₹        |
| AU   | amazon.com.au | en_AU  | $        |
| SE   | amazon.se     | sv_SE  | kr       |
| NL   | amazon.nl     | nl_NL  | €        |
| BE   | amazon.be     | fr_BE  | €        |
| PL   | amazon.pl     | pl_PL  | zł       |

List all supported countries:

```bash
scrapperAmazon list-countries
```

## Interactive CLI Guide 📖

When you run `python -m scrapperamazon.cli`, you'll see:

```
██████╗ ███╗   ███╗███████╗████╗
██╔════╝ ████╗ ████║██╔════╝██╔╝
██║█████╗██╔████╔██║███████╗██║
██║╚════╝██║╚██╔╝██║╚════██║██║
╚█████╗ ██║ ╚═╝ ██║███████║████╗
 ╚════╝ ╚═╝     ╚═╝╚══════╝╚═══╝

Amazon Product Scraper ✓ PRO
```

### Steps:

1. **Select Country** - Choose from 15 Amazon domains
2. **Search Query** - Enter your search term (e.g., "laptop", "headphones")
3. **Collection Mode** - Choose how to collect:
   - `1`: Collect N items (you specify number)
   - `2`: Scrape N pages (1-7 pages)
   - `3`: Collect from page range (e.g., pages 1-3)
   - `4`: Collect all products (pages 1-7)
   - `5`: Use default (20 items)
4. **Apply Filters** (optional):
   - Remove duplicate products
   - Remove similar products (>85% similarity)
   - Filter by search term in title
   - Filter by price range (min-max)
   - Filter by minimum rating (stars)
5. **View & Save** - Results display with emojis and colors, then save to CSV

## Output Format 📊

Results are saved to CSV with the following columns:

```
asin,title,price,rating,url
B000ABC123,Amazing Product,29.99 €,4.5,https://amazon.fr/...
B000ABC124,Great Item,34.50 €,4.2,https://amazon.fr/...
...
```

## Setup for Development 🛠️

### Clone and Setup

```bash
git clone https://github.com/amen-hadded/scrapperamazon.git
cd scrapperamazon

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install in development mode with all dependencies
pip install -e .
```

### Project Structure

```
scrapperAmazon/
├── scrapperamazon/           # Main package
│   ├── __init__.py           # Package initialization
│   ├── core.py               # Core scraper logic
│   └── cli.py                # CLI interface
├── setup.py                  # Setup configuration
├── pyproject.toml            # Modern Python project config
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── LICENSE                   # MIT License
└── .gitignore               # Git ignore rules
```

## How It Works 🔧

1. **Selenium Integration**: Uses Selenium WebDriver to automate Chrome browser
2. **Anti-Detection**: Includes headers and behaviors to avoid bot detection
3. **HTML Parsing**: Uses Parsel for efficient HTML parsing
4. **Data Extraction**: Extracts product info (title, price, rating, ASIN, URL)
5. **Filtering**: Applies multiple filter options to clean data
6. **Export**: Saves results to CSV format

## Important Notes ⚠️

- **Respect robots.txt**: Always check Amazon's terms of service
- **Rate Limiting**: The tool includes delays to avoid detection
- **Legal Use**: Use responsibly for personal/research purposes
- **Terms of Service**: Ensure compliance with Amazon's policies
- **IP Blocking**: May face IP blocks if used excessively
- **Data Accuracy**: Prices and availability may change frequently

## Troubleshooting 🐛

### Chrome/Chromium Not Found

The tool uses `webdriver-manager` to automatically download the correct ChromeDriver. Make sure you have Chrome or Chromium installed:

- **Windows**: Install Google Chrome from chrome.google.com
- **macOS**: `brew install google-chrome` or `brew install chromium`
- **Linux**: `sudo apt-get install google-chrome-stable` or `chromium`

### No Results Found

- Check your internet connection
- Try a different search query
- Verify the country code is correct
- Check verbose output: `scrapperAmazon scrape -q "search" -v`

### Connection Errors

- Wait a few minutes and try again
- Try searching in a different country
- Check if Amazon is blocking your IP (try VPN if allowed)

### CSV File Issues

- Ensure you have write permissions in the output directory
- Try specifying a full path: `-o /path/to/results.csv`
- Check disk space availability

## Contributing 🤝

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer ⚖️

This tool is for educational and research purposes only. Users are responsible for:

- Following Amazon's Terms of Service
- Respecting website policies and robots.txt
- Using the tool ethically and legally
- Complying with applicable laws in their jurisdiction

The authors assume no responsibility for misuse or damage caused by this tool.

## Support & Contact 💬

- 📧 Email: amenallahhadde6@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/amen-hadded/scrapperamazon/issues)
- 💭 Discussions: [GitHub Discussions](https://github.com/amen-hadded/scrapperamazon/discussions)
- 🏠 Repository: [github.com/amen-hadded/scrapperamazon](https://github.com/amen-hadded/scrapperamazon)

## Changelog 📝

### Version 1.0.0 (2024)

- Initial release
- Multi-country support
- CLI interface
- Advanced filtering options
- CSV export
- Cross-platform support

## Related Projects 🔗

- [Selenium](https://github.com/SeleniumHQ/selenium) - Web automation
- [Click](https://github.com/pallets/click) - CLI creation kit
- [Parsel](https://github.com/scrapy/parsel) - HTML parsing

---

**Made with ❤️ by Amen Allah Hadded**

📧 Questions? Email: amenallahhadde6@gmail.com

⭐ If you find this project useful, please consider starring it on GitHub!
