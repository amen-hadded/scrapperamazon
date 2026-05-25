# Quick Start Guide 🚀

Get scrapperAmazon up and running in 5 minutes!

## 1. Installation

### On Windows, macOS, or Linux:

```bash
# Clone the repository
git clone https://github.com/yourusername/scrapperAmazon.git
cd scrapperAmazon

# Install the package
pip install -e .
```

## 2. Verify Installation

```bash
scrapperAmazon --version
```

You should see: `scrapperAmazon, version 1.0.0`

## 3. First Scrape

```bash
scrapperAmazon scrape -q "laptop"
```

This will:

- Auto-detect your country by IP
- Search for "laptop" on your local Amazon site
- Collect up to 20 products
- Save results to `amazon_results.csv`

## 4. Check Results

```bash
# On Windows
type amazon_results.csv

# On macOS/Linux
cat amazon_results.csv
```

You'll see a CSV with columns: `asin`, `title`, `price`, `rating`, `url`

## 5. Try More Features

### Search in a specific country:

```bash
scrapperAmazon scrape -q "bicycle" -c US
```

### Collect more products:

```bash
scrapperAmazon scrape -q "headphones" --max-results 50
```

### Add price filter:

```bash
scrapperAmazon scrape -q "monitor" --min-price 200 --max-price 500
```

### Remove duplicates:

```bash
scrapperAmazon scrape -q "keyboard" --remove-duplicates
```

## 6. View All Options

```bash
scrapperAmazon scrape --help
```

## 7. List Supported Countries

```bash
scrapperAmazon list-countries
```

## Common Issues

### "Chrome not found"

Install Google Chrome: https://google.com/chrome

### "Command not found: scrapperAmazon"

Make sure you're in the project directory and ran `pip install -e .`

### No products found

- Try a different search term
- Check your internet connection
- Try a different country

## Next Steps

- 📚 Read the [full README](README.md)
- 💻 Check out the [examples](examples/)
- 🔧 Learn the [CLI options](README.md#cli-options-reference)
- 🌐 See [supported countries](README.md#supported-countries-)

---

**Need help?** Open an issue on [GitHub](https://github.com/yourusername/scrapperAmazon/issues)
