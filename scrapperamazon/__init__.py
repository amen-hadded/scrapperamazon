"""
scrapperAmazon - Amazon Scraper CLI Tool
A command-line tool to scrape Amazon products across multiple countries
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"

from .core import (
    AmazonScraperSelenium,
    remove_duplicates,
    remove_similar_duplicates,
    filter_by_search_term,
    filter_by_price_range,
    filter_by_rating,
)

__all__ = [
    "AmazonScraperSelenium",
    "remove_duplicates",
    "remove_similar_duplicates",
    "filter_by_search_term",
    "filter_by_price_range",
    "filter_by_rating",
]
