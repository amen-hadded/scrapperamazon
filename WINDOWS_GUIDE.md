# Windows Installation Guide 🪟

Step-by-step guide to install and use scrapperAmazon on Windows.

## Prerequisites

Before starting, make sure you have:

1. **Python 3.8 or higher** - Download from https://www.python.org/
2. **Git for Windows** - Download from https://git-scm.com/
3. **Google Chrome** - Download from https://google.com/chrome
4. **Text Editor** (Optional) - VS Code, Notepad++, or any text editor

## Step 1: Check Python Installation

Open PowerShell or Command Prompt and type:

```powershell
python --version
```

If you see a version number (e.g., `Python 3.11.0`), Python is installed correctly.

If not, download and install Python from https://www.python.org/downloads/

**Important**: During installation, check the box "Add Python to PATH"

## Step 2: Clone the Repository

### Using Command Prompt / PowerShell:

```powershell
# Create a folder for your projects (optional)
mkdir Projects
cd Projects

# Clone the repository
git clone https://github.com/amen-hadded/scrapperamazon.git
cd scrapperamazon
```

### Or Using Git GUI:

1. Open Git GUI
2. File → Clone Existing Repository
3. Source: `https://github.com/amen-hadded/scrapperamazon.git`
4. Target: `C:\Users\YourUsername\Projects\scrapperamazon`
5. Click Clone

## Step 3: Create Virtual Environment (Recommended)

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command prompt.

## Step 4: Install scrapperAmazon

```powershell
# Install the package
pip install -e .

# This will install all dependencies automatically
```

## Step 5: Verify Installation

```powershell
scrapperAmazon --version
```

You should see: `scrapperAmazon, version 1.0.0`

## Step 6: First Scrape!

```powershell
scrapperAmazon scrape -q "laptop"
```

This will create a file `amazon_results.csv` in your current directory.

## Step 7: View Results

```powershell
# Open in Excel or your default spreadsheet app
start amazon_results.csv

# Or view in command prompt
type amazon_results.csv
```

## Usage Examples

### Search for a different product

```powershell
scrapperAmazon scrape -q "gaming mouse"
```

### Search on US Amazon

```powershell
scrapperAmazon scrape -q "bicycle" -c US
```

### Collect more products

```powershell
scrapperAmazon scrape -q "headphones" -m 50
```

### Filter by price

```powershell
scrapperAmazon scrape -q "monitor" --min-price 200 --max-price 600
```

### List all options

```powershell
scrapperAmazon scrape --help
```

## Using as a Python Library

Create a file `my_scraper.py`:

```python
from scrapperamazon import AmazonScraperSelenium

scraper = AmazonScraperSelenium()
products = scraper.scrape_amazon("laptop", max_results=20)

for product in products:
    print(f"{product['title']} - {product['price']}")

scraper.save_csv(products, "laptops.csv")
scraper.close()
```

Run it:

```powershell
python my_scraper.py
```

## Common Issues on Windows

### Issue: "python command not found"

**Solution**: Python wasn't added to PATH during installation

1. Reinstall Python
2. Check "Add Python to PATH" during installation

Or add it manually:

1. Open System Properties → Environment Variables
2. Add Python to PATH (e.g., `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311`)

### Issue: "ChromeDriver not found"

**Solution**: Install Google Chrome

1. Download from https://google.com/chrome
2. Run the installer
3. The tool will automatically download the matching ChromeDriver

### Issue: "Access Denied" when installing

**Solution**: Run PowerShell as Administrator

1. Right-click PowerShell
2. Select "Run as Administrator"
3. Run the install command again

### Issue: Permission denied when running the command

**Solution**: Check execution policy

```powershell
# Check current policy
Get-ExecutionPolicy

# Change policy (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Updating scrapperAmazon

```powershell
# Activate your virtual environment
venv\Scripts\activate

# Update the package
pip install --upgrade -e .
```

## Uninstalling

```powershell
pip uninstall scrapperAmazon

# Or deactivate virtual environment
deactivate

# And delete the folder
rmdir /s scrapperAmazon
```

## Getting Help

- **Command help**: `scrapperAmazon --help`
- **Verbose output**: `scrapperAmazon scrape -q "test" -v`
- **List countries**: `scrapperAmazon list-countries`

## Tips for Windows Users

1. **Long paths**: Windows has a 260-character path limit. The tool handles this, but keep your project folder path short if possible.

2. **Antivirus**: Some antivirus software may block Selenium/ChromeDriver. Try adding the project folder to antivirus exceptions if you have issues.

3. **Firewall**: Ensure your firewall doesn't block internet access for Python or Chrome.

4. **Time zones**: Amazon shows prices based on your time zone. This is normal.

5. **Regional settings**: Results will show in your regional currency/language.

## Windows Terminal (Optional but Recommended)

For a better terminal experience on Windows 11:

1. Open Microsoft Store
2. Search for "Windows Terminal"
3. Install it
4. It's cleaner and supports modern features

## Next Steps

- 📚 Read the [README.md](README.md)
- ⚡ Check [QUICKSTART.md](QUICKSTART.md)
- 💻 See the [examples](examples/)
- 🚀 Learn about [publishing](PUBLISHING.md)

---

**Need help?** Open an issue on [GitHub](https://github.com/yourusername/scrapperAmazon/issues)

Happy scraping! 🎉
