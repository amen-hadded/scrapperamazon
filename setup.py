"""
Setup configuration for scrapperAmazon
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8") if (this_directory / "README.md").exists() else ""

setup(
    name="scrapperAmazon",
    version="1.0.0",
    description="A powerful CLI tool to scrape Amazon products across multiple countries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Amen Allah Hadded",
    author_email="amenallahhadde6@gmail.com",
    url="https://github.com/amen-hadded/scrapperamazon",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.0.0",
        "webdriver-manager>=4.0.0",
        "parsel>=1.7.0",
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "scrapperAmazon=scrapperamazon.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    keywords="amazon scraper cli selenium web-scraping",
)
