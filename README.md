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
git clone https://github.com/yourusername/scrapperAmazon.git
cd scrapperAmazon

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

```bash
# Simple search
scrapperAmazon scrape -q "laptop"

# Search with country specification
scrapperAmazon scrape -q "bicycle" -c US

# Search with multiple filters
scrapperAmazon scrape -q "headphones" --min-price 50 --max-price 200 --min-rating 4.0
```

### Available Commands

```bash
# Show help
scrapperAmazon --help

# List supported countries
scrapperAmazon list-countries

# Show version
scrapperAmazon version
```

## Usage Examples 📚

### 1. Basic Search

```bash
scrapperAmazon scrape -q "laptop"
```

Scrapes up to 20 products (default) matching "laptop" from your detected country's Amazon site.

### 2. Search in Specific Country

```bash
scrapperAmazon scrape -q "gaming mouse" -c US
```

Searches on Amazon.com (United States)

### 3. Collect Multiple Pages

```bash
scrapperAmazon scrape -q "monitor" -c DE --pages 3
```

Collects products from pages 1-3 on Amazon.de (Germany)

### 4. Large-Scale Collection

```bash
scrapperAmazon scrape -q "smartphone" -c UK -m 100
```

Collects up to 100 products from Amazon.co.uk

### 5. Price Range Filtering

```bash
scrapperAmazon scrape -q "headphones" --min-price 50 --max-price 300
```

Filters results to show only products between €50 and €300

### 6. Rating-Based Filtering

```bash
scrapperAmazon scrape -q "keyboard" --min-rating 4.5
```

Shows only products with 4.5+ stars

### 7. Remove Duplicates

```bash
scrapperAmazon scrape -q "laptop" --remove-duplicates --remove-similar
```

Removes exact duplicates and similar products

### 8. Custom Output File

```bash
scrapperAmazon scrape -q "camera" -o results/cameras_2024.csv
```

Saves results to a custom location

### 9. Complex Search with All Filters

```bash
scrapperAmazon scrape \
  -q "wireless speaker" \
  -c FR \
  --max-results 50 \
  --pages 2 \
  --min-price 30 \
  --max-price 200 \
  --min-rating 4.0 \
  --remove-duplicates \
  --remove-similar \
  -o output/speakers.csv
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

## CLI Options Reference 📖

```bash
scrapperAmazon scrape [OPTIONS]

OPTIONS:
  -q, --query TEXT              Search query (REQUIRED)
  -c, --country CODE            Country code (auto-detect if not set)
  -m, --max-results INTEGER     Max products to collect (default: 20)
  -p, --pages INTEGER           Number of pages to scrape (1-7)
  -o, --output PATH             Output CSV filename (default: amazon_results.csv)
  --min-price FLOAT             Minimum price filter
  --max-price FLOAT             Maximum price filter
  --min-rating FLOAT            Minimum rating (e.g., 4.0)
  --remove-duplicates           Remove exact duplicates
  --remove-similar              Remove similar products
  --filter-term TEXT            Filter by specific term in title
  -v, --verbose                 Enable verbose logging
  --help                        Show help message
```

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
git clone https://github.com/yourusername/scrapperAmazon.git
cd scrapperAmazon

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install in development mode with all dependencies
pip install -e ".[dev]"
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

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/scrapperAmazon/issues)
- 💭 Discussions: [GitHub Discussions](https://github.com/yourusername/scrapperAmazon/discussions)

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

**Made with ❤️ by Your Name**

⭐ If you find this project useful, please consider starring it on GitHub!
