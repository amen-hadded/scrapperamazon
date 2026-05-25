# Contributing to scrapperAmazon 🤝

First off, thank you for considering contributing to scrapperAmazon! It's people like you that make scrapperAmazon such a great tool.

## Code of Conduct

This project adheres to the Contributor Covenant. By participating, you are expected to uphold this code. Please report unacceptable behavior to your.email@example.com.

## How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots/error messages if possible**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements 💡

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests 🔄

- Fill in the required template
- Follow the Python styleguides
- Include appropriate test cases
- End all files with a newline
- Update documentation accordingly

## Styleguides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an emoji:
  - 🎨 `:art:` when improving the format/structure of the code
  - ⚡ `:zap:` when improving performance
  - 📝 `:memo:` when writing docs
  - 🐛 `:bug:` when fixing a bug
  - ✨ `:sparkles:` when adding a feature
  - 🚀 `:rocket:` when deploying stuff
  - 🔒 `:lock:` when dealing with security

Example:

```
:memo: Update README with installation instructions
```

### Python Styleguide

- Use [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable names
- Add docstrings to all modules, classes, and functions
- Use type hints where appropriate
- Maximum line length: 100 characters

Example:

```python
def scrape_products(query: str, country: str = None) -> list:
    """
    Scrape Amazon products for a given query.

    Args:
        query: The search query string
        country: Optional country code (e.g., 'US', 'FR')

    Returns:
        A list of product dictionaries
    """
    # Your code here
    pass
```

## Development Setup

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
5. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Testing

Before submitting a pull request, please ensure:

- Your code follows PEP 8 style guidelines
- All functions have docstrings
- You've tested your changes locally
- You haven't broken any existing functionality

## Documentation

- Update README.md if you add new features
- Update docstrings if you modify functions
- Add comments for complex logic
- Include usage examples for new features

## Release Process

Only maintainers can release new versions, but here's how it works:

1. Update version number in `setup.py` and `__init__.py`
2. Update `CHANGELOG.md` with new features and fixes
3. Tag the release in git: `git tag v1.0.0`
4. Push the tag: `git push origin v1.0.0`

## Questions?

Feel free to open an issue with the question tag, and we'll be happy to help!

---

**Thanks for contributing to scrapperAmazon!** 🙌
