# Publishing scrapperAmazon to GitHub and PyPI 📦

This guide explains how to publish scrapperAmazon to GitHub and PyPI so others can install it with `pip install scrapperAmazon`.

## Step 1: Set Up GitHub Repository

### 1.1 Create a GitHub Account

- Go to https://github.com and sign up (if you don't have an account)

### 1.2 Create a New Repository

1. Click the "+" icon in the top right corner
2. Select "New repository"
3. Name it: `scrapperAmazon`
4. Add description: "A powerful CLI tool to scrape Amazon products across multiple countries"
5. Choose "Public" for open source
6. Initialize with a README (optional, we have one)
7. Click "Create repository"

### 1.3 Push Code to GitHub

```bash
cd scrapperAmazon

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Add scrapperAmazon CLI tool"

# Add remote (replace with your GitHub username)
git remote add origin https://github.com/amen-hadded/scrapperamazon.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Set Up PyPI Publishing

### 2.1 Create PyPI Account

1. Go to https://pypi.org and sign up
2. Verify your email address
3. Go to Account Settings → API tokens
4. Create a new token with "Entire repository" scope
5. Copy the token (you'll need it later)

### 2.2 Configure GitHub Secrets (for automated publishing)

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste the token from PyPI
6. Click "Add secret"

### 2.3 Enable GitHub Actions (if not already enabled)

1. Go to your repository
2. Click "Actions" tab
3. Workflows should already be created from `.github/workflows/`
4. They'll run automatically on push and pull requests

## Step 3: Publishing to PyPI

### Option A: Automated Publishing (Recommended)

With GitHub Actions set up, publishing is automatic:

1. Update version in `setup.py` and `scrapperamazon/__init__.py`
2. Commit and push: `git push`
3. Create a release on GitHub:
   - Go to your repository
   - Click "Releases"
   - Click "Create a new release"
   - Tag: `v1.0.0` (matches your version)
   - Release title: `Version 1.0.0`
   - Click "Publish release"
4. GitHub Actions automatically publishes to PyPI!

### Option B: Manual Publishing

If you prefer to publish manually:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Publish to PyPI
twine upload dist/*
# Enter your PyPI username and token when prompted
```

## Step 4: Verify Installation

After publishing, test that it can be installed:

```bash
# Create a test virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from PyPI
pip install scrapperAmazon

# Test the command
scrapperAmazon --version

# Clean up
deactivate
rm -rf test_env
```

## Step 5: Create Releases

### Create a Release on GitHub

1. Go to your repository
2. Click "Releases"
3. Click "Create a new release" or "Draft a new release"
4. **Tag**: Type version number (e.g., `v1.0.0`)
5. **Release title**: "Version 1.0.0" or "Release 1.0.0"
6. **Description**: What's new in this release:

````markdown
## Changes

### Features

- Added multi-country support
- Implemented advanced filtering
- Created CLI interface with Click

### Fixes

- Fixed price extraction for different formats
- Improved error handling

### Improvements

- Better logging and verbose mode
- Cross-platform support (Windows, macOS, Linux)

## Installation

```bash
pip install scrapperAmazon
```
````

## Requirements

- Python 3.8+
- Chrome/Chromium browser

````

7. If you want to keep it as a draft, click "Save as a draft"
8. Click "Publish release"

## Step 6: Update Documentation

Update the following in your repo after publishing:

1. **README.md**: Update installation instructions with PyPI option:
   ```bash
   pip install scrapperAmazon
````

2. **GitHub Pages** (Optional): Set up documentation website
   - Go to Settings → Pages
   - Select main branch as source
   - GitHub will build a site automatically

## File Structure for Publishing

Your repository should look like this:

```
scrapperAmazon/
├── scrapperamazon/              # Main package
│   ├── __init__.py
│   ├── core.py
│   └── cli.py
├── examples/                     # Example scripts
│   ├── example_1_basic.py
│   ├── example_2_filtering.py
│   ├── example_3_pagination.py
│   └── README.md
├── .github/
│   └── workflows/               # GitHub Actions
│       ├── python-package.yml
│       └── publish.yml
├── setup.py                     # Package configuration
├── pyproject.toml               # Modern Python config
├── README.md                    # Main documentation
├── QUICKSTART.md                # Quick start guide
├── CONTRIBUTING.md              # Contributing guidelines
├── LICENSE                      # MIT License
├── MANIFEST.in                  # Package manifest
├── requirements.txt             # Dependencies
└── .gitignore                   # Git ignore rules
```

## Badges for README

Add badges to your README to show status:

```markdown
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
[![PyPI version](https://badge.fury.io/py/scrapperAmazon.svg)](https://badge.fury.io/py/scrapperAmazon)
[![Tests](https://github.com/yourusername/scrapperAmazon/workflows/Python%20Package%20Build%20%26%20Test/badge.svg)](https://github.com/yourusername/scrapperAmazon/actions)
```

## Maintaining Your Project

### Regular Updates

```bash
# Update version
echo "__version__ = '1.1.0'" > scrapperamazon/__init__.py

# Commit
git add .
git commit -m "🚀 Version 1.1.0: Add new features"

# Tag
git tag v1.1.0

# Push
git push origin main --tags
```

### Create Release Notes

Each release should have:

- Features added
- Bugs fixed
- Breaking changes (if any)
- Installation instructions
- Upgrade instructions

## Troubleshooting

### Package fails to build

```bash
pip install --upgrade setuptools wheel build
python -m build
```

### Upload fails

```bash
# Make sure twine is installed
pip install --upgrade twine

# Check token is valid
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

### GitHub Actions fails

1. Check the Actions tab for error logs
2. Common issues:
   - Dependencies not listed in `setup.py`
   - Python syntax errors
   - Missing files in `MANIFEST.in`

## Resources

- **PyPI**: https://pypi.org
- **setuptools**: https://setuptools.pypa.io/
- **GitHub Actions**: https://docs.github.com/actions
- **Semantic Versioning**: https://semver.org/

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Set up PyPI account and token
3. ✅ Configure GitHub Actions
4. ✅ Create first release
5. ✅ Test installation from PyPI
6. ✅ Create badges for README
7. ✅ Document the project well
8. ✅ Engage with users (issues, discussions)

---

**Congratulations!** Your package is now available for installation: `pip install scrapperAmazon`
